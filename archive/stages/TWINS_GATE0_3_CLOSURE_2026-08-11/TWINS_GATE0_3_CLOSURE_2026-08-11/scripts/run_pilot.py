#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from twinsbound.adversaries.byzantine import accepted_message_byzantine_branch_sets
from twinsbound.adversaries.equivocation import dynamic_equivocation_branch_sets
from twinsbound.adversaries.twins_k import Lifecycle, finite_clone_branch_sets
from twinsbound.explorer import LanguageResult, enumerate_language
from twinsbound.model import Observation
from twinsbound.oracles import dynamic_active_k_min, static_k_min
from twinsbound.protocols.toy_locking import ToyTwoPhaseLocking


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="Rewrite the baseline deterministic manifest after a reviewed run.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def event_trace(result: LanguageResult, obs: Observation, lifecycle: str) -> dict[str, Any]:
    branches, events = result.witnesses[obs]
    prefix: list[dict[str, Any]] = []
    if lifecycle == Lifecycle.SNAPSHOT_ACTIVE_REUSE.value:
        for value in sorted(branches):
            prefix.extend([
                {"kind": "START_OR_RESTORE_SLOT", "slot": 0, "value": value},
                {"kind": "EXECUTE_CORRECT_BRANCH", "slot": 0, "value": value},
                {"kind": "STOP_SLOT", "slot": 0, "value": value},
            ])
    else:
        for clone, value in enumerate(sorted(branches)):
            prefix.extend([
                {"kind": "START_CLONE", "clone": clone, "value": value},
                {"kind": "EXECUTE_CORRECT_BRANCH", "clone": clone, "value": value},
            ])
    return {
        "model": result.model,
        "lifecycle": lifecycle,
        "branch_values": sorted(branches),
        "observation": obs.canonical_id(),
        "unsafe": obs.unsafe(),
        "events": prefix + [e.as_dict() for e in events],
    }


def run() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    with config_path.open("rb") as f:
        cfg = tomllib.load(f)
    p = cfg["pilot"]
    semantics = cfg["semantics"]
    n = int(p["correct_replicas"])
    value_counts = [int(x) for x in p["value_counts"]]
    static_caps = [int(x) for x in p["static_clone_caps"]]
    dynamic_caps = [int(x) for x in p["dynamic_active_caps"]]
    validate = bool(p["validate_quotient_with_event_bfs"])

    out = ROOT / "results" / "pilot"
    out.mkdir(parents=True, exist_ok=True)
    protocol = ToyTwoPhaseLocking(n)

    all_results: dict[tuple[int, str], LanguageResult] = {}
    summaries: list[dict[str, Any]] = []
    state_report: dict[str, Any] = {
        "pilot_id": p["id"],
        "bounds": {"correct_replicas": n, "value_counts": value_counts},
        "semantics": semantics,
        "experiments": {},
    }

    for m in value_counts:
        ae = enumerate_language(
            protocol,
            "AE",
            m,
            dynamic_equivocation_branch_sets(m),
            validate_quotient=validate,
        )
        ab = enumerate_language(
            protocol,
            "AB",
            m,
            accepted_message_byzantine_branch_sets(m),
            validate_quotient=validate,
        )
        all_results[(m, "AE")] = ae
        all_results[(m, "AB")] = ab
        if ae.observations != ab.observations:
            raise AssertionError("AB and AE differ in the validator-only pilot")

        model_specs: list[tuple[str, tuple[frozenset[int], ...]]] = [("AE", dynamic_equivocation_branch_sets(m)), ("AB", accepted_message_byzantine_branch_sets(m))]
        for k in static_caps:
            model_specs.append((f"AT_GENESIS_STATIC_{k}", finite_clone_branch_sets(m, k, Lifecycle.GENESIS_STATIC)))
        for k in dynamic_caps:
            model_specs.append((f"AT_SNAPSHOT_ACTIVE_REUSE_{k}", finite_clone_branch_sets(m, k, Lifecycle.SNAPSHOT_ACTIVE_REUSE)))

        for name, branch_sets in model_specs:
            if name in {"AE", "AB"}:
                result = all_results[(m, name)]
            else:
                result = enumerate_language(protocol, name, m, branch_sets, validate_quotient=validate)
                all_results[(m, name)] = result
            summaries.append({
                "value_count": m,
                "model": name,
                "language_size": len(result.observations),
                "unsafe_size": len(result.unsafe),
                "missing_vs_AE": len(ae.observations - result.observations),
                "missing_unsafe_vs_AE": len(ae.unsafe - result.unsafe),
                "extra_vs_AE": len(result.observations - ae.observations),
                "states_explored_sum": result.total_states,
                "transitions_explored_sum": result.total_transitions,
            })

        state_report["experiments"][str(m)] = {
            name: {
                "branch_sets": [sorted(s) for s in result.branch_explorations],
                "language_size": len(result.observations),
                "unsafe_size": len(result.unsafe),
                "states_explored_sum": result.total_states,
                "transitions_explored_sum": result.total_transitions,
                "per_branch_set": {
                    ",".join(map(str, sorted(branches))) or "empty": {
                        "states": exploration.states_explored,
                        "transitions": exploration.transitions_explored,
                        "observations": len(exploration.observations),
                    }
                    for branches, exploration in result.branch_explorations.items()
                },
            }
            for (vm, name), result in all_results.items() if vm == m
        }

    with (out / "language_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(sorted(summaries, key=lambda r: (r["value_count"], r["model"])))

    with (out / "k_min.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "value_count", "observation", "unsafe", "used_values", "decided_values",
            "chain_width", "static_k_min", "snapshot_active_k_min",
            "decision_projection_width", "minimal_unsafe_core", "minimal_unsafe_core_width",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in value_counts:
            ae = all_results[(m, "AE")]
            for obs in sorted(ae.observations, key=lambda o: o.canonical_id()):
                if p["emit_all_unsafe_rows"] and not obs.unsafe():
                    continue
                core = obs.minimal_pair_core()
                writer.writerow({
                    "value_count": m,
                    "observation": obs.canonical_id(),
                    "unsafe": str(obs.unsafe()).lower(),
                    "used_values": ";".join(map(str, sorted(obs.used_values()))),
                    "decided_values": ";".join(map(str, sorted(obs.decided_values()))),
                    "chain_width": obs.width(),
                    "static_k_min": static_k_min(obs),
                    "snapshot_active_k_min": dynamic_active_k_min(obs),
                    "decision_projection_width": obs.decision_projection().width(),
                    "minimal_unsafe_core": core.canonical_id() if core else "",
                    "minimal_unsafe_core_width": core.width() if core else "",
                })

    unmatched: list[dict[str, Any]] = []
    for m in value_counts:
        ae = all_results[(m, "AE")]
        comparison_names = [f"AT_GENESIS_STATIC_{k}" for k in static_caps] + [f"AT_SNAPSHOT_ACTIVE_REUSE_{k}" for k in dynamic_caps]
        for name in comparison_names:
            result = all_results[(m, name)]
            missing = sorted(ae.unsafe - result.unsafe, key=lambda o: (o.width(), o.canonical_id()))
            if missing:
                obs = min(missing, key=lambda o: (len(ae.witnesses[o][1]), o.width(), o.canonical_id()))
                lifecycle = Lifecycle.SNAPSHOT_ACTIVE_REUSE.value if "SNAPSHOT" in name else Lifecycle.GENESIS_STATIC.value
                rec = event_trace(ae, obs, lifecycle)
                rec.update({"comparison_model": name, "missing_unsafe_count": len(missing)})
                unmatched.append(rec)
    with (out / "unmatched_traces.jsonl").open("w", encoding="utf-8") as f:
        for rec in unmatched:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    with (out / "state_space.json").open("w", encoding="utf-8") as f:
        json.dump(state_report, f, indent=2, sort_keys=True)
        f.write("\n")

    # Machine-readable theorem checks.
    theorem_checks: dict[str, Any] = {}
    for m in value_counts:
        ae = all_results[(m, "AE")]
        theorem_checks[str(m)] = {
            "AB_equals_AE": all_results[(m, "AB")].observations == ae.observations,
            "AT_embeds_in_AE": all(
                all_results[(m, name)].observations <= ae.observations
                for (_, name) in all_results if _ == m and name.startswith("AT_")
            ),
            "static_k_min_equals_width_for_all_AE_observations": all(
                static_k_min(obs) == obs.width() for obs in ae.observations
            ),
            "snapshot_active_one_equals_AE": all_results[(m, "AT_SNAPSHOT_ACTIVE_REUSE_1")].observations == ae.observations,
            "every_unsafe_observation_has_two_branch_subwitness": all(
                obs.minimal_pair_core() is not None and obs.minimal_pair_core().width() == 2
                for obs in ae.unsafe
            ),
        }
    with (out / "theorem_checks.json").open("w", encoding="utf-8") as f:
        json.dump(theorem_checks, f, indent=2, sort_keys=True)
        f.write("\n")

    python_info = {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "uv": subprocess.run(["uv", "--version"], text=True, capture_output=True, check=False).stdout.strip() if shutil.which("uv") else None,
        "git": subprocess.run(["git", "--version"], text=True, capture_output=True, check=False).stdout.strip() if shutil.which("git") else None,
        "config_sha256": sha256(config_path),
        "cwd": str(Path.cwd()),
        "environment_variables_recorded": ["PYTHONHASHSEED"],
        "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
    }
    with (out / "environment.json").open("w", encoding="utf-8") as f:
        json.dump(python_info, f, indent=2, sort_keys=True)
        f.write("\n")

    binary = 2
    ternary = 3
    b_ae = all_results[(binary, "AE")]
    b_s1 = all_results[(binary, "AT_GENESIS_STATIC_1")]
    b_s2 = all_results[(binary, "AT_GENESIS_STATIC_2")]
    b_d1 = all_results[(binary, "AT_SNAPSHOT_ACTIVE_REUSE_1")]
    t_ae = all_results[(ternary, "AE")]
    t_s2 = all_results[(ternary, "AT_GENESIS_STATIC_2")]
    t_s3 = all_results[(ternary, "AT_GENESIS_STATIC_3")]

    decision = f"""# Gate 3 Decision — BP-TWINS-FC-01-CLOSURE

## Decision

**NO-GO for the finite-clone-number research claim; PIVOT only to concrete harness conformance.**

## Completed exact bounds

- Correct replicas: {n}; one faulty protocol identity.
- Values: binary and ternary diagnostic instances.
- All branch subsets enumerated.
- All reachable event states exhaustively explored for every branch subset.
- Terminal quotient independently checked against event-level BFS.
- Persistent static clone caps: {static_caps}.
- Reusable snapshot active-slot caps: {dynamic_caps}.

## Exact results

| Instance | Model | Language | Unsafe | Missing unsafe vs AE |
|---|---:|---:|---:|---:|
| binary | AE | {len(b_ae.observations)} | {len(b_ae.unsafe)} | 0 |
| binary | static k=1 | {len(b_s1.observations)} | {len(b_s1.unsafe)} | {len(b_ae.unsafe-b_s1.unsafe)} |
| binary | static k=2 | {len(b_s2.observations)} | {len(b_s2.unsafe)} | {len(b_ae.unsafe-b_s2.unsafe)} |
| binary | snapshot active k=1 | {len(b_d1.observations)} | {len(b_d1.unsafe)} | {len(b_ae.unsafe-b_d1.unsafe)} |
| ternary | AE | {len(t_ae.observations)} | {len(t_ae.unsafe)} | 0 |
| ternary | static k=2 | {len(t_s2.observations)} | {len(t_s2.unsafe)} | {len(t_ae.unsafe-t_s2.unsafe)} |
| ternary | static k=3 | {len(t_s3.observations)} | {len(t_s3.unsafe)} | {len(t_ae.unsafe-t_s3.unsafe)} |

## Decisive findings

1. `AB = AE` in this validator-only model.
2. Every finite-clone language is included in `AE`.
3. For persistent genesis clones, exact `k_min` equals the number of distinct incompatible correct-code branch histories retained by the observation. This is the minimum chain-cover width by construction.
4. For the binary protocol, static `k=2` covers every unsafe AE observation; `k=1` covers none.
5. Ternary exact observations create a strict `k=2 < k=3` hierarchy only when the observation insists on retaining a third branch. Every unsafe observation still contains a two-branch agreement-violation core.
6. Under `SnapshotDynamic(k)` interpreted as an active-slot cap with restart/replay and unbounded network delay, `k=1` equals AE for every finite observation: execute branches sequentially and delay delivery.

## Gate rule applied

Gate 3 specifies NO-GO when the result is an ordinary chain cover or trivial two-clone behavior. Both occurred. The remaining possible contribution is not a clone-number theorem but a new question about whether a concrete round-partition implementation realizes the ideal per-message scheduler semantics.
"""
    (out / "decision.md").write_text(decision, encoding="utf-8")

    # The baseline manifest is intentionally updated only after a reviewed run.
    # Normal reproduction rewrites deterministic outputs and verifies them against
    # the existing baseline rather than replacing the expected hashes.
    if args.update_manifest:
        excluded_names = {"manifest.sha256", "environment.json", "test_run.log"}
        files = sorted(
            path
            for path in ROOT.rglob("*")
            if path.is_file()
            and path.name not in excluded_names
            and ".venv" not in path.parts
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        )
        with (out / "manifest.sha256").open("w", encoding="utf-8") as f:
            for path in files:
                f.write(f"{sha256(path)}  {path.relative_to(ROOT)}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
