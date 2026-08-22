from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("go") is None, reason="Go toolchain not available")
def test_controlled_comet_correspondence_fixture() -> None:
    completed = subprocess.run(
        ["go", "test", "./..."],
        cwd=ROOT / "implementation_fixture" / "go_harness",
        check=True,
        capture_output=True,
        text=True,
    )
    assert "ok" in completed.stdout
