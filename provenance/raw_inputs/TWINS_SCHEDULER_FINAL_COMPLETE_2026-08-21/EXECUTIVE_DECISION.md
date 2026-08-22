# Executive decision

## Decision

**CONDITIONAL PASS / COMPLETE SCIENTIFIC REVISION / SUBMISSION HOLD.**

All substantive research, formalization, protocol-bridge, narrative, prior-art, and artifact changes requested in the independent review have been implemented. The work now contains a structural quorum-pivot theorem, a parametric family as its corollary, exact scheduler semantics, a typed unsafe-observation definition, a legal-target closure theorem, a replay theorem with output congruence, a paper-level Boolean derivation, and a bounded rule-level instantiation to published CometBFT/Tendermint locking rules.

Two external verification steps remain unexecuted in this environment:

1. the pinned Lean or parallel Coq development was not compiled because neither toolchain was installed and outbound package retrieval was unavailable;
2. the official LIPIcs class build was not run because `lipics-v2021.cls` was absent.

The archive therefore does not use the phrases “Lean-kernel checked” or “official LIPIcs PDF.” It provides source, no-sorry hygiene checks, a pinned CI workflow, strict reproduction hooks, and an A4 review PDF.

## Main result after revision

Let a phase-sensitive admission policy distinguish enabling evidence `E` from later repair evidence `R` on the same sender, receiver, and view. If two conflicting quorum opportunities require one correct pivot, `E` enables the pivot, and `R` processed before the second opportunity disables it, then phase erasure can remove the unsafe observation: the phase-sensitive policy admits `E` while withholding `R`, whereas one type-uniform edge must either reject both or admit both.

The result is:

- structural rather than tied to one toy transition table;
- parameterized by a `3f+1`, quorum-`2f+1` family;
- instantiated in a bounded Tendermint-style rule system;
- separated from the diagnostic seven-flag truth table;
- checked by independent Python, independent Go, Z3, and a purpose-built certificate kernel.

## Natural-protocol bridge

The bridge pins CometBFT `v0.39.3` and maps:

- `E` to the PoLC-completing `PREVOTE` delivered to the pivot;
- `R` to the same-edge, same-height/round `PRECOMMIT` completing the pivot’s local commit evidence;
- `C0` and `C1` to two conflicting precommit-certificate opportunities;
- the mutation to omission of the persistent lock update after PoLC.

The exact bounded domain fixes all other edges, productions, and phase order. Python and Go agree on all 384 canonical terminal rows for `f=1..64`; an independent checker validates 768 bridge cases for `f=1..128`.

This is a rule-level refinement argument. It neither asserts that the mutation exists in CometBFT nor claims production event-loop conformance.

## Evidence summary

| Evidence route | Result |
|---|---:|
| Independent theorem/scheduler/protocol checker | PASS |
| Independent CometBFT bridge cases | 768 PASS |
| Python bounded instantiation | 384 PASS |
| Go bounded instantiation | 384 PASS |
| Python/Go comparison | exact match |
| Focused pytest | 3 PASS |
| Project-local proof kernel 1.1.0 | PASS |
| Project-kernel damaged controls | 5/5 rejected |
| Z3 obligations | 8 positive `UNSAT` |
| Z3 damaged controls | 4 negative `SAT` |
| Lean/Coq source hygiene | PASS |
| Mature Lean or Coq build | NOT RUN — toolchain unavailable |
| A4 review PDF | PASS and visually inspected |
| Official LIPIcs-class build | NOT RUN — class unavailable |

## Irreversible next step

Do not add new scheduler features or mutation campaigns. Run the pinned Lean CI or a local `lake build` plus `AxiomAudit.lean`, then compile `manuscript/lipics/main_lipics.tex` with the current official LIPIcs package. If either build exposes an error, repair the formal or typesetting source without broadening the paper claim.
