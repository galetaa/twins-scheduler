# Phase Erasure Can Hide Agreement-Violation Witnesses in Certificate-Driven Locking BFT Protocols

## Abstract

Use `ABSTRACT_DRAFT.md`.  The final abstract must preserve three distinctions:
raw trace inclusion versus unsafe-observation equality, theorem schemas versus
protocol instantiations, and an explicit separation family versus universal
scheduler incompleteness.

## 1. Introduction

Byzantine fault-injection systems differ not only in the Byzantine actions they
represent but also in the grammar used to control message delivery.  A
partition schedule makes one symmetric connectivity choice for a view.  A
directed schedule distinguishes endpoints.  A phase-specific schedule can
separate two messages that share an endpoint pair but carry different protocol
roles.  Per-message schedulers additionally distinguish message instances and
order, and replay-capable schedulers can deliver the same logical message more
than once.

The raw execution languages are therefore ordered by construction.  That fact
alone is not scientifically useful: two grammars can generate different traces
while exposing exactly the same agreement violations.  The central question is
property-preserving closure:

> When does erasing message-phase distinctions to one type-uniform directed
> endpoint graph preserve every finite agreement-violation observation, and
> when can the added messages destroy the witness?

The mechanism is non-monotone locking repair.  If closure only adds transitions
that are increasing in a preorder under which the unsafe set is upward closed,
then unsafety survives.  In a locking protocol, however, an added repair or
terminal certificate can remove a validator from a later conflicting quorum.
When that validator is the unique honest pivot in the intersection of two
quorums, closure can convert an unsafe trace into a safe one.

### Contributions

1. **Conditional closure theorem.** We state a relational sufficient condition
   for closure-added actions to preserve a finite unsafe observation and expose
   the exact monotonicity obligation that locking repair can violate.
2. **Parametric separation and premise boundary.** For every `f≥1`, we give an
   `n=3f+1`, `q=2f+1` quorum-pivot construction separating phase-specific from
   type-uniform directed scheduling.  For the supplied seven-flag model, strict
   separation holds exactly when
   `S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)`.
3. **Replay boundary and executable evidence.** We prove replay erasure under
   stable-key idempotence, give the complementary non-idempotent boundary, and
   validate the scheduler separation in two exact kernels and a fuller
   two-round event loop with independent Go/Python implementations.

The paper is not framed as a new fault-injection DSL.  Message filtering,
delay, ordering, replay, partition scenarios, mutation-based testing, and BFT
benchmark infrastructure are prior art.  The contribution is the
safety-observation effect of a specific closure transformation.

## 2. Background and problem statement

### 2.1 Certificate-driven locking protocols

Define a finite protocol schema with validator identities, rounds or views,
values, signed messages, quorum certificates, persistent locks, and irreversible
decisions.  Agreement is violated when two correct identities decide distinct
non-null values.  Cryptographic validity is abstracted as unforgeability of
correct identities and explicit signer sets; the result does not depend on a
particular signature scheme.

### 2.2 Scheduler grammars

Introduce the grammar ladder shown in
`paper_assets/figures/figure1_scheduler_grammar.svg`:

- `G_P`: one symmetric partition relation per view;
- `G_D`: one directed endpoint graph per view, uniform across controlled phases;
- `G_D1`: `G_D` plus bounded delay of terminal evidence;
- `G_T`: a directed graph per phase or message type;
- `G_M`: delivery and order per message instance;
- `G_R`: `G_M` plus replay.

State the embeddings `G_P⊆G_D⊆G_T⊆G_M⊆G_R` and the separate
`G_D⊆G_D1` branch.  Do not order `G_D1` and `G_T` without an additional theorem.

### 2.3 Observation languages

For protocol `P`, scheduler grammar `G`, and bounded execution domain `B`, let
`L_G(P,B)` be the execution language and let `O_s` project an execution to
safety-relevant terminal observations.  The relevant comparison is

`UnsafeObs_G(P,B) = { O_s(τ) | τ∈L_G(P,B) and Unsafe(O_s(τ)) }`.

Raw language strictness does not imply strictness of `UnsafeObs`.  A separation
requires one unsafe observation reachable under the stronger grammar and absent
from the complete weaker language within the formal domain, or a symbolic
construction proving the distinction.

## 3. Relational closure lifting

### 3.1 Closure transformation

A closure transforms an original trace by retaining all original actions in
order and inserting actions required by the coarser grammar.  For phase erasure,
the inserted actions are messages that share an admitted endpoint edge with a
message retained by the original trace but carry a different phase label.

### 3.2 Theorem T2

Let `R` be a preorder over protocol-relevant states.  Assume:

1. initial states are related;
2. each closure-added action is `R`-increasing;
3. each retained original action forward-simulates `R`;
4. `Unsafe` is upward closed under `R`.

Then every finite unsafe original trace has an unsafe closure trace.  Present the
proof by induction over the merged trace: inserted actions use increasingness
and transitivity; retained actions use forward simulation; terminal unsafety
uses upward closure.

### 3.3 Why locking repair violates the premise

A repair certificate is not necessarily increasing for a preorder that tracks
future quorum participation.  Delivering it can strengthen a lock or terminate
a branch, thereby deleting a future safety-relevant transition.  This is the
mechanism by which a coarser grammar can lose an unsafe observation even though
it only adds delivered messages.

## 4. Parametric quorum-pivot separation

### 4.1 Construction

For every `f≥1`, set `n=3f+1` and `q=2f+1`.  Partition identities into:

- `B`, `f` Byzantine identities;
- `A`, `f` correct identities supporting value 0;
- `C`, `f` correct identities supporting value 1;
- one correct pivot `p`.

Define `Q0=B∪A∪{p}` and `Q1=B∪C∪{p}`.  Both have size `q`, and their only
correct intersection member is `p`.  One sender-to-`p` edge carries enabling
evidence `E` followed by repair evidence `R`.

### 4.2 Theorem T3

Under phase-specific scheduling, deliver `E` and omit `R`.  The pivot can
contribute to both branches, so both certificates form.  Under a type-uniform
directed edge there are two cases:

- edge off: neither message arrives and the first branch has support
  `2f=q−1`;
- edge on: both messages arrive, and `R` disables `p` before the second quorum,
  leaving support `2f=q−1`.

Therefore the explicit schema has an unsafe observation under `G_T` and none
under either `G_D` edge choice.  Figure 2 visualizes the construction.

### 4.3 Scope

The theorem is an existential family, not a universal statement that every
locking protocol separates the grammars.  A protocol instance must exhibit the
phase coupling, timing, repair effect, shared endpoint edge, and quorum-pivot
structure.

## 5. Exact premise characterization

The seven Boolean premises are:

- `S1`: first base support is one below quorum;
- `S2`: second base support is one below quorum;
- `Rq`: the second use of the pivot requires enabling evidence;
- `D`: repair disables the pivot;
- `T`: repair acts before the second quorum opportunity;
- `E`: enabling and repair share one endpoint edge;
- `X`: the phase-specific grammar can separate them.

For the supplied operational model, strict separation holds exactly when

`S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)`.

The executable checker enumerates all 128 assignments; Z3 proves symbolic
equivalence.  Only `0111111`, `1101111`, and `1111111` are strict assignments.
Figure 3 and Table 3 summarize the result.

## 6. Replay erasure and its boundary

### 6.1 Theorem T1

Assign every logical signed message a stable replay key.  Assume that a
non-first delivery is a protocol-relevant stutter, emits no relevant output,
adds no voting power, and leaves subsequent behavior congruent; safety
observations depend only on protocol-relevant state.  Deleting repeated keys
then preserves every finite terminal observation.

### 6.2 Non-idempotent boundary

If quorum logic counts message instances rather than unique logical
contributions, replay is not erasable.  A sequence such as `B,H1,H1` can be
incorrectly counted as three contributions although it contains only two
validator identities.  This boundary is constructive and is not a claim about a
specific production implementation.

## 7. Executable validation

### 7.1 Exact kernels

Summarize the two bounded locking kernels inherited from Gates 4′ and 5′.  Their
role is regression and natural-instantiation evidence; the parametric theorem
does not depend on their state-space bounds.

### 7.2 Fuller two-round event loop

Describe the Go event loop with `PROPOSAL → PREVOTE → POLKA → PRECOMMIT → COMMIT`,
persistent locks, dynamically generated events, unique logical vote keys, and
irreversible decisions.  The only controlled mutation removes the lock update
after POLKA.

Table 2 reports six cases.  The correct baseline is safe under every tested
grammar.  The mutation is unsafe only under `G_T`; edge-off and edge-on directed
closures remain safe for the two distinct theorem reasons.

### 7.3 Independent implementation and order sensitivity

The independently written Python mirror agrees with Go on all terminal
observations in six cases.  FIFO, LIFO, and 256 seeded random queue orders yield
1,548 case runs without a classification or terminal-signature change.  This is
a bounded robustness check, not a liveness or arbitrary-timing theorem.

## 8. Mechanized and executable assurance

Explain the four assurance routes:

1. Z3 CHC/SMT re-encoding of T1, T2, T3, and T6;
2. the small auditable certificate kernel;
3. independent Go exact arithmetic;
4. independent Go/Python event loops.

Report all positive `UNSAT` obligations and negative `SAT` controls from Table
4.  State explicitly that the complete protocol-to-schema refinement is not
mechanized and remains visible in the assumption map.

## 9. Related work

### 9.1 Clone and partition testing

Discuss Twins as practical clone-based testing and the source of partition-style
scenarios.  Distinguish the current result from the rejected finite-clone
completeness question.

### 9.2 Communication closure and message adversaries

Discuss communication-closure reductions and directed dynamic-network/message-
adversary formalisms.  The difference is that this work studies preservation of
finite agreement observations under phase erasure and identifies a
repair/pivot non-monotonicity mechanism.

### 9.3 Richer testing DSLs and mutation systems

Discuss Netrix, randomized BFT testing/ByzzFuzz, and comparable message-level
filters.  These systems establish that richer control actions are engineering
prior art; they do not by themselves characterize when the richer actions
change the safety-observation language.

### 9.4 Benchmark infrastructure

Discuss ByzzBench separately.  Benchmarking testers and counting discovered
bugs is orthogonal to the theorem-level closure question.

## 10. Validity, limitations, and responsible use

Use `paper_assets/tables/table6_validity.md` and
`paper_assets/tables/table7_nonclaims.md`.  Emphasize:

- finite agreement observations only;
- explicit schemas rather than all BFT protocols;
- unweighted quorums in the central construction;
- no production vulnerability claim;
- no probability-of-discovery inference;
- no mainnet or public-validator experiment;
- responsible disclosure before publication of any future unexpected
  implementation-level finding.

## 11. Conclusion

Phase/type erasure is not automatically property preserving.  When closure-added
repair evidence removes a unique honest quorum pivot, a coarser directed
scheduler can lose an agreement-violation witness that a phase-specific
scheduler expresses.  The exact premise boundary separates cases where this
mechanism is active from cases where the distinction collapses.  Stable-key
idempotence provides the complementary condition under which replay adds no
safety-observation power.

The result gives a principled way to discuss scheduler expressiveness without
confusing raw trace count, API richness, and real safety coverage.

## Required figures and tables

- Figure 1: scheduler grammar embeddings;
- Figure 2: quorum-pivot construction;
- Figure 3: exact premise characterization;
- Table 1: grammar definitions;
- Table 2: fuller-loop outcomes;
- Table 3: premise summary;
- Table 4: SMT migration and negative controls;
- Table 5: claim-to-evidence ledger;
- Table 6: validity register;
- Table 7: prohibited claims.

Every item is generated by `scripts/generate_paper_assets.py` from versioned
JSON/CSV evidence.
