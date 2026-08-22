from __future__ import annotations

import argparse
from pathlib import Path

from schedcheck.reporting import run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the exact bounded scheduler-grammar safety pilot."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Artifact repository root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/pilot"),
        help="Output directory, relative to root unless absolute.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    run(root, output)
    print(f"wrote exact pilot results to {output}")


if __name__ == "__main__":
    main()
