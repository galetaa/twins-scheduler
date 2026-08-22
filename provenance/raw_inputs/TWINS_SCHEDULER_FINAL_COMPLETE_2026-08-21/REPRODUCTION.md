# Reproduction contract

## One command

```bash
./reproduce.sh
```

Run it from the project root. It does not contact a blockchain network and does not require a dataset.

## Always-executed checks in the verified environment

- independent theorem, scheduler, observation, and bounded protocol checks;
- Python bounded CometBFT/Tendermint refinement;
- Go bounded refinement;
- exact Python/Go terminal-row comparison;
- focused pytest suite;
- project-local certificate kernel 1.1.0 and five negative controls;
- twelve Z3 obligations/controls through the local Z3 shared library;
- Lean/Coq source-hygiene scan;
- A4 review-PDF build and content checks.

Expected core outcomes:

```text
independent theorem checks                   PASS
bounded CometBFT Python refinement           PASS
bounded CometBFT Go refinement               PASS
Python/Go terminal-row comparison            PASS
bounded refinement pytest                    PASS
project-local proof certificate              PASS
SMT obligations and controls                 PASS
formal source hygiene                        PASS
A4 review PDF build                          PASS
```

## Conditional external checks

### Lean

The project is pinned by `formal/lean/lean-toolchain`. With `lean` and `lake` available:

```bash
cd formal/lean
lake build
lake env lean AxiomAudit.lean
```

The GitHub workflow `.github/workflows/lean.yml` performs the build, LeanChecker, NanoDA, and no-sorry checks. It was not executed in the verified environment.

To require the local Lean build:

```bash
STRICT_MATURE_PROVER=1 ./reproduce.sh
```

### Coq

With `coqc` available, the reproduction script compiles the parallel Coq files. This route is secondary to the pinned Lean project.

### Official LIPIcs class

Place the current official author package, including `lipics-v2021.cls`, in the TeX path or in `manuscript/lipics/`, then run:

```bash
cd manuscript/lipics
latexmk -pdf -interaction=nonstopmode -halt-on-error main_lipics.tex
```

The supplied A4 PDF is a review build. It is not labeled as an official-class build.

## Determinism

Machine-readable theorem, protocol, kernel, and SMT results are deterministic. The review PDF is checked by page count, extracted text, fonts, LaTeX warnings, and rendered-page inspection rather than by assuming byte-identical TeX metadata across hosts.
