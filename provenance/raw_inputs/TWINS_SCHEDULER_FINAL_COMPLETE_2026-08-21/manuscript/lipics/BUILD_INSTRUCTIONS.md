# Official LIPIcs build instructions

The source targets the current Dagstuhl Publishing style `lipics-v2021 v2021.1.3` in A4 anonymous mode.

Required files from the official LIPIcs author package must be placed in this directory or made visible to TeX, including `lipics-v2021.cls`, `plainurl.bst`, and the style's image assets.

```bash
pdflatex -interaction=nonstopmode -halt-on-error main_lipics.tex
bibtex main_lipics
pdflatex -interaction=nonstopmode -halt-on-error main_lipics.tex
pdflatex -interaction=nonstopmode -halt-on-error main_lipics.tex
```

Acceptance criteria:

- no LaTeX or BibTeX errors;
- no undefined references or citations;
- no overfull boxes;
- A4 paper;
- one separate cover page;
- at most 15 main-text pages excluding cover, references, and appendices;
- all figures are PDF;
- bibliography uses `plainurl`.

The included review PDF is built with a local A4 compatibility template because the official class is not installed in the execution environment. It is not represented as an official-class build.
