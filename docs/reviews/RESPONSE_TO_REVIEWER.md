# Response to the review: recommendations 7.1–7.4

Thank you for identifying the gap between the original bounded witness and a stronger scheduler-preservation result. The revision addresses the four recommendations with a corrected behavioral contract, a complete four-validator execution, and an exact characterization of a larger scheduling domain. We distinguish ordinary proofs, kernel-checked components, finite validation, and production conformance throughout.

## 7.1. Strengthen Theorem 2 and separate behavior from the domain

We made second-vote persistence explicit. Enabling must supply the first pivotal contribution; enabling without repair must permit the required second contribution; timely repair must prevent that still-unissued contribution. The observation contract explicitly covers every agreement violation in the stated two-certificate domain. The admission partition and legal event-order language are separate assumptions.

The corrected Lean theorem quantifies over arbitrary execution and voting functions. It does not assume the pivot's second-vote behavior when its enabling edge is closed. A negative-control theorem demonstrates that first-vote necessity and repair efficacy do not imply persistence. This matters because the previous abstract Boolean law and the Tendermint-style edge-off law differed despite producing the same single-pivot classification.

The primary extension uses initial-ready pivots: an unopened enabling edge does not itself prevent a second-branch vote. For $k$ unit-weight pivots, certificate deficits $d_0,d_1$, and the repair-precedence graph

$$
i\to j\iff R_i\prec_P V_j,
$$

let $\alpha(H)$ be the largest induced acyclic vertex set. Here $V_i$ is a vote-issuance opportunity and $R_i$ a repair-delivery opportunity. The exact coarse-witness criterion is

$$
d_0\le k,\qquad d_1\le k,\qquad d_0+d_1\le k+\alpha(H).
$$

Fine control requires only the two individual bounds. Thus the original one-pivot separation is a special case of a quantified capacity boundary. The complete graph correspondence is proved mathematically; the Lean module verifies its quota arithmetic under the explicitly stated capacity contract. [Proof components](../../formal/lean/SchedulerClosure/RepairFrontier.lean).

## 7.2. Add a complete minimal Tendermint-style trace

We constructed a new four-validator transition model with an explicit message buffer, authenticated test records, local vote sets, and guarded timeouts. Certificates contain three distinct, actually emitted and locally received signatures. The mutation omits only P's round-zero lock assignment; P retains its valid-block state, its round-one lock update executes normally, and A/C are unmutated observers.

The trace supplies the formerly implicit details: C's nil votes, mixed-quorum timeout guards for round advancement, proposal relay without changing the proposer signature, selection of C as the next proposer, and acquisition of old block data when late repair triggers commit. In the fine mutant execution A decides 0 and C decides 1. The baseline and both fixed-order coarse policies have the stated safe classifications.

There are now twelve constructed executions: six canonical cases, four timing controls, and two additional relay controls. All internal legality audits pass. Fourteen targeted concrete-model tests cover the principal guards and negative cases. The source bridge uses an independently verified immutable v0.39.3 snapshot; the historical v0.40.0 fixture is identified separately. These executions establish a bounded rule-level witness, not production-client conformance. [Full trace](../research/CONCRETE_TRACE.md); [terminal cases](../../results/new/concrete_trace.csv).

## 7.3. Test weaker ordering and admission restrictions

The exact deadline is issuance of the indispensable second **precommit**, not the later observer decision. Repair after prevote but before precommit prevents the second certificate. Repair after precommit cannot retract the buffered signature; the observer can still decide the conflicting value even after P commits the old block.

The direct late-repair control permits non-FIFO overtaking. We explicitly identify it and add a separate gossip skeleton forwarding B's signed round-one prevote through C. That control preserves the audited FIFO order of admitted vote envelopes on each directed peer connection. It does not claim conformance of all production networking or preserve the original fixed forwarding skeleton.

The partial-order extension permits several independent controlled keys. Joint lateness is essential: two individually delayable repairs can obstruct one another. For unit weights and feasible fine witnesses, the minimum number of independently chosen phase-split keys is

$$
t_* = \max(0,d_0+d_1-k-\alpha(H)).
$$

The weighted common-deadline result retains attainable subset weights; weights $2,2$ with deficits $1,3$ refute a total-weight shortcut.

Independent event enumeration covers all 530 directed repair graphs through three pivots, 50,363 linear extensions, and 1,357,209 admission/split executions. It checks 13,074 reachability and, separately, 13,074 budget instances. An additional sweep covers all 219 labelled four-event partial orders using their cover relations. Common-deadline and weighted suites use declared support-equivalent or extremal order representatives. No mismatches were found. Eight focused frontier tests supplement these finite checks. [Exact scope and counters](../../results/revision/frontier_summary.json).

## 7.4. Focus the contribution and calibrate novelty

The revised argument centers on durable signed outputs, the repair deadline, certificate capacity, and the precise effect of phase coupling. Replay erasure is supporting material.

We explicitly credit the classical reversible-pair criterion of Trotter–Moore, recalled by Streib–Trotter, and Karp's graph reductions. Twins already discusses arriving certificates advancing a stale twin to a later round and disrupting the intended attack in its preferred-round mutation experiment. None of those observations or combinatorial ingredients is claimed as new. The proposed contribution is their exact semantic connection to the stated admission contract, quota boundary, and phase-control budget. The result does not refute communication closure or establish incompleteness of an entire testing framework. [Literature audit](../research/LITERATURE_AND_PROVENANCE_AUDIT.md).

The integrated validation passes: 35 Python tests, all Go checks, eight positive UNSAT and four damaged SAT obligations, a 12-job Lean build, the 20-declaration axiom audit, and independent leanchecker rechecking. The revised LIPIcs PDF has 13 pages of main text and 17 physical pages, with no overfull boxes, unresolved references, or bibliography warnings. The poset proof and concrete-model conformance are not presented as fully kernel-verified. A production adapter remains the separate requirement for an implementation-level claim.
