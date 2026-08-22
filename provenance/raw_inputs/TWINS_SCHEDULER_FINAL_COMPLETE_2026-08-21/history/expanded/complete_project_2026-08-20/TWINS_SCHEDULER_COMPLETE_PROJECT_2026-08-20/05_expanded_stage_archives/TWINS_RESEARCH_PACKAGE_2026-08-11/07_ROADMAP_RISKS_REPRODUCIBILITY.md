# Roadmap, Risks, Safety and Reproducibility

**Overall verdict:** **ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT**.  
**Work authorized immediately:** Gate 0, Gate 1, Gate 2 and the blocking Gate 3 pilot.  
**Work not authorized before pilot:** production-client integration, broad protocol portfolio, full Coq mechanization and performance engineering.

## 1. Resource registry

| Resource | Source | Open | License | Format | Approximate size | Currency on 11 Aug 2026 | Local acquisition | Preprocessing | Disappearance or change risk | Replacement | Version fixation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Research brief | S01 local file | Yes in project | User-provided | Markdown | 78 KB | Fixed input | Already local | None | Low | None | SHA-256 in S01 |
| First research report | S02 local file | Yes in project | User-provided | Text | 135 KB | Fixed input | Already local | None | Low | None | SHA-256 in S02 |
| Independent audit | S03 local file | Yes in project | User-provided | Markdown | 114 KB | Fixed input | Already local | None | Low | None | SHA-256 in S03 |
| Twins paper | S04 | Yes | CC-BY 4.0 for LIPIcs article | PDF and HTML metadata | Under 2 MB | Stable published paper | Download DOI or arXiv copy | Record page and section mapping | Low | Author copy | DOI and file checksum |
| VLSM paper | S05 | Yes | arXiv terms; paper copy | PDF | Under 3 MB | Version 4, 15 Dec 2023 | Download arXiv source/PDF | Extract theorem map only | Low | DOI-resolved arXiv copy | arXiv version and checksum |
| VLSM Coq repo | S06 | Yes | BSD-3-Clause | Git and Coq | Moderate | Active, 325 commits at audit | Git clone | Build in pinned opam switch | Medium due moving master | Archive selected commit | Commit hash, submodule and dependency lock |
| ByzzFuzz paper and code | S07 | Paper open; code availability to be reconfirmed | Paper publisher terms; code license per repo | PDF and source | Moderate | Stable paper | Download official/author copy | Map mutation operators to fault model | Medium for code | Reimplement minimal mutation comparator | DOI and commit hash |
| ByzzBench | S08 | Yes | MIT | Python repository | Moderate | Early active framework | Git clone | Use only adapter-compatible subset | Medium | Internal controlled harness | Commit hash and local patch checksum |
| Communication Closure artifacts | S09 | Paper open or author copy | Per artifact | PDF and source/model | Unknown | Stable paper | Download source if available | Extract formal conditions | Medium | Manual reproduction of theorem assumptions | DOI and checksum |
| Cutoff and short-counterexample papers | S10, S11 | Open versions expected | Article terms | PDF | Small | Stable | Download author copies | No data preprocessing | Low | DOI metadata plus library copy | DOI and checksum |
| MALLORY | S13 | Paper and artifact status checked at Gate 2 | Artifact license per repo | Source and traces | Potentially large | Stable 2023 result | Optional clone | Only terminology/causal comparison | Medium | Paper-level analysis | DOI, commit if used |
| Node-Centric Testing | S20 | Metadata confirmed; full text unconfirmed | Unknown until obtained | PDF | Unknown | 2026 current threat | Obtain official/author copy | Full-text novelty audit | **High** | Author request or institutional access | DOI, file checksum and access date |
| twins-simulator | S21 | Yes | Apache-2.0 | Python repository | Small | Research prototype, 20 commits at audit | Git clone | Convert JSON scenarios and traces | Medium-high due low activity | Internal Streamlet-like model | Commit hash and checksum |
| relab/hotstuff | S22 | Yes | MIT | Go repository | Moderate-large | Active, 1,849 commits at audit | Git clone | Build one local safety-test configuration | Medium due active changes | S21 or ByzzBench | Commit hash, Go version and module checksum |
| Python 3.14.7 | S23 | Yes | PSF | Runtime | Platform dependent | Released 5 Aug 2026 | Official installer or uv-managed Python | None | Low | Python 3.13 after compatibility audit | Patch version and binary hash where feasible |
| Hypothesis 6.165.3 | S24 | Yes | MPL-2.0 | Python package | Small | Released 11 Aug 2026 | uv/PyPI | None | Medium as rapid-release package | Exhaustive small generators | Version and source SHA-256 from S24 |
| pytest 9.1.1 | S25 | Yes | MIT | Python package | Small | Released 19 Jun 2026 | uv/PyPI | None | Low | unittest | Exact version in lockfile |
| uv | S26 | Yes | Project licensing per official distribution | Binary and lockfile | Small | Active current docs | Official installer/package manager | None | Medium due fast evolution | venv and hashed requirements | Exact binary version and checksum |
| Z3 5.0.0 | S27 | Yes | MIT | Binary/source | 37–76 MB per platform archive | Released 17 Jul 2026 | Official release asset | None | Medium; new release and known edge-case issues | Explicit enumeration or audited stable release | Release tag, asset SHA-256 and solver options |
| Generated traces | This project | Yes | Same as project artifact | JSONL | From MB to GB | Generated per run | Local | Canonicalization and manifesting | Low if archived | Regenerate from source | Run manifest and SHA-256 |
| Generated figures | This project | Yes | Same as project artifact | SVG, PDF and source CSV | Small | Derived | Local | Automated only | Low | Regenerate | Script hash and source manifest |

No project dependency relies on a commercial archive node, private validator telemetry, paid cloud, public RPC or mainnet funds.

## 2. Reproducibility contract

### 2.1. Environment pinning

- Python patch version in `.python-version`;
- direct package versions in `pyproject.toml`;
- complete resolved graph in committed `uv.lock`;
- exact uv version in `environment.json`;
- optional Coq dependencies in pinned opam switch export;
- optional Go external adapter in `go env` report and repository commit;
- optional solver binary checksum and command-line options.

### 2.2. Container and lockfile

Primary reproduction uses uv on native Linux. A container is supplied as secondary path, not the only path. Container base image is pinned by digest. The container build copies `uv.lock` and verifies dependency resolution before source code.

### 2.3. Randomness

Core enumeration is deterministic. Any randomized software test or optional fuzzer records:

- algorithm name;
- seed;
- generator version;
- run count;
- stopping rule;
- raw trace manifest.

Randomized results never substitute for exact language inclusion.

### 2.4. Configuration management

- every experiment has immutable TOML configuration;
- modifications produce a new file or versioned override;
- config hash is included in every result;
- all default values are materialized in resolved configuration output;
- environment variables may not alter semantic settings silently.

### 2.5. Data manifests

Each raw result directory contains:

- source commit;
- configuration checksum;
- protocol schema version;
- adversary profile;
- bound vector;
- completeness status;
- environment report;
- file sizes and SHA-256 checksums;
- upstream commit hashes.

### 2.6. Deterministic replay

Every stored trace can be replayed from initial state. Replay verifies:

- each event enabled;
- pre-state hash;
- post-state hash;
- emitted messages;
- observation;
- safety verdict.

A trace failing replay is excluded from analysis and triggers a blocking error.

### 2.7. Raw and processed results

- raw traces are immutable and never hand-edited;
- processed CSV and figures are regenerated by scripts;
- notebooks may explore but cannot produce final paper numbers;
- processing scripts reference raw manifest IDs;
- counterexamples are stored both machine-readable and human-readable.

### 2.8. Automated figures

One script regenerates all figures from processed tables. Figure captions include bound and protocol model. Visual styling does not encode unstated categories.

### 2.9. Hardware report

Record CPU model, core count, RAM, storage type, OS kernel, architecture and container runtime. GPU is reported but not used in central experiments.

### 2.10. Minimal-command reproduction

Target commands:

```text
uv sync
uv run pytest
uv run python scripts/run_pilot.py --config configs/pilot.toml
uv run python scripts/verify_manifest.py results/pilot/manifest.sha256
uv run python scripts/make_figures.py --manifest results/pilot/manifest.sha256
```

### 2.11. Artifact documentation

Required:

- README with 15-minute smoke test and full-run path;
- artifact-evaluation guide;
- expected outputs and checksums;
- resource estimates;
- known limitations;
- license and citation;
- safety policy;
- schema documentation;
- trace interpretation guide.

## 3. Safe experimental policy

- no mainnet interaction;
- no transfer, lock or theft of assets;
- no acquisition or use of third-party private keys;
- no unauthorized access to nodes, contracts or infrastructure;
- no DoS, spam, front-running, sandwich attack or market manipulation;
- no live public-network partitions or message suppression;
- dangerous schedules only in executable models, simulators, forked local state or isolated testnets;
- no deanonymization or personal-data collection;
- respect repository licenses and service terms;
- no publication of an immediately exploitable production trace before coordinated disclosure.

## 4. Preliminary responsible disclosure plan

### 4.1. Sensitivity criterion

A result is sensitive when it:

- produces a previously unknown safety violation in a maintained production implementation;
- identifies a practical sequence requiring no privileged access and affecting deployed networks;
- exposes a bypass of message validation or certificate verification;
- materially lowers attack cost or required Byzantine fraction.

A counterexample only to abstract Twins completeness is normally not a security vulnerability unless tied to a concrete deployed implementation bug.

### 4.2. Recipient

Notify the maintainer security contact of the affected repository or protocol foundation. If no channel exists, use private maintainer contact and record attempts. University supervisor is informed before external disclosure.

### 4.3. Evidence retention

Preserve:

- exact commit and build environment;
- minimized local trace;
- logs and checksums;
- proof that no public network was touched;
- validation by a second local run;
- timeline of communications.

### 4.4. Initially withheld information

Do not immediately publish:

- copy-paste exploit scripts against deployed endpoints;
- operational targeting instructions;
- keys, credentials or identifying telemetry;
- exact high-scale abuse parameters.

### 4.5. Reproducibility versus exploitation

Publish formal model, safety property and sanitized local reproducer. Delay production-specific adapter details only when they materially enable exploitation. The paper must still allow verification of the scientific claim through the isolated model.

### 4.6. Public release condition

Public release is appropriate after vendor coordination, remediation or an agreed disclosure window, subject to supervisor and legal/ethical review. No universal fixed number of days is imposed because policies differ; the communication record states the selected rule.

## 5. Roadmap by decision gates

### Gate 0 — Final novelty delta

1. **Inputs:** S01–S20, original audit, residual theorem candidate.  
2. **Tasks:** full VLSM theorem mapping, S20 full-text acquisition, refinement/chain-cover search, expert terminology review.  
3. **Outputs:** `prior_art_matrix.csv`, `claim_map.md`, exact theorem candidate, search log.  
4. **Completion criterion:** every core claim classified as known, new, killed or conditional.  
5. **Go:** no equivalent finite-clone cutoff/separation result and residual claim is nontrivial.  
6. **No-go:** direct prior art or direct generic theorem subsumes claim.  
7. **Pivot:** lifecycle-conformance gap survives but clone-number theorem collapses.  
8. **Dependencies:** none beyond current report.  
9. **Effort:** 4–7 focused person-days.  
10. **Main risk:** hidden prior art under refinement or virtual-copy terminology.

### Gate 1 — Minimum formal model

1. **Inputs:** exact residual claim and assumption map.  
2. **Tasks:** define protocol, `Valid`, `AB`, `AE`, `AT(k)`, observations and safety.  
3. **Outputs:** `spec/definitions.md`, executable type skeleton and proof obligations.  
4. **Completion:** every key term has operational definition; T0 embedding is credible.  
5. **Go:** non-vacuous validator protocol and asymmetric powers eliminated.  
6. **No-go:** class empty or theorem definitional.  
7. **Pivot:** narrow to concrete lifecycle separation.  
8. **Dependencies:** Gate 0.  
9. **Effort:** 5–8 days.  
10. **Risk:** validity predicate encodes desired theorem.

### Gate 2 — Tools and resources

1. **Inputs:** model requirements.  
2. **Tasks:** pin Python, uv, tests; clone and checksum critical repositories; run smoke builds; verify licenses.  
3. **Outputs:** lockfile, environment report, source manifest and license inventory.  
4. **Completion:** pilot runs offline after initial dependency fetch.  
5. **Go:** all mandatory resources available locally.  
6. **No-go:** critical formal source or tool unavailable and no replacement.  
7. **Pivot:** remove optional external integration or solver.  
8. **Dependencies:** Gate 1 can overlap late Gate 0.  
9. **Effort:** 2–4 days.  
10. **Risk:** dependency drift or external artifact build failure.

### Gate 3 — Blocking pilot

1. **Inputs:** executable definitions and pinned environment.  
2. **Tasks:** implement toy protocol, three adversaries, exact exploration, language comparison and minimization.  
3. **Outputs:** all BP-TWINS-FC-01 files and decision memo.  
4. **Completion:** decisive bound completed or explicitly inconclusive with resource diagnosis.  
5. **Go:** nontrivial hierarchy, invariant, bound or separation.  
6. **No-go:** result duplicates S05, chain cover or trivial two-clone behavior.  
7. **Pivot:** lifecycle, snapshot or conformance boundary.  
8. **Dependencies:** Gates 0–2.  
9. **Effort:** 7–12 days.  
10. **Risk:** no unsafe witness within tractable exact bound.

### Gate 4 — Main artifact

1. **Inputs:** Gate 3 GO theorem or separation route.  
2. **Tasks:** harden explorer, causal analyzer, second protocol model and regression suite.  
3. **Outputs:** research-quality repository and schema-stable trace corpus.  
4. **Completion:** all core experiments executable through scripts.  
5. **Go:** artifact reproduces pilot and second model.  
6. **No-go:** engineering complexity obscures claim or state explosion prevents validation.  
7. **Pivot:** proof-first paper with smaller artifact.  
8. **Dependencies:** Gate 3.  
9. **Effort:** 10–16 days.  
10. **Risk:** scope expansion into general BFT framework.

### Gate 5 — Full experiments or proofs

1. **Inputs:** stable artifact and theorem statement.  
2. **Tasks:** E3–E10, condition ablations, lower bounds, cross-protocol validation and optional mechanization.  
3. **Outputs:** proof draft, experiment manifests, witness corpus and tables.  
4. **Completion:** every atomic new claim has direct evidence.  
5. **Go:** theorem or counterexample family survives alternatives.  
6. **No-go:** central result becomes protocol-specific engineering fact with no general statement.  
7. **Pivot:** narrow publication to separation theorem or lifecycle condition.  
8. **Dependencies:** Gate 4.  
9. **Effort:** 12–25 days.  
10. **Risk:** proof difficulty or cross-protocol failure.

### Gate 6 — Robustness and validity

1. **Inputs:** complete claim-evidence ledger.  
2. **Tasks:** parameter sensitivity, reductions-off checks, independent oracle, threat analysis and reviewer-style attack.  
3. **Outputs:** validity report, revised assumptions and limitations.  
4. **Completion:** no unresolved high-impact internal-validity issue.  
5. **Go:** decisive results reproducible and scoped.  
6. **No-go:** result depends on canonicalizer, hidden asymmetric power or one arbitrary parameter.  
7. **Pivot:** weaken claim to verified domain.  
8. **Dependencies:** Gate 5.  
9. **Effort:** 5–8 days.  
10. **Risk:** late discovery of construct error.

### Gate 7 — Reproducible artifact

1. **Inputs:** validated experiments.  
2. **Tasks:** clean-room reproduction, container, documentation, checksum archive and artifact evaluation.  
3. **Outputs:** release archive, DOI-ready package and reproduction log.  
4. **Completion:** independent machine reproduces core result with documented commands.  
5. **Go:** artifact ready for anonymous or public evaluation.  
6. **No-go:** hidden manual step or unavailable dependency.  
7. **Pivot:** release minimal proof/checker subset with explicit exclusions.  
8. **Dependencies:** Gate 6.  
9. **Effort:** 4–7 days.  
10. **Risk:** reproducibility fails outside development machine.

### Gate 8 — Manuscript

1. **Inputs:** final evidence and artifact.  
2. **Tasks:** write paper, produce figures/tables, internal review, restrained novelty statement and venue fit.  
3. **Outputs:** submission-ready manuscript and supplementary package.  
4. **Completion:** all claims trace to evidence and no forbidden claim remains.  
5. **Go:** supervisor agrees contribution meets target audience.  
6. **No-go:** no coherent contribution beyond implementation.  
7. **Pivot:** technical report or workshop paper with narrower claim.  
8. **Dependencies:** Gates 0–7.  
9. **Effort:** 10–18 days.  
10. **Risk:** contribution-audience mismatch.

## 6. Critical path

`Gate 0 → Gate 1 → Gate 3 → theorem or counterexample route → Gate 5 cross-protocol validation → Gate 6 → Gate 7 → Gate 8`.

Gate 2 may overlap the end of Gate 1. Concrete production adapter is not on the critical path unless the intended paper claims practical harness conformance.

## 7. First fifteen tasks in order

| No. | Concrete action | Expected artifact | Dependency | Acceptance criterion | Size | Parallel |
|---|---|---|---|---|---|---|
| 1 | Create immutable source ledger and checksums | `data/manifests/sources.json` | None | All local and web-critical sources have ID, type, date and checksum or DOI | S | Yes |
| 2 | Map every S05 theorem assumption to the Twins vocabulary | `spec/vlsm_to_twins.md` | Task 1 | No use of full disclosure remains informal | M | Yes |
| 3 | Define accepted-message validity and exact Byzantine power | `spec/adversary_boundary.md` | Tasks 1–2 | Positive and negative message examples classify unambiguously | M | No |
| 4 | Specify toy locking protocol transition table | `spec/toy_locking.md` | Task 3 | Hand-derived safe and unsafe traces included | M | No |
| 5 | Define observation profiles and agreement oracle | `spec/observation_profiles.md` | Task 4 | Clone IDs erased and correct decisions preserved | S | Yes |
| 6 | Freeze JSONL trace schema | `spec/trace_schema.md` | Tasks 4–5 | Round-trip example and schema version | S | Yes |
| 7 | Implement accepted-message Byzantine generator | `byzantine.py` | Tasks 3–6 | Generates all tiny-bound hand examples and no rejected messages | M | No |
| 8 | Implement dynamic state-equivocation generator | `equivocation.py` | Tasks 4–6 | Reproduces S05-style copy examples in toy semantics | M | Yes after 6 |
| 9 | Implement fixed-`k` Twins generator | `twins_k.py` | Tasks 4–6 | Enforces cap and correct-code transitions | M | Yes after 6 |
| 10 | Implement canonicalization and symmetry | `canonical.py` | Tasks 5–6 | Idempotence and renaming tests pass | M | Yes |
| 11 | Implement explorer and exact language comparator | `explorer.py`, `language.py` | Tasks 7–10 | Complete tiny bound matches manual enumeration | L | No |
| 12 | Build unit, metamorphic and embedding tests | test suite | Tasks 7–11 | All stated invariants tested; reductions-off equivalence passes | M | Yes |
| 13 | Execute bounded pilot sweep | raw pilot results | Tasks 11–12 | Completion manifest or explicit resource-stop status | L | No |
| 14 | Implement witness minimizer and causal renderer | `minimize.py`, `render.py` | Task 13 | Decisive witness replayable and smaller than original when possible | M | Yes |
| 15 | Write GO, NO-GO or PIVOT decision memo | `results/pilot/decision.md` | Tasks 1–14 | Decision follows predeclared rules and cites exact evidence | M | No |

The first three tasks require no hidden conceptual decision beyond the specification in this package.

## 8. First three working sessions

### Session 1 — Source and novelty boundary

**Goal:** make the VLSM novelty kill and residual claim mechanically auditable.  
**Actions:** create source ledger, extract S04 conjecture and S05 theorem/assumptions, list exact differences between dynamic state copies and fixed-`k` harness.  
**Outputs:** `sources.json`, `vlsm_to_twins.md`, one-page residual theorem statement.  
**Acceptance:** another researcher can explain why original claim is rejected and what remains without reading the prior reports.

### Session 2 — Adversary and validity semantics

**Goal:** prevent asymmetric or circular fault models.  
**Actions:** write accepted/rejected message examples, define scheduler powers, clone lifecycle and observation erasure.  
**Outputs:** `adversary_boundary.md`, `observation_profiles.md`, trace examples.  
**Acceptance:** each example has one deterministic classification and the model separates valid equivocation from mutation.

### Session 3 — Minimal executable path

**Goal:** reach a state transition and observation through all three adversary models.  
**Actions:** implement types, toy protocol first round, one state-copy event, two-clone delivery split and safety projection.  
**Outputs:** initial modules and smoke tests.  
**Acceptance:** one configuration produces replayable traces for `AB`, `AE` and `AT(2)` with deterministic hashes.

## 9. Pre-mortem and risk register

Assume the project failed after several months. The following are the most likely causes.

| Risk | Probability | Damage | Early indicator | Prevention | Contingency | Gate closed |
|---|---|---|---|---|---|---|
| Original novelty collapse through S05 | Certain for original topic | Critical | General theorem already matches claim | Accept pivot and never defend original theorem | Study finite harness gap only | Gate 0 |
| Residual novelty collapse through refinement or chain cover | High | Critical | Proof becomes one paragraph after definitions | Search adjacent theory and formalize reduction before coding | Stop or pivot to concrete lifecycle separation | Gate 0 |
| Hidden prior art in S20 or dissertation | Medium-high | Critical | Similar terminology found in citations | Obtain full texts and expert citation review | Reframe only if independent claim remains | Gate 0 |
| Vacuous validator model | Medium | Critical | `Valid` accepts only correct-code messages with full proof | Include realistic protocol examples and ablations | Weaken or reject theorem | Gate 1 |
| Byzantine model too strong or too weak | High | High | `AB` trivially dominates or equals clones by definition | Explicit positive/negative messages and S05 mapping | Split validator and mutation results | Gate 1 |
| Wrong adversary model | Medium-high | High | Main mismatches only use malformed fields | Keep `AM` outside core and report boundary | Narrow to accepted-message theorem | Gate 3 |
| Non-identifiable mechanism | Medium | High | Same result explained by clone count, scheduler or snapshot | Factorial semantic ablations | Pivot to capability hierarchy | Gate 3–5 |
| No distinguishing witness | Medium | High | All completed unsafe traces use two branches | Diagnostic protocol family and proof-first analysis | Prove two-clone sufficiency or stop | Gate 3 |
| State-space explosion | High | High | First unsafe bound not completed | Symmetry, partial-order reduction, smaller semantics, SMT reserve | Publish proof/counterexample on narrower class | Gate 3–5 |
| Reduction unsoundness | Medium | Critical | Reduced and unreduced tiny languages differ | Preservation tests and independent canonicalizer | Disable reduction, shrink bound | Gate 3–6 |
| Implementation confound | Medium | High | Concrete adapter disagrees for undocumented reason | Keep formal core independent and replay normalized traces | Drop practical claim or publish conformance gap | Gate 5–6 |
| Abstraction gap to real BFT | High | High | Second protocol fails assumptions | Select models early and map assumptions explicitly | Restrict theorem class honestly | Gate 5 |
| Unbounded generalization from finite data | Medium | Critical | Manuscript language exceeds proof | Claim ledger and reviewer-style audit | Publish bounded separation only | Gate 6–8 |
| Dataset or workload bias | Low for exact core, medium for optional fuzzing | Medium | Random scenarios drive claims | Synthetic diagnostic cases and exact enumeration | Separate discovery from proof | Gate 5–6 |
| Unavailable external artifact | Medium | Medium | Repository fails to build at pinned commit | Gate 2 smoke builds and internal models | Omit adapter; use alternate S21/S22/S08 | Gate 2 |
| Toolchain drift | Medium | Medium | Lockfile no longer resolves | Archive wheels/source and container digest | Export standards-based lock or vendored minimal deps | Gate 2–7 |
| Z3 solver issue or unknown result | Medium if used | High | `unknown`, timeout or model replay failure | Optional only; explicit timeout and replay | Return to exact enumeration or audited release | Gate 4–6 |
| Coq proof scope explosion | High if attempted early | High | Weeks spent before theorem stable | Mechanize only after pilot and manual proof | Manual proof plus checker artifact | Gate 5 |
| No fixed clone cutoff | Medium | Not necessarily negative | `k_min` grows with witness depth | Treat as possible lower-bound theorem | Publish no-uniform-cutoff result | Gate 3–5 |
| Negative result not informative | Medium | High | Only “no bug found” or incomplete search | Predefine separation and necessary-condition outputs | Stop rather than overinterpret | Gate 3 |
| Excessive scope | High | High | More protocols, clients and tools added before pilot | Enforce gate dependencies | Remove integrations and return to toy theorem | Every gate |
| No publication audience | Medium | High | Result is too formal for testing and too tool-specific for formal methods | Venue-fit review after Gate 3 | Narrow contribution and target workshop/technical report | Gate 3 and 8 |
| Sensitive production vulnerability | Low | High ethical impact | Concrete replay triggers unknown safety bug | Local-only policy and disclosure plan | Coordinate privately, delay exploit details | Gate 5–8 |

## 10. Decision journal

- **D01:** The original audit recommendation is not accepted as truth; S05 is a novelty killer.
- **D02:** The study pivots from arbitrary Byzantine versus clones to abstract equivocation versus finite executable harness.
- **D03:** Safety only; liveness excluded.
- **D04:** Accepted-message validator adversary is primary; malformed mutation is comparator.
- **D05:** One Byzantine identity in pilot.
- **D06:** Exact explicit-state exploration is primary; SMT optional.
- **D07:** Python is chosen for model transparency, not performance leadership.
- **D08:** Production integration is conditional and off critical path.
- **D09:** No arbitrary effect-size or percentage threshold; decisions use exact inclusion and logical contribution rules.
- **D10:** Full implementation begins only after Gate 3 GO.
- **D11:** A direct chain-cover result is insufficient without a BFT-specific condition, bound or separation.
- **D12:** Two-clone sufficiency is an acceptable scientific result only if nontrivial, general and not already known.
- **D13:** Incomplete state-space search is labeled inconclusive.
- **D14:** Every decisive counterexample requires independent replay and minimization.
- **D15:** Negative production finding follows responsible disclosure.

## 11. Overall effort envelope

Conditional total after this report:

- Gate 0–3 to decision: **18–31 focused person-days**;
- Gate 4–7 after GO: **31–56 focused person-days**;
- manuscript Gate 8: **10–18 focused person-days**.

Total full route: **59–105 focused person-days**, with large uncertainty driven by proof and state-space complexity. These are effort ranges, not calendar promises.

## 12. Definition of reproducible completion

The project is reproducibly complete only when:

- source, tools and external repos are pinned;
- every result has a complete manifest;
- core commands work on a clean environment;
- exact bounds and incomplete cells are visible;
- every theorem assumption maps to executable semantics;
- every decisive witness replays;
- figures regenerate;
- licenses are documented;
- no live-system interaction occurred;
- artifact reviewer can reproduce the minimum publishable unit without private assistance.

## Реестр источников и проверяемых идентификаторов

Дата проверки веб-источников и состояния инструментов: 11 августа 2026 года.

| ID | Источник | Тип и статус | Идентификатор, артефакт и фактическая роль |
|---|---|---|---|
| S01 | `00_RESEARCH_BRIEF_BLOCKCHAIN_CS.md`, версия 2.0 | Локальный исходный бриф | SHA-256 `fa0ee734ff7f09690ee4e3e5b520d7a9d2d6485bef07b89e19128ba2dd5a660e`. Определяет область, ограничения, ресурсы, требования к вкладу, отрицательному результату и безопасности. |
| S02 | `Исследовательский анализ брифа.txt` | Локальный первый исследовательский проход | SHA-256 `723ac880390123aae20396d2bd8911c04560548ebda3dc3d5f69ba235f195b45`. Две загруженные копии имеют одно и то же имя и содержание; положительные оценки не использованы как доказательства. |
| S03 | `independent_audit_blockchain_topics_2026-08-11.md` | Локальный независимый аудит | SHA-256 `b541b2fdfa1470caaf0a2dcd62a7b97db9257232637460a25e787f2346a70742`. Источник выбранного кандидата, но не источник истины о новизне. |
| S04 | Shehar Bano, Alberto Sonnino, Andrey Chursin, Dmitri Perelman, Zekun Li, Avery Ching, Dahlia Malkhi. *Twins: BFT Systems Made Robust*. OPODIS 2021 | Рецензированная конференционная статья | DOI `10.4230/LIPIcs.OPODIS.2021.7`; arXiv `2004.10617`. Вводит correct-code clones с общей identity, оставляет строгую теорию coverage открытой и формулирует conjecture для deterministic full-disclosure protocols. Артефакты заявлены открытыми; статья CC-BY 4.0. |
| S05 | Vlad Zamfir, Mihai Calancea, Denisa Diaconescu, Wojciech Kołowski, Brandon Moore, Karl Palmskog, Traian Florin Șerbănuță, Michael Stay, Dafina Trufaș, Jan Tušil. *Validating Labelled State Transition and Message Production Systems: A Theory for Modelling Faulty Distributed Systems* | Препринт с машинно проверенной формализацией | arXiv `2202.12662v4`, 15 декабря 2023 года. Определяет validators, state/message equivocation и доказывает совпадение traces, наблюдаемых honest validators, под Byzantine и equivocation behavior при указанных предположениях. Все результаты проверены в Coq. Это главный novelty-killer исходного кандидата. |
| S06 | `runtimeverification/vlsm` | Открытый Coq-репозиторий | Лицензия BSD-3-Clause; Coq 8.16 и новее; рекомендован Coq 8.18; зависимости `coq-stdpp` 1.9 и новее, Itauto, Equations. Содержит формализацию S05. Commit hash должен быть зафиксирован в Gate 2. |
| S07 | Levin N. Winter, Florena Buse, Daan de Graaf, Klaus von Gleissenthall, Burcu Kulahcioglu Ozkan. *Randomized Testing of Byzantine Fault Tolerant Algorithms* | Рецензированная статья PACMPL OOPSLA1 2023 | DOI `10.1145/3586053`. Вводит ByzzFuzz; показывает fault executions с future-round field mutation, которые обычный Twins не порождает. Эти случаи не автоматически принадлежат validator-only модели S05. |
| S08 | João Miguel Louro Neto, Burcu Kulahcioglu Ozkan. *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms* | Рецензированная tool paper, FMBC 2025 | DOI `10.4230/OASIcs.FMBC.2025.13`. Описывает ByzzBench, контролируемую среду и начальные реализации random tester, ByzzFuzz и Twins. Репозиторий `joaomlneto/byzzbench`, лицензия MIT; commit hash фиксируется в Gate 2. |
| S09 | Cezara Drăgoi, Constantin Enea, Burcu Kulahcioglu Ozkan, Rupak Majumdar, Filip Nikšić. *Testing Consensus Implementations Using Communication Closure* | Рецензированная статья PACMPL OOPSLA 2020 | DOI `10.1145/3428278`. Ближайший prior art по schedule reduction и представительным executions, но не по эквивалентности двух Byzantine fault models. |
| S10 | Ognjen Marić, Christoph Sprenger, David Basin. *Cutoff Bounds for Consensus Algorithms* | Рецензированная статья CAV 2017 | DOI `10.1007/978-3-319-63390-9_12`. Ближайший prior art по process cutoffs; не даёт clone cutoff для Twins. |
| S11 | Igor Konnov, Marijana Lazić, Helmut Veith, Josef Widder. *A Short Counterexample Property for Safety and Liveness Verification of Fault-tolerant Distributed Algorithms* | Рецензированная статья POPL 2017 | DOI `10.1145/3009837.3009860`. Даёт bounded-witness reasoning для класса fault-tolerant algorithms, но не реализацию Byzantine witness finite-clone adversary. |
| S12 | Nathalie Bertrand, Vincent Gramoli, Igor Konnov, Marijana Lazić, Pierre Tholoniat, Josef Widder. *Holistic Verification of Blockchain Consensus* | Рецензированная статья DISC 2022 | DOI `10.4230/LIPIcs.DISC.2022.10`. Систематическая формальная проверка blockchain consensus; полезна для abstraction strategy, но объектом является protocol safety, а не completeness fault injector. |
| S13 | Ruijie Meng, George Pîrlea, Abhik Roychoudhury, Ilya Sergey. *Greybox Fuzzing of Distributed Systems* | Рецензированная статья ACM CCS 2023 | DOI `10.1145/3576915.3623097`. MALLORY использует causal behavior summaries для guided fault injection. Угрожает любому claim о новом causal coverage metric, но не решает trace-language inclusion Twins. |
| S14 | Peiyao Sheng, Gerui Wang, Kartik Nayak, Sreeram Kannan, Pramod Viswanath. *BFT Protocol Forensics* | Рецензированная статья ACM CCS 2021 | DOI `10.1145/3460120.3484566`. Формализует forensic evidence после нарушений BFT. Релевантна observations и evidence, но не clone expressiveness. |
| S15 | João Soares, Ricardo Fernandez, Miguel Silva, Tadeu Freitas, Rolando Martins. *ZERMIA: A Fault Injector Framework for Testing Byzantine Fault Tolerant Protocols* | Рецензированная глава, NSS 2021 | DOI `10.1007/978-3-030-92708-0_3`. Инженерный prior art по fault injection; не даёт coverage theorem. |
| S16 | Mads Frederik Madsen, Søren Debois. *On the Subject of Non-Equivocation: Defining Non-Equivocation in Synchronous Agreement Systems* | Рецензированная статья PODC 2020 | DOI `10.1145/3382734.3405731`. Уточняет понятие non-equivocation и границы fault assumptions; соседняя теория, не finite-clone testing theorem. |
| S17 | Prince Mahajan, Lorenzo Alvisi, Mike Dahlin. *Consistency, Availability, and Convergence* | Технический отчёт UTCS TR-11-22, 2011 | Соседний prior art: Byzantine inconsistencies представлены через forked или virtual views. Не рецензирован как основная статья по Twins; угрожает claims о самой идее виртуальных копий и fork counting. |
| S18 | Martín Abadi, Leslie Lamport. *The Existence of Refinement Mappings* | Рецензированная теоретическая статья, TCS 1991 | DOI `10.1016/0304-3975(91)90224-P`. Соседняя дисциплина: refinement и implementation mapping. Требует доказать соответствие abstract equivocation и concrete harness как refinement, а не только сравнить outputs. |
| S19 | Sebastião Amaro, Pedro Fonseca, Miguel Matos. *Rose: Reproducing External-Fault-Induced Failures in Distributed Systems with Lightweight Instrumentation* | Рецензированная статья EuroSys 2026 | DOI `10.1145/3767295.3803625`; открытый artifact DOI `10.5281/zenodo.18862553`, размер опубликованного архива 812.6 MB. Ближайший новый engineering prior art по воспроизведению fault-induced traces; не формализует Twins completeness. |
| S20 | Yu Liang, Yu Gao, Wensheng Dou, Wenhan Feng, Zheng Qin, Zhen Tang, Hui Li, Wen Wang, Jun Wei. *Node-Centric Systematic Testing for Distributed Systems* | Рецензированная статья ACM TOSEM 2026 | DOI `10.1145/3831368`; online publication 17 июля 2026 года. Официальные metadata и abstract доступны; полный текст через открытый источник не подтверждён. Работа вводит node-centric equivalence и NodeExplore, поэтому угрожает claims о новом behavior-preserving reduction, но не подтверждает finite-clone theorem. |
| S21 | `asonnino/twins-simulator` | Открытый research artifact | Apache-2.0; Streamlet и Fast-HotStuff; documented commands `pip install -e .`, `pytest`, `python scripts/twins_executor.py scripts/test_scenarios.json`. Research-only, 20 commits на дату проверки. Использовать только для внешней валидации. |
| S22 | `relab/hotstuff` | Открытый systems artifact | MIT; Go не ниже 1.18; включает Twins safety testing и три HotStuff variants. На дату проверки 1,849 commits. Использовать после абстрактного пилота, не как trusted reference semantics. |
| S23 | Python 3.14.7 | Официальный runtime | Выпуск 5 августа 2026 года. Основной язык explicit-state pilot; точная patch version фиксируется `.python-version` и environment report. |
| S24 | Hypothesis 6.165.3 | Официальный пакет PyPI | Выпущен 11 августа 2026 года; MPL-2.0; Python 3.10 и новее; source archive SHA-256 `687c5abb1a9c11478577c2cf18685c0eb82150d278477d3e14da290a1ef2a098`. Используется только для генеративных regression tests, не как научный oracle. |
| S25 | pytest 9.1.1 | Официальная документация | Выпущен 19 июня 2026 года. Используется для unit, metamorphic и regression tests. |
| S26 | uv | Официальная документация и репозиторий Astral | Лицензия Apache-2.0 OR MIT; поддерживает universal lockfile; проверенные команды `uv init`, `uv add`, `uv lock`, `uv sync`, `uv run`. Точная версия бинарника фиксируется в environment report. |
| S27 | Z3 5.0.0 | Официальный релиз GitHub | Выпущен 17 июля 2026 года; MIT. Резервный symbolic backend; не входит в минимальный пилот и подключается только при доказанной необходимости. |
| S28 | Nancy A. Lynch, Mark R. Tuttle. *An Introduction to Input/Output Automata* | Классическая работа по distributed-system semantics | CWI Quarterly 2(3), 1989. Определяет compositional state-machine view и external traces; соседняя основа для observation and simulation relation. |

## Ограничение поискового вывода

Фраза «источник не найден» означает только отсутствие результата в обследованных англоязычных научных базах, официальных репозиториях, citation searches и доступном инженерном prior art на 11 августа 2026 года. Она не доказывает абсолютного отсутствия работы, unpublished result, dissertation lemma, private engineering note или новой публикации после даты поиска.
