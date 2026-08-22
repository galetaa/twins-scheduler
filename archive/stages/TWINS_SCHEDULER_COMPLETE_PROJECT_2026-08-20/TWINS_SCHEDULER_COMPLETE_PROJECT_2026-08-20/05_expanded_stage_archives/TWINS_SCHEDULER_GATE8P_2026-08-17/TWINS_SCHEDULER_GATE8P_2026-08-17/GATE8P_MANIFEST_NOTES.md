# Gate 8′ Manifest Notes

`GATE8P_MANIFEST.sha256` covers every non-transient file in the Gate 8′ directory except:

- itself; and
- `manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf`.

The PDF is intentionally excluded from byte-for-byte regeneration because the XeLaTeX/dvipdfmx toolchain writes a fresh trailer identifier even when the document content, source, page count, geometry, and fixed source epoch are unchanged. The delivered PDF is protected by the outer ZIP SHA-256. The reproduction script instead regenerates the PDF and validates its title, A4 geometry, 17-page count, LaTeX warnings, and load-bearing text. The deterministic Markdown and generated `main.tex` remain covered by the manifest.
