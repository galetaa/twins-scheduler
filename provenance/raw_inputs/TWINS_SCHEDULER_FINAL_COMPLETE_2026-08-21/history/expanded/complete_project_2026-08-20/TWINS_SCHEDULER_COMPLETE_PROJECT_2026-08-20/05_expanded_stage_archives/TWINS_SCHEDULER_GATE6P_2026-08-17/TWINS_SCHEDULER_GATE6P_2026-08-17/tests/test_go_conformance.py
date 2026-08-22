from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conformance.corpus import generate_corpus
from conformance.python_harness import execute_corpus

ROOT = Path(__file__).resolve().parents[1]


def test_pinned_source_snapshot_contains_queue_and_admission_semantics() -> None:
    network = (ROOT / "inputs" / "hotstuff_snapshot" / "network.go").read_text(
        encoding="utf-8"
    )
    for snippet in (
        "i := int(view) - 1",
        "if i >= len(n.views)",
        "partition.Contains(sender) && partition.Contains(receiver)",
        "_, ok := n.dropTypes[reflect.TypeOf(message)]",
        "if msg.view > n.globalView",
        "if len(n.pendingMessages) == len(nextMsgs)",
        "n.globalView++",
    ):
        assert snippet in network


@pytest.mark.skipif(shutil.which("go") is None, reason="Go toolchain not available")
def test_go_fixture_and_python_abstraction_are_extensionally_equal(tmp_path) -> None:
    payload = generate_corpus(seed=7, random_cases=24)
    executable_payload = {"cases": payload["cases"]}
    expected = execute_corpus(executable_payload)

    binary = tmp_path / "harness_fixture"
    subprocess.run(
        ["go", "build", "-trimpath", "-o", str(binary), "."],
        cwd=ROOT / "conformance" / "go_harness",
        check=True,
        capture_output=True,
        text=True,
    )
    completed = subprocess.run(
        [str(binary)],
        input=json.dumps(executable_payload, sort_keys=True),
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(completed.stdout) == expected
