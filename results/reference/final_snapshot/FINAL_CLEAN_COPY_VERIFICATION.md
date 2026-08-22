# Final clean-copy reproduction verification

**Date:** 21 August 2026  
**Source package:** `TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21`

A fresh copy of the final research layer was created without Python caches, pytest caches, compiled bytecode, or the generated Z3 command-line wrapper. The sole project entry point was then executed:

```bash
./reproduce.sh
```

## Result

```text
exit_status=0
elapsed_seconds=10
result=PASS_WITH_EXPLICIT_EXTERNAL_BLOCKERS
```

The clean-copy run independently rebuilt or rechecked:

- the independent theorem, scheduler, typing, and protocol checker;
- the bounded Tendermint/CometBFT-style Python model;
- the independently implemented Go model;
- exact Python/Go terminal-row equality;
- focused pytest tests;
- the project-local proof-certificate kernel and all five damaged controls;
- eight positive SMT obligations and four negative controls;
- Lean/Coq source hygiene;
- the 13-page A4 manuscript PDF.

The run recorded, rather than concealed, the two external omissions:

```text
Lean pinned project build   NOT_RUN_TOOLCHAIN_UNAVAILABLE
Coq source build            NOT_RUN_TOOLCHAIN_UNAVAILABLE
official LIPIcs class build NOT_RUN_CLASS_UNAVAILABLE
```

No scientific claim relies on an unexecuted mature-prover or official-class build. Full command output is preserved in `clean_copy_reproduction.log`.
