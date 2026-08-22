# T3 — Parametric quorum-pivot separation

## Scope of the theorem

This is an existence result for an explicit two-round certificate-driven
protocol schema. It is not a theorem that every BFT protocol exhibits the same
separation.

For every natural `f ≥ 1`, let

\[
n=3f+1,\qquad q=2f+1.
\]

Partition the validator identities into disjoint sets:

- Byzantine identities `B`, with `|B|=f`;
- honest left supporters `A`, with `|A|=f`;
- honest right supporters `C`, with `|C|=f`;
- one honest pivot `p`.

Define conflicting supports

\[
Q_0=B\cup A\cup\{p\},\qquad
Q_1=B\cup C\cup\{p\}.
\]

Both have size `q`; their intersection consists of `B ∪ {p}` and has size
`f+1`.

## Protocol-schema premises

There are two differently labelled messages on the same sender-to-pivot edge:

- enabling evidence `E`;
- a later repair or terminal message `R`.

The supplied controlled transition permits `p` to support both conflicting
branches after `E` unless `R` is delivered before the second quorum opportunity.
No validator outside the declared base support can replace `p` in the second
quorum.

## Phase-specific branch

`G_T` can deliver `E` and omit `R` on the same endpoint edge. Each base support
has size

\[
|B|+|A|=|B|+|C|=2f=q-1.
\]

Adding `p` gives `2f+1=q` on both branches, so conflicting certificates are
reachable.

## Type-uniform directed branches

A single directed endpoint graph has only two choices for the shared edge.

### Edge absent

Neither `E` nor `R` is delivered. In the symmetric construction, the first
support remains `2f=q-1`; therefore both conflicting certificates cannot form.

### Edge present

Both `E` and `R` are delivered. The first branch reaches `q`; then `R` disables
`p` before the second quorum opportunity. The second support remains
`2f=q-1`. Again, both conflicting certificates cannot form.

Therefore

\[
UnsafeObs(G_D)=\varnothing,
\qquad
UnsafeObs(G_T)\neq\varnothing
\]

for the supplied family.

## Exact checks

The certificate checker proves the algebraic identities by exact polynomial
normalization, including `q-2f=1`. An independent Go implementation using
`math/big` evaluated 1,028 positive values of `f`, including one 400-digit
integer, without machine-word overflow. These evaluations are regression and
implementation-independence checks; the universal arithmetic step comes from
the normalized identities.

## Refined premise boundary

The complete seven-flag Boolean abstraction has exactly three strict-separation
assignments. Its exact characterization is

\[
S_2\land D\land T\land E\land X\land(S_1\lor R_q),
\]

where:

- `S2`: the second base support is one below quorum;
- `D`: repair disables the pivot;
- `T`: repair is effective before the second quorum opportunity;
- `E`: enabling and repair share one endpoint edge;
- `X`: the phase-specific grammar can split them;
- `S1`: the first base is one below quorum;
- `Rq`: the second pivot contribution requires enabling evidence.

This characterization is exact only for the supplied Boolean construction.

## Machine-readable assets

- `t3_quorum_pivot_certificate.json`;
- `results/gate6p/t3_quorum_pivot_proof_check.json`;
- `results/gate6p/t3_bigint_crosscheck.json`;
- `results/gate6p/premise_characterization.json`.
