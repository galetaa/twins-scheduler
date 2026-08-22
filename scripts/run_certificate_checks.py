#!/usr/bin/env python3
"""Run both project-local certificate kernels and their negative controls."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from twins_scheduler.certificate_kernel import (
    ProofFailure,
    check_induction_certificate,
    check_quorum_pivot_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
CERTS = ROOT / "formal" / "certificates" / "gate8"
GENERATED = ROOT / "results" / "generated"


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    checked = {
        "T1": check_induction_certificate(
            CERTS / "t1_rules.json", CERTS / "t1_replay_erasure_certificate.json"
        ),
        "T2": check_induction_certificate(
            CERTS / "t2_rules.json", CERTS / "t2_closure_lifting_certificate.json"
        ),
        "T3": check_quorum_pivot_certificate(
            CERTS / "t3_quorum_pivot_certificate.json"
        ),
    }

    tampered = json.loads(
        (CERTS / "t1_replay_erasure_certificate.json").read_text(encoding="utf-8")
    )
    tampered["premises"].remove("premise_duplicate_transition_stutters")
    rejected = False
    with tempfile.TemporaryDirectory(prefix="twins-cert-negative-") as temporary:
        damaged = Path(temporary) / "damaged.json"
        damaged.write_text(json.dumps(tampered), encoding="utf-8")
        try:
            check_induction_certificate(CERTS / "t1_rules.json", damaged)
        except ProofFailure:
            rejected = True
    if not rejected:
        raise SystemExit("tampered Gate 8 certificate was accepted")

    with tempfile.TemporaryDirectory(prefix="twins-kernel-") as temporary:
        project_output = Path(temporary) / "project_kernel.json"
        command = [
            sys.executable,
            str(ROOT / "formal" / "project_kernel" / "proof_kernel.py"),
            str(ROOT / "formal" / "project_kernel" / "certificate.json"),
            "--json-output",
            str(project_output),
            "--negative-controls",
        ]
        environment = os.environ.copy()
        environment["PYTHONHASHSEED"] = "0"
        subprocess.run(command, check=True, capture_output=True, text=True, env=environment)
        project_result = json.loads(project_output.read_text(encoding="utf-8"))
        project_result["certificate"] = "formal/project_kernel/certificate.json"

    result = {
        "status": "PASS",
        "gate8_certificates": checked,
        "tampered_gate8_certificate": "REJECTED_AS_EXPECTED",
        "project_local_kernel": project_result,
    }
    (GENERATED / "certificate_verification.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
