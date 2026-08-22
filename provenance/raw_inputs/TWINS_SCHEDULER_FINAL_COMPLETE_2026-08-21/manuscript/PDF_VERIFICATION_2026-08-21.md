# PDF verification — 21 August 2026

## Artifact

- File: `manuscript/TWINS_SCHEDULER_FINAL_MANUSCRIPT_2026-08-21.pdf`
- SHA-256: `a5a32cd0e5afa60b0f2c981ebbd2b17975baad506eb2a0f71a6dcba962a5d4a9`
- Size: 190990 bytes
- Page geometry: A4, 595.28 x 841.89 pt
- Physical pages: 13
- Structure: one anonymous cover page followed by twelve numbered article pages, including references
- PDF version: 1.5
- Encryption, forms, JavaScript, and embedded attachments: absent

## Build verification

The PDF was rebuilt from the final manuscript source with the project script. Two XeLaTeX passes completed successfully. The targeted warning scan found no overfull boxes, undefined references, missing citations, missing glyphs, emergency stops, or fatal LaTeX errors.

The current environment does not contain `lipics-v2021.cls`. Therefore this file is an A4 review build using the compatibility source, not an official Dagstuhl-class build. The official-class source is preserved under `manuscript/lipics/`.

## Font and structural checks

- `pdfinfo`: PASS
- `qpdf --check`: PASS
- `mutool info`: PASS
- Font embedding: PASS; every listed font is embedded and subsetted
- Unicode maps: present for all text fonts used in the manuscript
- Page count and A4 geometry: PASS

## Render verification

The PDF was rendered at 180 dpi with the project PDF workflow. Rendered pages are preserved under `manuscript/rendered_final/`.

A montage covering the cover, introduction, formal definitions, structural theorem, Boolean derivation, Tendermint-style bridge, replay theorem, validity section, conclusion, and references was inspected. Full-resolution pages 8 and 9 were additionally inspected because they contain the densest theorem and protocol-instantiation material.

Observed result:

- no clipped text;
- no overlapping paragraphs, tables, equations, headers, or footers;
- no black squares, missing symbols, or broken glyphs;
- figures and tables remain within margins;
- page numbers and running headers are visible;
- references fit within the final page;
- equations are legible at ordinary zoom.

## Verdict

**PASS AS AN A4 REVIEW PDF.**

The PDF is suitable for review and proof checking. Submission remains blocked until the same source is compiled with the current official LIPIcs author package and the official build is visually checked again.
