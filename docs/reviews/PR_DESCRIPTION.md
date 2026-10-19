# Strengthen phase-erasure paper with repair frontiers and a guarded BFT trace

## Why this revision is needed

The original single-pivot statement left positive persistence implicit and
compared repair with the second certificate rather than the irreversible
signature it needs. The original bounded classifier also did not provide a
complete local-message trace or characterize weaker delivery-order domains.

## What changes

- State the behavioral, observation and scheduler contracts separately and
  prove the corrected one-pivot theorem over arbitrary behavior functions.
- Derive the exact multi-pivot repair-frontier criterion for finite opportunity
  orders, with classical alternating-cycle attribution, a weighted extension,
  crossed deadlines and the optimal phase-splitting budget for unit weights.
- Add a four-validator Tendermint-style message executor, with one omitted
  P/round-0 lock assignment, explicit local quorums, nil votes and guarded
  timeouts. The canonical witness and late-precommit controls disagree at the
  unmutated A/C observers. A separate relay control has the declared FIFO scope.
- Pin the source bridge to the verified v0.39.3 commit, preserving the existing
  v0.40.0 fixture as separately labelled history.
- Rewrite the manuscript, move replay material to an appendix, synchronize both
  Markdown/LaTeX pairs, and update the claim/evidence ledgers and reviewer reply.
- Integrate all new checks into the reproduction command, bind the successful
  Lean receipt to source hashes, pin the Z3 wheel and normalize generated CSV.

## Validation

`./reproduce_revision.sh` passes all mandatory stages, including 35 Python
tests, all active Go packages, the retained 384-row cross-language classifier,
eight positive UNSAT and four damaged SAT checks, the 12-job Lean build,
20-declaration axiom audit, independent leanchecker and source hygiene.

The new event oracle checks all 530 directed repair graphs through three
pivots, 50,363 legal orders and 1,357,209 admission/split executions. It compares
13,074 boundary cases and 13,074 separate budget cases without mismatches.
General partial-order, common-frontier and weighted sweeps have separately
declared scopes. All 12 constructed protocol cases pass their legality audits.
Eighteen deterministic result files match their references byte for byte.

The LIPIcs PDF has 13 main-text and 17 physical pages. It passes source-sync,
page-budget, overflow, citation, bibliography and embedded-font checks.

## Assurance and submission limits

The complete graph correspondence and optimal graph capacity are paper proofs
with finite validation. The new Lean module checks the behavioral contract,
capacity arithmetic and persistent-output components; it does not mechanize
the complete graph proof or establish production CometBFT refinement.

FIFO compatibility covers admitted vote envelopes in the stated relay
skeleton. The direct late-precommit control explicitly diagnoses its ordering
inversion. No claim of a production vulnerability, bug prevalence or universal
testing-framework incompleteness is made.

Authors still need to confirm student-paper eligibility and choose an
appropriate anonymous artifact URL for submission. This is a research revision
prepared for review, without requesting reviewers or merging changes.
