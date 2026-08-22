from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

from scripts.run_implementation_fixture import run

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.skipif(shutil.which("go") is None, reason="Go toolchain not available")
def test_source_faithful_go_fixture(tmp_path: Path) -> None:
    result = run(ROOT, tmp_path)
    assert result["status"] == "PASS"
    assert all(result["source_checks"].values())
    assert all(result["fixture_checks"].values())
    serialized = json.loads((tmp_path / "implementation_correspondence.json").read_text())
    assert serialized["status"] == "PASS"
