# Coupled protocol transitions beyond independent pivots

The general transition-system optimizer is exercised on a complete, finite,
state-coupled quorum model. Its optimum is **2** under declared costs
`c(B→P)=5` and `c(A→P)=2`. The selected refinement permits A's proposal and
prevote to reach P while suppressing A's precommit. Two unmutated observers
then decide different blocks: **A decides 0 and C decides 1**. The unchanged
baseline has no unsafe state in the same bounded environment.

This result uses the actual guarded rule-level transitions in
[`concrete_trace.py`](../../src/python/twins_scheduler/concrete_trace.py),
including local vote sets, generated signed messages, locks, valid blocks,
timeout guards, irreversible decisions and missing-block recovery. It does
not replace those rules with additive pivot weights. The model is defined
in [`coupled_protocol.py`](../../src/python/twins_scheduler/coupled_protocol.py)
and solved by [`transition_synthesis.py`](../../src/python/twins_scheduler/transition_synthesis.py).
Raw counts and evidence are in [`results/transition`](../../results/transition).

## 1. Exactly what is bounded

There are four validator identities, `A`, `P`, `C`, and `B`, each of voting
power one. A quorum has three distinct signers. B is the one explicitly
Byzantine identity and may use the model's Byzantine signing primitive.
All messages counted in a certificate must have actually been emitted and
received. Authentication uses deterministic **test-only HMAC**, not a
production validator key or Ed25519.

The experiment fixes height 1, rounds 0 and 1, two valid blocks, and the
designated proposers B and C. The mutation omits only P's round-0 persistent
lock assignment. Its valid-block update, round-1 lock update, signing-slot
restriction, commit-state restriction and all A/C rules remain intact.
P therefore contains the declared faulty rule; it is not treated as an
unmutated observer. The unsafe predicate specifically requires A and C to
have both decided, with different values. A disagreement involving P alone
does not satisfy the experimental goal.

The environment supplies twelve groups containing 32 once-only opportunity
slots. Every permutation within each group is included. The group order is
part of the model, not a search optimization or a discovered partial-order
reduction. An opportunity whose message has not been emitted or whose timer
has not been armed records that absence; it cannot create the missing vote
or fire a disabled protocol timer.

| Group | Slots | Available opportunities |
|---|---:|---|
| 0 | 1 | Fixed guarded bootstrap: B proposes 0 to A; A emits a buffered relay to P; C's proposal timeout produces nil; B emits its two round-0 votes |
| 1 | 1 | Resolve the policy-controlled A→P proposal relay |
| 2 | 4 | Resolve P→A, B→A, A→P and B→P round-0 prevotes in every order |
| 3 | 3 | Resolve C→P, P→C and A→C round-0 prevotes in every order |
| 4 | 2 | Guarded P/C round-0 prevote-timeout opportunities |
| 5 | 6 | Resolve A→P, A→C, P→A, P→C, B→A and C→P round-0 precommits in every order |
| 6 | 3 | Resolve B→P's round-0 precommit and the P/C round-0 precommit-timeout opportunities in every order |
| 7 | 1 | If P is waiting for committed block 0 and A possesses it, A actually sends that block and the policy resolves its new envelope |
| 8 | 1 | If C lawfully reached round 1, C proposes using its unchanged valid-block rule; B emits its round-1 votes |
| 9 | 4 | Resolve C→P, B→P, P→C and B→C round-1 prevotes in every order |
| 10 | 2 | Guarded P/C round-1 prevote-timeout opportunities |
| 11 | 4 | Resolve P→C, B→C, C→P and B→P round-1 precommits in every order |

The bootstrap, proposal and conditional block-send slots are fixed finite
sequences of guarded internal actions followed, where relevant, by delivery.
They are atomic environment slots; interleavings inside those sequences are
outside this particular environment language. The unsafe witness contains
30 such slots and 172 logged protocol/transport events; the full graph also
contains continuations to the end of all 32 slots.

The two controlled coarse fibres are full endpoint/height/round keys:

| Fine-key index | Phase key | Coarse fibre | Split cost |
|---:|---|---:|---:|
| 0 | B→P, height 1, round 0, PREVOTE | 0 | 5 |
| 1 | B→P, height 1, round 0, PRECOMMIT | 0 | 5 |
| 2 | A→P, height 1, round 0, PROPOSAL | 1 | 2 |
| 3 | A→P, height 1, round 0, PREVOTE | 1 | 2 |
| 4 | A→P, height 1, round 0, PRECOMMIT | 1 | 2 |
| 5 | A→P, height 1, round 0, BLOCK | 1 | 2 |

Each cost is paid once per split fibre, not once per listed phase. The costs
are declared synthetic test-design costs, not measured CPU time or network
latency. No B→P proposal or block is sent in this environment. The adapter
rejects an unexpected controlled message kind instead of silently treating
it as fixed admission. The A→P proposal is controlled by the same fibre as
its votes; it is not exempted to make the witness possible. The BLOCK phase
is exercised on four labelled graph edges, produced by two guarded states
with both admission outcomes. The block payload is explicitly labelled
height 1/round 0 by `send_block`; a receiver's advance to round 1 does not
move that payload to a different scheduler fibre.

## 2. Why the independent-pivot contract does not apply

The two scheduler fibres do not represent two independent validators. They
both affect P and share the same evolving local quorum. After P receives
the proposal, P's first precommit for 0 requires both A's and B's prevotes,
in addition to P's own vote. Suppressing either required contribution removes
that precommit. There is no independent first contribution attached to each
controlled fibre.

Later, the precommit signed by P is delivered to A and C. At A it can complete
the matching `{A,P,B}:0` certificate. At C it can help form a mixed-value
any-precommit quorum that enables a round-advance timeout. At P, the effect
of A's or B's precommit depends on the other received votes and the current
round and step. It can enable a timeout, form a matching commit certificate,
or force a commit state that waits for block data. These are shared protocol
effects, not independently additive capacity changes.

The second signature is also not initially ready. It requires a legal
round advance, a generated proposal, a prevote chosen from lock/proposal
state, and an actual delivered prevote quorum. Closing one of the first
deliveries can remove a timeout quorum and thereby prevent the later
proposal/vote path. The independent schema's initial-readiness premise
therefore fails in a concrete way.

One explicit control admits both enabling prevotes while suppressing both
round-0 precommits to P. A still obtains the first value-0 commit certificate,
but P has only its own and C's precommits and cannot arm a round-advance
timeout. Only A decides. Admitting B's precommit in that same state can
*enable* the unsafe continuation by completing an any-precommit quorum;
with A's precommit also present, the same B message instead completes a
matching certificate and forces P into commit. Its role depends on the
received vote set. Refinement capabilities remain monotone, but the effect
of a particular admitted message is not a fixed independent repair action.

The unchanged valid-block rule is retained. C can propose block 1 because
it has not formed the round-0 value-0 PoLC. P, which learned value 0 as valid,
would have to reuse that valid block if P were the next proposer. The model
does not silently replace the proposer rule with an arbitrary fresh block.

## 3. Ordering changes feasibility under one fixed policy

The interaction is visible even after all fine admission bits have been
fixed. Consider

```text
B→P PREVOTE = admit; B→P PRECOMMIT = admit;
A→P PROPOSAL = admit; A→P PREVOTE = admit;
A→P PRECOMMIT = suppress; A→P BLOCK = suppress.
```

In group 6, delivering B's precommit first gives P an any-precommit quorum
with its own vote and C's nil precommit. The subsequent P timeout can then
advance the round. In the completed execution A decides 0 while P and C
decide 1.

With the same policy, spending P's timeout opportunity before B's precommit
arrives finds no armed timeout. After the delayed vote enables the timer,
that once-only opportunity has already passed. P does not advance in this
bounded environment, and only A decides. Thus the fixed policy has both a
safe and an unsafe schedule within the declared ordering domain.

The second control tests block availability. With the earlier A→P phases
admitted, P can advance the round before B's old precommit arrives. The old
matching certificate then puts mutated P into `COMMIT`, but its previous
proposal is no longer the current proposal and the omitted lock cannot
provide the block. The trace records `WAIT_COMMIT_BLOCK`. A already knows
block 0 and emits a real authenticated block payload. Admitting that BLOCK
envelope lets P decide 0; suppressing it leaves P waiting in commit. Waiting
does not restore permission to sign a conflicting round-1 vote.

These five complete controls, including the closed-precommit readiness
boundary, signatures, local certificates and
logs, are saved in
[`coupled_order_controls.json.gz`](../../results/transition/coupled_order_controls.json.gz).
All their guard and admission audits pass. They exercise actual state and
message dependencies; their safe/unsafe classifications are not supplied
as expected labels to the transition generator.

## 4. Complete graph construction and state identity

`build_model()` performs breadth-first exploration from empty replica/vote
state. At every node it enumerates every remaining opportunity in the current
group. An enabled controlled delivery has both Boolean successor branches;
an internal or absent opportunity has one unlabelled successor. Every
guarded effect runs through the protocol implementation. An unexpected
unsupported rule transition aborts construction rather than becoming a safe
terminal.

The canonical state preserves the environment group and remaining slots;
each replica's height, round, step, persistent lock, valid block, proposal,
known blocks, commit state, signed-vote slots, received votes/messages and
timers; all emitted signed payloads; and the multiset of envelope endpoints,
payload identities and delivery statuses. Multiplicity is retained.

Opaque envelope numbers and logging timestamps are excluded. They are
history bookkeeping, not guard inputs. The payload ID contains the signed
slot/value/proposal metadata; deterministic authentication is a function of
that payload. Local slot indices can therefore be recovered from retained
message identities. Certificate-log deduplication flags are also observation
bookkeeping and do not affect protocol transitions.

The concrete graph additionally retains the first A/B round-0 prevote peer
recorded at P. This is actual audit-history data, never read by a guard. The
provided quotient forgets just that field, merging 2,516 concrete states to
1,978 abstract states. It preserves every labelled concrete edge and the
unsafe observation. A state map is exported for the independent all-edge
simulation checker used by the general abstraction/refinement pipeline.
This small quotient is deliberately easy to inspect; it is distinct from
the coarser automatically refined abstraction in the separate bridge study.

`max_states` is a resource limit. Reaching it raises `EnumerationLimit`
with an `unknown` message and an unexpanded-frontier indication. No partial
`Problem` is returned. A complete safety or optimality result cannot be
obtained by treating unexplored states as safe. The explicit 32-slot bound
is different: it defines the accepted environment language from the start.

## 5. Exact results and negative controls

The main mutated graph contains **2,516 states**, **5,856 transitions** and
**16 states** satisfying A/C disagreement. The baseline has **2,372 states**,
**5,574 transitions** and **no unsafe state**. The graph difference is caused
by real protocol effects, including mutated P's missing-block commit wait.

| Input configuration | Exact result | Interpretation |
|---|---:|---|
| Mutant, either fibre may be split | 2 | Split A→P |
| Baseline, either fibre may be split | Infeasible | No A/C disagreement in the complete bounded domain |
| Mutant, all splits forbidden | Infeasible | No uniform coarse assignment exposes the fault in this domain |
| Mutant, only B→P may be split | 5 | The more expensive alternative is necessary |
| Mutant, only A→P may be split | 2 | The cheaper alternative remains feasible |
| Mutant, B→P splitting required | 5 | The mandatory split alone suffices |
| Mutant, both splits required | 7 | Both declared costs are charged |

The main certificate's strict-sublevel closed set contains 703 product
states. Its witness replays 30 environment actions through the guarded
protocol and reconstructs 172 log events, 16 signed messages and six local
certificates. These are message counts, not 16 distinct validator votes in
one certificate. In particular, the conflicting decision certificates
contain the actual signers `{A,B,P}:0` at A and `{B,C,P}:1` at C. All twelve
replay audits pass, including prior emission, authentication, received
distinct signer quorums, once-only vote slots, lock/vote guards, guarded
timeouts, fixed fine-key values, declared fixed/controlled admission, and
equality with every exported successor state.

The portable main-input digest is
`2ddfa0a8e5e414dec3204dbccf190b62810cee956e54021093aac8c32e62aa1a`.
The baseline-input digest is
`6e5a1b4a2ed31925e3241b08fcbdbe5c31351efa84472215b29b2ead169f843a`.
Certificates bind the complete problem, including unsafe states, allowed
splits, required splits and costs. The digests of the seven permission
configurations are listed in
[`model_cases.csv`](../../results/transition/model_cases.csv).

## 6. Validation independent of the product optimizer

The oracle enumerates **total Boolean fine-key policies and split subsets**.
It rejects any split set outside the allowed/required constraints and any
unsplit fibre whose total policy is nonuniform. It then checks ordinary
graph reachability under that fixed total policy and minimizes the explicitly
enumerated split cost. It does not call the product-state successor function,
the product cost function, or the optimizer.

The exhaustive graph family contains three states with initial state 0 and
unsafe state 2. Four possible directed positions, `0→1`, `1→2`, `1→0`, and
`0→0`, independently have one of six choices: absent, internal, or either
Boolean label at either of two fine keys. All **6⁴ = 1,296 graphs** are tested
under two costs and three permission modes: **7,776 configurations**. This
family includes cycles, absent edges, internal steps, zero-cost splitting,
required splitting and forbidden splitting. It is an exhaustive family of
these four positions, not every directed graph on three vertices.

A further **128** reproducibly generated cases use 4–8 protocol states,
3–6 fine keys, three coarse fibres, parallel transitions, cycles, internal
steps, arbitrary nonnegative costs and permission sets. The seed is
`20261019`. Together the **7,904** cases enumerate **35,368 total policies**
and **40,008 compatible policy/split pairs**. Every synthesized certificate
is independently checked; every optimum agrees with the total-policy
oracle. There are **zero mismatches**.

The coupled model is also checked by direct protocol generation under every
one of its 64 total six-key policies, for both mutant and baseline. For each
of these **128 checks**, a separate worklist starts from empty replicas,
generates guarded successors afresh, and compares bad reachability and the
exact reachable state/edge counts with the exported audit quotient. In total
those checks generate **17,690 states and 42,750 transitions**, with zero
mismatches. These are summed per-policy exploration counts, not distinct
states in one combined graph.

The direct and exported paths share the underlying guarded protocol rules.
This comparison validates graph construction separately from optimization;
it is not an independently implemented verification of every protocol rule.
The selected execution additionally receives the full signed-evidence and
guard audits described above.

## 7. Boundaries the generic examples exercise

Six small examples are stored with their complete inputs, certificates and
oracle results in
[`semantic_examples.json`](../../results/transition/semantic_examples.json).

| Example | Result | Boundary |
|---|---:|---|
| Static-key cycle | Infeasible | A path that needs the same fine key first true and then false is not a fixed scheduler policy, even after revisiting states |
| Three phases, repeated key | 7 | Three phase keys and a repeated use of one key incur one fibre cost, not a cost per encounter |
| Dependent cost choice | 2 | Two inputs jointly enable a shared state; either of two differently priced repairs can then be suppressed |
| Required unused fibre | 8 | Required refinement costs are charged even when the trace does not observe that fibre |
| Zero-cost split | 0 | Mixed phases can be feasible without increasing the declared cost |
| Spurious state merge | Concrete 3; abstract 0 | Merging unprepared/prepared states can create an abstract path with no concrete lift |

The cyclic static-key example has a graph path to the unsafe vertex if an
admission may be chosen afresh on every visit. Under a fixed policy it is
infeasible. This distinguishes static refinement synthesis from unrestricted
adaptive scheduling.

The spurious merge preserves every concrete edge but loses the prerequisite
prepare state. Its abstract value 0 is a lower bound only. It cannot be
reported as a concrete optimum without a matching concrete witness or a
refined abstraction. The input and state map are separately exported in
[`spurious_abstraction.json`](../../results/transition/spurious_abstraction.json).

## 8. Reproduce and interpret

From the repository root:

```bash
uv run python scripts/run_transition_study.py
uv run pytest -q tests/unit/test_coupled_protocol.py
```

The study writes deterministic graph inputs, certificates, state maps,
raw audited executions, controls, oracle rows and a summary to
`results/transition/`. `TWINS_OUTPUT_ROOT` redirects these results;
`TWINS_LOG_DIR` redirects timing observations. Gzip timestamps are fixed.
Wall times are kept outside the deterministic evidence files and are not
presented as a performance comparison with another synthesizer.

The broader optimality theorem applies to arbitrary finite labelled
transition systems with the stated static-key policy semantics; it does not
need an independent-pivot decomposition. This model demonstrates that
extension on interacting quorum, lock, timer and block-state dependencies.
The theorem's instantiation here is nevertheless the explicit finite
environment just described. The adapter is not a verified extraction of all
CometBFT behaviors, not an execution of a fault-modified production client,
and not a universal safety theorem for an unbounded BFT implementation.
Transferring a result to another implementation requires the documented
transition-coverage and witness-lifting conditions of the general bridge.
