# Lean 4 migration scaffold

This directory pins `leanprover/lean4:v4.33.0` and contains proposed direct
formalizations of T1–T3 without Mathlib.

## Evidence status

**Not kernel-checked in the Gate 7 execution environment.** Lean/Elan/Lake were
not installed and network access was unavailable. These files are therefore a
migration scaffold, not part of the evidence used to pass the executable core.
The evidence actually executed at Gate 7 is:

- solver-checked Z3 4.13.3.0 SMT/CHC obligations;
- the small explicit certificate kernel inherited from Gate 6;
- independent Go big-integer checks;
- independent Go and Python event-loop implementations.

After installing Lean through the official Elan workflow, the intended command is:

```bash
cd formal/lean
lake build
```

A successful future build would strengthen the current mature-solver route and may remove the submission hold, but it must not be recorded without actual kernel output and the toolchain hash.
