# Gate 8′ Reproducibility Contract

## Command

```bash
./scripts/reproduce_gate8p.sh
```

## Fixed environment assumptions

The verified host uses CPython 3.13.5, Go 1.23.2, Z3 4.13.3.0, Pandoc 3.1.11.1, XeLaTeX from TeX Live 2024, `pdftotext`, `pdfinfo`, `unzip`, and GNU `sha256sum`. `PYTHONHASHSEED=0`, UTC, and a fixed `SOURCE_DATE_EPOCH` are set by the runner.

The artifact is intentionally offline. No test requires a blockchain node, RPC endpoint, public network, private key, cloud service, GPU, or external dataset.

## Reproduced layers

1. Gate 7 theorem and event-loop evidence.
2. Gate 5 exact locking kernels from the nested frozen archive.
3. Gate 8 claim ledger and decision consistency.
4. Manuscript LaTeX and PDF from the Markdown source and pinned figures.
5. PDF page count, A4 geometry, and required load-bearing text.
6. Frozen Gate 8 checksums.

## Smoke-test exception

`GATE8_SKIP_LEGACY=1 ./scripts/reproduce_gate8p.sh` omits the nested Gate 5 rerun. It is useful only for checking the Gate 7 core and manuscript pipeline and does not fully reproduce the two-kernel claim.

## Non-reproduced submission blocker

The Lean scaffold is not part of the accepted proof route because Lean/Lake were unavailable in the verified environment. A future successful kernel build must be recorded separately and added to a new artifact version.
