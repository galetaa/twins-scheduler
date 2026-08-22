# Parametric phase-coupled separation

## Construction

For every `f≥1`, let

\[
n=3f+1,\qquad q=2f+1.
\]

Partition validators into:

- `B`, a Byzantine set of size `f`;
- `p`, one honest quorum-intersection pivot;
- `A`, `f` honest validators used only by the first branch;
- `C`, `f` honest validators used only by the conflicting branch.

Define two quorums:

\[
Q_0=B\cup\{p\}\cup A,
\qquad
Q_1=B\cup\{p\}\cup C.
\]

Both have size `2f+1` and intersect in `B∪{p}`. Thus the unique honest member of
the intersection is `p`.

On one sender-to-pivot edge in the first view, two phase-labelled messages are
emitted in order:

- `E`, enabling evidence that causes `p` to contribute to `Q0`;
- `R`, a repair or terminal message that, if delivered before the second branch,
  makes `p` unavailable for `Q1`.

The controlled defect allows `p` to process `E` and contribute to `Q0` without
retaining the intended persistent safety constraint.

## Theorem T3

For the construction above, phase-specific delivery admits a conflicting pair
of quorums, whereas a single type-uniform directed edge for the whole view does
not.

## Proof

A phase-specific scheduler admits the edge for `E` and omits it for `R`.
Therefore:

- first-branch support is `|B|+|A|+1 = 2f+1 = q`;
- `p` remains available;
- second-branch support is `|B|+|C|+1 = 2f+1 = q`.

Both conflicting certificates form.

A type-uniform directed scheduler has two relevant choices for the shared edge.

1. **Edge absent.** Neither `E` nor `R` is delivered. First-branch support is
   `|B|+|A| = 2f < q`, so the first certificate cannot form.
2. **Edge present.** Both `E` and `R` are delivered. The first certificate can
   form, but `R` disables `p` before the conflicting branch. Second-branch
   support is `|B|+|C| = 2f < q`.

Hence the conflicting observation exists under phase-specific delivery and not
under the type-uniform directed schedule of this protocol schema. ∎

## Corollary T4: bounded terminal delay

When `R` is terminal or otherwise may be delayed until after the conflicting
view without changing the remaining enabling transitions, a directed scheduler
with one-view delay reproduces the phase-specific witness: deliver `E` now and
`R` after the second branch. Immediate-delivery closure restores the safe
outcome.

This corollary does not make delayed directed delivery equivalent to all
phase-specific delivery. A defect requiring separation between two
non-terminal quorum-forming phases can remain outside its language.

## Executable evidence

- `results/gate5p/phase_coupled_family.json` checks the construction for every
  `f=1,…,8`; all rows satisfy the exact quorum sizes, intersection size, strict
  directed/phase separation, and the bounded-delay corollary.
- Gate 4′ instantiates the pattern with lock omission and a QC-guard error.
- The independent Tendermint-style kernel instantiates it with lock omission and
  a valid-round guard error.
- `results/gate5p/cross_protocol_result_matrix.csv` preserves the same
  zero/nonzero detection class for all six grammars across both kernels.

## Scientific interpretation

The missing scheduler power is not “more schedules” in the abstract. It is the
ability to retain an enabling phase while suppressing a later phase on the same
endpoint edge. The causal effect is to keep the unique honest quorum-intersection
pivot available for both conflicting branches.

## Scope

The theorem is a separation construction for a defined two-view protocol
schema. It is not a claim that every BFT protocol requires phase-specific
scheduling, nor that phase-specific scheduling is universally minimal.
