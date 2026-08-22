import json
import subprocess
from pathlib import Path

from twins_scheduler.event_loop import compare_suites, evaluate_suite


ROOT = Path(__file__).resolve().parents[2]


def go_json(package: str) -> dict[str, object]:
    process = subprocess.run(
        ["go", "run", package],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(process.stdout)


def test_full_event_loop_terminal_observations_match() -> None:
    assert compare_suites(evaluate_suite(), go_json("./src/go/full_event_loop"))["status"] == "PASS"


def test_go_arbitrary_precision_quorum_check() -> None:
    result = go_json("./src/go/proof_crosscheck")
    assert result["status"] == "PASS"
    assert result["cases_checked"] == 1028

