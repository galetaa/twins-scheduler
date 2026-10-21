#!/usr/bin/env python3
"""Explicit maintainer operation AFTER successful regeneration, never in verify."""
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'results/manifests/REFERENCE_SHA256SUMS'
paths={line.split(maxsplit=1)[1].strip() for line in p.read_text().splitlines() if line.strip()}
paths.update(str(x.relative_to(ROOT)) for x in (ROOT/'results/scaled').rglob('*') if x.is_file())
paths.add('manuscript/pdf/review_lipics_manuscript.pdf')
for path in paths:
    if not (ROOT/path).is_file(): raise SystemExit(f'missing generated reference: {path}')
p.write_text(''.join(f'{sha256((ROOT/path).read_bytes()).hexdigest()}  {path}\n' for path in sorted(paths)))
print(f'REFERENCE MANIFEST UPDATED: {len(paths)} files (verification must run separately)')
