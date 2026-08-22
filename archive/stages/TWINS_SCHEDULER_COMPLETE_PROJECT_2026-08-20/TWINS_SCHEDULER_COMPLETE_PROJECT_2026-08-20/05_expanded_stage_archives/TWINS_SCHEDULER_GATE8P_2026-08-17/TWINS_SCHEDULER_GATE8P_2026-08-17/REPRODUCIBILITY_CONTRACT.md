# Gate 7′ reproducibility contract

## Reproduction target

A valid exact reproduction regenerates the decisive result files and paper
assets from source, without network access or files outside the archive, and
passes both `CORE_RESULTS.sha256` and `ARTIFACT_MANIFEST.sha256`.

## Verified host

- Linux x86-64;
- CPython 3.13.5;
- Go 1.23.2;
- GCC-compatible C compiler 14.2.0;
- Z3 runtime 4.13.3.0 as `libz3.so.4`;
- `PYTHONHASHSEED=0`;
- no network access.

The exact-host route is verified. A container build is not claimed as verified.

## Command

```bash
./scripts/reproduce_gate7p.sh
```

The runner performs, in order:

1. regeneration of certificates, premise results, parameter checks, event-loop
   evidence, arithmetic evidence and source mapping;
2. comparison of 15 decisive files with frozen Gate 6′ hashes;
3. local compilation of the minimal Z3 C-API loader;
4. execution of five positive SMT/CHC files and four damaged controls;
5. generation of three SVG figures and seven tables in CSV/Markdown/LaTeX;
6. 17 dependency-free unit tests;
7. copying the frozen core and full-artifact manifests to temporary baselines;
8. artifact self-check and verification of both frozen manifests before and after regeneration.

## Determinism rules

- JSON uses sorted keys and fixed indentation;
- CSV uses `\n` line endings and fixed field order;
- random-order checks use seeds 0–255;
- Python hashing is pinned with `PYTHONHASHSEED=0`;
- no wall-clock times, temporary paths, hostnames or timestamps enter core files;
- generated `proofs_smt/z3cli`, caches and build directories are excluded;
- generated paper assets carry individual SHA-256 digests.

## Inputs

All inputs are local: certificates, SMT-LIB files, protocol/event-loop
specifications, pinned source fragments and licenses, machine-readable paper
data, and both executable implementations. No historical blockchain dataset,
RPC, public testnet, cloud resource or private material is required.

## Success criteria

A reproduction passes only when:

- core evidence has status `PASS`;
- 15 Gate 6′ files are byte-identical;
- SMT migration has 8 expected `UNSAT` and 4 expected `SAT` outcomes;
- the exact premise model has 128 assignments and zero mismatches;
- Go/Python conformance has six cases and zero mismatches;
- event-order sensitivity has 1 548 runs and zero failures;
- all 24 paper outputs verify;
- all 17 tests pass;
- both manifests verify.

## Trust boundary

The reproduction trusts Z3, SMT/CHC encodings, the minimal C loader and host
compiler, the project-local T2 certificate composition, the written mapping
from paper concepts to executable symbols, and the operating-system/language
runtimes. It does not establish full refinement from a production client to the
abstract schema.
