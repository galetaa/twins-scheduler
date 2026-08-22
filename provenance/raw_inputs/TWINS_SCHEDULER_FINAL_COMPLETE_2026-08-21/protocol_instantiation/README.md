# Protocol instantiation artifact

Run from the project root:

```bash
python src/cometbft_bounded.py
(cd go/cometbft_refinement && go run .)
python -m pytest -q tests/test_cometbft_bounded.py
```

The two implementations write deterministic results to `results/final/`.
`COMETBFT_V0393_MAPPING.md` states the exact refinement scope and nonclaims.
