#!/usr/bin/env python3
"""Independently verify the recorded native Ed25519 votes and their metadata.

Uses Python cryptography/OpenSSL rather than CometBFT's Ed25519 implementation.
The small protobuf reader checks recorded canonical sign bytes against the JSON
vote's type, height, round, block hash, chain ID, and nanosecond timestamp.
This reads positive evidence; it neither modifies nor runs any validator.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re

import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


ROOT = Path(__file__).resolve().parents[2]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def varint(data: bytes, offset: int) -> tuple[int, int]:
    number = 0
    for shift in range(0, 70, 7):
        if offset >= len(data):
            raise ValueError("truncated protobuf varint")
        value = data[offset]
        offset += 1
        number |= (value & 127) << shift
        if value < 128:
            return number, offset
    raise ValueError("oversized protobuf varint")


def fields(data: bytes) -> dict[int, int | bytes]:
    result: dict[int, int | bytes] = {}
    offset = 0
    while offset < len(data):
        tag, offset = varint(data, offset)
        field, wire = tag >> 3, tag & 7
        if field in result or field == 0:
            raise ValueError("duplicate or invalid canonical protobuf field")
        if wire == 0:
            result[field], offset = varint(data, offset)
        elif wire == 1:
            if offset + 8 > len(data):
                raise ValueError("truncated fixed64 field")
            result[field] = int.from_bytes(data[offset:offset + 8], "little", signed=True)
            offset += 8
        elif wire == 2:
            length, offset = varint(data, offset)
            if offset + length > len(data):
                raise ValueError("truncated length-delimited field")
            result[field] = data[offset:offset + length]
            offset += length
        else:
            raise ValueError(f"unexpected canonical protobuf wire type {wire}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path,
                        default=Path(os.environ.get("TWINS_OUTPUT_ROOT", ROOT)) / "results/native")
    args = parser.parse_args()
    directory = args.input_dir.resolve()
    evidence = json.loads((directory / "native_conformance.json").read_text())
    provenance = json.loads((directory / "native_provenance.json").read_text())
    summary = json.loads((directory / "native_summary.json").read_text())
    for filename, expected in provenance["result_sha256"].items():
        assert digest(directory / filename) == expected, f"stale or changed result: {filename}"
    assert provenance["harness_sha256"] == digest(Path(__file__).with_name("native_conformance_test.go.txt"))
    assert provenance["runner_sha256"] == digest(Path(__file__).with_name("run.py"))
    count = 0
    scenario_counts = {}
    for scenario in evidence["scenarios"]:
        scenario_counts[scenario["name"]] = len(scenario["native_signed_votes"])
        seen: dict[tuple[int, int, int, str], str] = {}
        for record in scenario["native_signed_votes"]:
            raw_key = bytes.fromhex(scenario["ed25519_public_keys_hex"][record["node"]])
            public_key = Ed25519PublicKey.from_public_bytes(raw_key)
            canonical = bytes.fromhex(record["sign_bytes_hex"])
            public_key.verify(bytes.fromhex(record["ed25519_signature_hex"]), canonical)
            assert hashlib.sha256(raw_key).digest()[:20].hex() == record["validator_address"]
            length, start = varint(canonical, 0)
            assert start + length == len(canonical), "canonical sign bytes must be one delimited message"
            parsed = fields(canonical[start:])
            assert parsed[1] == {"PREVOTE": 1, "PRECOMMIT": 2}[record["type"]]
            assert parsed.get(2, 0) == record["height"]
            assert parsed.get(3, 0) == record["round"]
            assert parsed[6].decode() == evidence["chain_id"]
            signed_hash = fields(parsed[4]).get(1, b"").hex() if 4 in parsed else ""
            assert signed_hash == record["block_hash"]
            seconds_and_nanos = fields(parsed[5])
            timestamp = re.fullmatch(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,9}))?Z", record["timestamp"])
            assert timestamp, "expected native RFC3339Nano timestamp"
            seconds = int(datetime.fromisoformat(timestamp[1]).replace(tzinfo=timezone.utc).timestamp())
            nanos = int((timestamp[2] or "").ljust(9, "0"))
            assert seconds_and_nanos.get(1, 0) == seconds
            assert seconds_and_nanos.get(2, 0) == nanos
            slot = (record["node"], record["height"], record["round"], record["type"])
            assert slot not in seen or seen[slot] == record["block_hash"], "same-slot vote changed block"
            seen[slot] = record["block_hash"]
            count += 1
    assert count == summary["native_signed_votes"]
    assert sum(len(s["events"]) for s in evidence["scenarios"]) == summary["scheduled_events"]
    assert sum(len(s["checks"]) for s in evidence["scenarios"]) == summary["checks_passed"]
    result = {
        "status": "PASS",
        "upstream_commit": evidence["upstream_commit"],
        "independently_verified_ed25519_signatures": count,
        "canonical_metadata_checks_per_vote": ["type", "height", "round", "block_hash", "chain_id", "timestamp_nanoseconds", "validator_address"],
        "conflicting_same_slot_records": 0,
        "scenario_vote_counts": scenario_counts,
        "cryptography_version": cryptography.__version__,
        "openssl_version": backend.openssl_version_text(),
        "auditor_sha256": digest(Path(__file__)),
        "input_evidence_sha256": digest(directory / "native_conformance.json"),
        "scope": "independent Ed25519 and canonical vote metadata audit of recorded positive native evidence; not an independent consensus implementation",
    }
    (directory / "native_signature_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
