# Twins Scheduler Closure

This research artifact studies when coupling admission across protocol phases
can hide an agreement violation. Its central result now characterizes an
explicit family of finite scheduling domains with several independently
controlled pivotal validators, partial delivery orders, and irreversible signed
outputs. A guarded four-validator Tendermint-style execution supplies a concrete
bounded witness and timing controls.

Start with the [revised manuscript](manuscript/pdf/final_lipics_manuscript.pdf),
the [revision report in Russian](docs/reviews/REVISION_REPORT_RU.md), or the
[response to the reviewer](docs/reviews/RESPONSE_TO_REVIEWER.md).

## Main result: the repair frontier

Repair must precede the indispensable **second signature**, not merely the
second decision. Once a conflicting vote has been signed and remains available
to its collector, later state repair cannot retract that output.

For the independent-pivot schema, let $k$ be the number of unit-weight pivots
and let $d_0,d_1$ be the contributions missing from two conflicting certificate
bases. An open coarse key admits both an enabling envelope $E_i$ and a repair
envelope $R_i$. A closed key admits neither; its initially ready pivot can still
contribute to the second branch. Let $V_i$ be the second-vote opportunity and
derive a directed graph, including self-loops, from **transitive** precedence:

$$
i\to j\quad\Longleftrightarrow\quad R_i\prec V_j,
\qquad
\alpha(H)=\max\{|J|:H[J]\text{ is acyclic}\}.
$$

Under the stated behavioral, output, independence, and complete-order
contracts, a coarse unsafe execution exists exactly when

$$
\max(d_0,d_1)\le k,
\qquad d_0+d_1\le k+\alpha(H).
$$

For **unit weights**, if fine admission can expose a witness, the exact minimum
number of optimally chosen keys that must distinguish enabling from repair is

$$
t_* = \max(0,d_0+d_1-k-\alpha(H)).
$$

The paper also gives a weighted subset characterization. Indivisible weights
require attainable subset sums; replacing $k$ by total weight in the unit-weight
budget formula is invalid. The reversible-set argument and underlying graph
optimization are classical. The contribution is their connection to scheduler
admission, signature timing, and certificate deficits. See the
[manuscript sources](manuscript/markdown/manuscript.md) and
[literature audit](docs/research/LITERATURE_AND_PROVENANCE_AUDIT.md) for proofs,
attribution, and assumptions.

## What was checked

| Evidence | Revised result |
| --- | --- |
| Python tests | 35 pass: 13 retained, 8 frontier tests, 14 concrete-trace tests |
| General repair graphs | All 530 directed graphs with loops for $k=1,2,3$; 50,363 legal orders; 1,357,209 policy/split executions |
| Exact boundary and budget | 13,074 checks of each; zero mismatches |
| General event orders | All 219 labelled partial orders on two repair and two vote opportunities, supplied as cover edges |
| Common and weighted frontiers | 44 common-deadline domains and 258 weighted domains, with explicitly stated order representatives |
| Concrete protocol execution | 12 legality-audited baseline, mutant, timing, and relay cases |
| Lean 4.33.0 | 12 build jobs; 20 audited declarations; build, axiom audit, source hygiene, and `leanchecker` exit successfully |
| SMT controls | 8 expected UNSAT and 4 expected SAT results using uv-pinned `z3-solver==4.13.3.0` |

The [frontier evaluator](src/python/twins_scheduler/repair_frontier.py) executes
guarded events independently of the capacity formula; the
[runner](scripts/run_repair_frontier.py) compares its outcomes with the theorem.
The [concrete trace](src/python/twins_scheduler/concrete_trace.py) tracks emitted
envelopes, actual signer sets, local quorums, nil votes, timeouts, and persistent
outputs. Its source pin is CometBFT v0.39.3, commit
`49b82838fcca442b2445f76605c101609ed04130`.

The concrete execution runs the declared local model. It does not run the
production CometBFT client. The two conflicting observers are unmutated; only
the pivot's round-0 lock assignment is omitted. The separate relay control
passes the stated FIFO audit for admitted vote envelopes; this is not full
transport-stack conformance. See the [trace explanation](docs/research/CONCRETE_TRACE.md).

### Formal assurance

[RepairFrontier.lean](formal/lean/SchedulerClosure/RepairFrontier.lean) checks the
corrected one-pivot theorem over an arbitrary behavioral contract, the capacity
and budget arithmetic under their hypotheses, the weighted admission interval,
and a small persistent-output machine. The graph reversal proof,
graph-to-execution correspondence, and attainment of optimal graph capacity are
paper proofs with finite executable cross-checks; they are not fully mechanized
by that arithmetic module. The concrete protocol model has no Lean transition
refinement proof.

The retained 384-row Python/Go agreement checks the earlier Boolean terminal
classifier. It is supporting evidence, not an independent implementation of the
new concrete trace. The [claim-to-evidence ledger](docs/CLAIM_EVIDENCE_LEDGER.md)
records these distinctions.

## Reproduce the revision

Prerequisites are Python 3.11–3.13, uv 0.6.14, Go 1.24, Pandoc, Git, curl, a C
compiler, base pdfTeX/BibTeX and Poppler commands, and `dpkg-deb`. Pandoc generates
the synchronized LaTeX manuscript from Markdown. Lean and the pinned TeX overlay
are installed into the repository-local cache; the Python dependency lock pins
the Z3 wheel used by the SMT checks.

```bash
./reproduce_revision.sh
```

This entry point delegates to `./reproduce.sh`, which includes the revised
frontier and concrete-trace runners. The stages are also available through
`make bootstrap`, `make test`, `make formal`, `make paper`, `make verify`,
`make reproduce`, and `make release`. A mandatory check failure stops the run.
For Docker instructions, see [container reproduction](containers/README.md).

Each reproduction creates an isolated output tree. Deterministic data results
are compared byte-for-byte with their committed references. The PDF is checked
by building it, enforcing the main-text page budget, checking warnings and font
embedding, and checking Markdown/LaTeX synchronization. Identical PDF bytes
across different TeX engines are not required. The current verified PDF has
17 physical pages, including 13 main-text pages; the enforced main-text limit is
15. Detailed counts and output locations are in
[expected outputs](docs/reproduction/EXPECTED_OUTPUTS.md).

## Repository guide

- [Manuscript](manuscript/): Markdown sources, official LIPIcs source, figures,
  and the revised PDF.
- [Revision results](results/revision/): frontier summary and graph, common,
  and weighted case tables; [concrete results](results/new/): complete traces.
- [Code](src/) and [tests](tests/): executable models and checks.
- [Formal evidence](formal/): Lean, supporting SMT, and certificate checks.
- [Source fixtures](models/tendermint_style/): verified v0.39.3 snapshot and
  separately preserved historical v0.40.0 material.
- [Provenance](provenance/PROVENANCE.md) and [decision log](docs/DECISION_LOG.md):
  source lineage and canonical choices.
- [Limitations](docs/LIMITATIONS.md): exact scope of the mathematical,
  executable, and reproducibility claims.

Citation metadata is in [CITATION.cff](CITATION.cff). Original code and
documentation use the MIT license; third-party materials retain the terms
listed in [third-party notices](THIRD_PARTY_NOTICES.md).
