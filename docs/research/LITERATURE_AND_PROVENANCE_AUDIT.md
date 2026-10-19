# Literature and provenance audit

Audit date: 19 October 2026. This document distinguishes claims supported by the submitted manuscript, claims supported only by its algebraic models, and proposed extensions. It is an independent technical audit, not a claim of a production-client vulnerability or an exhaustive proof of novelty.

## 1. Main findings

The most defensible contribution is a specific semantic obstruction to **coupling admission decisions across protocol steps**, together with a precise characterization of when timing and additional pivots remove that obstruction. The broad observations that reductions need preservation conditions, that state projections can hide relevant behavior, and that arriving certificates can destroy a desired attack state already have clear predecessors.

The following issues materially affect the manuscript's claims.

| Issue | Evidence in the original artifact | Required treatment |
|---|---|---|
| Source-version mismatch | `models/tendermint_style/upstream_fragments/SOURCE.json` identifies **v0.40.0**, commit `0880b4d378f347ab16e54ec677ff50d803f37d62`; the manuscript's bridge cites **v0.39.3**. | Keep the historical snapshot accurately labelled. Use the independently fetched and verified `upstream_v0393/` snapshot for the revised bridge. |
| Missing positive behavioral premise | Theorem 2 uses persistence of the pivot's second-branch contribution when repair is absent, without explicitly imposing that behavior through the second vote opportunity. | Separate protocol behavior from the scheduler skeleton; require the enabling/no-repair case to issue the needed votes. |
| Repair timing is stated too late | The original order compares repair with the observer's second certificate/decision opportunity. | Compare repair with **issuance of the pivot's second precommit**. A previously emitted, valid signature remains deliverable after its signer commits or changes height. |
| Algebraic instantiation is not a transition refinement | `bounded.py` and `CometBFTInstantiation.lean` compute second participation directly from height, decision and lock booleans. They do not construct the second proposal, prevote quorum, or legal round transition. | Retain these results as algebraic evidence. Use a separate per-validator message trace to establish operational realizability. |
| The older event loop models a different interface | `event_loop.py` sends `POLKA` and `COMMIT` messages from a centralized collector; its phase-specific policy filters `COMMIT`, and its mutation suppresses lock updates in every modeled honest replica. | Do not present that event loop as a sole-pivot mutation of the distributed PREVOTE/PRECOMMIT rules. Its results remain results for its stated toy model. |
| Admission does not specify all scheduler semantics | The original grammar also fixes order, all uncontrolled deliveries, and processing deadlines. | State the admission partition and delivery-order/delay policy separately. A generic directed-graph scheduler does not imply the stable-filter restriction. |

## 2. Verified source pin

The GitHub plugin resolved the official tag and fetched each file at the resulting immutable commit:

- Repository: `cometbft/cometbft`.
- Tag: `v0.39.3`.
- Commit: `49b82838fcca442b2445f76605c101609ed04130`.
- Tree: `ae9420e96f0fb41ee26588b4d16ca36a30fd1b27`.
- Retrieval time: 19 October 2026, 15:09:38 UTC.
- Destination: `models/tendermint_style/upstream_v0393/`.
- Official tag receipt: <https://api.github.com/repos/cometbft/cometbft/git/ref/tags/v0.39.3>.
- Official commit receipt: <https://api.github.com/repos/cometbft/cometbft/git/commits/49b82838fcca442b2445f76605c101609ed04130>.

The snapshot includes `SOURCE.json`, the original tag and commit API responses in `GITHUB_RECEIPTS.json`, and `MANIFEST.sha256`. The Go source fixtures are stored locally as `state.go.txt` and `vote_set.go.txt`, without changing their bytes, so that repository-wide Go commands do not compile them as local packages. `SOURCE.json` records the upstream paths and local filenames. Every downloaded file's Git blob SHA-1 was recomputed from its bytes using the Git blob header and compared with the SHA returned by GitHub. All four matched. SHA-256 hashes and byte lengths are also recorded in `SOURCE.json`.

| Upstream path | Official Git blob SHA-1 |
|---|---|
| `consensus/state.go` | `c16c3570ba71da8391a84268139546ea201f4b47` |
| `types/vote_set.go` | `ac70c128a1bc2f1d2a37b311112f3f6f78ce644d` |
| `spec/consensus/consensus.md` | `baa711f329ad725eddb5838cf889c3ff9c451017` |
| `LICENSE` | `d645695673349e3947e8e5ae42332d0ac3164cd7` |

The historical v0.40.0 snapshot was not replaced. Its `state.go` and `consensus.md` are different blobs. The vote-set file happens to have the same blob in both snapshots; that coincidence is not evidence that the snapshots are interchangeable.

### Relevant source rules

The pinned [consensus specification](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/spec/consensus/consensus.md) separates prevote, precommit and commit. A matching prevote quorum updates the lock before precommitting a block. A block precommit quorum triggers commit. Advancing after a precommit timeout requires receipt of a quorum of precommits for any values; a local timer is not an unconditional round-change command. The source therefore supports a mixed set of block and nil precommits as a lawful route to the next round.

The pinned [implementation](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/state.go) supplies concrete guards: `defaultDecideProposal` starts at line 1246, `defaultDoPrevote` at 1387, `enterPrecommit` at 1484, `enterPrecommitWait` at 1606, `enterCommit` at 1638, `tryFinalizeCommit` at 1701 and `addVote` at 2175. The lock assignments are at 1572–1574. `enterPrecommitWait` checks `HasTwoThirdsAny`; the precommit branch of `addVote` distinguishes a matching majority from a mixed quorum. These are evidence for a rule-level model, not proof that the entire Go event loop has been executed or refined.

## 3. Exact boundary against prior work

### Communication closure: the closest theoretical predecessor

Drăgoi, Enea, Kulahcioglu Ozkan, Majumdar and Nikšić, *Testing Consensus Implementations Using Communication Closure*, PACMPL 4(OOPSLA), 210, 2020. DOI: [10.1145/3428278](https://doi.org/10.1145/3428278). [Author-hosted primary PDF](https://fniksic.github.io/assets/files/oopsla2020/consensus-testing.pdf).

Definition 4.3 compares asynchronous executions with lossy synchronous executions modulo per-process stuttering. A communication round is a send/receive/update step: the running example uses `(ballot, step)`, not just a BFT view. Different communication rounds may lose different messages. Section 5 additionally restricts losses to a per-round kernel, and Theorem 5.3 treats leader-based communication. Proposition 6.1 quantifies over suitable harnesses and parameters; the discussion identifies `k=1` as allowing recovery at every communication round.

**Boundary:** the manuscript aggregates several such steps into one endpoint admission bit. Its counterexample does not refute the communication-closure theorem. The additional aggregation requires a separate preservation argument. Terminology must distinguish a communication round, a BFT round/view, and the period for which an admission policy remains fixed.

### Twins: a directly relevant certificate-repair observation already exists

Bano et al., *Twins: BFT Systems Made Robust*, OPODIS 2021, published 2022. DOI: [10.4230/LIPIcs.OPODIS.2021.7](https://doi.org/10.4230/LIPIcs.OPODIS.2021.7). [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol217-opodis2021/LIPIcs.OPODIS.2021.7/LIPIcs.OPODIS.2021.7.pdf).

Section 4 describes enumeration of per-round leader/partition scenarios. Section 5.1 also states that the underlying network playground can filter specified message types; the generator and the underlying API must therefore be distinguished. In Section 6.1, the preferred-round mutation experiment explains why reconnecting an old twin does not preserve the intended stale-round behavior: incoming quorum/timeout certificates advance its round. The authors use a crash/restart scenario to realize their desired attack state.

**Boundary:** neither missing persistent updates nor certificate arrival destroying an intended attack state is new by itself. A defensible extension formalizes when admission coupling necessarily includes such repair, how much surviving quorum capacity remains, and how delivery order changes the result. Do not infer incapability of the entire Twins framework from a restricted partition generator.

### Netrix: programmable filters and semantic tests are established

Drăgoi, Nagendra and Srivas, *A Domain Specific Language for Testing Distributed Protocol Implementations*, NETYS 2024. DOI: [10.1007/978-3-031-67321-4_6](https://doi.org/10.1007/978-3-031-67321-4_6). The earlier [primary arXiv manuscript](https://arxiv.org/pdf/2303.05893) has the title *A Domain Specific Language for Testing Consensus Implementations*.

The paper provides filters, state-machine monitors, message reordering and implementation instrumentation. Section 5 explains how tests derive from protocol clauses and invariants; it also studies filter distance and uses Tendermint examples. Thus deriving a test from a lock invariant or exposing a phase-selective API is not an independent new contribution here. The proposed contribution is a preservation/separation characterization for an explicitly stated family of scheduler languages.

### ByzzBench: a benchmark execution substrate, not a scheduler theorem

Louro Neto and Kulahcioglu Ozkan, *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms*, FMBC 2025. DOI: [10.4230/OASIcs.FMBC.2025.13](https://doi.org/10.4230/OASIcs.FMBC.2025.13). [Primary full text](https://drops.dagstuhl.de/storage/01oasics/oasics-vol129-fmbc2025/html/OASIcs.FMBC.2025.13/OASIcs.FMBC.2025.13.html).

Sections 2.2–2.3 describe controlled time progression and transport, including messages in flight and enforcement of execution scenarios. The published framework includes benchmark protocol implementations and multiple testing strategies. This is an appropriate potential validation substrate, but its programmable transport cannot be identified with the manuscript's two-policy stable-filter domain without an explicit adapter and a description of disabled capabilities.

### Simulation and partial-order reduction: preservation obligations have a long history

Lynch and Vaandrager, *Forward and Backward Simulations: I. Untimed Systems*, Information and Computation 121(2), 214–233, 1995. DOI: [10.1006/inco.1995.1134](https://doi.org/10.1006/inco.1995.1134). [Primary journal manuscript](https://pure.uva.nl/ws/files/977588/1153_12073y.pdf).

The paper develops simulation techniques for trace inclusion with internal actions. The manuscript's merged-trace induction is best presented as a specialized sufficient simulation lemma, with the scheduler legality condition made explicit. It should not be advertised as a new general theory of simulation.

Neele, Valmari and Willemse, *A Detailed Account of the Inconsistent Labelling Problem of Stutter-Preserving Partial-Order Reduction*, LMCS 17(3:8), 2021. DOI: [10.46298/LMCS-17(3:8)2021](https://doi.org/10.46298/LMCS-17(3:8)2021). [Primary paper](https://lmcs.episciences.org/7709/pdf).

This work gives counterexamples showing that action-oriented reduction reasoning can fail to preserve state-labelled stutter traces, and strengthens the relevant conditions. It is a particularly important predecessor to any broad claim that scheduler reduction can hide a state-observable error. Its reduction operator and failure mechanism differ from endpoint admission coupling and certificate repair. The distinction should be stated rather than relying on a general state-versus-trace slogan.

### Reversible pairs in a poset: the graph lemma is also classical

Streib and Trotter, *Dimension and height for posets with planar cover graphs*, European Journal of Combinatorics 35, 474–489, 2014. DOI: [10.1016/j.ejc.2013.06.017](https://doi.org/10.1016/j.ejc.2013.06.017). [Author-hosted primary PDF](https://trotter.math.gatech.edu/papers/129-StreibTrotter.pdf).

Section 4, page 477, recalls the classical criterion: a family of incomparable poset pairs can all be reversed in one linear extension exactly when it contains no strict alternating cycle. Applying that criterion to pairs `(R_i,V_i)` gives the proposed simultaneous-lateness graph lemma. A forced-early pair is represented by a self-loop; an already-forced-late pair needs no additional reversal. The graph version also follows directly by adding `V_i < R_i` constraints and checking acyclicity.

**Boundary:** the alternating-cycle argument itself should be credited as a specialization of an established poset criterion. A possible contribution here is its connection to durable vote issuance, the declared admission contract, certificate deficits and the phase-splitting budget. Neither the lemma nor the graph-hardness step independently establishes novelty of those scheduler consequences.

### Complexity of the proposed partial-order extension

Karp, *Reducibility among Combinatorial Problems*, 1972, pp. 85–103. DOI: [10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9). [Primary original](https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf); [authorized reprint with the author's introduction](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf).

The original paper's page 98 explicitly reduces node cover to feedback node set by replacing undirected edges with opposing directed edges. Consequently, the symmetric-graph argument relating induced acyclicity to independent sets is classical. If the revised work proves that a specific scheduler's realizable late-pivot sets are exactly the induced acyclic sets of a derived dependency graph, the **semantic correspondence and its scheduler consequences** are the contribution. The underlying graph-hardness reduction must be credited to this established result.

## 4. Three substantive directions for improvement

1. **Operationally legal minimal witness.** Construct the four-validator run from signed proposals, local vote sets and guarded timeouts. Mutate only the pivot's round-zero lock update. Use two unmutated validators as the conflicting decision observers. Include mixed nil/block precommits, source-backed proposal behavior and retrieval of the old block for a late commit. The additional work is evidence that the intended mechanism exists in a faithful transition vocabulary, not just in a Boolean table.

2. **An issuance-sensitive timing boundary.** Separate repair before the pivot's second prevote, repair between its second prevote and precommit, and repair after its second precommit but before the observer's decision. The last case tests the central output-durability issue. Extend the theorem to partial orders only after naming vote opportunities, their enabledness, and the persistence of signed outputs.

3. **A quantitative scheduler characterization.** Replace one unique pivot and two fixed policies with several independent pivots, certificate deficits and partial-order constraints. An exact capacity formula, together with a minimum phase-splitting budget and a proof of the graph correspondence, provides more substance than additional values of `f` in the original family. State clearly that independence and the opportunity skeleton are model assumptions. Production realizability of arbitrary dependency graphs is a separate question.

## 5. Obligations for the partial-order extension

The proposed graph `i → j` iff `R_i` precedes `V_j` in a fixed poset is useful because acyclic event orders can induce cyclic obstructions to making several repairs late. The graph itself need not be a happens-before graph of actual emitted messages.

For mathematical precision:

- `V_i` should denote a scheduled vote opportunity; if the pivot was already repaired, the opportunity can be a silent step rather than an impossible signed message.
- The graph must use the **transitive precedence relation**, not only a chosen transitive-reduction edge list.
- Suppressing a repair must preserve the stated precedence relation on the remaining opportunities. Deleting vertices and forgetting induced precedence can change the graph and invalidate an unchanged formula.
- The capacity calculation requires that different pivots do not alter each other's vote availability except through the declared constraints.
- NP-completeness is for the explicit schema with variable pivot count and explicitly represented order constraints. It does not establish a new complexity bound for the fixed four-validator client.
- A successful coarse execution means that one legal coarse execution retains an unsafe observation. It need not equal the particular candidate obtained by inserting messages into a fine trace.

## 6. Recommended claim language

> We study an additional aggregation of admission decisions across communication steps. In a bounded locking schema, aggregation can force certificate evidence that suppresses a still-unissued quorum contribution. The obstruction depends on the remaining certificate capacity and on whether repair precedes vote issuance. We characterize this dependence for an explicit independent-pivot model and exhibit a four-validator rule-level trace under one controlled lock-update mutation. The result neither refutes communication-closure theorems nor establishes incompleteness of an entire testing framework.

This wording is intentionally narrower than a claim of universal novelty. The audit searched the primary works above and targeted literature on communication closure, Byzantine testing and observation-preserving reductions; it does not certify that no equivalent result exists elsewhere.

## 7. Independent audit of the new concrete trace

The final audit examined `src/python/twins_scheduler/concrete_trace.py`, `scripts/run_concrete_trace.py` and `tests/unit/test_concrete_trace.py` against the exact v0.39.3 snapshot, including the added `via_C` relay controls. It did not edit those implementation files. No fatal mismatch was found in the **twelve executions actually constructed**, after the implementation narrowed the mutation to P's round-zero assignment and corrected the pinned source URL. This conclusion is about the exercised transition subset; it is not a refinement proof for all inputs accepted by the Python API or an execution of the Go client.

### Guards and evidence checked

| Concern | Audit result for the constructed executions |
|---|---|
| Authentic messages and distinct signers | Every delivery resolves an existing envelope carrying an authenticated record. Local vote slots include height, round, type and signer. Replaying a signed vote therefore cannot supply another unit of quorum power. The source vote-set implementation also validates the vote slot, validator identity and signature before adding voting power. The model uses test HMAC authentication and four equal weights, with threshold three. |
| Proposal and valid-block behavior | B's round-zero proposal is relayed to P by A without changing its signer. C has no round-zero block PoLC and can propose block 1 in round 1 with `validRound=-1`. P retains `valid=0@0`; the negative control making P proposer correctly reuses block 0 and `validRound=0`. Thus the witness does not silently delete the valid-block update. |
| Precommit issuance | Each non-nil A/P/C precommit follows three locally received, matching prevotes. A and C execute normal lock updates, and P also executes its round-one lock update. Only the round-zero P lock assignment is suppressed. No correct validator emits two votes in one height/round/type slot. |
| Mixed-quorum timeout | C's absent round-zero proposal leads to a nil prevote. Receiving A/P block-0 prevotes supplies a three-signer mixed set and enables the prevote timeout, producing C's nil precommit. The mixed precommit set then enables P/C round advancement. This supplies the guards omitted from the original Boolean witness. |
| Locked baseline pivot | P's baseline lock survives round advancement. On C's new proposal P prevotes 0. The round-one prevote set stays mixed, so a timeout produces a nil precommit without unlocking P. Receipt of mixed votes alone does not create a PoLC for 1 or authorize a block-1 precommit. |
| Old-round repair while in round 1 | The precommit branch of `addVote` can observe a round-zero majority after local round advancement. Calls to `enterNewRound(0)` and `enterPrecommit(0)` return under their stale-round guards, but `enterCommit` permits `commitRound=0` while keeping the current round. The model's late repair therefore does not require an extra repair mutation. |
| Missing block at late commit | A mutant P that has moved to proposal/lock 1 cannot finalize commit 0 from the vote quorum alone. It waits for an explicit block-0 transfer from A. `addProposalBlockPart` at lines 1997–2005 explicitly permits a block-part round mismatch, since blocks can be reused; the old block remains admissible at the same height. Aggregating valid block parts into one abstract transfer is a stated modeling choice. |
| Durable signed outputs | P's round-one precommit remains in C's receive buffer after P commits 0 and advances height. C's later certificate is assembled from its own vote, B's vote and that previously emitted P vote. The model does not generate a replacement signature or delete an old one during repair. |

The exact late-repair boundary respects eager local transitions. In the `after_pivot_prevote` case, R reaches P **before** delivery of the other two round-one prevotes required for P's PoLC. P has signed its prevote but has not yet enabled a precommit; entering commit 0 suppresses that later precommit. In the `after_pivot_precommit` case, the third prevote has already been processed and P's resulting precommit has been signed and emitted before R is delivered. No scheduler action is inserted between discovering that quorum and the automatic precommit transition.

### Executed checks

An independent invocation of `uv run --frozen pytest -q tests/unit/test_concrete_trace.py` completed with **14 passed**. An independent standard-library evaluation of `evaluate_suite()` completed with **12 cases, PASS**, with every suite check and all twelve internal trace legality audits passing. The six canonical cases had the reported baseline/fine/coarse classifications; four direct timing controls distinguished repair before versus after the pivot's indispensable precommit issuance. Two additional `via_C` controls checked a separate gossip skeleton. Both relay controls had zero admitted-vote FIFO violations; the baseline remained safe and the mutant retained `A=0, P=0, C=1`. Each direct late-precommit control correctly reported one FIFO inversion. These are targeted constructed witnesses and negative controls, not exhaustive schedule exploration.

### Remaining scope restrictions

The model combines a valid proposal with its complete block, abstracts valid block parts and uses test authentication. It assumes an application that accepts both blocks, disabled/unmodeled vote extensions, a feasible fixed proposer prefix, and a finite asynchronous delivery/timeout skeleton. Choosing local self-message processing before the next external delivery is a legal event ordering for these traces; it is not a claim that the production event loop always processes self-messages immediately.

Several production branches are outside the exercised subset: weighted voting, proposer-priority computation, proposal completion by late old-round POL votes, precommit-majority transitions before local precommit, future-round catch-up and full commit-step vote bookkeeping. The implementation now explicitly rejects unsupported quorum-transition paths. During the audit its proposal-completion predicate was also aligned with the source `isProposalComplete`, which checks whether a majority exists in the advertised POL round. All proposals in the twelve main traces have `validRound=-1`; the additional P-proposer control already possesses a matching PoLC. These restrictions do not create the reported witness, but they preclude claiming a general API-level refinement from these executions alone.

**The direct late-repair control permits non-FIFO envelope reordering; the added relay control avoids that inversion.** In the direct control P receives B's round-one prevote before the earlier-emitted B-to-P round-zero repair precommit. Thus abstract emission cannot automatically be identified with enqueueing a message onto one FIFO wire connection. At the same immutable commit, [`consensus/reactor.go`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/consensus/reactor.go) routes votes through the common `VoteChannel` (declaration at line 29; `sendVoteSetHasVote` at 1286), and [`p2p/conn/connection.go`](https://github.com/cometbft/cometbft/blob/49b82838fcca442b2445f76605c101609ed04130/p2p/conn/connection.go) uses a channel send queue and finishes the current message before dequeuing the next (`sendBytes` at 819; `isSendPending` at 856; `updateNextPacket` at 868). The FIFO implication follows from those source operations.

The implemented `via_C` control first delivers B's signed round-one prevote to C. C possesses that message before forwarding the same signed record to P, after its own earlier prevote on C-to-P. In the mutant execution, P's local value-1 PoLC therefore forms before R without a newer direct B-to-P vote overtaking R. The original direct copy reaches P only after R; it cannot count as a second signer contribution. The mutant P's already-emitted round-one precommit remains deliverable to C after P commits 0. The checker compares all earlier/later pairs of **admitted PREVOTE/PRECOMMIT envelopes on each directed peer edge across rounds**, including earlier envelopes not yet delivered. It excludes proposal/block traffic and envelopes rejected by the declared admission policy. Passing this check establishes compatibility of this finite admitted vote order with FIFO, not execution of CometBFT networking or a refinement of all production channels. The relay is a separate, explicitly changed gossip skeleton; the original fixed-order separation theorem is not being extended to arbitrary reorderings of its unchanged skeleton.

The concluding source-guard review reconfirmed the single P/round-zero logical lock-update omission, retention of P's round-one lock and valid-block updates, quorum-enabled mixed-vote timeouts, C's lawful round-one proposal, and old-round commit with explicit matching block acquisition. In both late-precommit mutant routes, repair occurs after the eager local transition has issued the indispensable signed precommit. No additional source mutation or unsupported transition is needed by the twelve constructed executions.

## Further revision: synthesis and adaptive testing (19 October 2026)

The second revision uses the existing fixed-set capacity lemma as a starting
point. Its new application combines weighted certificate deficits, unequal
control costs, allowed/required keys, a constructed event order and a separately
checked optimality or infeasibility certificate. This is not a claim that
feedback vertex set, SCC decomposition, order reversal or Bellman potentials
are new techniques. At full quotas the optimization specializes to weighted
directed feedback vertex set, with restricted deletions.

McConnell, Mehlhorn, Näher and Schweitzer, *Certifying algorithms*, Computer
Science Review 5(2), 119–161 (2011), explicitly supplies the established design
principle of a result accompanied by independently checkable evidence.
[Journal metadata](https://doi.org/10.1016/j.cosrev.2010.09.009) and the
[primary author manuscript](https://www.mpi-sb.mpg.de/~mehlhorn/ftp/CertifyingAlgorithms.pdf)
were consulted. The current artifact applies that principle to the declared
phase-control synthesis problem. Its checker can still require exponential
local enumeration; no universally polynomial certificate is claimed.

Li, Desai and Padhye, *Feedback-guided Adaptive Testing of Distributed Systems
Designs*, NSDI 2026, pp. 701–719, develops adaptive schedule generation driven by
behavioral and scenario feedback. The
[official USENIX paper and presentation](https://www.usenix.org/conference/nsdi26/presentation/li)
were reviewed for current positioning. The manuscript separates adaptive
exploration within scheduler constraints from exact minimum-cost changes to a
supplied phase-admission contract. It does not infer that FEST is incomplete
or claim a measured bug-finding-speed advantage.

The non-submodular three-key example is an explicit negative result for one
specified positive immediate-gain-per-cost rule. It is not a survey-based
impossibility statement about all greedy or approximation algorithms.
The reviewed sources support this bounded positioning; they do not establish
absence of equivalent prior results across the full literature.

## Third revision: general semantics, abstraction and paid labels (19 October 2026)

The previous independent-pivot characterization is now a structural special
case. The main paper uses arbitrary protocol transition state with an explicit
static admission interface, exact once-paid fibre costs, separately checked
closed-cost certificates, and a checked transfer from abstract lower bounds to
concrete witnesses. The primary sources below were consulted for the broader
positioning. They do not establish that this combination has no equivalent
elsewhere; the manuscript makes no unrestricted priority claim.

### Counterexample-guided abstraction refinement

Clarke, Grumberg, Jha, Lu and Veith, *Counterexample-Guided Abstraction Refinement
for Symbolic Model Checking*, Journal of the ACM 50(5), 752–794 (2003),
[DOI](https://doi.org/10.1145/876638.876643),
[primary author PDF](https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Counterexample-guided%20abstraction%20refinement.pdf).
The paper develops iterative existential abstraction, analysis of spurious
counterexamples and refinement. Those general ideas predate this work.

The present implementation specializes them to a complete finite input graph,
persistent Boolean admission decisions and one-time split costs. A false total
policy yields a safe reachability invariant; splitting blocks by that invariant
eliminates all unsafe abstract paths under the policy. Saved histories additionally
check each exact quotient, invariant, cost certificate and strict partition
refinement. The prototype constructs the detailed graph first. The 2,516-to-26
state example therefore demonstrates a smaller certified abstraction, not a
measured reduction in total model-generation memory or a symbolic scalability
claim. The accompanying local-simulation theorem states the wider semantic
obligation, including the correct lower-bound direction.

### Minimal revision of a specification

Kim, Fainekos and Sankaranarayanan, *On the Minimal Revision Problem of
Specification Automata*, The International Journal of Robotics Research 34(12),
1515–1535 (2015), [DOI](https://doi.org/10.1177/0278364915587034),
[primary manuscript](https://arxiv.org/abs/1404.2289).
This work studies minimal changes to an automaton specification to restore
realizability on a system and establishes relevant computational hardness.

The distinction here is the object being changed. The target unsafe predicate
and protocol transitions remain fixed; refinement exposes independent admission
decisions inside selected coarse scheduler fibres. The same fine decision must
repeat consistently across visits. The paper must not present minimum repair
of a formal specification or its general complexity as an invention of this
artifact.

### Paths with once-paid labels

Kumar, Lokshtanov, Saurabh and Suri, *A Constant Factor Approximation for Navigating
Through Connected Obstacles in the Plane*, SODA 2021, 822–839,
[DOI](https://doi.org/10.1137/1.9781611976465.52),
[primary manuscript](https://arxiv.org/abs/2011.14463).
The minimum-color-path framework charges the set of labels used along a path,
rather than repeatedly charging each traversal. It is relevant precedent for
one-time label costs. Its geometric approximation conditions do not supply an
approximation theorem for arbitrary scheduler transition graphs.

The scheduler product additionally remembers consistent fine-key answers and
activates a paid coarse fibre only when its observations mix, or when the fibre
is required. Its Set Cover reduction is an explicit application of classical
hardness, not a claim that paid-label path hardness is new. The supplied reduction
family is checked against independent covering-subset enumeration.

### Resulting defensible claim

The new contribution is the stated semantic connection among coarse-to-fine
static admission, stateful unsafe reachability, checkable lower bounds and
concrete optimality, together with a dependent-quorum instantiation and a formal
connection back to the old structured case. The new model genuinely violates
the old readiness decomposition: suppressing incoming precommits can remove
round-change enabledness even when first-vote enabling prevotes arrive. It remains
a bounded local HMAC-authenticated model. The retained unchanged native Ed25519
tests support selected protocol guards and do not establish full Go-client
coverage or native reproduction of the mutant disagreement.
