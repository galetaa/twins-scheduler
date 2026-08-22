# Gate 7′ artifact — scheduler-grammar safety-observation closure boundaries

This archive freezes the narrow Gate 6′ result into a standalone research
artifact and manuscript-ready evidence package.

## Frozen claim

For an explicit class of finite certificate-driven locking schemas, erasing
message-phase distinctions to one type-uniform directed endpoint graph can
remove an agreement-violation witness. The mechanism is that closure-added
repair evidence disables a unique honest quorum pivot before a later
conflicting certificate can form. Exact replay is observationally erasable only
under stable-key idempotence and state-based safety observations.

## Gate 7′ result

- 15 decisive Gate 6′ files reproduce byte-for-byte;
- five positive Z3 SMT/CHC files produce eight `UNSAT` results;
- four deliberately damaged controls produce `SAT` countermodels;
- 17 dependency-free unit tests pass;
- the Go/Python fuller event loops agree on all six cases;
- the event-order corpus contains 1 548 case runs;
- all 128 premise assignments match the closed characterization;
- three paper figures and seven tables are generated in three formats;
- clean-copy offline reproduction passes both core and full-artifact manifests.

## Reproduce

```bash
./scripts/reproduce_gate7p.sh
```

No network, blockchain node, RPC service, Python package download, mainnet
interaction, or external dataset is used. See
`artifact/ARTIFACT_EVALUATION.md`, `REPRODUCTION_VERIFICATION.md` and
`environment/EXACT_HOST_INSTRUCTIONS.md`.

## Directory map

- `proofs_smt/` — solver-checked SMT/CHC encodings and negative controls;
- `proof_outputs/` — exact solver outputs and machine-readable report;
- `proofs_checked/` — small explicit certificates and rules;
- `src/` — minimal dependency-free Python model;
- `implementation_fixture/` — independent Go event loop and big-integer route;
- `results/gate7p/` — generated evidence, extraction check and Gate 7′ decision;
- `paper_assets/` — generated figures and tables;
- `manuscript/` — abstract, populated paper skeleton and evidence index;
- `proof_review/` — SMT migration and objection ledger;
- `artifact/` — artifact-evaluation instructions;
- `environment/` — exact host, hardware and offline contract;
- `inputs/` — pinned source fragments and upstream licenses.

## Assurance status

The verified route uses Z3 4.13.3.0, a small certificate kernel, independent Go
arithmetic, and independently written Go/Python event loops. External human
proof review was not performed. `formal/lean/` is a migration scaffold and was
**not kernel-checked**.

## Scope discipline

This is not a claim about every BFT protocol, a production vulnerability,
universal scheduler minimality, liveness, or unbounded partial synchrony. The
complete non-claim list is generated as
`paper_assets/tables/table7_nonclaims.md`.
