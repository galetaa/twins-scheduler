# Limitations

## What the mathematical result covers

The repair-frontier theorem quantifies over arbitrary finite instances of the
declared independent-pivot certificate schema. Its proof is not restricted to
the small instances enumerated by the artifact. Its application to a protocol
does require discharging the schema's behavioral and scheduling assumptions.

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

requires **unit weights**, fine feasibility, and optimal choice of independent
split keys. It does not say that every set of $t_*$ arbitrary message exceptions
works. Weighted pivots require the stated attainable-subset criterion. The
common-deadline interval cannot be replaced by a continuous total-capacity
inequality, and the unit-weight budget cannot be generalized by substituting
total weight for $k$. Membership and weights are fixed; dynamic validators,
staking behavior, and changing quorum systems are outside this model.

## Concrete protocol and source correspondence

The new execution is a bounded local model derived from selected CometBFT
v0.39.3 rules. It uses four equal-weight validators, one height, two rounds, and
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
execution equivalence. A production-level conformance claim would require an
adapter that runs the pinned client, realizes the stated admission and delivery
orders, and checks its emitted votes and observer decisions against the model.
No deployed-client vulnerability or such adapter result is claimed here.

## Proof and experiment boundaries

Lean 4.33.0 checks the corrected one-pivot theorem over an arbitrary behavioral
contract, the capacity and split-budget arithmetic under their hypotheses, the
weighted interval, and a small persistent-output machine. The integrated build,
20-declaration axiom audit, source-hygiene check, and `leanchecker` rechecking
pass. These successes do not discharge the assumptions for an arbitrary
protocol instance.

Graph reversal, graph-to-execution correspondence, attainment of optimal graph
capacity, and the explicit-schema NP-completeness reduction are paper proofs.
The graph theorem and capacity construction also have finite executable
cross-checks. They are not fully mechanized by the arithmetic Lean module. The
concrete transition model has neither a Lean refinement proof nor an independent
Go implementation.

The general graph and four-event-order suites exhaust the legal orders of their
stated finite instances. The common-deadline sweep uses support-equivalent
barrier representatives; the weighted sweep uses an extremal late order and
all admissions. These latter suites do not enumerate every event permutation.
The millions of policy executions count executions in one declared schema,
not independent protocols, bug prevalence, or probabilities of discovery.

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
preexisting Twins preferred-round repair mechanism are credited in the
[literature audit](research/LITERATURE_AND_PROVENANCE_AUDIT.md).

## Reproduction and scientific scope

The results concern finite agreement observations. They do not establish
liveness, unbounded partial synchrony, timing performance, exploitability,
prevalence, discovery probabilities, or completeness of a production tester.

Empty caches require external dependency downloads. Lean, the TeX overlay,
uv-managed Python packages, and source fixtures have their stated pins;
Pandoc, the host TeX engine, and other executed tools are recorded in build
logs. The container base image is pinned, while its package installation also
depends on the configured Debian package repositories.

Deterministic data results are compared byte-for-byte. The PDF is validated by
successful build, source synchronization, page-budget checks, diagnostic checks,
and embedded fonts. Different TeX engines may produce different PDF bytes;
cross-engine SHA-256 identity is not a promised reproducibility property.
The current checked document has 13 main-text pages within the enforced
15-page limit. See [expected outputs](reproduction/EXPECTED_OUTPUTS.md) and the
[claim-to-evidence ledger](CLAIM_EVIDENCE_LEDGER.md) for the exact gates.
