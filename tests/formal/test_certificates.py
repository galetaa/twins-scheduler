import json
import subprocess
import sys
from pathlib import Path

import pytest

from twins_scheduler.certificate_kernel import (
    ProofFailure,
    check_induction_certificate,
    check_quorum_pivot_certificate,
)
from twins_scheduler.source_mapping import verify_source_mapping


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATES = ROOT / "formal" / "certificates" / "gate8"


def test_gate8_certificates() -> None:
    assert check_induction_certificate(CERTIFICATES / "t1_rules.json", CERTIFICATES / "t1_replay_erasure_certificate.json")["status"] == "PASS"
    assert check_induction_certificate(CERTIFICATES / "t2_rules.json", CERTIFICATES / "t2_closure_lifting_certificate.json")["status"] == "PASS"
    assert check_quorum_pivot_certificate(CERTIFICATES / "t3_quorum_pivot_certificate.json")["status"] == "PASS"


def test_tampered_certificate_rejected(tmp_path: Path) -> None:
    certificate = json.loads((CERTIFICATES / "t1_replay_erasure_certificate.json").read_text())
    certificate["premises"].remove("premise_duplicate_transition_stutters")
    damaged = tmp_path / "damaged.json"
    damaged.write_text(json.dumps(certificate))
    with pytest.raises(ProofFailure):
        check_induction_certificate(CERTIFICATES / "t1_rules.json", damaged)


def test_final_project_kernel_and_negative_controls(tmp_path: Path) -> None:
    output = tmp_path / "kernel.json"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "formal/project_kernel/proof_kernel.py"),
            str(ROOT / "formal/project_kernel/certificate.json"),
            "--json-output",
            str(output),
            "--negative-controls",
        ],
        check=True,
    )
    result = json.loads(output.read_text())
    assert result["status"] == "PASS"


def test_upstream_source_mapping() -> None:
    assert verify_source_mapping(ROOT)["status"] == "PASS"

