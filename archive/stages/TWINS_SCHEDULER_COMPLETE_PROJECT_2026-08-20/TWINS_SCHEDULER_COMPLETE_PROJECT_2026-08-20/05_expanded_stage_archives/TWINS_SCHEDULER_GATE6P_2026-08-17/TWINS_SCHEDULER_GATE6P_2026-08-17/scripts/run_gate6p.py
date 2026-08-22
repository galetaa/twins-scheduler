#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from schedcheck.formal.source_mapping import verify_source_mapping  # noqa: E402
from schedcheck.gate6.event_loop import (  # noqa: E402
    compare_suites,
    evaluate_suite,
    order_sensitivity,
)
from schedcheck.gate6.necessity import (  # noqa: E402
    exhaustive_premise_characterization,
    parameter_sensitivity,
    premise_ablation_matrix,
)
from schedcheck.gate6.proof_kernel import (  # noqa: E402
    check_induction_certificate,
    check_quorum_pivot_certificate,
    write_json,
)

OUT = ROOT / "results" / "gate6p"
PROOFS = ROOT / "proofs_checked"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_json(command: list[str], cwd: Path) -> tuple[dict[str, object], str]:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    log = (
        f"$ {' '.join(command)}\n"
        f"exit={process.returncode}\n"
        f"--- stdout ---\n{process.stdout}"
        f"--- stderr ---\n{process.stderr}"
    )
    if process.returncode != 0:
        raise RuntimeError(log)
    try:
        value = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not emit JSON\n{log}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"command emitted non-object JSON\n{log}")
    return value, log


def _go_fixture(directory: Path) -> tuple[dict[str, object], str]:
    test = subprocess.run(
        ["go", "test", "./..."],
        cwd=directory,
        text=True,
        capture_output=True,
        check=False,
    )
    if test.returncode != 0:
        raise RuntimeError(
            f"Go tests failed in {directory}\n{test.stdout}\n{test.stderr}"
        )
    value, run_log = _run_json(["go", "run", "."], directory)
    return value, (
        "$ go test ./...\n"
        f"exit={test.returncode}\n{test.stdout}{test.stderr}\n"
        + run_log
    )


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def _proof_kernel_report() -> dict[str, object]:
    path = ROOT / "src" / "schedcheck" / "gate6" / "proof_kernel.py"
    text = path.read_text(encoding="utf-8")
    logical_lines = [
        line
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "physical_lines": len(text.splitlines()),
        "nonblank_noncomment_lines": len(logical_lines),
        "runtime_dependencies": [],
        "trusted_primitives": [
            "finite Horn-rule application",
            "well-founded induction schema on natural-number measures",
            "exact univariate integer-polynomial normalization",
            "dedicated quorum-branch certificate checks",
        ],
        "assurance_boundary": (
            "small auditable proof script; not equivalent to a mature proof "
            "assistant kernel or independent peer review"
        ),
    }


def _case_matrix(suite: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in suite["cases"]:  # type: ignore[index]
        rows.append(
            {
                "grammar": case["grammar"],
                "mutation": case["mutation"],
                "unsafe": case["unsafe"],
                "decisions": json.dumps(case["decisions"], sort_keys=True),
                "locks": json.dumps(case["locks"], sort_keys=True),
                "polka_rounds": json.dumps(case["polka_rounds"]),
                "commit_rounds": json.dumps(case["commit_rounds"]),
            }
        )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    logs: list[str] = []

    inherited = _load_json(ROOT / "results" / "gate5p" / "gate5p_decision.json")
    if inherited.get("status") != "PASS":
        raise RuntimeError("Gate 5' prerequisite is not PASS")

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
    write_json(OUT / "t1_replay_erasure_proof_check.json", t1)
    write_json(OUT / "t2_closure_lifting_proof_check.json", t2)
    write_json(OUT / "t3_quorum_pivot_proof_check.json", t3)
    kernel_report = _proof_kernel_report()
    write_json(OUT / "proof_kernel_report.json", kernel_report)

    ablation = premise_ablation_matrix()
    characterization = exhaustive_premise_characterization()
    sensitivity = parameter_sensitivity(
        max_f=256, random_cases=256, seed=60617
    )
    write_json(OUT / "premise_ablation.json", ablation)
    write_json(OUT / "premise_characterization.json", characterization)
    write_json(OUT / "parameter_sensitivity.json", sensitivity)
    _write_csv(OUT / "premise_ablation.csv", ablation["ablations"])
    _write_csv(
        OUT / "premise_truth_table.csv", characterization["truth_table"]
    )

    python_loop = evaluate_suite(strategy="fifo", seed=0)
    order = order_sensitivity(random_seeds=256, first_seed=0)
    write_json(OUT / "full_event_loop_python.json", python_loop)
    write_json(OUT / "event_order_sensitivity.json", order)

    go_available = shutil.which("go") is not None
    if not go_available:
        raise RuntimeError("Go toolchain is required for Gate 6' cross-checks")

    go_loop, go_loop_log = _go_fixture(
        ROOT / "implementation_fixture" / "full_event_loop"
    )
    logs.append(go_loop_log)
    write_json(OUT / "full_event_loop_go.json", go_loop)
    conformance = compare_suites(python_loop, go_loop)
    write_json(OUT / "full_event_loop_conformance.json", conformance)
    _write_csv(OUT / "full_event_loop_matrix.csv", _case_matrix(go_loop))

    bigint, bigint_log = _go_fixture(
        ROOT / "implementation_fixture" / "proof_crosscheck"
    )
    logs.append(bigint_log)
    write_json(OUT / "t3_bigint_crosscheck.json", bigint)

    source_mapping = verify_source_mapping(ROOT)
    write_json(OUT / "pinned_source_recheck.json", source_mapping)

    theorem_ledger: dict[str, object] = {
        "T1_replay_erasure": {
            "statement": (
                "Deleting non-first deliveries of stable replay keys preserves "
                "protocol-relevant finite behavior and state-based safety "
                "observations under explicit stutter, no-output, suffix-congruence, "
                "and observation-extensionality assumptions."
            ),
            "status": "CHECKED_BY_SMALL_TRUSTED_PROOF_SCRIPT",
            "proof_result": "results/gate6p/t1_replay_erasure_proof_check.json",
            "residual_obligation": (
                "Map stable-key idempotence assumptions to each studied implementation; "
                "the theorem does not erase equivocations or side-effectful callbacks."
            ),
        },
        "T2_relational_closure_lifting": {
            "statement": (
                "R-increasing closure insertions preserve finite unsafety when original "
                "steps forward-simulate R and Unsafe is upward closed under R."
            ),
            "status": "CHECKED_BY_SMALL_TRUSTED_PROOF_SCRIPT",
            "proof_result": "results/gate6p/t2_closure_lifting_proof_check.json",
            "residual_obligation": (
                "Each protocol instantiation must discharge the local R-monotonicity "
                "and forward-simulation premises; locking repair messages can violate them."
            ),
        },
        "T3_parametric_quorum_pivot_separation": {
            "statement": (
                "For every f>=1 the supplied n=3f+1, q=2f+1 two-branch schema "
                "admits a phase-specific unsafe execution while both type-uniform "
                "directed edge choices remain safe."
            ),
            "status": "CHECKED_CERTIFICATE_PLUS_INDEPENDENT_BIGINT_CROSSCHECK",
            "proof_result": "results/gate6p/t3_quorum_pivot_proof_check.json",
            "independent_crosscheck": "results/gate6p/t3_bigint_crosscheck.json",
            "fuller_loop_validation": "results/gate6p/full_event_loop_go.json",
            "scope": (
                "existential separation for an explicit protocol schema, not universal "
                "incompleteness of directed or partition schedules"
            ),
        },
        "T4_terminal_delay_boundary": {
            "status": "INHERITED_CONDITIONAL_COROLLARY_WITH_REGRESSION_EVIDENCE",
            "source": "results/gate5p/gate5p_theorem_ledger.json",
        },
        "T5_non_idempotent_replay_separation": {
            "status": "INHERITED_CONSTRUCTIVE_BOUNDARY",
            "source": "results/gate5p/gate5p_theorem_ledger.json",
        },
        "T6_boolean_premise_characterization": {
            "statement": characterization["exact_characterization"],
            "status": "EXHAUSTIVE_EXACT_FOR_SUPPLIED_SEVEN_FLAG_MODEL",
            "assignments_checked": characterization["assignments_checked"],
            "strict_patterns": characterization[
                "strict_patterns_in_field_order"
            ],
            "scope": characterization["scope"],
        },
    }
    write_json(OUT / "gate6p_theorem_ledger.json", theorem_ledger)

    checks = {
        "gate5_prerequisite_passes": inherited.get("status") == "PASS",
        "T1_checked_proof_passes": t1["status"] == "PASS",
        "T2_checked_proof_passes": t2["status"] == "PASS",
        "T3_checked_certificate_passes": t3["status"] == "PASS",
        "T3_independent_bigint_crosscheck_passes": bigint.get("status") == "PASS",
        "one_at_a_time_premise_ablation_passes": ablation["status"] == "PASS",
        "exact_premise_characterization_passes": characterization["status"] == "PASS",
        "parameter_sensitivity_passes": sensitivity["status"] == "PASS",
        "python_full_event_loop_passes": python_loop["status"] == "PASS",
        "go_full_event_loop_passes": go_loop.get("status") == "PASS",
        "go_python_full_event_loop_conforms": conformance["status"] == "PASS",
        "event_order_sensitivity_passes": order["status"] == "PASS",
        "pinned_source_mapping_still_passes": source_mapping["status"] == "PASS",
    }
    checks["status"] = (
        "PASS"
        if all(value for key, value in checks.items() if key != "status")
        else "FAIL"
    )
    write_json(OUT / "gate6p_machine_checks.json", checks)

    pass_gate = checks["status"] == "PASS"
    decision = {
        "gate": "Gate 6'",
        "status": "PASS" if pass_gate else "FAIL",
        "decision": "PASS / GO TO GATE 7'" if pass_gate else "NO-GO",
        "research_status": (
            "READY_FOR_REPRODUCIBLE_PAPER_AND_ARTIFACT_BUILD_IN_NARROW_SCOPE"
            if pass_gate
            else "REQUIRES_SUBSTANTIAL_PIVOT"
        ),
        "scientific_claim": (
            "Safety-observation closure boundaries of scheduler grammars for "
            "certificate-driven locking BFT protocols"
        ),
        "claim_freeze": (
            "Phase/type erasure can remove finite agreement-violation witnesses in "
            "an explicit certificate-driven locking schema because closure-added "
            "repair evidence disables a unique honest quorum pivot; exact replay is "
            "erasable only under stable-key idempotence."
        ),
        "gate6_new_evidence": [
            "checked proof scripts for T1 and T2 with explicit trusted assumptions",
            "exact polynomial and branch certificate for T3",
            "independent Go math/big cross-check for 1,028 parameters including a 400-digit f",
            "full two-round Go event loop with proposal, prevote, POLKA, precommit, and COMMIT",
            "independent Python mirror with 6/6 exact conformance cases",
            "258 queue strategies/seeds and 1,548 case runs with unchanged safety classification",
            "complete 2^7 premise truth table and exact Boolean characterization for the supplied construction",
        ],
        "publication_readiness": (
            "NOT_YET_SUBMISSION_READY: Gate 7 must freeze the artifact, regenerate "
            "tables/figures, and obtain independent human proof review or migrate the "
            "small proofs to a mature prover."
        ),
        "residual_risks": [
            "the checked proof kernel is deliberately small but is not Lean/Coq/Isabelle",
            "the fuller event loop is an isolated local fixture, not the complete CometBFT implementation",
            "T3 is an existence/separation theorem for an explicit schema, not a universal scheduler-minimality theorem",
            "novelty remains conditional on the enumerated search and possible hidden engineering prior art",
        ],
        "prohibited_claims": [
            "production CometBFT or HotStuff vulnerability",
            "universal incompleteness of partition or directed schedules",
            "universal minimality of G_T",
            "liveness or unbounded partial-synchrony completeness",
            "bug prevalence or discovery probability",
            "absolute novelty",
        ],
    }
    write_json(OUT / "gate6p_decision.json", decision)

    environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "go": subprocess.run(
            ["go", "version"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "runtime_dependencies": [],
        "pythonhashseed_required_for_reproduction": "0",
        "random_seed_for_parameter_sensitivity": 60617,
        "event_order_seed_range": [0, 255],
        "network_access_during_checks": "none",
        "public_network_interaction": "none",
    }
    write_json(OUT / "environment.json", environment)
    (OUT / "run_log.txt").write_text("\n\n".join(logs), encoding="utf-8")

    status_rows = [
        {
            "work_package": "WP6.1 T1/T2 proof hardening",
            "status": "PASS" if t1["status"] == t2["status"] == "PASS" else "FAIL",
            "evidence": (
                "results/gate6p/t1_replay_erasure_proof_check.json; "
                "results/gate6p/t2_closure_lifting_proof_check.json"
            ),
        },
        {
            "work_package": "WP6.2 T3 proof hardening",
            "status": "PASS" if t3["status"] == bigint.get("status") == "PASS" else "FAIL",
            "evidence": (
                "results/gate6p/t3_quorum_pivot_proof_check.json; "
                "results/gate6p/t3_bigint_crosscheck.json"
            ),
        },
        {
            "work_package": "WP6.3 fuller event-loop mutation",
            "status": "PASS" if go_loop.get("status") == conformance["status"] == "PASS" else "FAIL",
            "evidence": (
                "results/gate6p/full_event_loop_go.json; "
                "results/gate6p/full_event_loop_conformance.json"
            ),
        },
        {
            "work_package": "WP6.4 necessity characterization",
            "status": "PASS" if characterization["status"] == "PASS" else "FAIL",
            "evidence": "results/gate6p/premise_characterization.json",
        },
        {
            "work_package": "WP6.5 artifact hardening",
            "status": "CONDITIONAL PASS",
            "evidence": (
                "scripts/reproduce_gate6p.sh; scripts/selfcheck_gate6p.py; "
                "final clean-copy verification is performed during packaging"
            ),
        },
        {
            "work_package": "WP6.6 paper claim freeze",
            "status": "PASS WITH NARROW CLAIM",
            "evidence": "gate6p/PAPER_CLAIM_FREEZE.md",
        },
        {
            "work_package": "Gate 6' overall",
            "status": decision["decision"],
            "evidence": "results/gate6p/gate6p_decision.json",
        },
    ]
    _write_csv(ROOT / "GATE_STATUS.csv", status_rows)

    print(json.dumps(decision, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if pass_gate else 1


if __name__ == "__main__":
    raise SystemExit(main())
