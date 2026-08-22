#!/usr/bin/env python3
"""Create a deterministic inventory of the immutable supplied snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path


DISCOVERED = "2026-08-22"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def describe(relative: Path) -> tuple[str, str]:
    name = relative.name.lower()
    suffix = relative.suffix.lower()
    text = relative.as_posix().lower()
    if suffix == ".zip":
        if "gate" in name or "research_package" in name:
            return "historical gate package", "archive"
        if "post_audit" in name:
            return "post-audit layer", "archive"
        if "complete_project" in name:
            return "complete-project package", "archive"
        return "source archive", "archive"
    if suffix in {".lean", ".v", ".smt2"}:
        return "formal source", "source"
    if suffix in {".py", ".go", ".c", ".sh"}:
        return "executable source or check", "source"
    if suffix in {".tex", ".bib", ".cls", ".sty"}:
        return "manuscript source", "source"
    if suffix == ".pdf":
        return "rendered manuscript or figure", "generated result"
    if suffix in {".log", ".json", ".csv"} and (
        "result" in text or "log" in text or "build" in text
    ):
        return "execution evidence", "generated result"
    if "audit" in name or "review" in name or suffix in {".md", ".txt"}:
        return "report or research record", "report"
    if "sha256" in name or "manifest" in name:
        return "integrity metadata", "manifest"
    return "project material", "source"


def logical_family(relative: Path) -> str | None:
    name = relative.name.upper()
    if "MANUSCRIPT" in name and relative.suffix.lower() in {".md", ".pdf"}:
        cleaned = re.sub(r"20\d\d[-_]\d\d[-_]\d\d", "DATE", name)
        cleaned = re.sub(r"_(FINAL|REVISED|SUBMISSION|FULL|LIPICS|REVIEW)", "", cleaned)
        return f"manuscript:{cleaned}"
    if relative.suffix.lower() == ".zip" and any(
        token in name for token in ("GATE", "COMPLETE_PROJECT", "POST_AUDIT")
    ):
        return f"archive:{name}"
    return None


def replacement(relative: Path) -> str:
    name = relative.name
    gate_order = ["GATE0_3", "GATE0P_3P", "GATE4P", "GATE5P", "GATE6P", "GATE7P", "GATE8P"]
    for index, gate in enumerate(gate_order[:-1]):
        if gate in name:
            return gate_order[index + 1]
    if "TWINS_SCHEDULER_GATE8P" in name or "COMPLETE_PROJECT_2026-08-20" in name:
        return "TWINS_SCHEDULER_POST_AUDIT_FINAL_2026-08-20.zip"
    if "POST_AUDIT_FINAL_2026-08-20" in name:
        return "supplied final-complete snapshot dated 2026-08-21"
    if "FULL_MANUSCRIPT" in name and "2026-08-20" in name:
        return "manuscript/TWINS_SCHEDULER_FINAL_MANUSCRIPT_2026-08-21.pdf"
    if relative.suffix.lower() == ".md" and "MANUSCRIPT" in name and "2026-08-21" not in name:
        return "manuscript/FULL_MANUSCRIPT_FINAL_2026-08-21.md"
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_root", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("sums", type=Path)
    args = parser.parse_args()

    files = sorted(path for path in args.raw_root.rglob("*") if path.is_file())
    records: list[dict[str, str | int]] = []
    families: dict[str, set[str]] = {}
    hashes: dict[Path, str] = {}
    for path in files:
        relative = path.relative_to(args.raw_root)
        sha = digest(path)
        hashes[relative] = sha
        family = logical_family(relative)
        if family:
            families.setdefault(family, set()).add(sha)

    for relative in sorted(hashes):
        path = args.raw_root / relative
        stat = path.stat()
        role, material_type = describe(relative)
        family = logical_family(relative)
        records.append(
            {
                "original_name": relative.name,
                "original_relative_path": relative.as_posix(),
                "size_bytes": stat.st_size,
                "sha256": hashes[relative],
                "source_mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "discovered_date": DISCOVERED,
                "role": role,
                "source": "supplied TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21 snapshot",
                "material_type": material_type,
                "superseded_by": replacement(relative),
                "content_conflict": "yes" if family and len(families[family]) > 1 else "no",
            }
        )

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    with args.sums.open("w", encoding="utf-8", newline="\n") as stream:
        for relative in sorted(hashes):
            stream.write(f"{hashes[relative]}  raw_inputs/{relative.as_posix()}\n")


if __name__ == "__main__":
    main()
