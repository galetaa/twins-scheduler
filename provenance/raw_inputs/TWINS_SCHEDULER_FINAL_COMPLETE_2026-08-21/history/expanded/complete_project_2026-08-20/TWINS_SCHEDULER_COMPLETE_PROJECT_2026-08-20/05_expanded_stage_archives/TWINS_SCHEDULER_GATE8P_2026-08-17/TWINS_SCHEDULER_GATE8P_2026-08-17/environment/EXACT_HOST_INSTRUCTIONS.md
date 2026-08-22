# Exact host and offline execution contract

## Pinned environment used for Gate 7′

- Linux x86-64, kernel 6.18.35;
- CPython 3.13.5;
- Go 1.23.2;
- GCC-compatible `cc` 14.2.0;
- Z3 runtime 4.13.3.0 exposed as `libz3.so.4`;
- `PYTHONHASHSEED=0`;
- no network access during checks.

## Why Z3 is compiled through a small loader

The host contains the Z3 runtime library but not the standalone `z3` executable
or development headers.  `proofs_smt/z3cli.c` declares only the small stable C
API surface required to load an SMT-LIB string and print the result.  The
reproduction script compiles this loader locally and records the exact Z3
version reported by the runtime.

## Offline contract

The reproduction script must not invoke package managers, Git, HTTP clients,
RPC endpoints, or blockchain nodes.  All source snapshots and model inputs are
inside the archive.  A failure caused by missing system tools is an environment
failure, not permission to download dependencies silently.

## Minimal commands

```bash
export PYTHONHASHSEED=0
export PYTHONPATH="$PWD/src"
./scripts/reproduce_gate7p.sh
```

## Version policy

Logical checks may also pass under a newer Z3 or Go version, but byte-identical
proof objects and manifests are guaranteed only for the pinned versions above.
A run under different versions must be reported as a portability experiment,
not as an exact reproduction.
