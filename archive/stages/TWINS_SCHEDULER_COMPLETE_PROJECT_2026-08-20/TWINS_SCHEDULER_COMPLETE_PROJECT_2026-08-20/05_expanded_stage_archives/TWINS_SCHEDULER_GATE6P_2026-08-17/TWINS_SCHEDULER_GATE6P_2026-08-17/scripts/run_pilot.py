from __future__ import annotations

from pathlib import Path

from schedcheck.reporting import run


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    run(root, root / "results" / "pilot")
    print(root / "results" / "pilot")
