# Gate 5′ independent clean-copy reproduction verification

**Verification date:** 15 August 2026  
**Result:** **PASS**

## 1. Procedure

The project directory was copied into a new clean location while excluding
`.pytest_cache`, `.venv`, all `__pycache__` directories, and all `.pyc` files.
The following one-command workflow was then executed without network access:

```bash
./scripts/reproduce.sh
```

The workflow regenerated Gate 5′ results, ran the exact second-kernel search,
executed formal regression checks, compiled and ran the Go fixtures, performed
the independent self-check, and verified the deterministic core manifest.

## 2. Environment

```text
CPython 3.13.5
Go 1.23.2 linux/amd64
PYTHONHASHSEED=0
runtime Python dependencies: none
```

The package uses only the Python standard library at runtime. Go is required
only for the executable correspondence fixtures.

## 3. Test and checker results

```text
Gate 5′ runner: PASS / GO TO GATE 6′
pytest: 28 passed, 28 skipped
Gate 5′ self-check: PASS
formal results: T1, T2, T3, T4, T5
second-kernel serialized witnesses: 15
Go/Python vote-processing cases: 728/728 PASS
phase-coupled family: f=1…8 PASS
replay sequences: 364 PASS
```

The 28 skipped tests are older exhaustive Gate 4′ and second-kernel tests whose
same state spaces are regenerated and independently checked by the Gate 5′
runner in fast reproduction mode. They are skipped to avoid executing the same
exhaustive search twice in one reproduction command.

## 4. Byte-for-byte determinism

The clean-copy run was compared with the original run using the explicit
`CORE_RESULTS.sha256` allow-list.

```text
core files compared: 17
byte-identical files: 17
mismatches: 0
CORE_RESULTS.sha256 digest:
5e49a863263f423dc625ec0727f4225320707c7188263a3c565428a4fb9f1c53
```

The core includes the machine-readable decision, theorem ledger, aggregate
checks, second-kernel language matrix, separation table, closure
counterfactuals, minimized witnesses, parametric family, replay checks,
source-obligation mapping, Go/Python conformance output, implementation
correspondence output, and cross-protocol transfer matrix.

## 5. Pinned-source integrity

Both source snapshots passed their local SHA-256 manifests:

- `relab/hotstuff` Gate 4′ frozen inputs and outputs;
- CometBFT `v0.40.0`, commit
  `0880b4d378f347ab16e54ec677ff50d803f37d62`.

The CometBFT correspondence is deliberately limited to duplicate-vote
idempotence, validator-slot voting-power accounting, valid-round state, and
lock-before-precommit ordering. This verification does not establish full
client conformance and does not report a production vulnerability.

## 6. Reproduction verdict

**PASS.** A clean extraction reproduced all 17 deterministic core result files
byte-for-byte and passed every non-duplicated regression, theorem check,
witness replay, source mapping, and Go correspondence check.
