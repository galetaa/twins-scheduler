from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest

from schedcheck.gate6.event_loop import (
    compare_suites,
    evaluate_suite,
    order_sensitivity,
)

ROOT = Path(__file__).resolve().parents[1]
GO_FIXTURE = ROOT / "implementation_fixture" / "full_event_loop"
BIGINT_FIXTURE = ROOT / "implementation_fixture" / "proof_crosscheck"


def test_python_full_event_loop_reproduces_boundary() -> None:
    result = evaluate_suite()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())
    typed_mutant = next(
        case
        for case in result["cases"]
        if case["grammar"] == "G_T_TYPE_SPECIFIC"
        and case["mutation"] == "MISSING_LOCK_UPDATE"
    )
    assert typed_mutant["unsafe"]
    assert {row["value"] for row in typed_mutant["decisions"]} == {0, 1}


def test_bounded_event_order_sensitivity() -> None:
    result = order_sensitivity(random_seeds=32, first_seed=0)
    assert result["status"] == "PASS"
    assert result["runs_checked"] == 34
    assert result["case_runs_checked"] == 204
    assert not result["classification_failures"]


@pytest.mark.skipif(shutil.which("go") is None, reason="Go unavailable")
def test_go_event_loop_and_python_conform() -> None:
    subprocess.run(["go", "test", "./..."], cwd=GO_FIXTURE, check=True)
    process = subprocess.run(
        ["go", "run", "."],
        cwd=GO_FIXTURE,
        text=True,
        capture_output=True,
        check=True,
    )
    go_result = json.loads(process.stdout)
    python_result = evaluate_suite()
    assert go_result["status"] == "PASS"
    assert compare_suites(python_result, go_result)["status"] == "PASS"


@pytest.mark.skipif(shutil.which("go") is None, reason="Go unavailable")
def test_independent_bigint_crosscheck() -> None:
    subprocess.run(["go", "test", "./..."], cwd=BIGINT_FIXTURE, check=True)
    process = subprocess.run(
        ["go", "run", "."],
        cwd=BIGINT_FIXTURE,
        text=True,
        capture_output=True,
        check=True,
    )
    result = json.loads(process.stdout)
    assert result["status"] == "PASS"
    assert result["cases_checked"] == 1028
    assert len(result["largest_f"]) == 400
    assert not result["failed_cases"]
