# Protocol class and scheduler-closure model for Gate 5′

## 1. Scope

This specification defines the smallest protocol-independent model needed to
interpret the Gate 4′ and Gate 5′ results. It is not a complete specification of
HotStuff, Tendermint, or CometBFT. The model isolates three mechanisms:

1. phase/type coupling on a directed network edge;
2. temporal coupling between enabling and terminal evidence;
3. duplicate delivery of one authenticated logical vote.

The current claims concern finite agreement observations of deterministic,
certificate-driven, view/round-based BFT protocols. Liveness, probabilistic bug
finding, economic behavior, and public-network execution are out of scope.

## 2. Protocol structure

A **phase-labelled certificate-driven protocol** is a tuple

\[
P=(N,V,\Lambda,S,M,\delta,\mathsf{emit},O),
\]

where:

- `N` is a finite set of logical validator identities;
- `V` is a totally ordered set of views or rounds;
- `Λ` is a finite set of protocol phases;
- `S=∏_{i∈N}S_i` is the global product of local states;
- `M` is a set of authenticated messages;
- `δ_i : S_i × M → S_i × M*` is a deterministic handler;
- `emit` gives the messages emitted at each phase barrier;
- `O : S → Ω` is the selected safety observation.

Every controlled message has at least

\[
(sender,receiver,view,phase,kind,payload,replay\_key,contribution\_key).
\]

`replay_key` identifies one exact signed protocol action. Re-delivery of the
same signed vote has the same replay key. `contribution_key` identifies the
validator slot that may contribute voting power at most once, normally
`(height, round, vote type, validator identity)`. Two equivocations may have
different replay keys while sharing one contribution key.

## 3. Safety observation

For agreement, the observation is

\[
O(s)=(decision_i)_{i\in H},
\]

where `H` is the set of correct replicas. It is unsafe exactly when at least two
non-null decisions differ. Internal counters and logs are excluded unless they
change a protocol-visible transition.

## 4. Scheduler grammars

Within each view or round:

- `G_P` — one symmetric partition relation, shared by all controlled message
  kinds;
- `G_D` — one directed endpoint graph, shared by all controlled kinds;
- `G_D1` — `G_D` plus one-view deferral of terminal evidence;
- `G_T` — one directed endpoint graph per message phase or kind;
- `G_M` — an independent delivery decision for each emitted message instance;
- `G_R` — `G_M` plus one bounded replay of an already emitted logical message.

Constructive embeddings used by the checkers are

\[
G_P\subseteq G_D\subseteq G_T\subseteq G_M\subseteq G_R,
\qquad G_D\subseteq G_{D1}.
\]

No inclusion is asserted between `G_D1` and `G_T`: one adds time, the other adds
phase discrimination.

## 5. Closure operators

### 5.1 Type erasure `C_type`

For a `G_T` schedule, retain every used directed endpoint edge in a view and
admit every emitted controlled kind on that edge. This erases phase/type
selectivity without adding reverse edges.

### 5.2 Terminal-time erasure `C_time`

For a `G_D1` schedule, deliver admitted terminal evidence immediately rather
than after the next view.

### 5.3 Replay erasure `C_dup`

For a `G_R` schedule, retain the first delivery of each replay key and remove
later identical deliveries. Different signed actions are retained.

## 6. Replay-idempotent processing

A handler is **stable-key idempotent** when reprocessing an already processed
replay key:

- leaves protocol-relevant state unchanged;
- emits no new protocol-relevant message;
- does not add voting power or a signer contribution;
- does not change the safety observation.

Quorum state must be derived from unique contribution keys, not message-instance
count.

## 7. Relational closure premise

Let `R` be a preorder over protocol-relevant states. Closure insertion is
**R-monotone** when:

1. every closure-added message maps `s` to `s'` with `R(s,s')`;
2. every original protocol transition is forward simulated by `R`;
3. the unsafe predicate is upward closed under `R`.

These are local transition obligations. They do not assume equality of complete
execution languages. If `R` also preserves `O` in both directions, it yields an
observation-equivalence corollary; otherwise it yields only preservation of
unsafety.

## 8. Quorum-pivot separation template

For each `f≥1`, let `n=3f+1` and quorum `q=2f+1`. Partition validator identities
into:

- Byzantine set `B`, `|B|=f`;
- honest left-only set `A`, `|A|=f`;
- honest right-only set `C`, `|C|=f`;
- one honest pivot `p`.

Define two conflicting quorum supports

\[
Q_0=B\cup A\cup\{p\},\qquad Q_1=B\cup C\cup\{p\}.
\]

Both have size `q`; the only honest identity shared by them is `p`.

A two-round instance is **phase-coupled at p** when:

1. enabling evidence `e` and a later repair/terminal message `r` travel on the
   same directed sender-to-`p` edge but have different phases or kinds;
2. receiving `e` makes `p` contribute to `Q0`;
3. a defective transition after `e` fails to retain the intended persistent
   safety constraint, so `p` remains eligible to contribute to `Q1`;
4. receiving `r` before the second round makes `p` unavailable for the
   conflicting contribution, by deciding or repairing the state;
5. members of `B∪A` and `B∪C` provide the fixed base supports for the two
   rounds, and no additional identity can replace `p` in either quorum.

Under `G_T`, the edge can deliver `e` and omit `r`. Under type-uniform `G_D`, the
edge delivers neither or both.

## 9. Instantiations

### 9.1 Gate 4′ certificate-driven kernel

The enabling message is intermediate certificate evidence; the persistent
constraint is a value/view lock; the repair/terminal message is commit evidence.
A second instance replaces lock omission with a defective value/view
justification guard.

### 9.2 Gate 5′ Tendermint-style kernel

The phases are proposal, prevote, POLKA, precommit, and commit. A POLKA is
+2/3 prevote evidence. It establishes `(locked value, locked round)` and
`(valid value, valid round)`. The second natural defect ignores the value or
strict-round requirement of disclosed valid-round evidence. Commit evidence is
the terminal message.

### 9.3 Replay instance

The exact kernels count one Byzantine contribution plus honest vote receipts. A
single repeated honest vote creates a false quorum only in the controlled
message-instance-counting mutation. Stable-key processing erases the replay.

## 10. Bounded-model restrictions

The executable kernels use:

- `n=4`, `f=1`, `q=3`;
- one Byzantine logical identity represented by two physical twins;
- two conflicting views/rounds;
- binary values;
- a leader/honest-replica star within each view;
- deterministic phase barriers;
- finite agreement observations.

The algebraic quorum-pivot construction is parameterized by `f`; the full
protocol executions are not. Therefore the artifact supports a reusable
separation mechanism, not a universal completeness theorem for all BFT
implementations.
