#!/usr/bin/env python3
"""Map promoted active files back to immutable historical sources."""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "provenance" / "CANONICAL_FILE_MAP.csv"
ACTIVE_ROOTS = (
    "src",
    "formal",
    "models",
    "manuscript",
    "docs/research",
    "docs/reviews",
    "results/reference",
)
ACTIVE_FILES = ("LICENSE", "THIRD_PARTY_NOTICES.md", "lean-toolchain")


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def preference(path: Path) -> tuple[int, int, str]:
    text = path.as_posix()
    if "provenance/raw_inputs/TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21/" in text and "/history/" not in text:
        return (0, len(text), text)
    if "archive/stages/TWINS_SCHEDULER_GATE8P_2026-08-17/" in text and text.count("TWINS_SCHEDULER_GATE8P_2026-08-17") == 2:
        return (1, len(text), text)
    return (2, len(text), text)


def reason(destination: str) -> str:
    if destination.startswith("src/python"):
        return "latest verified Python model promoted into canonical package"
    if destination.startswith("src/go"):
        return "latest corresponding Go implementation promoted into one module"
    if destination.startswith("formal/lean"):
        return "2026-08-21 post-audit Lean source selected as primary mature proof"
    if destination.startswith("formal/coq"):
        return "post-audit Coq source retained as secondary formalization"
    if destination.startswith("formal/smt"):
        return "post-audit SMT obligation or damaged control"
    if destination.startswith("formal/"):
        return "supporting proof certificate or project-local kernel"
    if destination.startswith("manuscript/markdown"):
        return "newest content-complete manuscript text"
    if destination.startswith("manuscript/pdf"):
        return "newest supplied PDF retained explicitly as historical review build"
    if destination.startswith("manuscript/"):
        return "newest supplied paper source or figure"
    if destination.startswith("models/"):
        return "latest protocol correspondence source retained with license"
    if destination.startswith("results/reference"):
        return "supplied result retained as reference, not substituted for a new run"
    if destination.startswith("docs/"):
        return "latest audit or research record promoted into canonical documentation"
    return "selected license, notice, or pinned toolchain metadata"


def main() -> None:
    existing: dict[str, str] = {}
    if OUTPUT.exists():
        with OUTPUT.open(encoding="utf-8", newline="") as stream:
            existing = {row["new_path"]: row["historical_source"] for row in csv.DictReader(stream)}

    sources = [
        path
        for base in (ROOT / "provenance" / "raw_inputs", ROOT / "archive" / "stages")
        for path in base.rglob("*")
        if path.is_file()
    ]
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for path in sources:
        by_hash[sha256(path)].append(path)

    active: list[Path] = []
    for name in ACTIVE_ROOTS:
        base = ROOT / name
        if base.exists():
            active.extend(path for path in base.rglob("*") if path.is_file())
    active.extend(ROOT / name for name in ACTIVE_FILES if (ROOT / name).is_file())

    rows: list[dict[str, str]] = []
    for destination_path in sorted(set(active)):
        destination = destination_path.relative_to(ROOT).as_posix()
        source: Path | None = None
        if destination in existing:
            candidate = ROOT / existing[destination]
            if candidate.is_file():
                source = candidate
        if source is None:
            matches = by_hash.get(sha256(destination_path), [])
            if matches:
                source = min(matches, key=preference)
        if source is None:
            continue
        rows.append(
            {
                "historical_source": source.relative_to(ROOT).as_posix(),
                "old_path": source.relative_to(ROOT).as_posix(),
                "new_path": destination,
                "old_sha256": sha256(source),
                "new_sha256": sha256(destination_path),
                "content_changed_during_consolidation": "yes" if sha256(source) != sha256(destination_path) else "no",
                "selection_reason": reason(destination),
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
