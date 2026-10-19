# Limitations

## General transition-system optimality

The new primary result covers arbitrary transition systems under a specified
static Boolean admission interface. Protocol states and transitions may contain
interdependent locks, joint quorum assembly, changing message availability,
repeated messages, branching and cycles. The least trace-refinement theorem,
closed-set lower-bound principle and local simulation transfer do not require
independent pivots or finite protocol state.

The executable solvers and checkers accept complete finite graphs and finite
fine/coarse key sets. Every policy-dependent action must be represented by its
actual key/answer label; unlabelled reads of the policy invalidate the interface
contract. Each fine key is persistent for the entire execution. Adaptive-per-visit
choices are a different scheduler language. Costs are declared nonnegative
integers paid once per selected coarse fibre, including required unused fibres.
The objective is existential finite unsafety, not universal controller synthesis
or a fairness/liveness guarantee.

The product has at most |states| times 3 to the number of fine keys states.
NP-completeness already holds for acyclic graphs with two phases per fibre.
Certificates may be exponentially large, and checker resource limits also mean
unknown. An incomplete search frontier never certifies infeasibility. For
unrestricted programs even zero-cost reachability can encode halting; the tool
does not claim a terminating complete solver for all such programs.

## Model-to-model bridge and abstraction refinement

The all-edge simulation checker preserves the complete fine-key/fibre/cost and
allowed/required interface, initial states and unsafe-state inclusion. It checks
every concrete edge. Controlled labels must match; only internal edges may
stutter. Thus an abstract lower bound covers every concrete execution in the
supplied graph. A concrete witness matching that lower bound proves its optimum.
A single matched trace cannot establish the lower-bound coverage obligation,
and a forward abstraction alone cannot establish a concrete unsafe witness.

The iterative state abstraction begins from a complete explicit concrete graph.
For a false static policy it computes a safe reachable-state invariant and splits
quotient groups by invariant membership, eliminating the whole policy. The
prototype does not avoid initial graph construction or automatically discover
a source-code abstraction. Its selected example reduces the search quotient
from 2,516 concrete states to 26, but no speedup over industrial model checkers or
runtime scaling law is claimed. The audit-only quotient removes an extra
first-arrival diagnostic field and is a projection test.

The coupled protocol case is an exhaustively enumerated bounded rule model:
one height, two rounds, 12 opportunity groups and 32 once-only slots, including
repair/timeout permutations and actual missing-block delivery. Both controlled
fibres act on the same quorum. All within-group permutations are included, but
not all delivery orders, future rounds, block gossip or client executions.
Unsafety requires the unmutated observers A,C to disagree. Deterministic HMAC
is test authentication; it does not execute production Ed25519 in this model.
128 separately generated total-policy explorations challenge the exporter,
while guard replay checks every selected witness transition. These executable
checks are not a machine proof of exporter completeness for arbitrary client code.

The Lean simulation theorem can cover an infinite implementation if its local
transition/control/observation relation is proved. The current executable
bridge is finite model-to-model. Ordinary unchanged-client conformance tests
remain separate and do not establish universal CometBFT correspondence.

## Independent-pivot structural specialization

The repair-frontier theorem and weighted refinement characterization quantify
over arbitrary finite instances of the declared independent-pivot certificate
schema. Their proofs are not restricted to the small instances enumerated by
the artifact. Applying them to a protocol requires discharging the schema's
behavioral and scheduling assumptions. The structural certifying synthesis procedure takes
this schema as input. The general transition-system procedure described above
does not require these independent-pivot assumptions.

In particular, enabling admission must characterize first-family participation;
pivots must be initially ready for their second signatures; and, whenever the
first certificate is feasible, second participation must be governed by the
stated repair test. Other transitions must not independently remove or add the
pivotal contributions. Fixed base support, distinct certificate signers,
irreversible signed output, availability at the specified collectors, and
complete coverage of the designated agreement observation are essential.
The corrected one-pivot theorem states positive persistence explicitly.

The order language admits all linear extensions of a finite opportunity partial
order for each admission policy. Suppressed delivery slots and disabled voting
opportunities stutter while retaining their precedence constraints. Endpoint
keys are independently controllable. Arbitrary real schedulers need not realize
this language. If a harness admits fewer orders, safety in the larger schema
transfers only under the same behavioral correspondence; an existential model
witness still needs a realizable harness order.

An extra edge may alter transitive precedence, provide substitute votes, or
change local behavior. Those changes require updating the graph, deficits, or
behavioral contract. The theorem does not establish a universal incompleteness
result for directed graphs, communication-closure methods, Twins, or other
testing frameworks. It also does not rank framework capabilities or identify a
universally minimal scheduler grammar.

## Timing and weights

The repair deadline is the indispensable second **signature opportunity**.
Repair before a later certificate or decision is insufficient when the needed
signature has already been emitted and remains available. This is a conditional
statement about persistent outputs, not a claim that every late repair causes
disagreement or that network delivery can never prevent a certificate.

The minimum phase budget

$$
t_* = \max(0,d_0+d_1-k-\alpha(H))
$$

requires **unit weights and costs**, fine feasibility, all keys allowed, none
required, and optimal choice of independent split keys. It does not say that every set of $t_*$ arbitrary message exceptions
works. A prescribed set has capacity $|S|+\alpha(H[I\setminus S])$; its size
alone does not determine its effectiveness. Weighted pivots require the exact
four-role support condition, or the attainable-subset criterion in the common
deadline special case. The common-deadline interval cannot be replaced by a
continuous total-capacity inequality, and the unit-weight budget cannot be
generalized by substituting total weight for $k$. Membership and weights are
fixed; dynamic validators, staking behavior, and changing quorum systems are
outside this model.

## Structured synthesis, certificates, and resource bounds

The optimizer supports positive integer vote weights, nonnegative integer
split costs, and declared allowed/required keys. These are inputs to a finite
design problem. The synthetic control costs are not measured latency, network
overhead, engineering effort, or a framework's empirical bug-finding cost.
The returned order is a legal execution of the supplied opportunity schema;
implementing it in an adapter still requires the behavioral correspondence and
schedule realizability obligations above.

Each finite optimum combines a replayed feasible execution with independently
checked Bellman lower-bound potentials. A feasible execution alone proves only
an upper bound. The separate checker reconstructs reachability, components and
all legal local assignments; checking only the optimizer's chosen assignments
would not establish minimality. The certificate may also prove infeasibility
using an infinite initial potential. The Python parser, reconstruction,
enumeration, execution checker, and their connection to the formal state graph
remain executable obligations rather than mechanically verified source code.

The reference algorithm enumerates assignments within strongly connected
components and uses a quota-indexed potential table. It is exponential in the
largest component after self-loop exclusion, and pseudo-polynomial in integer
quota values. There is no polynomial-time claim, no fixed-parameter tractability
claim in component size alone for binary-encoded weights, and no guarantee of
polynomial-size certificates. Independent verification need not be faster than
optimization on every instance.

The default component-size limit is 10 and the potential-table limit is two
million cells. An optional wall-clock budget is available for standalone runs.
Exhaustion is `RESOURCE_LIMIT` (unknown), not infeasibility; a standalone CLI
request exits with code 2 in that case. The deterministic scale study contains
15 cases: 13 certified optima and 2 expected unknowns caused by the explicit
component-size cutoff, not by measured timeouts. Solved structured cases reach
48 pivots; this does not establish that arbitrary 48-pivot problems are easy.
A 24-vertex single cycle is deliberately retained as unknown for this generic
implementation even though a specialized cycle algorithm could solve it.

The non-submodularity example and unbounded approximation ratio concern the
specified maximum-positive-immediate-gain-per-cost rule. They are not a lower
bound for every heuristic or for established feedback-vertex-set solvers. The
single-run timing record is separate from deterministic results and supports
no statistical performance or speedup claim.

## Concrete protocol and source correspondence

The guarded disagreement execution is a bounded local model derived from
selected CometBFT v0.39.3 rules. It uses four equal-weight validators, one height,
two rounds, and
the declared proposer prefix. Only the pivot's round-0 lock assignment is
omitted; its valid-block state and round-1 lock update are retained. The
conflicting designated observers are unmutated. The baseline and mutant are
compared on the specified 12-case matrix, not on all possible executions of the
protocol.

The model includes guarded proposal, prevote, precommit, timeout, and commit
transitions, local signer sets, and explicit emitted envelopes. It does not run
the production client. Deterministic test-only authentication checks envelope
and signer integrity; it is not a production cryptographic implementation.
Proposer-priority updates, serialization, block-part gossip, recovery, the full
event loop, and application execution are not modeled end to end. Complete
block delivery and the proposer prefix are explicit environmental choices.

The FIFO audit concerns **admitted vote envelopes** on each transport peer pair,
including their order across rounds. It excludes proposal/block traffic and
messages dropped before transmission. The direct late-precommit control is
non-FIFO and is reported as such. The separate relay control preserves the
original vote signer and passes this scoped audit, but adds declared forwarding
opportunities to the gossip skeleton. It must not be silently identified with
the original fixed trace or a full transport-stack execution.

The verified v0.39.3 snapshot preserves exact source bytes, Git blob identifiers,
and SHA-256 manifests. The older v0.40.0 snapshot remains separately identified.
These checks establish source identity; source matching alone does not establish
execution equivalence. Reproducing the model's disagreement in a production
adapter would require running the pinned client under the same declared program
variant, realizing the stated admission and delivery orders, and checking its
emitted votes and observer decisions against the model. No deployed-client
vulnerability or such adapter result is claimed here.

## Targeted execution of unchanged implementation code

A separate conformance bridge executes the unmodified CometBFT v0.39.3 consensus
package with Go 1.25.0. Four ordinary-operation scenarios instantiate four
unchanged native states each. Actual native queues supply all proposals, block
parts and votes; timeout dispatch consumes requests actually made by the native
implementation. The real proposer-priority, vote validation, locking, block
validation, block-store and local ABCI application code execute. The 14 checks
cover 32 native Ed25519 votes and 132 recorded events. Three additional normal
runs preserve the semantic summaries, and one race-detector run passes.

Dispatch is synchronous and in process. The reactor, sockets, WAL receive loop,
production timer goroutines, and persistent private-validator signer are not
exercised. The upstream `MockPV` uses deterministic test keys; the native block
store and application use in-memory fixtures, so a store write is not evidence
of disk durability or crash recovery. Both deciding observers in the normal
commit scenario store the same block. These scenarios neither inject the model's
mutation nor reproduce its disagreement.

The independent Python/OpenSSL audit verifies all 32 signatures and parses the
canonical protobuf vote metadata, including nanosecond timestamps. It is an
independent cryptographic and evidence check, not an independent implementation
of consensus. Output immutability is directly observed across normal height
advancement; the model's stronger repair-timing argument retains its separate
proof and bounded-execution evidence. Four finite native scenarios validate
the exercised implementation obligations, not all schedules or a full refinement.

## Proof and experiment boundaries

Lean 4.33.0 checks the corrected one-pivot theorem over an arbitrary behavioral
contract, the capacity and split-budget arithmetic under their hypotheses, the
weighted interval, and a small persistent-output machine. The expanded integrated
build has 15 jobs, its axiom audit covers 46 named declarations, the hygiene
check covers 23 source files, and `leanchecker` rechecking passes. Verification
receipts are bound to the current Lean source hashes. These successes do not
discharge the assumptions for an arbitrary protocol instance.

`TransitionRefinement.lean` additionally proves total static-policy completion,
least trace cost, consistent memory updates, sublevel certificates, local labelled
simulation, concrete optimality transfer and invariant-guided policy elimination.
The finite refinement-count bound remains paper-level cardinality reasoning.
Python parsing, complete successor construction and client correspondence are
not mechanized. See [the detailed scope](research/TRANSITION_MECHANIZATION.md).

`GraphRealization.lean` fully proves the graph-reversal equivalence, finite
acyclicity versus existence of an injective event schedule, and the graph-to-order
bridge, including input supplied as cover edges. It derives the graph from
transitive event precedence and does not assume a capacity formula or a
compatible schedule. `CertificateOptimality.lean` proves the generic Bellman
lower-bound, matching-witness optimality, and infinite-potential infeasibility
principles for arbitrary nonnegative-cost paths.

The weighted four-role correspondence, maximum-acyclic-set optimization and
optimal graph-capacity attainment, Python SCC decomposition and exhaustive
enumeration, and the explicit-schema NP-completeness reduction remain paper
proofs or executable obligations. The concrete transition model has neither a
Lean refinement proof nor an independent Go implementation. The new native Go
conformance checks exercise unchanged implementation rules; they do not fill
those formal refinement gaps.

The general graph and four-event-order suites exhaust the legal orders of their
stated finite instances. The common-deadline sweep uses support-equivalent
barrier representatives; the weighted sweep uses an extremal late order and
all admissions. These latter suites do not enumerate every event permutation.
The millions of policy executions count executions in one declared schema,
not independent protocols, bug prevalence, or probabilities of discovery.

The synthesis study compares and independently verifies 35,223 optimization
certificates over its stated graph, weighting, quota, restricted-key and
four-event-order subcorpora. A separately written oracle checks another 3,253
problems from 48 seeded arbitrary three-pivot event DAGs. It exhausts the orders,
admissible modes and quota pairs for those 48 inputs, not every three-pivot DAG,
weighting or cost vector. The synthesis graph corpus overlaps the older frontier
corpus; matching execution totals provide a cross-check and are not additional
independent protocol samples. The 15-case scale corpus is synthetic and reported
separately, including its two resource-limited cases.

The retained 384 Python/Go observations compare the old Boolean terminal
classifier. The historical declaration named
`bounded_tendermint_refines_quorum_pivot` proves matching classifications, not
transition refinement. SMT obligations and custom certificate checks provide
supporting evidence for their stated encodings. Retained Coq files are archival
material, not a second maintained mature-prover build.

Replay erasure still requires relevant-state and output congruence, stable
processed keys, projected duplicate stutter, and silent duplicate output. The
`X,X,Y` controls show why immediate silence alone is insufficient. The classical
reversible-set criterion, graph reductions, simulation arguments, and the
previously reported certificate-driven round advancement in Twins' preferred-round
mutation experiment are credited in the
[literature audit](research/LITERATURE_AND_PROVENANCE_AUDIT.md).

## Reproduction and scientific scope

The results concern finite agreement observations. They do not establish
liveness, unbounded partial synchrony, timing performance, exploitability,
prevalence, discovery probabilities, or completeness of a production tester.

Empty caches require external dependency downloads. Lean, the native Go 1.25.0
toolchain, the TeX overlay, uv-managed Python packages (including the
`native-audit` extra), and source fixtures have their stated pins;
Pandoc, the host TeX engine, and other executed tools are recorded in build
logs. The container base image is pinned, while its package installation also
depends on the configured Debian package repositories.

All synthesis outputs, including compressed certificates with deterministic
gzip headers, and the other listed deterministic results are compared
byte-for-byte. Native execution retains wall-clock timestamps. Only its semantic
`native_summary.json` is byte-compared; native raw votes, signatures, provenance,
signature-audit output, repeatability receipts and execution logs are regenerated
and checked rather than required to match old bytes. The full reproduction also
reruns the three normal repetitions and one race-detector execution.

The PDF is validated by
successful build, source synchronization, page-budget checks, diagnostic checks,
and embedded fonts. Different TeX engines may produce different PDF bytes;
cross-engine SHA-256 identity is not a promised reproducibility property.
The enforced main-text limit is 15 pages; actual page counts for a build are
recorded in `build_logs/lipics_page_budget.log`. See
[expected outputs](reproduction/EXPECTED_OUTPUTS.md) and the
[claim-to-evidence ledger](CLAIM_EVIDENCE_LEDGER.md) for the exact gates.
