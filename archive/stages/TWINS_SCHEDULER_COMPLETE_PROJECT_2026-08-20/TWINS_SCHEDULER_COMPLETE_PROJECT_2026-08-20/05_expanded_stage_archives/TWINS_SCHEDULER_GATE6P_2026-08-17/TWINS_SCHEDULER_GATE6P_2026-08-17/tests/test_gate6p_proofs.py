from __future__ import annotations

import json
from pathlib import Path

import pytest

from schedcheck.gate6.proof_kernel import (
    ProofFailure,
    check_induction_certificate,
    check_quorum_pivot_certificate,
    parse_polynomial,
)

ROOT = Path(__file__).resolve().parents[1]
PROOFS = ROOT / "proofs_checked"


def test_t1_t2_and_t3_certificates_check() -> None:
    t1 = check_induction_certificate(
        PROOFS / "t1_rules.json",
        PROOFS / "t1_replay_erasure_certificate.json",
    )
    t2 = check_induction_certificate(
        PROOFS / "t2_rules.json",
        PROOFS / "t2_closure_lifting_certificate.json",
    )
    t3 = check_quorum_pivot_certificate(
        PROOFS / "t3_quorum_pivot_certificate.json"
    )
    assert t1["status"] == "PASS"
    assert t2["status"] == "PASS"
    assert t3["status"] == "PASS"
    assert t1["trusted_induction_rule"] == "well_founded_induction_on_Nat"
    assert t3["branch_results"]["directed_edge_present"].endswith(
        "after repair"
    )


def test_t1_certificate_rejects_missing_required_premise(tmp_path: Path) -> None:
    certificate = json.loads(
        (PROOFS / "t1_replay_erasure_certificate.json").read_text()
    )
    certificate["premises"].remove("premise_duplicate_transition_stutters")
    tampered = tmp_path / "tampered_t1.json"
    tampered.write_text(json.dumps(certificate), encoding="utf-8")
    with pytest.raises(ProofFailure, match="missing facts"):
        check_induction_certificate(PROOFS / "t1_rules.json", tampered)


def test_t3_certificate_rejects_repaired_branch_reaching_quorum(
    tmp_path: Path,
) -> None:
    certificate = json.loads(
        (PROOFS / "t3_quorum_pivot_certificate.json").read_text()
    )
    certificate["branches"]["directed_edge_present"]["second_support"] = (
        "2*f+1"
    )
    tampered = tmp_path / "tampered_t3.json"
    tampered.write_text(json.dumps(certificate), encoding="utf-8")
    with pytest.raises(ProofFailure, match="miss second quorum by one"):
        check_quorum_pivot_certificate(tampered)


def test_polynomial_kernel_rejects_untrusted_syntax() -> None:
    with pytest.raises(ProofFailure, match="unsupported syntax"):
        parse_polynomial("f ** 2")
