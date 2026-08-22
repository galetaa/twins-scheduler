# Artifact evaluation guide

## Claims supported by this artifact

The artifact supports the following narrow claims:

1. replay erasure under stable-key idempotence and state-based safety observations;
2. a relational sufficient condition for closure-added actions to preserve unsafety;
3. a parametric quorum-pivot separation between a type-uniform directed scheduler and a phase-specific scheduler for an explicit schema;
4. an exact seven-flag characterization for that construction;
5. reproduction of the boundary in a fuller two-round Go event loop and an independent Python mirror.

It does not claim a production vulnerability, liveness result, universal
scheduler minimality, or full conformance with CometBFT/HotStuff.

## Host requirements

- Linux x86-64;
- CPython 3.13;
- Go 1.23;
- a C11 compiler available as `cc`;
- Z3 runtime `libz3.so.4`, exact version 4.13.3 for exact proof-output reproduction;
- standard POSIX tools: `bash`, `sha256sum`.

No Python packages, network services, blockchain nodes, datasets, RPC endpoints
or public networks are required.

## Reproduction

```bash
./scripts/reproduce_gate7p.sh
```

The command runs offline and performs:

1. exact core evidence regeneration;
2. 15-file Gate 6′ hash comparison;
3. Z3 loader compilation and solver execution;
4. four negative-control checks;
5. Go/Python event-loop conformance;
6. 128-assignment premise characterization;
7. 1 028-case big-integer cross-check;
8. 17 unit tests;
9. generation of all paper figures and tables;
10. self-check and verification of both manifests.

## Expected terminal markers

```text
CORE EVIDENCE PASS
SMT PROOF MIGRATION PASS
PAPER ASSETS PASS
UNIT TESTS PASS (17)
GATE 7' SELF-CHECK PASS
CORE MANIFEST PASS
ARTIFACT MANIFEST PASS
GATE 7' REPRODUCTION PASS
```

## Primary result files

- `results/gate7p/gate7p_decision.json`
- `results/gate7p/gate7p_theorem_ledger.json`
- `results/gate7p/extraction_equivalence.json`
- `proof_outputs/smt_proof_report.json`
- `results/gate7p/full_event_loop_matrix.csv`
- `results/gate7p/premise_truth_table.csv`
- `paper_assets/MANIFEST.json`

## Quick interpretation

The decisive fuller-loop observation is that the controlled
`MISSING_LOCK_UPDATE` variant violates agreement only under
`G_T_TYPE_SPECIFIC`. Both type-uniform directed choices are safe for distinct
reasons: edge-off prevents the first quorum, while edge-on delivers repair
before the second quorum opportunity.

## Evaluation boundary

A successful run validates the packaged claims on the explicit bounded models.
It does not validate a production vulnerability or replace review of the
statement-to-encoding and protocol-to-schema mappings.
