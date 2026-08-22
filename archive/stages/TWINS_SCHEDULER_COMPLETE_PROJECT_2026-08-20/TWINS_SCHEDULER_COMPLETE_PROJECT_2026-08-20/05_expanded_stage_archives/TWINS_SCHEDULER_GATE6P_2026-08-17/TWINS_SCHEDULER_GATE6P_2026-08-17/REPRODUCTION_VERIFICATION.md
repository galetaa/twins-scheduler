# Gate 6′ independent clean-copy reproduction verification

**Verification date:** 17 August 2026  
**Result:** **PASS**

## 1. Procedure

The final package was copied to a new directory while excluding
`.pytest_cache`, `.venv`, all `__pycache__` directories, and `.pyc`/`.pyo`
files. The following offline workflow was executed:

```bash
./scripts/reproduce_gate6p.sh
```

The workflow:

1. regenerated every Gate 6′ machine-readable result;
2. compiled and tested both Go fixtures;
3. ran the full fast regression suite;
4. rechecked T1–T3 proof certificates;
5. recomputed the 128-row premise truth table;
6. reran parameter and event-order sensitivity;
7. performed the independent Gate 6′ self-check;
8. verified the deterministic core manifest and the stable artifact manifest.

## 2. Environment

```text
CPython 3.13.5
Go 1.23.2 linux/amd64
pytest 9.0.2
uv 0.10.0
PYTHONHASHSEED=0
runtime Python dependencies: none
network access during reproduction: none
```

## 3. Checker results

```text
Gate 6′ runner: PASS / GO TO GATE 7′
full fast pytest suite: 43 passed, 28 skipped
Gate 6′ self-check: PASS
checked proofs: T1, T2, T3
premise assignments: 128
parameter cases: 512
Go big-int cases: 1,028
Go/Python fuller-loop conformance: 6/6
bounded event-order case runs: 1,548
```

The 28 skipped tests are older Gate 4′/5′ exhaustive searches whose same state
spaces were already regenerated and checked by the inherited runners. They are
skipped in fast reproduction mode to avoid duplicating expensive enumeration.

## 4. Byte-for-byte determinism

`CORE_RESULTS.sha256` contains 21 decisive files: the Gate 6′ decision, theorem
ledger, aggregate checks, proof results, fuller-loop outputs, conformance result,
premise analyses, parameter sensitivity, environment, source recheck, and gate
status.

The clean-copy workflow verified all 21 entries:

```text
core files listed: 21
core files verified: 21
mismatches: 0
CORE_RESULTS.sha256 digest:
4fc5051e85adbd9b63db55162d66d980e9ab3b57beb5a1e46433dbe9671a26
```

The stable artifact manifest listed 227 files and was also verified after the
reproduction command. Mutable caches, compiled Python bytecode, ZIP archives,
and run logs are intentionally excluded.

## 5. Interpretation

The clean-copy result establishes reproducibility of the supplied formal
certificates, finite models, local Go fixtures, independent Python model, and
machine-readable evidence in the stated environment. It does not establish
production-client conformance and does not replace independent mathematical
peer review.

## 6. Verdict

**PASS.** A clean extraction reproduced every deterministic core output,
passed all non-duplicated tests and self-checks, and verified the package
integrity manifests without network access.
