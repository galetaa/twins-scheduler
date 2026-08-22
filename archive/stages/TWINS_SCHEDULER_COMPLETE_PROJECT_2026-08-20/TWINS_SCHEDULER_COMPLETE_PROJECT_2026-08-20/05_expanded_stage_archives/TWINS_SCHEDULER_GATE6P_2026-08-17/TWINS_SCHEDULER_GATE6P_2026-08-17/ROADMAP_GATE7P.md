# Roadmap — Gate 7′: reproducible artifact and manuscript-ready evidence

## Gate objective

Freeze the Gate 6′ theorem-and-counterexample result into a minimal artifact
suitable for independent evaluation and generate every manuscript table and
figure from versioned machine-readable data.

## Work packages

### WP7.1 Minimal artifact extraction — 1–2 focused person-days

- remove historical files not required to reproduce the frozen claim;
- retain proof assets, exact checkers, both event-loop implementations, tests,
  source manifests, and final results;
- document the trusted computing base and external tool versions.

**Acceptance:** a fresh archive reproduces the decision without relying on any
file outside the archive.

### WP7.2 Independent proof review or mature-prover migration — 2–5 days

- obtain line-by-line review of T1–T3 from a formal-methods/distributed-systems
  specialist; or
- encode the same statements in a mature prover;
- record every requested correction and rerun all evidence.

**Acceptance:** no unresolved proof objection affecting the frozen claim.

### WP7.3 Automated figures and tables — 1–2 days

Generate at minimum:

1. scheduler-grammar/closure diagram;
2. quorum-pivot construction figure;
3. six-case fuller event-loop result table;
4. premise-characterization truth-table summary;
5. claim-to-evidence table;
6. validity/non-claim table.

**Acceptance:** one command regenerates all outputs from CSV/JSON files.

### WP7.4 Artifact instructions and container/lock validation — 1–2 days

- retain dependency-free Python runtime and pinned Go requirement;
- add a minimal container definition or exact host instructions;
- verify offline execution;
- report hardware and elapsed resources without promising performance.

**Acceptance:** clean-copy run passes on a second environment or container.

### WP7.5 Manuscript skeleton population — 2–4 days

- theorem statements and mechanism before system evaluation;
- related work separated into message adversaries, communication closure,
  testing frameworks, and mutation/fuzzing;
- limitations and prohibited claims copied from the claim freeze;
- all figures/tables linked to generation scripts.

## Go/no-go

**GO to Gate 8′ manuscript:** clean extraction reproduces all core hashes,
independent proof review has no blocking objection, and every paper artifact is
automatically generated.

**PIVOT:** proof review requires a narrower schema but the fuller-loop boundary
and exact premise characterization remain valid.

**NO-GO:** a proof premise is circular or false, independent reproduction fails,
or a newly found source contains the same closure/separation result.

## Critical path

`proof review → minimal archive → clean reproduction → automated figures/tables
→ manuscript evidence freeze`.
