# Extend certified scheduler refinement to stateful protocol semantics

## Why this change is needed

The previous exact minimum depended on an independent-pivot behavioral contract.
Shared quorum state, message availability and timer guards can invalidate that
decomposition. The manuscript needs a general semantics and a checked connection
between an abstract optimum and a more detailed protocol model.

## Changes and resulting behavior

The main theorem now accepts arbitrary labelled transition systems with a
control-complete static Boolean admission interface. Exact product exploration
remembers repeated fine-key answers and minimizes once-paid coarse-fibre costs.
Separate checkers validate unsafe witnesses and closed-sublevel lower bounds,
including infeasibility, allowed/required splits and exact input identity.

An all-edge simulation checker transfers abstract lower bounds to a detailed
model. A matching guarded witness proves its optimum. Invariant-guided CEGAR
eliminates entire false policies, with checked quotient/refinement histories and
finite strict-partition progress. Resource cutoffs remain unknown.

A coupled four-validator model covers 12 stages and 32 opportunity slots,
including unordered repair/timeouts and guarded missing-block catchup. Its
2,516-state, 5,856-transition mutant graph refines from one abstract state to
26 after eliminating 11 policies; the proved minimum is 2. The witness replays
through protocol rules and ends in conflicting decisions by unmutated A and C.

New Lean proofs cover general policy completion, trace refinement, persistent
memory, closed-cost certificates, simulation transfer and invariant elimination.
The previous weighted/SCC result is retained as a specialization with an explicit
state exporter, equal-optimum normalization proof and independent comparison.

## Validation

- 119 Python tests pass, with retained Go and 384-row cross-language checks.
- 7,904 general graph/cost/permission oracle cases have zero mismatches.
- A separate 2,960-case suite gives 5,920 optimum comparisons and 6,857 checked
  refinement iterations, with no mismatch or invalid certificate.
- 1,507 specialization cases give 3,014 raw-oracle optimum comparisons and
  1,189 equal-cost witness normalizations, all passing.
- 128 total-policy protocol checks cover 17,690 states and 42,750 transitions
  in a separate exploration loop sharing the model guards, compared with the
  export's quotient that omits the same first-arrival diagnostic field.
- Lean passes 15 build jobs, the 46-declaration axiom audit, independent kernel
  rechecking and 23-source-file hygiene checks.
- The official LIPIcs PDF has 12 main-text and 24 physical pages and passes its
  reference, citation, overfull-box, page-budget and font gates.
- `make transition` and `./reproduce_revision.sh` regenerate the new results;
  research CI compares all deterministic transition, bridge and synthesis files.

## Scope

The main semantics no longer assumes independent pivots. It still requires a
declared static control interface and an unsafe predicate. Finite exhaustive
export precedes the current abstraction loop. Model control costs are inputs.
The protocol exporter and Python checkers are not mechanized; the protocol
cross-check shares guards, and no full Go-client refinement is asserted.
Retained native evidence exercises unchanged CometBFT ordinary operation with
real Ed25519 signatures. The local model uses HMAC test authentication.
