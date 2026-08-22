from __future__ import annotations

from pathlib import Path

from schedcheck.locking.reporting import run


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    output = root / "results" / "gate4p"
    result = run(root, output)
    print(result["decision"]["status"])
    print(output)
