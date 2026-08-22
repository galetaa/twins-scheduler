# Глубокая проверка, формализация и подготовка темы Twins к реализации

**Дата:** 11 августа 2026 года  
**Роль отчёта:** независимый Research Specification Lead audit  
**Исходный бриф:** S01  
**Первый проход:** S02  
**Независимый аудит тем:** S03  
**Выбранный кандидат:** основной и единственный кандидат S03  
**Итоговый вердикт:** **ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT**

---

# Раздел 1. Executive decision

## Выбранная тема

Исходная тема аудита:

**«Формальные границы полноты метода Twins для safety-тестирования BFT-протоколов блокчейн-систем: детерминированные протоколы с полным раскрытием причинной истории»**.

После независимой проверки допустима только минимальная переработка:

**«Границы полноты конечноклонового Twins-тестирования валидируемых BFT-протоколов: соответствие между абстрактной state equivocation и исполнимой инъекцией отказов»**.

English title:

**“Completeness Boundaries of Finite-Clone Twins Testing for Validated BFT Protocols: Relating Abstract State Equivocation to Executable Fault Injection.”**

## Итоговый статус

**ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT.**

## Краткое основание

S04 действительно оставляет rigorous theory of Twins coverage открытой и формулирует conjecture для deterministic protocols with full disclosure. Но S05 уже вводит более общую formal semantics validators and state equivocation, разрешает динамическое копирование корректных состояний и доказывает equality traces, наблюдаемых honest validators, под Byzantine and equivocation behavior при своих assumptions. Следовательно, исходный центральный novelty claim — свести arbitrary Byzantine behavior к correct-code clones through causal disclosure — уже существует в более общей и Coq-checked форме.

Научный остаток возможен только на уровне разрыва между:

- abstract dynamic state equivocation S05;
- concrete Twins harness with fixed active clone cap `k`;
- explicit snapshot, lifecycle and scheduler capabilities;
- bounded safety observation language;
- minimum clone number or separation witness.

Даже этот остаток пока не защищён: theorem может оказаться прямым refinement mapping, minimum chain cover or trivial one-clone-per-history construction.

## Главный novelty claim после pivot

В обследованных источниках не найден theorem, который одновременно определяет production-style fixed-`k` Twins semantics, связывает её с abstract dynamic state equivocation, характеризует minimum clone number for bounded safety observations and isolates lifecycle/scheduler limitations. Допустимый claim ограничен этим bridge; он не включает общий Byzantine-to-equivocation theorem.

## Главный блокирующий риск

Residual result collapses to known theory:

- S05 already supplies abstract equivalence;
- S18/S28 supply generic refinement language;
- classic chain-cover or width theory may determine minimum clones directly;
- S10/S11 may make bounded cutoff aspect routine;
- S20 full text remains an unresolved 2026 threat.

## Следующий необратимый шаг

Первый действительно необратимый commitment — переход к full artifact and proof route after a Gate 3 GO decision. До него все действия reversible: source audit, definitions and blocking pilot.

## Можно ли начинать реализацию немедленно

**Полную реализацию — нет.**

**Можно немедленно начать:** source ledger, VLSM-to-Twins assumption mapping, executable definitions, toy protocol and blocking exact pilot. Эти задачи не требуют дополнительных концептуальных решений.

---

# Раздел 2. Почему выбран именно этот финалист

Отдельная карточка кандидата не была приложена. S03 после независимого kill test отклонил все пять исходных тем S02 и оставил одну replacement theme — formal completeness boundaries of Twins. Поэтому full gate review нескольких равноправных финалистов не требовался: только этот кандидат получил рекомендацию аудита.

При этом кандидат не был принят автоматически. Независимая проверка дала более строгий результат, чем S03: VLSM S05 является прямым novelty killer исходного theorem. Кандидат сохраняется только после существенного pivot, потому что у него остаются три преимущества, соответствующие S01:

1. protocol-level formal question rather than benchmark or engineering tool;
2. exact falsification on one workstation with synthetic traces;
3. meaningful negative result as separation theorem, no fixed cutoff or necessary harness capability.

## Отложенные варианты

| Вариант | Почему не выбран для этого прохода |
|---|---|
| Finality stall diagnosability | Общий mechanism covered by diagnosability, failure detectors, forensics and accountable liveness; novelty depended on a new evidence-minimality theorem not yet found. |
| Rollup temporal composition | Local-to-global liveness gap is standard compositional reasoning; no nontrivial necessary-and-sufficient property fixed. |
| Causal differential oracle | Mature partial-order and causal testing techniques; likely tool-specific improvement, with unresolved SpecTrum overlap. |
| Parallel execution observability | General parameterized observable-equivalence theory already exists; proposed tuple is an instantiation. |
| Correlation-robust DAS | Needs specialized crypto audit; closest works already connect formal DAS and networking; dangerous source not fully audited. |

They are not implementation backups. Returning to one requires a new independent search.

---

# Раздел 3. Нормализованная research specification

## Окончательное рабочее название

**RU:** «Границы полноты конечноклонового Twins-тестирования валидируемых BFT-протоколов: соответствие между абстрактной state equivocation и исполнимой инъекцией отказов».

**EN:** “Completeness Boundaries of Finite-Clone Twins Testing for Validated BFT Protocols: Relating Abstract State Equivocation to Executable Fault Injection.”

## Исследуемый класс систем

Deterministic authenticated validator-style BFT consensus protocols with explicit message validation, replayable choices, finite safety witnesses and asynchronous network semantics for safety.

## Научная проблема

Abstract state equivocation may dynamically copy correct states without a fixed cap. A real Twins harness runs a finite number of correct-code clones sharing one identity and may restrict when clones start, snapshot or receive messages. It is unknown whether fixed-`k` executable semantics preserves every bounded unsafe observation of the abstract model and what controls minimum `k`.

## Scope

Included:

- agreement safety only;
- finite traces;
- one Byzantine identity in pilot;
- deterministic authenticated validator protocols;
- exact explicit-state exploration;
- accepted-message Byzantine, dynamic equivocation and finite-clone models;
- clone lifecycle and scheduler ablations;
- toy locking protocol plus one independent model after GO.

## Non-goals

Excluded:

- liveness and timing guarantees;
- malformed packet or arbitrary memory corruption;
- cryptographic break;
- mainnet or public-testnet attacks;
- performance as scientific contribution;
- a new consensus protocol or blockchain platform;
- ML;
- token economics and trading;
- broad production-client portfolio before theorem.

## Основной исследовательский вопрос

For deterministic authenticated validator BFT protocols and a concrete Twins harness with at most `k` active clones per faulty identity, under what lifecycle and scheduling conditions does the harness preserve all bounded safety-violating observations of abstract state equivocation, and what is minimum `k`?

## Основной тезис

При условиях U — deterministic replayable transitions, validated messages, explicit causal evidence, asynchronous safety network and correct-node observation — mechanism M maps each mutually incompatible faulty causal history to one correct-code clone. It predicts P: every bounded unsafe abstract-equivocation observation is executable with clone count at least a structural bound. Alternative A predicts Q: two clones suffice, no finite profile-independent bound exists, or the number is ordinary chain cover. Observation R — a valid witness whose exact `k_min` violates the proposed bound or no strict hierarchy where width exceeds two — refutes the strong mechanism.

## Предполагаемый механизм

1. Use S05 only for Byzantine-to-equivocation abstraction.
2. Decompose one abstract equivocation witness into internally consistent correct-code histories.
3. Assign incompatible histories to separate clones.
4. Construct selective deliveries preserving causal inputs.
5. Compare correct-node locks, certificates and decisions.
6. Failure yields a separation witness and necessary harness capability.

## Ближайшие альтернативы

- two-clone sufficiency for restricted locking protocols;
- ordinary minimum chain cover explains `k_min`;
- lifecycle and snapshot ability, not clone count, determines expressiveness;
- only mutation-model differences exist outside validator semantics.

## Тип вклада

Only theorem, bound, impossibility or separation is acceptable. A new harness, more scenarios or more bugs is not the central contribution.

## Единица анализа

A bounded unsafe observation witness: finite causal trace plus projected correct-replica states and incompatible decisions.

## Research artifact

Dual-adversary exact checker generating and comparing `AB`, `AE` and `AT(k)` languages, computing `k_min` and minimizing unmatched traces.

---

# Раздел 4. Claim and evidence ledger

| Claim | Type | Required evidence | Current status | Falsifier | Novelty depends on it |
|---|---|---|---|---|---|
| C1. Topic must be formal, protocol-level, local and negative-result valuable | Brief fact | Trace to S01 | Confirmed | Scope violates S01 | No |
| C2. Twins uses correct-code shared-identity clones | Known fact | S04 paper and artifact | Confirmed | S04 mechanism differs | No |
| C3. Twins leaves rigorous coverage theory open | Literature fact | Exact future-work text S04 | Confirmed | Published resolution predates search | No |
| C4. VLSM equates Byzantine and equivocation effects for validators under assumptions | Literature fact | S05 theorem and Coq artifact | Confirmed | Theorem has materially different scope than mapped | **Kills original novelty** |
| C5. Fixed-`k` executable Twins is stricter than dynamic state equivocation | New formal hypothesis | Semantic profiles and separating or equivalence proof | Conditional | Machines equivalent by direct mapping without nontrivial condition | Yes |
| C6. Message mutation is stronger than validator-only clone behavior | Literature/model inference | S07 and `Valid` membership examples | Confirmed conceptually | Mutations are valid correct-history outputs | No |
| C7. Every concrete finite-clone trace embeds in abstract equivocation | Formal obligation | T0 proof and exhaustive tiny checks | Unproved | Concrete trace absent from `AE` | Infrastructure |
| C8. Minimum clone number has nontrivial structural characterization | New central hypothesis | Theorem or exact counterexample-resistant invariant | Unproved | Valid witness violates characterization | **Yes** |
| C9. Lifecycle/scheduler restrictions create formal expressiveness boundaries | New hypothesis | Paired profile comparison and theorem | Unproved | Profiles equivalent under all relevant traces and proof | Yes or pivot |
| C10. Two clones may suffice for restricted class | Nearest alternative | Theorem or exhaustive induction basis | Unproved | Valid witness requires more than two | No, but determines route |
| C11. Exact bounded language comparison distinguishes claims | Measurement assumption | Complete enumeration, canonicalization tests, independent oracle | Conditional | Incomplete search or projection conflation | No |
| C12. Mutation-only mismatch does not refute validator-scoped claim | Model inference | Explicit `Valid` boundary | Confirmed conceptually | Protocol accepts mutation under agreed validator model | No |
| C13. Negative separation remains scientific | Methodological claim | Necessary condition, lower bound or counterexample family | Conditional | Mismatch is coding error or arbitrary harness quirk | Yes |
| C14. Pilot needs no mainnet or historical data | Engineering fact | Tool and resource audit | Confirmed | Hidden production dependency appears | No |
| C15. Full implementation waits for Gate 3 | Decision rule | Roadmap compliance | Fixed | Not applicable | No |

The only defensible novelty can rest on C5, C8, C9 and C13. C2–C4 are prior art.

---

# Раздел 5. Deep prior-art review

## Closest-work map

| Role | Closest source | Audit conclusion |
|---|---|---|
| Problem | S04 Twins | Defines practical method and open coverage question, but not formal theorem. |
| Mechanism | S05 VLSM | Dynamic correct-state copies and equivalence already formalized; destroys original claim. |
| Formal model | S18 refinement mappings plus S28 I/O automata | Trace inclusion and implementation relation are standard; must add nontrivial BFT-specific result. |
| Experimental design | S08 ByzzBench | Controlled BFT testing infrastructure already exists; new benchmark is not novel. |
| Practical artifact | S22 relab/hotstuff | Includes Twins safety testing; another HotStuff implementation is not contribution. |
| Neighbor discipline | Poset chain cover and cutoff theory S10/S11 | May trivialize minimum clone result. |

## Threat-ranked sources

1. **S05 VLSM — destroying threat.** It already establishes the abstract reduction central to the original topic.
2. **S04 Twins — source of method and conjecture.** Open question must be reinterpreted in light of S05.
3. **S18/S28 — critical adjacent theory.** A bridge theorem must exceed generic refinement.
4. **S07 ByzzFuzz — critical fault-model boundary.** It demonstrates mutations that correct-code clones may not generate.
5. **S09–S11 — schedule, cutoff and bounded-witness theory.** They threaten novelty of finite verification aspects.
6. **S08, S21, S22 — practical artifact threats.** They remove engineering novelty.
7. **S20 — unresolved 2026 threat.** Full text required before publication claim.

## Novelty kill test summary

- Same original combination already exists more generally: **yes, S05**.
- Elements individually known: **yes**.
- Original combination non-obvious after S05: **no**.
- Residual new prediction: potentially fixed-`k` hierarchy or lifecycle separation.
- Scientific meaning: only if nontrivial and class-level.
- Risk of new application of known method: high.
- Engineering idea already implemented: yes.
- Network/client-only novelty: forbidden.
- Contribution without “first applied”: possible only as theorem/bound/separation.
- Minimum evidence: strict hierarchy or necessary/sufficient realization condition on two protocol models, not direct chain cover.

## Final novelty delta

Nearest work establishes X and Y: practical shared-identity clones and abstract Byzantine/equivocation equivalence for validator systems. The surveyed sources do not show a result simultaneously defining a fixed-`k` executable harness, relating it to dynamic state equivocation, determining minimum clone count and isolating lifecycle/scheduler restrictions. The proposed contribution is limited to C5, C8, C9 and C13. This statement is date-, database-, terminology- and access-limited and remains blocked by Gate 0.

---

# Раздел 6. Формальная модель

## Core specification

`P = (I, S, S0, M, Delta, Valid, Obs)`.

- `I`: protocol identities;
- `S`: local states;
- `S0`: initial states;
- `M`: authenticated messages;
- `Delta`: deterministic transition function after explicit choices;
- `Valid`: accepted-message predicate;
- `Obs`: correct-node observation projection.

## Participants and roles

Correct replicas, one faulty identity in pilot, multiple physical clones sharing its protocol identity, abstract adversary and scheduler.

## Events

Initialization, local step, send, deliver, drop, duplicate state, start clone, stop clone and decide.

## Network and synchrony

Asynchronous for safety; arbitrary delay, reorder and selective drop; no fairness, latency bound or GST. Therefore no liveness claim.

## Cryptographic and trust assumptions

Ideal authentication, no correct-key forgery, clones share the faulty identity key, hashes/signatures treated abstractly. `Valid`, observation and trace checker are trusted specification components.

## Adversary models

- `AB`: arbitrary accepted sender-faulty messages, not arbitrary bytes;
- `AE`: unbounded finite dynamic correct-state copies over each finite trace;
- `AT(k)`: at most `k` active correct-code clones with declared lifecycle;
- `AM`: optional mutation comparator outside main theorem.

## Safety

No two correct replicas decide incompatible values.

## Completeness

`AT(k)` is bounded safety-complete for `AE` when every canonical unsafe correct-node observation of `AE` within bound is also reachable under `AT(k)`.

## Minimum clone number

`k_min(w,h)` is the smallest clone cap realizing witness observation `w` under harness profile `h`, or unknown/infinite only under explicitly proved conditions.

## Strong and weak claims

- Strong: `k_min` equals a canonical incompatibility width.
- Weak: every finite witness has some computable finite clone upper bound.
- Alternative: two clones suffice.
- Alternative: no profile-independent bound.
- Kill alternative: ordinary chain cover is the entire result.

## Main proof obligations

- concrete clones embed in abstract equivocation;
- histories admit correct-code chain decomposition;
- scheduler realizes the decomposition;
- required states are available under lifecycle profile;
- incompatible histories require separate clones;
- canonicalization preserves language and `k_min`;
- bounded results are not overgeneralized.

## Counterexample families

Hidden randomness, unverifiable state claims, merging incompatible histories, snapshot-dependent late branch, more-than-two branches and false mismatch from canonicalization.

---

# Раздел 7. Различающие предсказания и falsification map

## Mechanism chain

Validator constraints → abstract state branches → finite correct-code clones → selective causal delivery → same correct-node observation → coverage statement or separation.

## Four mandatory predictions

1. Main: a valid witness requires more than two clones or yields a nontrivial cutoff statement.
2. Boundary: snapshot lifecycle changes `k_min` or realizability for late branching.
3. Adversarial: weakening validity creates mutation witnesses outside every correct-code clone language.
4. Failure: causal-width equality fails or collapses to generic chain cover.

## Falsifiers

- valid witness violates proposed bound;
- no strict hierarchy despite structural width above two;
- dynamic snapshots cannot realize a finite valid witness;
- mismatch disappears after canonicalizer correction;
- exact prior art proves same result;
- result depends only on malformed messages;
- theorem becomes definitional after full-disclosure definition.

## Value of a false hypothesis

A false strong hypothesis can establish no fixed cutoff, a required snapshot capability, a separation between valid equivocation and mutation, or a minimal blind spot of concrete Twins. Thus the negative result remains scientific.

---

# Раздел 8. Минимальный решающий пилот

## Pilot

**BP-TWINS-FC-01:** four replicas, one faulty identity, binary values, deterministic two-phase locking protocol, exact bounded exploration.

## Models compared

- accepted-message Byzantine `AB`;
- dynamic equivocation `AE`;
- finite clones `AT(k)` for increasing `k`;
- optional mutation comparator.

## Baselines

`AE`, one clone, two clones and one clone per discovered history upper bound.

## Variables

Independent: model, `k`, lifecycle, bound, scheduler and semantic ablations.  
Dependent: exact unsafe languages, set differences, `k_min`, causal predictors and minimized witnesses.

## Decision thresholds

No arbitrary percentage. GO requires nontrivial exact hierarchy, invariant, lower bound or separation and no equivalent prior art. NO-GO follows from S05 restatement, direct chain cover, trivial two-clone result without general theorem or mutation-only difference. PIVOT follows when lifecycle rather than clone count is the meaningful boundary.

## State-space rule

Start at minimum bound capable of lock and decision, increase to first unsafe `AE` witness, complete exact enumeration at that bound and one larger bound if resources permit. Resource stop means inconclusive, not support.

## Expected effort

7–12 focused person-days after Gates 0–2.

## Exact outputs

Configuration, protocol and adversary modules, tests, state-space summary, language matrix, unmatched traces, `k_min` table, decision memo, environment and checksum manifest.

---

# Раздел 9. Полный исследовательский дизайн

## Primary strategy

Formal trace refinement or separation theorem supported by exact explicit-state model checking.

## Reserve strategy

Counterexample-first capability hierarchy and concrete harness conformance if a general positive theorem fails.

## Experiments

- E0 definitions and non-vacuity;
- E1 `AB` versus `AE` sanity;
- E2 fixed-`k` hierarchy;
- E3 causal-width characterization;
- E4 semantic assumptions ablations;
- E5 lifecycle and scheduler boundary;
- E6 cross-protocol validation;
- E7 concrete harness conformance;
- E8 parameter sensitivity;
- E9 counterexample minimization and regression;
- E10 proof or mechanization.

## Controls

Same protocol, validity, scheduler powers, observation and bounds; reductions-off tiny checks; independent safety oracle; identity and value symmetry; mutation model kept separate.

## Statistical treatment

Core is exact enumeration, so no p-values, confidence intervals or independence assumptions. Optional randomized fuzzing is reported separately and cannot establish completeness.

## Formal-method details

Executable Python LTS, explicit bounds, symmetry and verified partial-order reduction, optional Z3 only with model replay, optional Coq after theorem stability.

---

# Раздел 10. Implementation specification

## Purpose

Deterministic dual-adversary exact checker, not a blockchain platform.

## Components

Protocol semantics, adversary models, explorer, canonicalization, oracles, causal analysis and optional external adapters.

## Formats

TOML configuration, JSONL traces, JSON manifests, CSV matrices, Markdown decision reports, DOT causal graphs and optional Coq sources.

## Technical stack

- Python 3.14.7;
- uv with committed lockfile;
- pytest 9.1.1;
- Hypothesis 6.165.3 for software tests only;
- optional Z3 5.0.0 with timeouts and replay;
- optional VLSM Coq repository;
- external validation via twins-simulator, relab/hotstuff or ByzzBench.

## Trusted computing base

Protocol transition, `Valid`, adversary semantics, canonicalizer/reductions, observation, safety oracle and language comparator.

## Vertical slice

Config → toy protocol → `AE` and `AT(2)` exploration → safety projection → exact language difference → decision report.

## Repository

Separate directories for specification, source, protocols, adversaries, experiments, configurations, raw/processed results, proof, tests, figures, containers, documentation and reproduction scripts.

---

# Раздел 11. Resource and reproducibility plan

## Availability

All mandatory resources are open or local. No archive node, public RPC, cloud, token or private data is required.

## Pinning

SHA-256 for input files; DOI/arXiv version for papers; commit hashes for repositories; Python patch version; uv binary version; lockfile; optional Coq opam export; optional solver asset checksum.

## Reproduction

- deterministic search order;
- immutable configurations;
- explicit complete/incomplete status;
- raw trace replay;
- generated figures from scripts;
- hardware report;
- minimal commands using uv;
- container as secondary path;
- clean-machine reproduction before release.

## Licensing

VLSM BSD-3-Clause, twins-simulator Apache-2.0, relab/hotstuff and ByzzBench MIT, uv Apache-2.0 OR MIT, pytest MIT, Hypothesis MPL-2.0 and Z3 MIT. Exact third-party notices are preserved.

---

# Раздел 12. Roadmap и backlog

## Gates and effort

| Gate | Outcome | Effort |
|---|---|---|
| G0 novelty delta | Exact residual claim or stop | 4–7 days |
| G1 formal model | Executable definitions and proof obligations | 5–8 days |
| G2 tools/data | Pinned offline-capable environment | 2–4 days |
| G3 blocking pilot | GO, NO-GO or PIVOT | 7–12 days |
| G4 main artifact | Stable research repository | 10–16 days |
| G5 proofs/experiments | Claim-complete evidence | 12–25 days |
| G6 validity | Robustness and threat closure | 5–8 days |
| G7 reproducible artifact | Clean-machine release | 4–7 days |
| G8 paper | Submission-ready conditional package | 10–18 days |

Critical path: G0 → G1 → G3 → theorem/counterexample route → G5 → G6 → G7 → G8.

## First fifteen tasks

1. Source ledger and hashes.
2. VLSM-to-Twins assumption map.
3. Accepted-message validity and adversary boundary.
4. Toy protocol transition table.
5. Observation profiles and safety oracle.
6. Trace schema.
7. `AB` generator.
8. `AE` generator.
9. `AT(k)` generator.
10. Canonicalization and symmetry.
11. Explorer and language comparator.
12. Tests and tiny-bound cross-checks.
13. Exact pilot sweep.
14. Witness minimizer and causal renderer.
15. Decision memo.

## First three sessions

- Session 1: source and novelty boundary.
- Session 2: adversary and validity semantics.
- Session 3: one end-to-end trace through all models.

---

# Раздел 13. Риски, безопасность и disclosure

## Top risks

- residual novelty collapse;
- vacuous validator class;
- asymmetric adversary power;
- chain-cover triviality;
- no distinguishing witness;
- state explosion;
- unsound reduction;
- toy-to-real abstraction gap;
- unavailable external artifact;
- hidden 2026 prior art;
- unbounded overclaim;
- publication audience mismatch;
- proof-assistant scope explosion;
- non-informative negative result;
- sensitive implementation finding.

Each risk has gate, early indicator, prevention and contingency in file 07.

## Safe policy

All experiments local and synthetic. No mainnet, assets, external keys, unauthorized access, DoS, spam, front-running or market manipulation.

## Disclosure

A concrete unknown safety bug triggers private maintainer notification, preservation of minimized local evidence, withholding of immediately exploitable operational details and coordinated release. The abstract coverage result alone is not automatically a vulnerability.

---

# Раздел 14. Publication package

## Audience

Formal methods, distributed systems, BFT testing and dependable computing. Blockchain specificity is context, not novelty.

## Contribution statement

1. Operational relation between dynamic state equivocation and finite-clone harness.
2. Nontrivial bound, separation or capability theorem.
3. Reproducible exact checker and cross-protocol validation.

## Minimum publishable result

Either a nontrivial theorem with two-model validation or a minimized separation family with necessary-condition analysis. Pilot equality alone is insufficient.

## Stretch

Coq mechanization, fixed cutoff, snapshot-capability theorem, concrete HotStuff conformance or scenario synthesis from abstract witnesses.

## Reviewer 2 core objections

VLSM already solves it; generic refinement; chain-cover tautology; two clones suffice; weakened adversary; toy protocol; bounded evidence; observation hides differences; scheduler too strong; concrete harness mismatch; ByzzFuzz already proves incompleteness; hidden prior art.

## Required figures and tables

Fault-model matrix, assumptions, prior-art map, language lattices, `k_min` table, ablations, cross-protocol mapping, decisive causal DAG and artifact manifest.

## Forbidden claims

No universal Twins completeness, no first formal equivocation model, no unbounded conclusion from bounded checking, no all-BFT two-clone claim, no production verification without adapter, no guaranteed venue or publication.

---

# Раздел 15. Definition of Ready

| Readiness criterion | Status | Evidence | Blocking action for FAIL or UNKNOWN |
|---|---|---|---|
| 1. Scientific problem unambiguous | PASS after pivot | Fixed-`k` realization versus dynamic state equivocation | None |
| 2. Thesis decomposed into atomic claims | PASS | C1–C15 ledger | None |
| 3. Closest prior art and defensible novelty delta | **FAIL for original; UNKNOWN for residual** | S05 kills original; chain-cover/refinement and S20 unresolved | Complete Gate 0, full S20 review and adjacent-theory reduction test |
| 4. Scope and non-goals exact | PASS | Safety-only, finite, validator and local scope | None |
| 5. System, roles, states, events and adversary model | PASS | `03_FORMAL_MODEL.md` | None |
| 6. Properties, hypotheses and alternatives | PASS | Hstrong, Hweak, H2–H5 | None |
| 7. Distinguishing test exists | PASS | Exact unsafe-language inclusion and `k_min` | None |
| 8. Explicit falsifier | PASS | Valid unmatched witness or bound violation | None |
| 9. Minimum decisive pilot | PASS | BP-TWINS-FC-01 | None |
| 10. Data, code, tools and compute available | PASS | Open/local registry and one-workstation design | None |
| 11. Artifact architecture defined | PASS as specification | Components, interfaces, formats and TCB fixed | Implement only vertical slice after Gate 1 |
| 12. Reproducible formal/experimental plan | PASS | E0–E10 and reproducibility contract | None |
| 13. GO, NO-GO and PIVOT criteria | PASS | Logical exact decision rules | None |
| 14. Negative result retains value | PASS | Separation, no cutoff or necessary capability | None |
| 15. No trading, financial risk or live-network effect | PASS | Local-only safe policy | None |
| 16. First tasks start without conceptual decisions | PASS | Backlog tasks 1–3 and three sessions | None |

## Repeated final verdict

**ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT.**

The source candidate is not ready for implementation because its central novelty claim is already covered more generally by S05. The repaired finite-clone candidate is ready only for Gate 0–3 specification and blocking pilot. It cannot receive “ГОТОВО ПОСЛЕ БЛОКИРУЮЩЕГО ПИЛОТА” yet because novelty itself, not only empirical feasibility, remains unresolved.

---

# Раздел 16. Пакет файлов, готовых к созданию

Ниже приведены восемь самостоятельных Markdown-блоков. Их содержимое идентично отдельным файлам пакета.

## File: 01_RESEARCH_CHARTER.md

````markdown
# Research Charter

**Дата спецификации:** 11 августа 2026 года  
**Исходный кандидат:** «Формальные границы полноты метода Twins для safety-тестирования BFT-протоколов блокчейн-систем: детерминированные протоколы с полным раскрытием причинной истории».  
**Итоговый статус исходного кандидата:** **ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT**.  
**Минимально переработанная тема:** **«Границы полноты конечноклонового Twins-тестирования валидируемых BFT-протоколов: соответствие между абстрактной state equivocation и исполнимой инъекцией отказов»**.  
**English title:** **“Completeness Boundaries of Finite-Clone Twins Testing for Validated BFT Protocols: Relating Abstract State Equivocation to Executable Fault Injection.”**

## 1. Executive decision

Исходная тема не может сохранять заявленный общий novelty claim. Twins действительно оставляет строгую теорию coverage открытой и формулирует conjecture для deterministic full-disclosure protocols, однако VLSM уже вводит динамическое копирование корректных состояний и доказывает, что для systems of validators наблюдаемые honest components traces под Byzantine behavior совпадают с traces под equivocation behavior при указанных assumptions. Поэтому центральный тезис «произвольный Byzantine adversary сводится к correct-code clones при полном раскрытии причинной истории» уже существует в более общей, формально проверенной форме. Основание: S04, S05 и S06.

Сохраняется более узкий и проверяемый разрыв между:

- абстрактной VLSM state-equivocation model, способной динамически создавать независимые copies состояния;
- реальным Twins harness, ограниченным конечным числом одновременно активных clones, concrete lifecycle, конкретным scheduler и корректным protocol code;
- bounded safety witness, который требуется воспроизвести без синтеза произвольных accepted messages.

Именно этот разрыв становится объектом переработанной темы. Даже он ещё не является доказанной novelty delta: возможный результат `minimum clones equals causal branch width` может оказаться прямой теоремой о chain cover или почти определением модели. Поэтому разрешено начинать только Gate 0, Gate 1 и блокирующий Gate 3 pilot. Полный implementation commitment до Gate 3 запрещён.

## 2. Основание в исходном брифе

Тема соответствует исходному брифу по следующим проверяемым основаниям, взятым непосредственно из S01:

| Требование брифа | Соответствие переработанной теме |
|---|---|
| Protocol/system level | Изучается expressiveness двух fault models для BFT consensus, а не токен, сеть или рынок. |
| Теоретико-вычислительный тип | Нужны formal trace semantics, refinement or separation theorem и exact bounded checker. |
| Новый механизм, model, bound или impossibility | Возможный вклад — finite-clone realization theorem, clone lower bound либо separation counterexample. |
| Различающее предсказание | Exact set inclusion между unsafe observation languages различает основную гипотезу и альтернативы. |
| Фальсификатор | Unmatched valid equivocation trace либо collapse результата в известный refinement/chain-cover theorem. |
| Независимость от одной сети | Claim относится к классу deterministic authenticated validator BFT protocols; protocol instances служат validation. |
| Один мощный компьютер | Core pilot — exhaustive small-state exploration на `n=4, f=1`; исторические chain data не требуются. |
| Ценность отрицательного результата | Separation theorem или отсутствие fixed clone cutoff определяет principled blind spot Twins. |
| Запрет mainnet risk | Все executions synthetic/local; никаких средств, private keys публичных систем или live attacks. |

В брифе не указано: конкретный BFT protocol, целевой venue, необходимость mechanized proof, точная продолжительность эксперимента, язык реализации и практический опыт с Coq. Консервативные решения фиксируются ниже.

## 3. Нормализованная спецификация

### 3.1. Исследуемый класс систем

Authenticated deterministic round-based BFT state-machine replication protocols, в которых correct replicas:

- применяют детерминированную transition function;
- принимают только messages, удовлетворяющие explicit validation predicate;
- могут проверить causal justification принятого сообщения;
- сохраняют safety при произвольных network delays;
- допускают finite safety witnesses, наблюдаемые по states и decisions correct replicas.

### 3.2. Научная проблема

VLSM устанавливает abstract equivalence Byzantine and equivocation behavior для validators, но production-style Twins fault injector не является неограниченной state-equivocation machine: он обычно запускает ограниченное число correct-code replicas с общей identity и управляет delivery. Не установлено, когда fixed-`k` executable harness реализует все bounded unsafe observations абстрактной equivocation model и как вычислять минимальное `k`.

### 3.3. Основной исследовательский вопрос

**Для deterministic authenticated validator BFT protocols и concrete Twins harness с не более чем `k` одновременно активными clones на Byzantine identity при каких условиях harness сохраняет все bounded safety-violating observations abstract state-equivocation model, и каков минимальный `k` для конкретного witness или protocol class?**

### 3.4. Основной тезис в требуемой форме

**При условиях U**, где protocol transitions deterministic, accepted messages validated, causal dependencies explicit, сеть asynchronous for safety, а observation ограничена states и decisions correct replicas, **механизм M**, отображающий каждую несовместимую causal history equivocating identity в отдельную correct-code clone branch, **должен приводить к следствию P**: каждый bounded unsafe abstract-equivocation trace воспроизводим fixed-`k` Twins execution при `k`, не меньшем structural width множества требуемых causal histories. **Ближайшая альтернатива A** предсказывает Q: либо две clones всегда достаточны для выбранного locking class, либо никакая protocol-independent structural width не характеризует executable realization из-за lifecycle и scheduler constraints. **Наблюдение R**, а именно valid witness с `k_min`, не совпадающим с заявленным width, или отсутствие strict hierarchy там, где width больше двух, опровергнет сильную версию M.

### 3.5. Механизм

1. Known reduction: Byzantine behavior для validators заменяется abstract equivocation behavior по S05.
2. Новый bridge obligation: abstract equivocation trace раскладывается на causally consistent correct-code histories.
3. Каждая одновременно необходимая несовместимая history назначается отдельной clone.
4. Scheduler доставляет каждой clone только causally allowed inputs и доставляет produced valid messages выбранным correct replicas.
5. Observation projection сравнивает locks, accepted certificates и decisions correct replicas.
6. Failure to construct such schedule даёт separation witness abstract model versus executable harness.

### 3.6. Ближайшие альтернативные объяснения

- **A1 — Two-clone sufficiency:** для одного Byzantine identity и рассматриваемого locking protocol вся safety-relevant equivocation бинарна, поэтому `k=2` всегда достаточно; proposed width machinery избыточна.
- **A2 — Trace-dependent but trivial:** для любого finite trace достаточно одной clone на каждую history, а minimum clone number является обычным minimum chain cover без protocol-specific theorem; вклад математически тривиален.
- **A3 — Harness limitation:** mismatch определяется не causal branching, а operational restrictions конкретной implementation, например невозможностью snapshot/restore в произвольном state или слишком грубым scheduler.
- **A4 — Accepted-message gap:** ByzzFuzz-like future-field mutations находятся вне validator model, поэтому apparent incompleteness относится к изменённой fault model, а не к finite-clone gap.

### 3.7. Тип вклада

Условно допустимы только следующие типы вклада:

- characterization theorem для finite-clone realization;
- lower or upper bound на `k_min`;
- separation theorem между dynamic state equivocation и fixed-`k` harness;
- necessary conditions on snapshot, validation, causal disclosure and scheduler;
- executable exact checker, служащий proof-discovery and validation artifact.

Не считается вкладом: очередной Twins implementation, больше найденных bugs, ускорение scenario generation, новый benchmark без theorem или использование HotStuff как новой сети.

### 3.8. Единица анализа

Единица анализа — **bounded unsafe observation witness**: finite causal trace together with the projection of correct-replica states and incompatible decisions. Дополнительная структурная единица — set of mutually incompatible faulty causal histories required to emit delivered messages.

### 3.9. Исследовательский артефакт

Dual-adversary explicit-state checker, который на одной protocol semantics генерирует:

- abstract accepted-message Byzantine traces;
- dynamic state-equivocation traces;
- fixed-`k` executable Twins traces;
- canonical unsafe observation signatures;
- minimal unmatched counterexamples and `k_min` maps.

### 3.10. Scope

Включено:

- safety and agreement only;
- finite traces;
- one Byzantine identity in blocking pilot;
- deterministic authenticated validator protocols;
- two application values;
- explicit causal justification DAG;
- arbitrary message delay, drop and reorder for safety;
- exact bounded exploration;
- static and dynamic clone lifecycle as separate models;
- one toy locking protocol and one independent protocol validation after Gate 3.

### 3.11. Non-goals

Не включено:

- liveness, timing attacks, GST and performance;
- malformed bytes, signature forgery, future-round field mutation not accepted by `Valid`;
- economic incentives, slashing, token markets;
- mainnet or public testnet attacks;
- production-client completeness across all code paths;
- universal proof for randomized or probabilistic protocols;
- multiple Byzantine identities in the pilot;
- empirical bug-count comparison as main contribution;
- ML-based test generation.

## 4. Атомарный claim ledger

| Claim | Формулировка | Тип | Требуемое доказательство | Текущий статус | Что опровергнет | Novelty depends |
|---|---|---|---|---|---|---|
| C1 | Тема должна быть formal, protocol-level, locally reproducible и давать meaningful negative result. | Известный факт из брифа | Прямая трассировка к S01 | Подтверждён | Несоответствие scope требованиям S01 | Нет |
| C2 | Twins использует несколько correct-code instances с общей identity и оставляет rigorous coverage open. | Известный факт | Полный текст S04 | Подтверждён | Иная формулировка в final publication | Нет |
| C3 | VLSM state equivocation создаёт independent copies states и для validators имеет те же exposed traces, что Byzantine behavior. | Формальное известное утверждение | Теоремы и Coq artifact S05–S06 | Подтверждён | Ошибка в theorem assumptions или неверное mapping выбранного class | Да, как novelty-killer |
| C4 | Исходный general Twins coverage claim уже не защищаем как новый. | Вывод из prior art | Сопоставление C2 и C3 | Подтверждён как audit conclusion | Невозможность отнести full-disclosure protocols к validators/equivocation class | Да |
| C5 | Fixed-`k` concrete harness строго ограниченнее dynamic abstract state equivocation. | Формальное и инженерное предположение | Найти trace или определить refinement, показывающий inclusion and possible strictness | Не доказан | Exact equivalence при `k=2` для всего заявленного class | Да |
| C6 | Любой finite abstract-equivocation trace может быть реализован конечным числом correct-code clones при ideal snapshot and scheduler. | Формальная гипотеза, вероятно слабая | Constructive trace mapping | Не доказан; вероятно близок к definition | Valid trace without any finite clone realization under agreed ideal model | Частично |
| C7 | Число clones не превосходит числа distinct faulty histories в finite witness. | Формальное предположение | Constructive upper-bound proof | Не доказан | Witness requiring more clones than histories or ill-defined history mapping | Нет, слишком слабый claim |
| C8 | `k_min` равно maximum antichain width causal-history incompatibility poset. | Новая сильная гипотеза | Necessary and sufficient theorem plus exhaustive validation | Не доказан | `k_min` differs from width in any valid model instance | Да, главный surviving claim |
| C9 | Не существует universal fixed `k` для широкого validator class. | Новая альтернативная гипотеза | Parametric counterexample family | Не доказан | Proof of fixed cutoff independent of witness length for stated class | Да, как negative route |
| C10 | Для ограниченного two-phase locking class две clones могут быть достаточны. | Ближайшая альтернатива | Protocol-class proof or exhaustive induction support | Не доказан | Valid width greater than two witness in class | Нет, но определяет pivot |
| C11 | Exact bounded language comparison различает C8, C9 и C10 без statistical ambiguity. | Измерительное предположение | Complete enumeration, canonicalization tests and independent oracle | Conditional | Incomplete exploration or projection conflates distinct witnesses | Нет |
| C12 | Mismatch, существующий только при invalid future-field mutations, не опровергает validator-scoped claim. | Вывод из модели | Membership check in `Valid` and comparison with S07 | Подтверждён концептуально | Protocol accepts such messages under agreed validator model | Нет |
| C13 | Minimal separation counterexample сохраняет научную ценность. | Методологический вывод | Show necessary condition or impossibility boundary | Conditional | Counterexample caused only by coding error or arbitrary harness restriction | Да |
| C14 | Core pilot доступен без mainnet and historical data. | Инженерный факт | Local tool/resource check | Подтверждён | Required production infrastructure discovered later | Нет |
| C15 | Full implementation не должен начинаться до nontrivial Gate 3 result. | Decision rule | Gate protocol | Зафиксирован | Не применимо | Нет |

## 5. Журнал решений

| ID | Решение | Основание | Отвергнутые альтернативы |
|---|---|---|---|
| D01 | Статус — «ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT». | S05 already covers general Byzantine-to-equivocation equivalence. | «ГОТОВО» и «ГОТОВО ПОСЛЕ ПИЛОТА» скрыли бы collapse original novelty. |
| D02 | Сузить объект до finite-clone executable gap. | Это минимальный repair, сохраняющий Twins, BFT testing и coverage question. | Полная смена темы на новый protocol или ML tester. |
| D03 | Safety-only and finite traces. | Уменьшает synchrony assumptions и делает exact witness comparison возможным. | Liveness and timing coverage оставлены вне scope. |
| D04 | One Byzantine identity in pilot. | Минимальный nontrivial setting `n=4, f=1`; multiple identities multiplies state space before central risk resolved. | Multi-fault pilot. |
| D05 | Accepted-message Byzantine baseline, not arbitrary bytes. | Иначе VLSM and full-disclosure comparison incoherent; S07 covers broader mutation model separately. | Message corruption without semantic validity. |
| D06 | Primary method — explicit-state checker, not Coq first. | Быстро уничтожает trivial or false conjectures and yields counterexamples. | Immediate mechanized proof risks months on wrong statement. |
| D07 | Reserve method — VLSM/Coq mechanization only after invariant. | Existing formalization and BSD artifact reduce proof setup cost. | New proof assistant stack or full TLA+ model before pilot. |
| D08 | Python 3.14.7 plus uv, pytest, Hypothesis. | Current, open, adequate for small exact model; S23–S26. | Production Go/Rust implementation before theorem. |
| D09 | Z3 optional, not baseline. | Explicit-state semantics is easier to audit; solver adds TCB. | Symbolic encoding from day one. |
| D10 | External validation first choice — `twins-simulator`; second — `relab/hotstuff` or ByzzBench. | Minimal Python integration first; production-style Go validation later. | Building a new blockchain client. |

## 6. Decisions still required by evidence, not preference

The following are research outcomes rather than hidden design choices:

- whether `k_min` is characterized by causal width;
- whether two clones suffice for the chosen locking class;
- whether a fixed cutoff exists for a useful class;
- whether executable snapshot and scheduler assumptions are non-vacuous;
- whether the surviving difference is mathematically nontrivial after S05 and S18;
- whether second-protocol validation confirms transfer.

The operational choices needed to start the first tasks are fixed in this charter.

## 7. Minimal Definition of Start

Work may start immediately only on:

1. source and claim ledger freeze;
2. mapping S05 theorem assumptions to the concrete Twins semantics;
3. formal definitions of `Valid`, observations and the three adversaries;
4. blocking dual-adversary pilot.

A production client adapter, large benchmark campaign or manuscript novelty claim may not start before Gate 3.

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
````

## File: 02_PRIOR_ART_AND_NOVELTY.md

````markdown
# Prior Art and Novelty Audit

**Дата поиска и спецификации:** 11 августа 2026 года  
**Исходный кандидат:** формальная полнота Twins для deterministic full-causal-disclosure BFT protocols.  
**Вердикт по исходному novelty claim:** **УНИЧТОЖЕН БЛИЖАЙШИМ PRIOR ART**.  
**Остаточный кандидат:** конечноклоновая реализуемость абстрактной state equivocation конкретным executable Twins harness.

## 1. Цель и пределы аудита

Аудит отвечает на два разных вопроса:

1. Существует ли уже общий результат, сводящий Byzantine behavior валидируемых компонентов к equivocation нескольких корректных histories?
2. Если такой результат существует, остаётся ли самостоятельный научный разрыв между неограниченной абстрактной state equivocation и реальным harness с конечным числом clones, ограниченным lifecycle и concrete scheduler?

Ответ на первый вопрос положительный: S05 формализует validators и state/message equivocation, разрешает динамическое копирование корректных состояний и доказывает совпадение traces, наблюдаемых honest validators, под Byzantine и equivocation behavior при своих assumptions. Поэтому исходное утверждение, предложенное в S03 как разрешение conjecture Twins, не может заявляться новым.

Ответ на второй вопрос пока условный. В обследованных источниках не обнаружено отдельного theorem, который связывает абстрактную VLSM state-equivocation machine с fixed-`k` production-style Twins harness и характеризует минимальное число одновременно активных clones. Но это отсутствие не доказывает новизну: разрыв может быть обычным refinement obligation, minimum chain-cover fact либо следствием уже известных cutoff theorems.

## 2. Поисковая стратегия

Поиск проводился отдельно по следующим осям:

- исходная проблема: completeness, coverage и blind spots clone-based Byzantine testing;
- формальное свойство: trace inclusion, observational simulation, refinement, conformance и adversary-model equivalence;
- механизм: shared-identity correct-code clones, state equivocation, forked histories, snapshot and restore;
- противник: arbitrary Byzantine, valid-message Byzantine, equivocator, message mutator, scheduler-controlled adversary;
- различающее предсказание: fixed clone cutoff, trace-dependent clone number, separation witness;
- проверка: bounded model checking, explicit-state exploration, communication closure, parameterized verification;
- системный артефакт: Twins, ByzzFuzz, ByzzBench, MALLORY, ZERMIA и failure-reproduction systems;
- старая терминология: virtual nodes, forked views, state splitting, non-equivocation, refinement mapping, I/O automata;
- соседние дисциплины: formal languages, automata refinement, concurrency width, chain cover, conformance testing и cutoff reasoning;
- engineering prior art: open Twins simulators, HotStuff test harnesses, benchmark frameworks и research repositories.

Использовались backward and forward citation searches от S04 и S05, exact-phrase searches по conjecture Twins, поиски по механизму без слова blockchain, официальные репозитории и свежая literature 2026 года. Тематическое насыщение считалось достигнутым, когда новые результаты перестали менять три главных вывода: S05 уничтожает общий claim; S07 показывает более сильную message-mutation fault model; S09–S11 и S18 задают наиболее опасные способы сделать остаточный finite-clone result тривиальным или уже известным.

## 3. Карта ближайших аналогов

| Источник | Тип | Проблема | Формальная или системная модель | Механизм | Противник и предположения | Свойство | Способ проверки | Артефакт | Совпадение | Реальное отличие | Отличие содержательно | Угроза новизне | Что ещё допустимо заявлять |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S05 VLSM | Препринт, Coq-checked theory | Faulty distributed systems through valid messages | Validating labelled state/message systems; components are validators | Dynamic state copies and message equivocation | Byzantine components affect honest validators only through messages accepted by validity constraints | Equality of honest-exposed trace sets under Byzantine and equivocation behavior | Formal proofs checked in Coq | S06 | Почти весь исходный theorem | Не рассматривает concrete fixed-`k` Twins lifecycle and scheduler | Да, если найден нетривиальный cutoff or separation | **Уничтожающая** | Только bridge abstract equivocation to executable finite-clone harness |
| S04 Twins | Peer-reviewed systems paper | Practical Byzantine attack generation | Correct-code twin copies with shared identity and network credentials | Selective message delivery, equivocation, double vote, state loss scenarios | Deterministic protocol intuition; limited scenario generator | Empirical attack coverage; conjectured broader completeness | Production implementation and scenario execution | Public artifacts | Исходный объект, mechanism and open question | Нет formal adversary-language theorem, no clone cutoff | Да | **Критическая** | Formalize exact harness and prove or refute bounded realization only |
| S07 ByzzFuzz | Peer-reviewed testing paper | Find BFT bugs beyond network faults | Randomized message and network fault injection | Small-scope field/time mutations | Byzantine process may create mutated messages accepted or mishandled by implementation | Bug-finding ability and fault-model reach | Randomized testing on PBFT, Tendermint and Ripple | Public research code reported | Shows behaviors ordinary Twins may miss | Mutations may lie outside validator-only accepted-message class | Да, as fault-model boundary | **Критическая** | Explicitly separate valid-message coverage from arbitrary malformed-message testing |
| S08 ByzzBench | Peer-reviewed tool paper | Standardized evaluation of BFT testers | Controlled protocol execution and fault scheduling | Plug-in random, ByzzFuzz and preliminary Twins testers | Controlled nondeterminism; benchmark protocols | Comparative detection and replay | Benchmark execution | MIT repository | Concrete reusable harness and baselines | No theorem about fault-model completeness | Да | Высокая practical novelty threat | Research artifact must not be sold as a new benchmark |
| S09 Communication Closure | Peer-reviewed PL/formal paper | Reduce asynchronous consensus tests to canonical executions | Communication-closed rounds and schedule reduction | Transform representative asynchronous schedules | Protocol class satisfying closure conditions | Preservation of safety-relevant behaviors under schedule reduction | Formal reasoning and testing | Research artifacts reported | Same goal of representative execution reduction | Relates schedules, not Byzantine versus clone fault models | Да | Высокая | New result must be a fault-model relation, not schedule canonicalization |
| S10 Cutoff Bounds | Peer-reviewed formal-methods paper | Verify parameterized consensus with finite instances | Parameterized threshold automata and process cutoffs | Small instance represents unbounded process counts | Protocol class and threshold assumptions | Cutoff for safety/liveness verification | Theorem plus model checking | Formal models | Bound-oriented methodology | Number of protocol processes, not clones per faulty identity | Да | Высокая | A clone cutoff must not follow immediately from existing process cutoff |
| S11 Short Counterexample Property | Peer-reviewed PL/formal paper | Bound counterexample length for fault-tolerant algorithms | Threshold automata | Small finite witnesses | Restricted algorithm class | Existence of short safety/liveness counterexamples | Formal theorem | Tool-related artifacts | Justifies bounded pilot | Does not realize witness with clone adversary | Да | Medium-high | Bounded witness scope is acceptable, but not itself novel |
| S18 Refinement mappings | Peer-reviewed theory | Relate abstract and concrete state machines | State-machine refinement and implementation mappings | Mapping plus auxiliary/history variables | Safety refinement assumptions | Every concrete behavior implements abstract specification or vice versa | Mathematical proof | None required | Exact conceptual form of bridge obligation | Not BFT or Twins specific | Mostly methodological, may subsume theorem shape | **Критическая adjacent threat** | Need a nontrivial BFT-specific bound or separation, not generic refinement restatement |
| S28 I/O automata | Classical formal model | Compositional distributed-system semantics | Input/output automata and external traces | Trace inclusion and simulation | Fairness and composition assumptions as selected | Implementation via external behavior inclusion | Mathematical formalism | None | Supplies definitions for observations and executions | No clone-specific bound | No by itself | Medium | Use as foundation, never claim trace inclusion as new |
| S16 Non-equivocation | Peer-reviewed distributed computing | Define and reason about non-equivocation | Synchronous agreement systems | Restrict inconsistent histories/messages | Synchronous assumptions and fault restrictions | Agreement under non-equivocation notions | Formal analysis | None | Clarifies equivocation boundary | No executable clone realization | Yes | Medium-high | Must align terminology and avoid redefining equivocation loosely |
| S17 CAC report | Technical report | Model consistency and faulty views | Forked/virtual client views | Forking and merge-like reasoning | Distributed storage consistency assumptions | Consistency/availability/convergence trade-offs | Formal arguments | No central artifact | Neighboring idea of virtual histories | Different property and setting | Limited | Medium | Cannot claim virtual/forked histories are novel |
| S13 MALLORY | Peer-reviewed security paper | Guided external-fault testing | Causal summaries of distributed executions | Greybox fault injection using happens-before information | External faults and observed behavior | Coverage and bug discovery | Systems experiments | Artifact reported | Uses causal structure in testing | No completeness or finite clone theorem | Yes | Medium-high | Causal width may be used only if it yields theorem, not coverage heuristic |
| S15 ZERMIA | Peer-reviewed chapter/tool | Inject Byzantine faults into BFT systems | Fault-injector architecture | Configurable Byzantine behaviors | Implementation-level assumptions | Ability to reproduce faults | Prototype evaluation | Framework | Same engineering space | No formal coverage bound | Yes | Medium | New harness alone has no novelty |
| S19 Rose | Peer-reviewed systems paper 2026 | Reproduce external-fault-induced failures | Lightweight instrumentation and execution replay | Capture/replay fault-relevant behavior | External faults, concrete systems | Reproduction fidelity | Systems artifact and evaluation | Open 812.6 MB artifact | Reproduction and replay concern | Not shared-identity clone expressiveness | Yes | Medium-high practical threat | Concrete replay must be secondary validation |
| S20 Node-Centric Systematic Testing | Peer-reviewed metadata; full text not verified | Systematic distributed-system testing | Node-centric exploration | Unknown in full detail at search date | Full assumptions not verified | Systematic exploration | Reported research evaluation | Availability unconfirmed | Potential overlap in node-branch exploration | Exact relation unknown | Unknown | **Unresolved threat** | Must obtain full text before publication claim |
| S12 Holistic Verification | Peer-reviewed formal paper | Verify blockchain consensus end to end | Formal protocol abstractions | Combined verification workflow | Protocol-specific BFT assumptions | Safety and correctness | Formal verification | Models/artifacts | Similar protocol models and checker infrastructure | Verifies protocol, not tester completeness | Yes | Medium | Use model patterns; do not present model checking workflow as contribution |
| S14 BFT Protocol Forensics | Peer-reviewed security paper | Identify faulty replicas after safety violations | Transcript/evidence model | Forensic support in BFT protocols | Authenticated messages and protocol-specific evidence | Number of identifiable faulty replicas | Formal analysis | Reported tools/models | Correct-node observations and causal evidence | Attribution, not clone realization | Yes | Medium | Observation function must distinguish decisions from full forensic trace |

## 4. Шесть наиболее близких ориентиров

### 4.1. Максимально близкая работа по проблеме

**S04 Twins.** Она формулирует practical coverage problem и оставляет rigorous theory открытой. Однако её conjecture нельзя читать изолированно от S05.

### 4.2. Максимально близкая работа по механизму

**S05 VLSM.** State equivocation реализуется посредством копирования корректных состояний, после чего copies развиваются независимо. Это более абстрактная и более сильная версия интуиции clones.

### 4.3. Максимально близкая работа по формальной модели

**S18 refinement mappings**, дополненная S28 I/O automata. Они задают стандартную форму proof obligation между abstract and concrete machines. Любой theorem, который лишь повторяет trace inclusion при специально выбранном relation, будет методологически известным.

### 4.4. Максимально близкая работа по экспериментальному дизайну

**S08 ByzzBench.** Она уже предоставляет controlled environment для сравнения BFT testing algorithms. Поэтому пилот должен измерять exact language relations and minimal witnesses, а не обычную bug-detection rate.

### 4.5. Инженерный артефакт, наиболее угрожающий практической новизне

**S22 relab/hotstuff**, потому что он включает production-oriented HotStuff variants и Twins safety testing. Дополнительная реализация Twins на HotStuff не будет самостоятельным вкладом.

### 4.6. Соседняя дисциплина, которую легко пропустить

**Minimum path or chain cover in partially ordered sets**, а также refinement theory. Если число clones просто равно minimum number of causally consistent chains covering required faulty actions, mathematical core может оказаться прямым применением классического результата. Gate 0 обязан проверить этот риск до кода большой системы.

## 5. Novelty kill test

| Вопрос | Результат аудита |
|---|---|
| Существует ли уже та же комбинация исходной проблемы, механизма и свойства | **Да в более общей форме.** S05 уже связывает Byzantine behavior и equivocation behavior для validators. |
| Известны ли все элементы исходной идеи отдельно | Да: correct-code clones, state equivocation, validators, trace equivalence, refinement and bounded checking. |
| Является ли исходное соединение неочевидным | После S05 — нет. Оно уже формализовано и mechanized. |
| Возникает ли новое проверяемое следствие после pivot | Потенциально: finite-`k` realization hierarchy, clone cutoff or separation from dynamic state equivocation. |
| Меняет ли это понимание системы | Только если выявляется nontrivial bound or blind spot concrete harness, а не одно clone per history by definition. |
| Является ли тема новым применением известного анализа | Исходная — фактически да; переработанная остаётся под риском такого вердикта. |
| Описана ли идея вне академической статьи | Twins artifacts and HotStuff implementations already realize practical clone testing. |
| Зависит ли delta только от клиента или workload | Не должна. Claim формулируется по protocol class and harness capabilities. |
| Можно ли сформулировать вклад без «впервые применили» | Да только как theorem, lower bound or separation. |
| Минимальное доказательство для сохранения novelty | Strict finite-clone hierarchy or necessary-and-sufficient realization condition that is not direct chain cover, validated on at least two non-isomorphic protocol models. |

## 6. Атомарная novelty delta

### 6.1. Claims, которые уже известны и не входят в новизну

- **C1:** Twins использует correct-code copies с общей identity для создания Byzantine-like executions. Установлено S04.
- **C2:** Для validator systems Byzantine effects on honest nodes могут быть представлены equivocation effects. Установлено S05.
- **C3:** State equivocation можно моделировать динамическим копированием корректных states. Установлено S05.
- **C4:** Bounded state exploration и small counterexamples полезны для BFT verification. Установлено S09–S12.
- **C6:** ByzzFuzz fault model может выходить за пределы ordinary Twins. Установлено S07.

### 6.2. Claims, на которых условно может держаться вклад

- **C5:** Concrete fixed-`k` Twins harness не тождествен abstract dynamic state-equivocation model.
- **C8:** Существует нетривиальная structural characterization минимального числа clones для bounded unsafe witness.
- **C9:** Lifecycle and scheduler restrictions создают formally characterizable separation beyond trivial chain cover.
- **C13:** Result переносится хотя бы между двумя protocol families without redefining the property.

### 6.3. Claims, которые могут уничтожить остаточную тему

- **C10:** Minimum clones is ordinary minimum chain cover of a witness DAG. Если это весь результат, novelty недостаточна.
- **C11:** Для выбранного safety class две clones всегда sufficient. Тогда broad hierarchy collapses; остаётся лишь узкий theorem, ценность которого нужно оценить отдельно.
- **C12:** Any mismatch arises only from malformed messages outside validator semantics. Тогда это comparison of different fault models, already expected from S07.
- **C14:** Existing refinement or cutoff literature already states equivalent finite-realization theorem under different terminology.

## 7. Итоговая формулировка novelty delta

Ближайшие работы уже вводят correct-code shared-identity clones, формализуют state equivocation и устанавливают equivalence Byzantine and equivocation behavior for validator systems. Поэтому общий coverage theorem исходного кандидата не является защищаемой новизной.

В обследованных источниках по состоянию на 11 августа 2026 года не обнаружена работа, которая одновременно:

1. фиксирует конкретную executable semantics production-style Twins harness;
2. ограничивает число одновременно активных clones величиной `k`;
3. связывает эту semantics с abstract dynamic state equivocation через trace refinement or separation;
4. даёт nontrivial characterization минимального `k` для bounded safety observations;
5. показывает, какие lifecycle or scheduler restrictions нарушают realization.

Предлагаемый вклад ограничен claims C5, C8, C9 и C13. Claims C1–C4 и C6 уже известны. Заявление ограничено использованными базами, английскими терминами, доступностью S20, возможным unpublished engineering prior art и риском того, что residual theorem является прямым следствием classical chain-cover or refinement theory.

## 8. Gate 0: обязательный дополнительный поиск до реализации

Gate 0 завершается только после выполнения всех действий:

1. Получить полный текст S20 и проверить его relation to node branching and systematic exploration.
2. Провести citation search по S05, отдельно по словам clone, cutoff, bounded equivocation, finite copies and executable adversary.
3. Проверить dissertations and technical reports авторов Twins and VLSM.
4. Провести search в I/O automata, process algebra, conformance and refinement literature без blockchain terminology.
5. Формально свести tentative clone-number problem к poset chain cover и проверить, остаётся ли protocol-specific obstruction.
6. Получить экспертную проверку accepted-message adversary model и non-vacuity validator class.
7. Зафиксировать exact theorem candidate before implementation.

**No-go Gate 0:** найден эквивалентный theorem; остаточный claim сводится к прямому chain-cover result; или executable model отличается от abstract model только очевидным hard cap `k` без научно значимой структуры.

## 9. Отложенные кандидаты

Аудит S03 оставил только Twins-кандидат. Остальные варианты не разрабатываются параллельно:

- finality-stall diagnosis поглощается diagnosability and accountable-liveness literature;
- rollup timing composition не имеет нетривиального necessary-and-sufficient claim;
- causal differential oracle является application of mature partial-order testing;
- parallel-execution observability почти целиком покрыта параметризованной theory;
- DAS correlation требует отдельного cryptographic audit и имеет unresolved closest prior art.

Возврат к ним допустим только после отдельного нового gate review; они не являются резервными implementation tracks текущего проекта.

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
````

## File: 03_FORMAL_MODEL.md

````markdown
# Formal Model

**Тема:** границы полноты finite-clone Twins testing для валидируемых BFT-протоколов.  
**Статус модели:** исполнимая спецификация для Gate 1 и Gate 3; не является доказательством novelty.  
**Тип исследования:** гибрид consensus, formal methods, software testing and adversary-model refinement.

## 1. Почему выбрана именно эта рамка

Минимально достаточная рамка состоит из:

- labelled transition systems для protocol and adversary semantics;
- causal partial orders для histories одного faulty identity;
- external-trace observation correct replicas;
- language inclusion or observational simulation для сравнения fault models;
- exact bounded exploration для pilot;
- индуктивного proof либо minimized separation counterexample для main result.

Timed automata не нужны: исследуется safety under arbitrary delay, а не liveness. Cryptographic game formalism не нужен: signatures идеализируются как unforgeability assumption. Probabilistic model не нужен: core result exact and non-statistical. Full production client semantics не нужна до завершения blocking pilot.

## 2. Базовые множества и роли

Пусть:

- `I` — конечное множество protocol identities;
- `H` — множество correct identities;
- `B` — множество Byzantine identities, причём `I` является disjoint union `H` и `B`;
- `V` — конечное множество application values;
- `R` — множество logical rounds or views;
- `Ty` — множество message types;
- `M` — множество authenticated protocol messages;
- `S` — множество local protocol states;
- `E` — множество execution events;
- `C_b` — множество concrete clones, принадлежащих Byzantine identity `b`;
- `K` — выбранный global clone cap per Byzantine identity.

Blocking pilot использует `I = {p0, p1, p2, p3}`, `B = {p3}`, `V = {v0, v1}`, `f = 1` and `n = 4`.

## 3. Сообщения

Сообщение `m` имеет поля:

- sender identity;
- type;
- round or view;
- value or block identifier;
- justification identifier;
- dependency digest;
- signature;
- optional disclosed nondeterministic choice.

Для toy protocol types are `PROPOSE`, `VOTE`, `LOCK_CERTIFICATE` and `DECIDE`.

### 3.1. Cryptographic abstraction

Предполагается идеальная authentication:

- adversary может подписывать сообщения только identities из `B`;
- correct identity не может быть forged;
- все clones одной Byzantine identity законно используют один и тот же signing key;
- hash collision and signature forgery находятся вне модели.

Эта abstraction не утверждает безопасность конкретной cryptographic library.

### 3.2. Validity predicate

`Valid(i, s, m)` определяет, может ли identity `i` в state `s` принять `m` как protocol-valid input.

Отдельно определяются:

- `AuthValid(m)` — подпись and sender identity valid;
- `SyntaxValid(m)` — type and fields well formed;
- `Justified(m)` — referenced causal evidence exists and is internally consistent;
- `ProtocolValid(i, s, m)` — message satisfies protocol-specific preconditions.

`Valid` является conjunction этих predicates, кроме явно указанной ablation.

Критическое ограничение: arbitrary Byzantine model не получает право отправлять любой byte string. Она получает право создавать любой sender-`b` message, который может быть принят через `Valid` в рассматриваемом execution. Это согласует comparison с validator semantics S05. ByzzFuzz-style malformed or future-field mutations анализируются как отдельная stronger fault model, а не как counterexample к validator-only theorem.

## 4. Локальное и глобальное состояние

### 4.1. Local state

Local state correct protocol instance содержит:

- current round;
- highest known certificate;
- current lock;
- accepted-message store;
- sent-message store;
- decision status;
- disclosed nondeterministic state;
- protocol-specific monotonic metadata.

Toy model использует immutable canonical representation, чтобы state equality and hashing были exact.

### 4.2. Global state

Global state содержит:

- one local state per correct identity;
- adversary state according to selected model;
- multiset of in-flight messages;
- delivered-message relation;
- event trace prefix;
- causal dependency relation;
- set of decisions by correct identities;
- clone lifecycle map for finite-clone model.

No wall-clock time is included.

## 5. Correct protocol machine

Protocol specification is

`P = (I, S, S0, M, Delta, Valid, Obs)`.

Where:

- `S0` is the set of permitted initial states;
- `Delta` is deterministic transition function from identity, local state and optional delivered message to new local state and finite emitted-message sequence;
- `Valid` filters receive transitions;
- `Obs` maps a global execution prefix to externally relevant correct-replica observations.

Determinism means that after fixing local state, delivered input and explicitly disclosed choice, `Delta` produces a unique result. Hidden randomness is forbidden in the core class; random coins are permitted only when represented as explicit validated inputs or proof-carrying choices.

## 6. Events and transition system

Events are:

- `INIT(i, s)`;
- `LOCAL_STEP(i, label)`;
- `SEND(actor, m)`;
- `DELIVER(recipient, m)`;
- `DROP(m)`;
- `DUPLICATE_STATE(b, source_copy, target_copy)`;
- `START_CLONE(b, clone, initial_or_snapshot_state)`;
- `STOP_CLONE(b, clone)`;
- `DECIDE(i, v)`.

A trace is a finite sequence of enabled events. Event enablement depends on protocol state, adversary semantics and channel rules.

## 7. Causal structure

The causal order `precedes` is the transitive closure of:

- per-instance program order;
- `SEND` before every corresponding `DELIVER`;
- justification dependencies before the message that cites them;
- state-copy source history before `DUPLICATE_STATE`;
- delivered input before the transition it enables;
- certificate constituent votes before certificate production.

A causal history for faulty identity `b` is a downward-closed subset of events executed by one internally consistent state branch together with all external inputs on which those events depend.

Two faulty histories are incompatible when no single correct-code local execution can contain both while respecting `Delta`, `Valid` and disclosed choices.

## 8. Network model

For safety:

- asynchronous reliable-or-lossy scheduler, chosen by adversary;
- arbitrary delay, reorder, selective delivery and drop;
- point-to-point authenticated channels;
- no fairness assumption;
- no upper latency bound;
- no synchrony or GST;
- partitions are represented by sustained nondelivery;
- message duplication by the network is excluded unless explicitly enabled as an ablation.

This model does not support liveness conclusions. Any result about liveness, timeout behavior or eventual delivery is out of scope.

## 9. Fault models

### 9.1. Correct execution model `A0`

All identities run `Delta`; scheduler may delay or reorder but cannot alter messages. Used as sanity baseline.

### 9.2. Accepted-message Byzantine model `AB`

For each Byzantine identity `b`, adversary may:

- emit any message carrying sender `b` that is admissible under the receiving validator constraints in the constructed trace;
- choose different valid messages for different recipients;
- omit messages;
- schedule all network delivery;
- use any causally admissible message evidence already present in trace.

It may not forge correct identities or cause a correct node to accept a message rejected by `Valid`.

`AB` is an abstract oracle model. It need not execute correct `Delta` for `b`.

### 9.3. Dynamic state-equivocation model `AE`

For each faulty identity `b`, adversary maintains an unbounded finite set of state copies over every finite trace. It may:

- create a new copy of an initial state;
- duplicate an existing state copy;
- independently execute correct `Delta` in each copy;
- feed each copy a different causally available valid-message subset;
- deliver emitted messages selectively.

This is the operational abstraction closest to S05. It is dynamic and not constrained by a predetermined clone cap.

### 9.4. Finite-clone Twins model `AT(k)`

For each faulty identity `b`, at most `k` clones may be simultaneously active. Every clone:

- runs unmodified correct `Delta`;
- shares sender identity and signing key with sibling clones;
- starts only through an allowed lifecycle operation;
- receives only messages selected by scheduler;
- emits only messages generated by its local execution.

Harness profile parameterizes:

- whether clones start only at protocol genesis or may start from snapshots;
- whether snapshot may be taken at arbitrary local state;
- whether stopped clone state may be restored;
- whether scheduler sees internal state;
- whether delivery can be clone-specific;
- whether clone messages may be suppressed after emission;
- whether local durable state can be reset.

The primary profile is `GenesisStatic(k)`: all `k` clones exist from initial state and persist. The reserve profile is `SnapshotDynamic(k)`: clones may be spawned from an existing snapshot but active count never exceeds `k`.

### 9.5. Mutation model `AM`

Used only as out-of-scope comparator. It can alter fields of emitted messages, including values that no correct execution would produce. It approximates S07. A witness exclusive to `AM` does not refute finite-clone completeness relative to `AB` or `AE`; it demonstrates a stronger fault model.

## 10. Observations

Primary observation projection `ObsSafety` retains only:

- local lock state of every correct replica at designated boundaries;
- accepted certificates of correct replicas;
- values decided by correct replicas;
- identity and causal evidence of messages actually delivered to correct replicas.

It removes:

- internal clone identifiers;
- scheduler bookkeeping;
- messages never delivered to a correct replica;
- event interleavings that do not change the causal relation or correct states.

Secondary observations:

- `ObsDecision` keeps only decisions;
- `ObsState` keeps full correct local states;
- `ObsTrace` keeps delivered-message causal DAG.

Main theorem must state exactly which projection it preserves. No result may silently switch observation level.

## 11. Safety property

Agreement safety is:

> No finite execution contains two correct identities that decide incompatible values.

For binary toy protocol, values are incompatible when unequal. For block-tree validation, incompatibility means neither decision extends the other under protocol-defined ancestry.

An unsafe observation is a value of `ObsSafety` containing an agreement violation.

Safety is prefix-closed: once an observation contains incompatible correct decisions, every extension remains unsafe.

## 12. Execution languages

For depth bound `d`, protocol `P`, harness profile `h` and clone cap `k` define:

- `LB(P,d)` — canonical observations from `AB` traces of depth at most `d`;
- `LE(P,d)` — canonical observations from `AE` traces of depth at most `d`;
- `LT(P,h,k,d)` — canonical observations from `AT(k)` traces under profile `h` of depth at most `d`;
- `UnsafeB`, `UnsafeE`, `UnsafeT` — corresponding unsafe subsets.

The depth metric is a tuple, not a single arbitrary event count:

- maximum protocol rounds;
- maximum delivered messages;
- maximum local transitions;
- maximum certificate constructions.

Pilot enumerates a finite rectangular bound and records all components.

## 13. Core definitions

### 13.1. Bounded finite-clone completeness

`AT(k)` is bounded-complete for `AE` under observation `Obs`, profile `h` and bound `d` when:

`LE(P,d) subset of LT(P,h,k,d)`.

For safety-only completeness, replace languages with unsafe subsets.

### 13.2. Exact bounded equivalence

Exact equivalence holds when both inclusions hold. The reverse inclusion is expected if every concrete clone execution is admitted by abstract equivocation semantics; it is a model-consistency obligation, not the main novelty claim.

### 13.3. Minimum clone number

For witness observation `w` in `LE(P,d)`,

`k_min(w,h) = min k such that w belongs to LT(P,h,k,d)`.

If no finite `k` under profile `h` realizes `w`, the value is infinity.

### 13.4. Protocol-level clone cutoff

A finite cutoff `K(P,h,d)` is the maximum `k_min` over all abstract-equivocation observations in the bound. A protocol-class cutoff independent of `d` is a stronger object and is not assumed to exist.

### 13.5. Faulty-history incompatibility width

For an abstract witness trace `t`, construct poset `Hist(t)` of faulty causal actions. A chain is a subset realizable by one correct-code local history. `width(t)` is maximum number of pairwise incompatible histories required at one realization frontier.

This definition is provisional. Gate 1 must prove it is independent of arbitrary trace decomposition and is computable from canonical causal evidence.

## 14. Established facts versus new obligations

### 14.1. Established or source-supported

- S04: correct-code shared-identity clones can produce several important Byzantine behaviors.
- S05: under validator assumptions, Byzantine effects on honest validators equal equivocation effects.
- S05: state equivocation permits state copies that evolve independently.
- S09–S12: bounded and reduced verification is legitimate for suitable protocol classes.
- S18 and S28: trace inclusion and refinement are standard formal tools.

### 14.2. New and unproved

- Every bounded abstract-equivocation safety witness has finite-clone realization under `GenesisStatic` or `SnapshotDynamic` profile.
- `k_min` is characterized by a causal width quantity.
- A nontrivial bound transfers between protocol families.
- Concrete Twins artifacts conform to formal `AT(k)` semantics.

## 15. Central hypotheses

### 15.1. Strong hypothesis Hstrong

For the target protocol class and `SnapshotDynamic` profile:

1. every finite `AE` trace has an observationally equivalent finite-clone trace;
2. `k_min` equals canonical faulty-history incompatibility width;
3. the equality is invariant under protocol-preserving renaming and independent-event reordering.

### 15.2. Weak hypothesis Hweak

For every bounded unsafe `AE` observation there exists a computable finite upper bound on clones, even if it is larger than width and depends on trace depth.

### 15.3. Nearest alternatives

- **H2:** two clones suffice for all safety violations in the restricted locking class.
- **H3:** no profile-independent finite characterization exists; snapshot capability changes expressiveness fundamentally.
- **H4:** finite realization always holds but minimum clones is direct chain cover, providing no new BFT-specific insight.
- **H5:** only accepted-message abstraction yields equivalence; implementation-level mutations lie outside the theorem.

## 16. Main conjectures and theorem targets

### Target T0: Model sanity

Every `AT(k)` execution reduces to a valid `AE` execution with the same correct-node observation.

This should be proved first. Failure indicates inconsistent semantics.

### Target T1: Finite realization

For every finite `AE` trace in target class there exists finite `k` and `AT(k)` trace with equal `ObsSafety`.

### Target T2: Width upper bound

For every finite witness `t`, `k_min` is at most a function of canonical incompatibility width and permitted snapshot profile.

### Target T3: Width lower bound

Construct a witness family requiring at least `width(t)` simultaneously active clones under selected profile.

### Target T4: Condition separation

Removing each candidate condition — determinism, validator constraint, causal evidence, snapshot ability or clone-specific delivery — either preserves T1 or yields a minimized counterexample.

### Target T5: Transfer

At least one theorem or counterexample schema applies to two structurally different BFT models without changing definitions.

## 17. Required lemmas

1. **Clone consistency lemma:** events from one clone form a legal correct-code local history.
2. **Observation erasure lemma:** clone identifiers are irrelevant under `ObsSafety` after sender projection.
3. **Abstract embedding lemma:** every finite-clone trace embeds into dynamic state equivocation.
4. **History decomposition lemma:** relevant faulty actions in finite `AE` witness admit a cover by correct-code causal chains.
5. **Schedule realization lemma:** given such a cover, scheduler can deliver inputs to corresponding clones without introducing extra observed messages.
6. **State availability lemma:** required chain start states are obtainable under selected lifecycle profile.
7. **Lower-bound lemma:** pairwise incompatible histories cannot share one clone.
8. **Canonicalization lemma:** symmetry reduction preserves observations and `k_min`.
9. **Ablation lemma:** each removed assumption has explicit semantic effect.

Lemmas 4–7 are the scientific core. Lemmas 1–3 and 8 are infrastructure obligations.

## 18. Proof obligations

- PO1: `Valid` does not smuggle arbitrary Byzantine power into correct clones.
- PO2: `AB` and `AE` relation used from S05 is mapped correctly, with all assumptions listed.
- PO3: external observation is neither so coarse that all models trivially agree nor so fine that hidden clone IDs force disagreement.
- PO4: causal history decomposition is unique enough for width to be well-defined, or result is stated over minimum decomposition.
- PO5: clone lifecycle profile is explicit in every theorem.
- PO6: scheduler has equal network power in abstract and concrete models.
- PO7: certificate aggregation and signature identity do not permit one clone to consume evidence unavailable in its causal branch.
- PO8: bounded checker is sound with respect to mathematical transition rules.
- PO9: finite-state result is not generalized beyond stated bounds without proof.
- PO10: second protocol instantiation satisfies target-class assumptions non-vacuously.

## 19. Conditions that make the claim false or vacuous

The strong claim is false or scientifically unusable when:

- Byzantine-valid messages can assert an internal state transition no correct history can produce;
- nondeterministic choices are hidden and cannot be replayed by clones;
- one message can depend on mutually incompatible histories without carrying verifiable combination evidence;
- harness cannot initialize or snapshot the states required by the decomposition;
- observation includes physical process identity rather than protocol identity;
- scheduler cannot selectively deliver to clones while abstract model can;
- theorem defines full disclosure so strongly that every message contains a full proof of correct execution, making realization definitional;
- `k_min` is exactly minimum chain cover with no protocol-specific constraint or new bound;
- protocol class excludes all practically relevant locking BFT designs.

## 20. Counterexample templates

### CE1: Hidden randomness

A Byzantine validator emits two valid messages derived from different hidden random choices, but the harness cannot instantiate the choices in separate clones because the choice is not an input or snapshot state.

### CE2: Unverifiable state claim

A message is accepted based only on signature and round, although no correct `Delta` path yields its payload. `AB` can emit it; `AT(k)` cannot for any `k`.

### CE3: Merge of incompatible histories

A valid message depends on evidence from two incompatible branches and can be synthesized abstractly, while no single correct clone can combine them. Whether validator constraints prohibit this is a critical test.

### CE4: Lifecycle restriction

Dynamic state equivocation copies a state after a rare prefix, while `GenesisStatic(k)` lacks enough clones that followed that prefix. The same witness may be realizable under `SnapshotDynamic(k)`.

### CE5: More-than-two branch family

Three recipients require three pairwise incompatible, safety-relevant faulty histories at the same frontier. If two clones nevertheless realize the witness, proposed width definition is wrong or observation too coarse.

### CE6: False unmatched trace

Checker reports separation because canonicalizer treats two certificate encodings as different. This is a measurement failure, not scientific counterexample.

## 21. State-space bounds and reduction strategy

Pilot state space is bounded by:

- four protocol identities;
- one faulty identity;
- two values;
- at most five rounds initially;
- finite message types;
- clone caps one through four;
- bounded in-flight message multiset;
- safety property only.

Reduction methods:

- rename symmetry among correct identities while preserving designated faulty identity;
- value symmetry swapping `v0` and `v1`;
- partial-order reduction for independent deliveries to different nodes when no shared certificate dependency exists;
- canonical multiset ordering;
- hash-consed immutable local states;
- stop exploration after first safety violation for witness-language mode, while retaining full prefixes for inclusion checks;
- quotient internal clone labels under sender identity.

Every reduction requires a preservation test against unreduced tiny bounds.

## 22. Analytic, model-checking and empirical division

| Question | Method |
|---|---|
| Definitions and adversary power | Analytic specification review |
| `AT(k)` embeds in `AE` | Manual proof, later optional Coq |
| Bounded language inclusion | Exact explicit-state model checking |
| Minimum `k` for bounded witness | Exact search over increasing `k` |
| Causal-width equality | Counterexample search plus theorem proof |
| Necessary assumptions | Formal ablations and minimized counterexamples |
| Cross-protocol transfer | Second executable formal model |
| Concrete artifact conformance | Differential trace replay against S21, S22 or S08 |
| Unbounded theorem | Analytic induction or mechanized proof; not inferred from finite tests |

## 23. Applicability boundary

Results apply only to:

- authenticated validator-style components;
- deterministic or explicitly replayable transitions;
- safety observations under asynchronous scheduling;
- selected clone lifecycle profile;
- message-validation semantics explicitly modeled;
- finite witnesses unless an unbounded theorem is proved.

Results do not automatically apply to:

- arbitrary implementation corruption;
- memory safety bugs;
- malformed packet parsing;
- hidden nondeterminism;
- cryptographic compromise;
- liveness failures requiring fairness or time;
- adaptive key compromise;
- economic attacks;
- production performance.

## 24. Formal readiness criterion

Gate 1 passes only when:

1. all machines `AB`, `AE` and `AT(k)` are executable from one protocol specification;
2. `Valid` and `ObsSafety` have unit examples and counterexamples;
3. T0 is proved on paper and exhaustively checked at tiny bounds;
4. clone lifecycle profile is fixed;
5. a nontrivial candidate T2 or an explicit separation question remains after chain-cover analysis;
6. no term such as safety, completeness, equivocation or observation remains undefined.

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
````

## File: 04_PILOT_PROTOCOL.md

````markdown
# Blocking Pilot Protocol

**Pilot ID:** BP-TWINS-FC-01  
**Role:** блокирующий experiment before full implementation.  
**Decision target:** determine whether the repaired finite-clone question contains a nontrivial scientific result beyond VLSM, generic refinement and ordinary chain cover.  
**Expected effort:** 7–12 focused person-days after Gate 0 and Gate 1 definitions pass.

## 1. Точный вопрос пилота

Для minimal deterministic authenticated locking BFT protocol with `n=4`, `f=1` and one Byzantine identity:

> Does every bounded unsafe observation generated by dynamic state equivocation have an observationally equivalent execution generated by a fixed-`k` correct-code Twins harness, and is minimum `k` predicted by a nontrivial causal-history structure rather than by a definitional one-clone-per-history construction?

## 2. Проверяемые claims

- **C5:** fixed-`k` executable Twins is strictly more constrained than abstract dynamic state equivocation.
- **C8:** minimum clone number has a structural characterization.
- **C9:** clone lifecycle and scheduler restrictions create meaningful completeness boundaries.
- **C10 kill claim:** the result collapses to ordinary chain cover and is not a new BFT theorem.
- **C11 alternative:** two clones suffice for every bounded safety witness in the pilot protocol.

## 3. Минимальная формальная или программная модель

### 3.1. Protocol

Two-phase deterministic locking protocol with:

- four identities;
- one proposer per round;
- binary values `v0` and `v1`;
- signed proposals and votes;
- a lock certificate formed from quorum votes;
- lock update rule requiring valid justification;
- decision rule requiring a second compatible certificate;
- exact agreement safety oracle.

The protocol is intentionally small but nontrivial: conflicting decisions require branches, certificates and selective information flow.

### 3.2. Fault models

The same protocol implementation is executed under:

1. accepted-message Byzantine generator `AB`;
2. dynamic state-equivocation generator `AE`;
3. finite-clone Twins generator `AT(k)` for increasing `k`;
4. optional mutation comparator `AM`, excluded from main completeness claim.

### 3.3. Harness profiles

- Primary: `GenesisStatic(k)`, all clones start at genesis and persist.
- Secondary ablation: `SnapshotDynamic(k)`, snapshots may spawn clones at reachable states.

## 4. Источник traces

All traces are generated locally by exact state-space exploration. No historical blockchain data, public node, RPC service or archive access is used.

Each trace is stored as canonical JSON Lines with:

- event sequence;
- causal parent identifiers;
- pre-state and post-state hashes;
- delivered and emitted message identifiers;
- correct-replica observation;
- safety result;
- adversary model and harness profile;
- bound vector and software revision.

## 5. Выбранные protocol instances

### Blocking pilot instance

A self-contained toy locking protocol defined in `src/twinsbound/protocols/toy_locking.py`.

### Post-pilot validation only

One Streamlet-like model and one HotStuff-like model. S21, S22 or S08 may supply engineering validation, but none is a prerequisite for pilot success.

## 6. Baseline

Primary theoretical baseline is dynamic state equivocation `AE`, because S05 already establishes its relation to Byzantine behavior for validator systems under stated assumptions.

Operational baselines:

- one clone, equivalent to one correct local history under shared identity;
- published/common two-clone Twins intuition;
- unrestricted finite realization with one clone per discovered faulty history, used only as an upper-bound construction;
- optional ByzzFuzz-style mutation model to demonstrate fault-model boundary, not to compete on bug count.

## 7. Ближайшая альтернатива

The nearest scientific alternative is:

> For the chosen locking class, two clones are sufficient for all safety-relevant equivocation, and any larger `k` hierarchy is an artifact of observation granularity or harness design.

The second alternative is:

> Minimum `k` is simply the minimum number of causally consistent chains covering faulty actions, so the result is generic combinatorics rather than a new BFT testing boundary.

## 8. Независимые переменные

- adversary model: `AB`, `AE`, `AT(k)` and optional `AM`;
- clone cap `k`;
- clone lifecycle profile;
- round bound;
- delivered-message bound;
- protocol condition ablations;
- scheduler visibility and clone-specific delivery capability;
- observation projection: decisions only, correct states, or delivered causal trace;
- protocol parameter variants, only after core pilot.

## 9. Зависимые переменные

- exact set of canonical unsafe observations;
- set-inclusion relation between model languages;
- number and identity of unmatched observations;
- `k_min` for each abstract-equivocation witness;
- candidate causal width for each witness;
- difference between `k_min` and candidate width;
- minimal counterexample size;
- state-space size and reduction ratio;
- classification of mismatch cause.

## 10. Контролируемые параметры

- same protocol transition function across all models;
- same `Valid` predicate;
- same correct-node set;
- same network scheduling powers except the explicitly ablated capability;
- same observation canonicalization;
- same round/message/local-step bound vector;
- same value set and quorum rule;
- same signature abstraction;
- deterministic enumeration order used only for reproducibility, not semantics.

## 11. Adversarial scenarios

1. Binary equivocation: conflicting proposals delivered to disjoint correct subsets.
2. Double vote: sibling histories vote for incompatible values.
3. Lock forgetting, modeled only if reachable through permitted clone lifecycle; direct state corruption is not silently allowed.
4. Delayed certificate revelation.
5. Three-way causal branching where three recipients require pairwise incompatible faulty histories.
6. Merge attempt using evidence from incompatible branches.
7. Snapshot-dependent witness realizable under `SnapshotDynamic` but not `GenesisStatic` at same `k`.
8. Hidden-choice ablation.
9. Weak-validation ablation permitting messages not produced by correct transitions.
10. Stronger mutation-model witness outside validator semantics.

## 12. Метрики

Core metrics are exact logical quantities, not aggregate performance scores:

- `missing(k) = UnsafeE minus UnsafeT(k)`;
- `extra(k) = UnsafeT(k) minus UnsafeE`;
- exact `k_min` per witness;
- equality indicator `k_min equals width`;
- minimum witness depth for separation;
- minimum assumption set necessary for realization;
- soundness indicator for canonicalization and reductions.

Engineering metrics such as runtime, peak memory and states per second are recorded only for feasibility and do not establish the scientific claim.

## 13. Объём state space and repetitions

No stochastic repetitions are used in the decisive core. The pilot performs exact enumeration within a predeclared bound.

The bound is selected procedurally:

1. start at the smallest bound capable of forming one lock certificate and one decision certificate;
2. increase one round at a time until the first unsafe `AE` witness appears;
3. complete exact enumeration at that bound;
4. repeat at one strictly larger round bound if resource limits permit;
5. stop expansion only when the predeclared memory or wall-time budget is reached, recording an incomplete status rather than treating partial search as evidence.

The initial expected range is three to five rounds, clone caps one through four, and a message bound derived mechanically from maximum protocol emissions per transition. No arbitrary sample size is used.

For optional randomized regression tests, seeds are fixed and listed, but those tests cannot decide the research hypothesis.

## 14. Способ анализа

1. Enumerate and canonicalize `AE` reachable states and unsafe observations.
2. Enumerate `AT(k)` for increasing `k` under identical bounds.
3. Compute exact set differences.
4. For each `AE` witness, search smallest `k` producing same observation.
5. Construct causal-history incompatibility graph or poset.
6. Compare `k_min` with candidate width and simpler predictors.
7. Minimize unmatched witnesses by event deletion, bound reduction and symmetry normalization.
8. Classify each mismatch as semantic, lifecycle, scheduler, validation, observation or implementation artifact.
9. Repeat under condition ablations.
10. Write a decision memo applying go, no-go or pivot rules.

No p-value or statistical significance test is applicable to exact language inclusion. Confidence comes from proof obligations, exhaustive bounds, independent implementation checks and reduction validation.

## 15. Критерий успеха

The pilot supports continuation only if at least one nontrivial outcome is obtained:

- a strict and reproducible clone hierarchy with a witness requiring more than two clones under a realistic profile;
- a structural predictor of `k_min` that survives all bounded cases and is not identical by definition to minimum chain cover;
- a minimal separation counterexample between `AE` and every finite-clone execution under a clearly justified harness restriction;
- a necessary-condition counterexample family produced by removing one realistic assumption;
- a plausible inductive invariant leading to a theorem that is not already S05 or generic refinement.

Success is not defined by runtime, number of generated scenarios or number of implementation bugs.

## 16. Критерий опровержения

The strong mechanism is refuted when any valid bounded witness satisfies one of the following:

- `k_min` differs from the proposed canonical width after canonicalization is independently checked;
- a witness with width greater than two is realized by two clones without revealing a flaw in width definition;
- a witness with finite width cannot be realized by any tested `k` and the obstruction persists under dynamic snapshot profile;
- fixed-clone and abstract languages disagree because the mapping assumptions are false, not because of insufficient bound;
- exact prior art discovered during Gate 0 already proves the same characterization.

## 17. Критерий неоднозначного результата

Result is inconclusive when:

- no unsafe `AE` witness exists inside the largest completed bound;
- exploration is incomplete due to memory or time limits;
- unmatched traces disappear under a corrected canonicalizer or validity predicate;
- all observed witnesses use at most two histories, so the pilot cannot distinguish Hstrong from two-clone sufficiency;
- only mutation-model witnesses differ;
- the toy protocol fails the target validator assumptions.

An inconclusive result does not count as support.

## 18. Go, no-go and pivot decision rules

### Go

Proceed to full artifact and proof route only when:

- Gate 0 finds no equivalent prior art;
- exact pilot exposes a nontrivial invariant, hierarchy or separation;
- result remains after reduction validation and assumption audit;
- negative or positive theorem statement can be written before adding a production client;
- a second protocol model is plausibly within scope.

### No-go

Stop this research theme when:

- the only theorem is the already-known Byzantine-to-equivocation equivalence;
- minimum clones is a direct chain-cover identity with no new protocol condition;
- two-clone sufficiency is immediate from the toy definition and does not generalize;
- every difference depends on malformed messages outside validator semantics;
- result is only implementation coverage or scenario-count improvement;
- target protocol class becomes empty or unrealistic after assumptions are made explicit.

### Pivot

Pivot to a narrower separation result when:

- lifecycle or snapshot ability, rather than clone count itself, creates a reproducible boundary;
- no general cutoff exists but a protocol-class-specific lower bound is nontrivial;
- concrete harness conformance exposes a systematic abstraction gap;
- finite-trace result is strong but unbounded theorem is not tractable.

These rules are logical consequences of the contribution requirement and do not use arbitrary percentage thresholds.

## 19. Ожидаемые ресурсы

- one Linux-compatible workstation;
- Python 3.14.7;
- pytest 9.1.1;
- Hypothesis 6.165.3 for regression generation only;
- uv-managed environment;
- standard library data structures for primary explorer;
- optional Z3 5.0.0 if exact enumeration cannot express a proof obligation efficiently;
- 8–32 GB RAM expected for pilot, with actual hardware recorded;
- no GPU requirement;
- no paid cloud or external service.

## 20. Оценка длительности

Focused person-days:

- formal schema and toy protocol: 2–3;
- three adversary generators: 2–3;
- canonicalization and language comparison: 1–2;
- exact sweep and minimization: 1–2;
- analysis and decision memo: 1–2.

Total: **7–12 focused person-days**, excluding literature Gate 0 and optional proof mechanization.

## 21. Минимальный программный артефакт

The minimum artifact is a deterministic command-line explicit-state checker that:

1. loads one TOML configuration;
2. instantiates the toy protocol;
3. enumerates `AE` and `AT(k)` state spaces;
4. evaluates agreement safety;
5. canonicalizes observations;
6. computes exact set differences and `k_min`;
7. emits minimized JSONL witnesses and a Markdown decision report.

No web interface, distributed deployment or production node is required.

## 22. Точный список выходных файлов

- `configs/pilot.toml`
- `src/twinsbound/protocols/toy_locking.py`
- `src/twinsbound/adversaries/byzantine.py`
- `src/twinsbound/adversaries/equivocation.py`
- `src/twinsbound/adversaries/twins_k.py`
- `src/twinsbound/explorer.py`
- `src/twinsbound/oracles.py`
- `tests/test_protocol.py`
- `tests/test_adversary_embedding.py`
- `tests/test_canonicalization.py`
- `results/pilot/state_space.json`
- `results/pilot/language_summary.csv`
- `results/pilot/unmatched_traces.jsonl`
- `results/pilot/k_min.csv`
- `results/pilot/decision.md`
- `results/pilot/environment.json`
- `results/pilot/manifest.sha256`

## 23. Главные угрозы валидности

### Construct validity

- `Valid` may be too strong or too weak.
- `ObsSafety` may hide a relevant distinction or preserve irrelevant scheduling noise.
- causal width may depend on arbitrary decomposition.

### Internal validity

- explorer or canonicalizer bug may fabricate inclusion or separation.
- asymmetrical scheduler power may bias one model.
- reduction may merge non-equivalent states.

### External validity

- toy protocol may not represent HotStuff/Tendermint-like locking semantics.
- single Byzantine identity may miss multi-fault interactions.
- finite round bound may not expose unbounded behavior.

### Conclusion validity

- bounded equality cannot prove unbounded theorem.
- one counterexample refutes a universal claim but may not support a broad replacement theory.
- implementation mismatches may be harness-specific.

Mitigations are explicit cross-checks, unreduced tiny runs, second-model validation and restrained claims.

## 24. Воспроизведение другим исследователем

A reproducer must be able to:

1. clone a version-pinned repository;
2. install the recorded Python patch version and uv version;
3. execute `uv sync` from committed `uv.lock`;
4. run `uv run pytest`;
5. run the one-command pilot script;
6. verify source and result checksums;
7. regenerate JSONL traces, CSV matrices and decision report;
8. compare generated manifests byte-for-byte where deterministic;
9. inspect an unmatched trace through a plain-text trace renderer;
10. rerun tiny bounds with reductions disabled.

The reproduction contract requires no private data, token, RPC endpoint or cloud account.

## 25. One-command pilot contract

The intended command after repository creation is:

```text
uv run python scripts/run_pilot.py --config configs/pilot.toml
```

This command is a repository design contract, not a claim that the script already exists. The external tool commands listed in S21 and S06 are used only in later validation and remain pinned to their official documentation snapshot.

## 26. Pilot decision record template without blank fields

The generated `decision.md` must contain:

- completed bound vector;
- model and code revision;
- exact language sizes;
- every set difference;
- `k_min` distribution as exact counts;
- strongest surviving theorem statement;
- strongest counterexample statement;
- chain-cover novelty check result;
- prior-art recheck result;
- one final decision: GO, NO-GO or PIVOT;
- rationale tied to the rules in Section 18.

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
````

## File: 05_EXPERIMENT_PLAN.md

````markdown
# Full Research Design and Experiment Plan

**Scope:** conditional plan after blocking pilot BP-TWINS-FC-01.  
**Main strategy:** formal trace refinement plus exact bounded model checking.  
**Reserve strategy:** counterexample-first separation analysis with concrete harness validation.  
**Statistical character:** core results are exact; no inferential statistics are used to establish completeness.

## 1. Mechanism chain

| Link | Status before study | What is implemented | What is measured or proved | Nearest confounder |
|---|---|---|---|---|
| Validator assumptions constrain accepted Byzantine messages | Established by S05 in its model; mapping to chosen protocol unproved | Explicit `Valid` predicate and accepted-message generator | Assumption conformance and `AB` versus `AE` bounded equality | `Valid` silently excludes real accepted behaviors |
| Abstract state equivocation branches correct local histories | Established abstractly by S05 | Dynamic state-copy machine `AE` | Trace embedding and unsafe observation language | State copy lifecycle differs from intended VLSM semantics |
| Finite clones realize causally consistent branches | New working mechanism | `AT(k)` with shared identity and concrete scheduler | `LT(k)` and witness realization | Scheduler or snapshot gives hidden extra power |
| Incompatible histories require separate clones | New formal claim | Causal-history extractor and incompatibility relation | `k_min`, width and lower-bound witnesses | Incompatibility relation is circularly defined from clone count |
| Sufficient clone count yields same honest observation | New central claim | Language comparator and constructive schedule extraction | Exact inclusion or separation | Observation is too coarse or too fine |
| Cross-protocol persistence indicates a class-level result | Unproved | Second and third formal protocol models | Same theorem statement without semantic repair | Result is toy-protocol-specific |
| Concrete harness follows formal clone semantics | Engineering assumption | Trace adapter for S21, S22 or S08 | Replay agreement and conformance deviations | Production harness has undocumented behavior |

Scientific inference is permitted only from links that are proved or exactly checked. A successful concrete replay cannot repair a failed formal inclusion; a formal theorem cannot by itself establish production harness conformance.

## 2. Distinguishing predictions

### P1 — Main prediction

There exists at least one bounded safety witness for which `k_min` is greater than two and is explained by a canonical incompatibility structure of faulty causal histories.

### P2 — Boundary prediction

Under `SnapshotDynamic`, every finite witness in the target validator class is realizable with finite `k`, while under `GenesisStatic` some witnesses require strictly larger `k` or are unrealizable at the same cap.

### P3 — Adversarial-condition prediction

Weakening message validation to accept a signed message not produced by any correct local history creates `AB` witnesses outside every finite correct-code clone language. This marks the boundary between validator faults and arbitrary implementation mutation.

### P4 — Strong-mechanism failure prediction

When the causal-width definition is replaced by a canonical minimum chain cover, either the same predictor explains every witness trivially or a valid witness violates the equality. In either case the strong original width mechanism fails unless a specifically BFT-dependent constraint remains.

### P5 — Transfer prediction

A surviving realization or separation condition applies without redefinition to both a Streamlet-like and a locking HotStuff-like model. If definitions must be changed, only protocol-specific contribution remains.

## 3. Prediction matrix

| Possible observation | Main finite-clone structural hypothesis | Two-clone sufficiency alternative | Generic chain-cover alternative | Harness-confound alternative |
|---|---|---|---|---|
| Strict `k=2` versus `k=3` unsafe-language growth and width equals 3 | Strong support | Refuted | Compatible; needs nontriviality test | Compatible if lifecycle differs |
| All unsafe witnesses realized by two clones | Weakens or refutes strong hierarchy | Strong support | Compatible with width at most 2 | Compatible |
| `k_min` always equals ordinary minimum chain cover | Mechanism may be mathematically correct but novelty weak | Not necessarily | Strong support | Weak support |
| Same abstract witness needs different `k` under lifecycle profiles | Supports boundary aspect, not universal width alone | Weakens universal two-clone claim | Chain cover insufficient | Strong support; may justify pivot to harness semantics |
| Valid abstract witness unrealizable under any finite `k` with dynamic snapshots | Refutes weak finite-realization claim | Refutes | Refutes simple chain cover | Supports fundamental lifecycle or semantic gap |
| Only malformed-message mutation produces unmatched witness | Validator claim survives | Compatible | Compatible | Indicates fault-model mismatch, not finite-clone science |
| Bounded equality but no invariant or strict hierarchy | Weak empirical support only | Compatible | Compatible | Compatible; scientifically ambiguous |
| Same theorem and counterexample schema on two protocol models | Strong support for class-level result | Could still hold if theorem is two-clone | Chain-cover novelty still must be killed | Weakens implementation-only explanation |
| Difference disappears when canonicalization bug is fixed | No support | No inference | No inference | Measurement error confirmed |
| Concrete harness fails formal replay while abstract model succeeds | Formal result survives; implementation claim fails | No direct inference | No direct inference | Strong support for conformance-gap pivot |

## 4. Interpretation map

### Strong confirmation

A theorem or compelling inductive invariant plus exact bounded evidence establishes a nontrivial necessary-and-sufficient finite-clone condition, a strict lower bound, or a separation family that transfers to a second protocol model.

### Weak confirmation

All completed bounds satisfy expected inclusion and width equality, but no nontrivial proof structure or witness beyond two clones exists. This is pilot evidence only.

### Ambiguous result

No unsafe abstract witness within completed bounds, incomplete state-space exploration, protocol-specific mismatch, or equality compatible with all alternatives.

### Refutation

A valid minimized counterexample violates claimed finite realization or width characterization under all stated assumptions.

### Measurement error signal

Language differences disappear when reductions are disabled, event canonicalization changes, or independently implemented oracle is used.

### Wrong adversary-model signal

Differences arise only from messages outside validator constraints or from asymmetric scheduler power.

### Pivot signal

Nontrivial separation is controlled by clone lifecycle, snapshot or scheduler capability rather than clone count alone.

## 5. What becomes known if the main hypothesis is false

A false strong hypothesis can still yield one of four scientific results:

1. a minimal counterexample to finite-clone realization despite abstract validator equivocation;
2. a proof that no fixed protocol-independent clone cutoff exists;
3. a necessary capability theorem for snapshot, replayable nondeterminism or clone-specific delivery;
4. a precise boundary showing that production Twins covers only state-equivocation faults, while message mutation forms a strictly stronger fault model.

Therefore a negative outcome is not merely absence of metric improvement. It identifies the expressiveness boundary of a widely used testing abstraction.

## 6. Comparison of research strategies

| Strategy | What it can verify | What it cannot verify | Tools | False-conclusion risk | Cost | Scalability | Reproducibility | Decision |
|---|---|---|---|---|---|---|---|---|
| Analytic proof | Unbounded theorem, necessary/sufficient conditions | Discovery of hidden counterexamples if definitions wrong | Paper proof, optional Coq | Vacuous assumptions or missed case | Medium to high | Best if theorem found | High with proof artifact | Core after pilot |
| Theorem proving | Machine-check lemmas and refinement | Practical harness behavior | Coq, S06 patterns | Large modeling overhead and trusted extraction gap | High | Limited by proof effort | Very high | Reserve after theorem stabilizes |
| Explicit model checking | Exact bounded languages, minimal counterexamples and `k_min` | Unbounded generalization | Python explorer | State explosion and implementation bugs | Low to medium | Small models only | High | **Primary pilot method** |
| SMT bounded checking | Larger symbolic bounds, witness synthesis | Unbounded proof and concrete harness fidelity | Z3 5.0.0 | Encoding unsoundness or solver model misread | Medium | Better on constraints, worse on rich data | High with pinned solver | Reserve backend |
| Protocol simulation | Performance and randomized schedules | Completeness or proof of absence | Custom simulator | Sampling bias | Medium | Moderate | Medium-high | Secondary only |
| Local multi-node prototype | Harness conformance and implementation realism | General theorem | S21, S22, S08 | Implementation confounds | Medium-high | Few nodes | Medium | Conditional validation |
| Differential testing | Compare formal and concrete traces | Determine which semantics is correct alone | Trace adapters | Shared bug or oracle mismatch | Medium | Moderate | High | Secondary conformance test |
| Fuzzing | Discover deep concrete executions | Prove completeness | ByzzFuzz, Hypothesis | Coverage mistaken for proof | Medium | High scenario count | Medium-high | Not central |
| Trace analysis | Minimize and classify witnesses | Establish unbounded inclusion alone | Custom DAG analysis | Causal model error | Low-medium | Good after traces exist | High | Core analysis support |
| Synthetic workloads | Controlled branch patterns | Real-world prevalence | Generated schedules | Toy bias | Low | High | Very high | Appropriate for mechanism tests |
| Measurement study | Harness overhead or frequency | Central formal claim | Profiling | Performance distraction | Medium | Moderate | High | Out of primary contribution |

**Chosen strategy:** analytic refinement or separation theorem supported by exact explicit-state exploration.  
**Reserve strategy:** minimized counterexample family plus lifecycle-conformance study if a general positive theorem fails.

This is minimal but sufficient because the central claim is a relation between trace languages. A production testnet cannot establish that relation, whereas a small executable semantics can falsify it and generate proof obligations.

## 7. Summary experiment matrix

| ID | Claim | Main method | Decisive result | Dependency |
|---|---|---|---|---|
| E0 | Definitions are consistent and non-vacuous | Definition audit and examples | Valid accepted traces plus rejected counterexamples | Gate 0 |
| E1 | `AB` and `AE` coincide on bounded honest observations | Exact model checking | Equality or mapped discrepancy | E0 |
| E2 | Fixed-`k` languages form meaningful hierarchy | Exact sweep over `k` | Strict inclusion or collapse | E1 |
| E3 | Structural width predicts `k_min` | Causal DAG analysis and proof search | Equality, bound or counterexample | E2 |
| E4 | Assumptions are necessary or sufficient | Controlled semantic ablations | Minimal counterexample per assumption | E1–E3 |
| E5 | Lifecycle and scheduler alter expressiveness | Harness-profile comparison | Separation between profiles | E2 |
| E6 | Result transfers across protocol models | Cross-protocol formal validation | Same statement survives | E3–E5 |
| E7 | Concrete harness conforms to formal `AT(k)` | Differential trace replay | Match or classified conformance gap | E6 |
| E8 | Result is robust to bounded parameters | Exact sensitivity sweep | Stable schema or boundary map | E3 |
| E9 | Counterexamples and reductions are trustworthy | Independent minimization and regression | Reproducible minimal witness | All prior |
| E10 | Main theorem or separation is mechanizable | Proof development | Checked core lemmas or explicit proof limit | E3–E6 |

## 8. Detailed experiment cards

### E0 — Definition consistency audit

1. **Claim:** `Valid`, `AB`, `AE`, `AT(k)` and observations define distinct, internally consistent machines.  
2. **Research question:** Are assumptions explicit and does the target protocol class contain a nontrivial locking protocol?  
3. **Setup:** hand-constructed positive and negative traces, machine-readable transition tests.  
4. **Baselines and alternatives:** VLSM terminology S05; I/O automata external traces S28.  
5. **Controlled factors:** one protocol, one identity map, fixed signature abstraction.  
6. **Interventions:** toggle each validity subpredicate.  
7. **Workloads or traces:** minimal one-message, one-certificate and conflicting-message traces.  
8. **Fault conditions:** valid equivocation, invalid forgery and impossible state claim.  
9. **Metrics or properties:** enabled-transition sets, acceptance decisions and nonempty safe/unsafe reachability.  
10. **Expected main result:** all intended examples classify uniquely.  
11. **Expected alternatives:** ambiguity exposes underspecified model.  
12. **Falsifier:** same trace both accepted and rejected under supposedly identical state; empty validator class.  
13. **Analysis:** manual derivation plus unit tests.  
14. **Artifacts:** definition table, executable examples, tests.  
15. **Dependencies:** Gate 0 source audit.  
16. **Compute:** negligible.  
17. **Risk:** validity oracle becomes circular.  
18. **Positive contribution:** reliable foundation only, not publishable alone.  
19. **Negative contribution:** early rejection of vacuous topic.  
20. **Decision:** must pass before any exhaustive experiment.

### E1 — Byzantine versus dynamic equivocation sanity

1. **Claim:** bounded honest observations of `AB` and `AE` match for the toy validator model.  
2. **Question:** Is the local instantiation consistent with S05?  
3. **Setup:** exact enumeration under same bound vector.  
4. **Baseline:** S05 theoretical equality.  
5. **Controls:** identical protocol, validity, scheduler and observation.  
6. **Intervention:** adversary model only.  
7. **Traces:** all bounded traces.  
8. **Faults:** accepted-message equivocation.  
9. **Property:** exact language equality.  
10. **Expected main:** equality after canonical projection.  
11. **Alternative:** discrepancy reveals mapping or model error.  
12. **Falsifier:** minimized accepted trace present in only one language.  
13. **Analysis:** set difference and trace replay.  
14. **Artifacts:** language hashes and unmatched traces.  
15. **Dependency:** E0.  
16. **Compute:** small to medium.  
17. **Risk:** finite generator incompleteness.  
18. **Positive value:** validates foundation.  
19. **Negative value:** identifies why S05 assumptions do not map.  
20. **Decision:** no further completeness claim until equality or justified refinement direction is established.

### E2 — Fixed-clone hierarchy

1. **Claim:** `LT(k)` may strictly grow with `k`, and some unsafe witness requires more than two clones.  
2. **Question:** Does clone cap create a nontrivial expressive hierarchy?  
3. **Setup:** enumerate `AT(k)` for increasing `k` at completed bounds.  
4. **Baselines:** `k=1`, common `k=2`, unbounded `AE`.  
5. **Controls:** lifecycle, scheduler, protocol and observation fixed.  
6. **Intervention:** increment `k` by one.  
7. **Traces:** all bounded executions.  
8. **Faults:** equivocation and selective delivery.  
9. **Metrics:** strict language inclusion, `missing(k)`, `k_min`.  
10. **Expected main:** at least one strict step beyond two or a principled collapse theorem.  
11. **Alternatives:** two-clone sufficiency or no finite realization.  
12. **Falsifier:** hierarchy predicted by mechanism does not appear in decisive witness space.  
13. **Analysis:** exact set lattice and minimal witnesses.  
14. **Artifacts:** `k_min.csv`, trace families and figures.  
15. **Dependency:** E1.  
16. **Compute:** medium to high.  
17. **Risk:** state explosion.  
18. **Positive value:** establishes object worth theorizing.  
19. **Negative value:** two-clone sufficiency or separation is itself a possible theorem.  
20. **Decision:** proceed only if result is nontrivial and prior-art-safe.

### E3 — Causal-width characterization

1. **Claim:** a canonical causal-history width predicts or bounds `k_min`.  
2. **Question:** What structural quantity controls clone number?  
3. **Setup:** extract witness DAG and compute competing predictors.  
4. **Baselines:** action count, number of recipients, binary equivocation count and ordinary minimum chain cover.  
5. **Controls:** same witness and observation.  
6. **Intervention:** vary trace structure through generated diagnostic witnesses.  
7. **Traces:** all minimal unsafe witnesses plus synthetic branch families.  
8. **Faults:** two-way, three-way and merge-attempt equivocation.  
9. **Metrics:** exact prediction error and theorem obligations.  
10. **Expected main:** one protocol-semantic quantity exactly characterizes or tightly bounds `k_min`.  
11. **Alternatives:** chain cover explains all; two clones; lifecycle dominates.  
12. **Falsifier:** valid witness violates proposed bound.  
13. **Analysis:** exhaustive comparison, proof construction and counterexample minimization.  
14. **Artifacts:** DAG renderer, predictor table, theorem draft.  
15. **Dependency:** E2.  
16. **Compute:** low after traces generated.  
17. **Risk:** circular definition.  
18. **Positive value:** central scientific claim.  
19. **Negative value:** a counterexample establishes limit of structural abstraction.  
20. **Decision:** no novelty if ordinary chain cover is the full result.

### E4 — Assumption ablations

1. **Claim:** determinism, validator validity, causal disclosure and replayable choices have separable roles.  
2. **Question:** Which assumptions are necessary and which merely convenient?  
3. **Setup:** one semantic change at a time.  
4. **Baselines:** full target model.  
5. **Controls:** all other semantics fixed.  
6. **Interventions:** hide choice, weaken validity, remove justification, permit state merge, disable snapshot.  
7. **Traces:** matched diagnostic families.  
8. **Faults:** invalid-state claim and hidden nondeterminism.  
9. **Metrics:** first separating witness and changed `k_min`.  
10. **Expected main:** each essential condition has a minimal counterexample when removed.  
11. **Alternatives:** condition irrelevant inside class or duplicate of another.  
12. **Falsifier:** claimed necessary condition can be removed without semantic effect across completed bounds and proof argument.  
13. **Analysis:** exact differential semantics.  
14. **Artifacts:** ablation matrix and minimized traces.  
15. **Dependency:** E1–E3.  
16. **Compute:** medium.  
17. **Risk:** multiple changes accidentally bundled.  
18. **Positive value:** necessary/sufficient characterization.  
19. **Negative value:** simplifies theorem assumptions.  
20. **Decision:** retain only assumptions with formal role.

### E5 — Lifecycle and scheduler boundary

1. **Claim:** `GenesisStatic` and `SnapshotDynamic` have different finite-`k` expressiveness for some witnesses.  
2. **Question:** Is operational harness capability the real boundary?  
3. **Setup:** same protocol and witness language under two profiles.  
4. **Baselines:** dynamic abstract equivocation.  
5. **Controls:** clone cap and scheduler power.  
6. **Interventions:** allow snapshot, restore, late clone start and clone-specific delivery individually.  
7. **Traces:** witnesses with long shared prefixes and late branching.  
8. **Faults:** delayed branch creation.  
9. **Metrics:** profile-specific `k_min` and realizability.  
10. **Expected main:** precise capability hierarchy.  
11. **Alternatives:** profiles equivalent for safety observations.  
12. **Falsifier:** no difference and no proof reason for a boundary.  
13. **Analysis:** paired exact language comparison.  
14. **Artifacts:** capability lattice and witness suite.  
15. **Dependency:** E2.  
16. **Compute:** medium.  
17. **Risk:** profile definition unrealistic.  
18. **Positive value:** practical harness design theorem.  
19. **Negative value:** removes unnecessary implementation complexity.  
20. **Decision:** pivot here if clone-count theorem collapses but lifecycle separation survives.

### E6 — Cross-protocol validation

1. **Claim:** surviving theorem or separation applies to more than one toy semantics.  
2. **Question:** Is result protocol-class-level?  
3. **Setup:** Streamlet-like and HotStuff-like formal models.  
4. **Baselines:** toy locking model.  
5. **Controls:** same adversary definitions and observations.  
6. **Intervention:** protocol family.  
7. **Workloads:** diagnostic witness patterns adapted only through message constructors.  
8. **Faults:** same equivocation classes.  
9. **Metrics:** theorem assumption satisfaction, hierarchy and witness transfer.  
10. **Expected main:** same statement holds or same separation schema appears.  
11. **Alternatives:** result depends on one lock rule.  
12. **Falsifier:** definitions require protocol-specific repair.  
13. **Analysis:** trace-language comparison and assumption mapping.  
14. **Artifacts:** two model modules and mapping table.  
15. **Dependency:** E3–E5 and pilot GO.  
16. **Compute:** high.  
17. **Risk:** scope expansion.  
18. **Positive value:** external validity and publication strength.  
19. **Negative value:** explicit boundary to one protocol class.  
20. **Decision:** at least one independent model required for publication claim beyond toy result.

### E7 — Concrete harness conformance

1. **Claim:** one open Twins implementation realizes selected formal profile.  
2. **Question:** Does concrete behavior match `AT(k)` at trace level?  
3. **Setup:** adapter to S21, S22 or S08 on matched small scenarios.  
4. **Baselines:** formal trace generator.  
5. **Controls:** protocol parameters, schedule and clone count.  
6. **Intervention:** formal versus concrete execution.  
7. **Traces:** selected safe and unsafe witnesses.  
8. **Faults:** equivocation, double vote and late branch scenarios supported by artifact.  
9. **Metrics:** event correspondence, decision equality and unexplained divergence.  
10. **Expected main:** formal witnesses replay or divergences map to documented harness limits.  
11. **Alternatives:** implementation adds or loses behaviors.  
12. **Falsifier:** systematic mismatch invalidates practical interpretation.  
13. **Analysis:** differential trace normalization.  
14. **Artifacts:** adapters, pinned commits and conformance report.  
15. **Dependency:** E6.  
16. **Compute:** medium.  
17. **Risk:** integration cost dominates.  
18. **Positive value:** practical relevance, not core novelty.  
19. **Negative value:** conformance-gap pivot or restrained systems claim.  
20. **Decision:** may be omitted from minimum paper if theorem is strong and integration unavailable, but then no production-harness claim is allowed.

### E8 — Parameter sensitivity

1. **Claim:** result is structural, not one parameter accident.  
2. **Question:** How does `k_min` change with rounds, values, quorum and identity count?  
3. **Setup:** exact feasible parameter grid.  
4. **Baselines:** pilot configuration.  
5. **Controls:** one factor at a time where possible.  
6. **Interventions:** bound and protocol parameters.  
7. **Traces:** all bounded executions.  
8. **Faults:** target equivocation patterns.  
9. **Metrics:** cutoff map and first-separation frontier.  
10. **Expected main:** theorem-predicted monotonic or bounded behavior.  
11. **Alternatives:** irregular implementation-driven pattern.  
12. **Falsifier:** parameter change violates derived theorem.  
13. **Analysis:** exact tables, no significance tests.  
14. **Artifacts:** parameter manifest and generated figures.  
15. **Dependency:** E3.  
16. **Compute:** high; bounded by resource policy.  
17. **Risk:** combinatorial explosion.  
18. **Positive value:** robustness.  
19. **Negative value:** locates applicability boundary.  
20. **Decision:** incomplete cells explicitly marked, never imputed.

### E9 — Counterexample minimization and regression

1. **Claim:** decisive witnesses are genuine and minimal under declared order.  
2. **Question:** Can another implementation reproduce and shrink them?  
3. **Setup:** delta debugging, independent replay and reduction-disabled runs.  
4. **Baselines:** original witness.  
5. **Controls:** safety observation fixed.  
6. **Interventions:** remove events, rounds, messages or clones.  
7. **Traces:** every decisive unmatched or lower-bound witness.  
8. **Faults:** inherited.  
9. **Metrics:** minimal event, round and clone counts.  
10. **Expected main:** stable minimal witness.  
11. **Alternatives:** mismatch disappears as artifact.  
12. **Falsifier:** independent checker cannot reproduce.  
13. **Analysis:** deterministic minimization and manual derivation.  
14. **Artifacts:** regression corpus and human-readable proof trace.  
15. **Dependency:** all decisive experiments.  
16. **Compute:** low to medium.  
17. **Risk:** minimizer changes semantic class.  
18. **Positive value:** trustworthy counterexample evidence.  
19. **Negative value:** catches false conclusions early.  
20. **Decision:** no counterexample enters paper without E9.

### E10 — Proof and mechanization route

1. **Claim:** core result can be stated and checked independently of explorer implementation.  
2. **Question:** Which proof obligations can be mechanized within scope?  
3. **Setup:** theorem draft; optional Coq development using S06 concepts.  
4. **Baselines:** manual proof and bounded evidence.  
5. **Controls:** same definitions.  
6. **Intervention:** mechanize core lemmas incrementally.  
7. **Workload:** embedding, decomposition, schedule realization and lower bound.  
8. **Faults:** not an empirical condition.  
9. **Property:** proof checker acceptance.  
10. **Expected main:** at least embedding and key finite theorem checked or exhaustively justified.  
11. **Alternatives:** mechanization cost exceeds value; publish manual theorem plus executable model.  
12. **Falsifier:** proof requires an unstated assumption or theorem cannot be formulated non-vacuously.  
13. **Analysis:** proof dependency audit.  
14. **Artifacts:** proof files or formal proof appendix.  
15. **Dependency:** stable E3–E6 result.  
16. **Compute:** low, human effort high.  
17. **Risk:** proof assistant learning dominates.  
18. **Positive value:** stronger formal-methods contribution.  
19. **Negative value:** exposes hidden assumptions.  
20. **Decision:** full mechanization is stretch; core theorem clarity is mandatory.

## 9. Baselines, controls and ablations checklist

Mandatory:

- no-fault correct execution baseline;
- dynamic state-equivocation baseline;
- `k=1` and `k=2` clones;
- unrestricted finite realization upper-bound construction;
- same scheduler and observation across models;
- reductions off at tiny bounds;
- one independent safety oracle implementation;
- determinism, validity, causal evidence, snapshot and scheduler ablations;
- parameter sensitivity;
- cross-protocol validation;
- counterexample regression corpus.

Conditional:

- ByzzFuzz mutation comparator;
- concrete HotStuff or Twins artifact replay;
- SMT backend;
- Coq mechanization.

## 10. Statistical plan

The decisive experiments enumerate finite state spaces exactly. Therefore:

- unit of observation is a canonical bounded trace observation, not a random run;
- observations are not treated as independent samples;
- no random seeds enter the main set-inclusion result;
- no confidence intervals or hypothesis tests are used for exact counts;
- no multiple-comparison correction is needed;
- practical significance is determined by whether a witness changes coverage interpretation or required harness capabilities.

If optional randomized fuzzing is used for engineering discovery, it is reported separately with fixed seeds, run counts, confidence intervals for discovery probability and no inference about completeness.

## 11. Formal-methods execution plan

- **Specification language:** executable typed Python model for discovery; mathematical LTS specification in Markdown and paper; optional Coq for stable lemmas.
- **Properties:** agreement, language inclusion, refinement, finite-clone realizability and lower bound.
- **State-space bounds:** explicitly recorded tuple of identities, rounds, values, messages, local steps and clones.
- **Abstraction:** signatures as ideal authentication; certificates as canonical signer sets; payloads as finite values.
- **Symmetry reduction:** correct-identity and value renaming.
- **Partial-order reduction:** only independently delivered events with preservation tests.
- **Proof obligations:** listed in `03_FORMAL_MODEL.md`.
- **Counterexample interpretation:** unmatched canonical correct-node observation, followed by manual semantic derivation.
- **Model-to-implementation link:** E7 trace adapter, not assumed.
- **Transfer limitation:** bounded evidence does not prove unbounded theorem; toy protocol evidence does not imply production coverage.

## 12. Experiment dependency graph and stopping policy

Critical experimental path:

`E0 → E1 → E2 → E3 → E4/E5 → E6 → E9 → E10`.

E7 is conditional after E6. E8 runs after E3 when a candidate theorem exists.

Stop immediately when:

- E0 reveals vacuous class;
- E1 contradicts the claimed S05 mapping without a justified repair;
- E2 produces only trivial behavior and Gate 0 confirms no novelty;
- E3 collapses entirely to known chain-cover theory;
- exact prior art resolves the same question;
- state-space incompleteness prevents the decisive comparison and no proof-first route exists.

Proceed to publication package only after E9 validates every decisive witness and E6 establishes at least one independent model or a clearly scoped theorem class.

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
````

## File: 06_IMPLEMENTATION_SPEC.md

````markdown
# Implementation Specification

**Artifact name:** `twinsbound`  
**Purpose:** executable formal model and exact bounded checker for comparing accepted-message Byzantine behavior, dynamic state equivocation and finite-clone Twins behavior.  
**Status:** architecture ready for blocking pilot; full implementation conditional on Gate 0 and Gate 1.

## 1. Artifact purpose and non-purpose

The artifact must answer exact semantic questions:

- which correct-node observations are reachable under each adversary model;
- whether one observation language includes another;
- minimum clone cap needed to reproduce an abstract-equivocation witness;
- which assumption or harness capability explains an unmatched trace.

It is not:

- a new blockchain client;
- a production consensus implementation;
- a high-throughput simulator;
- a mainnet attack tool;
- a general-purpose fuzzer;
- a performance benchmark;
- a dashboard or hosted service.

## 2. Architecture

The architecture has seven layers:

1. **Pure protocol semantics** — immutable local states, messages, transition function and validation.
2. **Adversary semantics** — correct, accepted-message Byzantine, dynamic equivocation, finite-clone and optional mutation models.
3. **Execution engine** — enabled-event generation, state transition and bounded exploration.
4. **Canonicalization and reduction** — symmetry, causal normalization and partial-order reduction.
5. **Oracles** — safety, observation projection, language inclusion and minimum-clone search.
6. **Analysis** — witness minimization, causal-history extraction, width predictors and decision rules.
7. **Adapters** — optional import/export to S21, S22, S08 and S06.

The core remains single-process and deterministic. Parallel search may be added only after correctness is established because parallel enumeration complicates reproducibility and state deduplication.

## 3. Components and responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| `model.types` | Frozen data types for identity, state, message, event and observation | Contain protocol-specific rules |
| `model.causality` | Dependency DAG, histories and incompatibility operations | Infer validity from implementation logs |
| `protocols.base` | Protocol interface and transition contracts | Schedule network events |
| `protocols.toy_locking` | Minimal pilot protocol | Encode adversary shortcuts |
| `protocols.streamlet_like` | Post-pilot independent model | Change common observation definitions |
| `protocols.hotstuff_like` | Conditional validation model | Depend on production client internals |
| `adversaries.correct` | No-process-fault baseline | Mutate messages |
| `adversaries.byzantine` | Accepted-message abstract generator | Emit messages rejected by declared `Valid` |
| `adversaries.equivocation` | Dynamic state-copy semantics | Impose finite clone cap |
| `adversaries.twins_k` | Concrete finite-clone lifecycle and scheduler | Execute non-protocol transitions |
| `adversaries.mutation` | Optional stronger comparator | Enter main coverage theorem |
| `engine.enabled` | Enumerate enabled semantic events | Canonicalize observations |
| `engine.step` | Apply one event and verify invariants | Hide invalid transitions |
| `engine.explorer` | BFS or layered DFS under explicit bounds | Treat partial search as complete |
| `engine.store` | Deduplicate canonical global states | Merge states without preservation proof |
| `oracle.safety` | Detect agreement violation | Use model-specific clone internals |
| `oracle.observation` | Project correct-node observable semantics | Include physical clone IDs |
| `oracle.language` | Compute exact inclusion and differences | Estimate set inclusion statistically |
| `analysis.minimize` | Delta-debug decisive traces | Change observation class silently |
| `analysis.width` | Extract competing structural predictors | Define width using already known `k_min` |
| `analysis.decision` | Apply predeclared GO, NO-GO, PIVOT rules | Override rules for a preferred outcome |
| `adapters` | Concrete artifact conformance and trace normalization | Become a required core dependency |

## 4. Interfaces

### 4.1. Protocol interface

A protocol module supplies:

```text
initial_local_state(identity, config) -> LocalState
validate(recipient, local_state, message, context) -> ValidationResult
step(actor, local_state, input_event, context) -> TransitionResult
observe_local(local_state) -> LocalObservation
is_value_compatible(value_a, value_b) -> bool
```

`TransitionResult` contains new state, emitted messages and disclosed causal dependencies. It is a pure value; no network I/O or global mutation is permitted.

### 4.2. Adversary interface

```text
initial_adversary_state(protocol, config) -> AdversaryState
enabled_actions(global_state, bounds) -> iterable of AdversaryAction
apply_action(global_state, action) -> GlobalState
profile_metadata() -> Mapping
```

Every action must identify semantic authority: scheduler action, correct local step, abstract message production, state copy or clone lifecycle.

### 4.3. Explorer interface

```text
explore(model, bounds, reductions, sink) -> ExplorationSummary
```

The summary must state whether enumeration is complete, which bound frontier was reached, number of unique states, number of transitions, unsafe observations and termination reason.

### 4.4. Oracle interface

```text
project(trace_or_state, observation_profile) -> CanonicalObservation
violates_safety(observation) -> SafetyResult
compare_languages(left_manifest, right_manifest) -> LanguageDifference
minimum_clone(witness, clone_range, profile) -> CloneSearchResult
```

## 5. Data model

### 5.1. Immutable identifiers

All identities, messages, events and states receive deterministic content hashes. Hashes are conveniences for storage and comparison; semantic equality is defined by canonical serialized content, not collision-prone assumptions.

### 5.2. Message record

Contains:

- schema version;
- protocol identity of sender;
- message type;
- round;
- value identifier;
- justification identifiers;
- disclosed choice;
- abstract signature token;
- payload fields;
- causal dependency identifiers.

### 5.3. Event record

Contains:

- trace-local event number;
- event kind;
- actor or recipient;
- clone identifier only in internal execution record;
- input message identifier;
- emitted-message identifiers;
- pre-state and post-state hashes;
- direct causal parents;
- semantic rule identifier.

### 5.4. Observation record

Contains only declared correct-node states, accepted certificates, decisions and delivered evidence. Internal clone IDs are replaced by shared protocol identity.

## 6. File formats

- **TOML:** human-authored configurations, parsed by Python standard library `tomllib`.
- **JSON Lines:** event traces and witness corpora; one deterministic record per line.
- **JSON:** exploration summary, environment and manifests.
- **CSV:** language sizes, parameter matrices, `k_min` tables and ablation results.
- **Markdown:** decision memos, proof sketches and human-readable witness explanation.
- **Graphviz DOT:** optional causal DAG rendering; source DOT is canonical, rendered images are derived.
- **Coq source:** optional proof development after theorem stabilization.

Every format contains a schema version. A migration script is required before breaking a stored schema.

## 7. Configuration schema

`configs/pilot.toml` contains:

```text
schema_version = 1
experiment_id = "BP-TWINS-FC-01"
protocol = "toy_locking"
identities = 4
byzantine_identities = 1
values = 2
round_bound = 4
delivery_bound = 24
local_step_bound = 32
certificate_bound = 8
clone_caps = "1,2,3,4"
observation_profile = "safety_state"
clone_profile = "genesis_static"
search_order = "breadth_first"
symmetry_reduction = true
partial_order_reduction = true
stop_after_complete_bound = true
```

Numerical defaults are not scientific thresholds. Before execution they are derived from protocol emission rules and minimum decision depth, then recorded in `decision.md`. If the minimum unsafe witness requires a larger bound, the configuration is versioned rather than edited in place.

## 8. Logging and observability

### 8.1. Human logs

Structured text records:

- phase start and finish;
- active configuration hash;
- completed frontier;
- resource use;
- reduction statistics;
- invariant violations;
- incomplete-search reason.

### 8.2. Machine logs

JSON event logs include exact timestamps only for operational diagnostics. Timestamps never enter semantic equality.

### 8.3. Progress reporting

Progress is based on completed BFS layers and canonical states, not estimated percentage. Explorer must never print “complete” when a resource cap stopped enumeration.

## 9. Error handling

Error classes:

- configuration error;
- invalid protocol transition;
- invalid adversary action;
- canonicalization collision or nondeterminism;
- bound overflow;
- resource exhaustion;
- schema mismatch;
- external-adapter mismatch;
- proof or invariant violation.

Policy:

- semantic errors stop the run immediately;
- resource exhaustion writes an incomplete manifest and exits nonzero;
- external adapter failures do not invalidate core results but block practical-conformance claims;
- no exception is converted into an empty language.

## 10. Reproducibility mechanism

- `.python-version` pins Python 3.14.7;
- `pyproject.toml` pins direct dependencies;
- `uv.lock` pins the resolved graph;
- `environment.json` records OS, architecture, CPU, RAM, Python, uv and optional solver versions;
- every run stores Git commit and dirty-tree status;
- configuration and source hashes are embedded in result manifests;
- exploration order is deterministic;
- generated figures are recreated from committed CSV or JSON;
- raw traces are immutable;
- processed outputs name their raw-manifest dependency;
- external repos are recorded by commit hash, license and local patch checksum.

## 11. Test strategy

### 11.1. Unit tests

- local transition rules;
- message validity;
- certificate construction;
- event causality;
- safety oracle;
- observation projection;
- canonical serialization.

### 11.2. Property-based tests

Using S24 only for software validation:

- canonicalization idempotence;
- identity-renaming invariance;
- value-renaming invariance;
- `AT(k)` language monotonicity in `k` within same profile;
- every finite-clone trace embeds into dynamic equivocation;
- replay of serialized trace yields same observation.

Property-based tests do not establish the research theorem.

### 11.3. Metamorphic tests

- adding an undelivered message does not change `ObsDecision`;
- renaming physical clone IDs does not change observation;
- disabling reductions yields same tiny-bound languages;
- expanding a bound cannot remove a previously reachable observation;
- increasing clone cap cannot reduce finite-clone language.

### 11.4. Differential tests

- two independent safety-oracle implementations;
- two serializers produce identical semantic hashes;
- optional Python versus SMT witness check;
- formal trace versus S21, S22 or S08 adapter.

### 11.5. Regression corpus

Every decisive counterexample is committed as minimized JSONL plus a human derivation and a test asserting its classification.

## 12. Trusted computing base

Scientific trust depends on:

1. protocol transition implementation;
2. message-validity predicate;
3. adversary semantics;
4. canonicalizer and reductions;
5. observation projection;
6. safety oracle;
7. set-comparison code;
8. Python runtime and standard-library serialization.

Hypothesis, pytest, uv, plotting tools and external Twins implementations are outside the semantic TCB. Z3 joins the TCB only for results it decides; therefore all decisive solver witnesses must be replayed concretely.

## 13. External dependencies and licenses

| Tool or artifact | Purpose | Official status on 11 Aug 2026 | License | Maturity | Limitations | Simpler fallback |
|---|---|---|---|---|---|---|
| Python 3.14.7, S23 | Core implementation | Official maintenance release, 5 Aug 2026 | PSF | High | New patch line may not be installed on all systems | Python 3.13 pinned after compatibility test |
| uv, S26 | Environment and lockfile | Official Astral docs, universal lockfile | Apache-2.0 or MIT dual project licensing as distributed | High and actively maintained | Exact CLI version must be recorded; lock format uv-specific | Standard `venv` plus hashed requirements export |
| pytest 9.1.1, S25 | Test runner | Official stable changelog, 19 Jun 2026 | MIT | High | Major-version deprecations; avoid private APIs | Standard-library `unittest` |
| Hypothesis 6.165.3, S24 | Property-based software tests | Official PyPI, 11 Aug 2026 | MPL-2.0 | High | Not a formal proof and may find only sampled cases | Exhaustive tiny-domain generators |
| Z3 5.0.0, S27 | Optional symbolic backend | Official release, 17 Jul 2026 | MIT | High but recent release has publicly reported edge-case issues | Never accept `unknown`; set timeout; replay models; avoid experimental parallel mode | Explicit enumeration or stable earlier pinned solver after audit |
| VLSM repo, S06 | Prior-art verification and optional Coq reuse | 325 commits; Coq 8.16+; recommended 8.18 | BSD-3-Clause | Research-grade formal library | Nontrivial Coq learning cost; abstract model not concrete harness | Manual theorem plus executable Python model |
| twins-simulator, S21 | External scenario replay | Small research repo; Streamlet and Fast-HotStuff | Apache-2.0 | Research prototype | Research-only, limited maintenance and scope | Internal formal models |
| relab/hotstuff, S22 | HotStuff conformance validation | Active framework, 1,849 commits, Go 1.18+ | MIT | Mature research framework | Complex production-style code and instrumentation gap | S21 or ByzzBench |
| ByzzBench, S08 | Controlled BFT testing baseline | Peer-reviewed tool paper and MIT repository | MIT | Early but purpose-built | Preliminary Twins integration; benchmark semantics may differ | Internal adapter and toy model |
| Graphviz | Derived DAG figures | Version fixed at Gate 2 | EPL-1.0 | Mature | Rendering nondeterminism across versions | Plain DOT and textual DAG tables |
| Coq 8.18 | Optional proof assistant matching S06 recommendation | Official ecosystem version required by pinned opam switch | LGPL family for Coq distribution | Mature | High human cost | Manual proof with checked executable lemmas |

## 14. Verified setup commands

The following commands were checked against official documentation available on 11 August 2026. Exact binary versions must still be recorded in the repository environment report.

### 14.1. Create project and dependencies

```text
mkdir twinsbound
cd twinsbound
uv init
uv add --dev pytest==9.1.1 hypothesis==6.165.3
uv lock
uv sync
uv run pytest
```

`uv init`, `uv add`, `uv lock`, `uv sync` and `uv run` are documented by S26. Python version is then pinned by setting `.python-version` to `3.14.7` and `requires-python` to the intended compatible range. The project must not rely on an unverified `uv init --python` variation.

### 14.2. Build VLSM formalization for independent prior-art inspection

Official S06 commands:

```text
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq.8.18.0 coq-stdpp.1.9.0 coq-itauto coq-equations
git clone https://github.com/runtimeverification/vlsm.git
cd vlsm
make
```

Before use, replace the floating repository state with a recorded commit checkout. The listed commands verify buildability of S06, not integration with `twinsbound`.

### 14.3. Twins simulator external validation

Official S21 commands:

```text
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest
pytest
python scripts/twins_executor.py scripts/test_scenarios.json
```

These commands belong to external validation only. The main project continues to use uv and does not copy S21 environment uncritically.

### 14.4. relab HotStuff validation

Official S22 minimum commands and requirements:

```text
make
./hotstuff help run
```

Go 1.18 or later is required. Exact experiment command must be selected from the repository documentation at the pinned commit; no unverified command is specified here.

## 15. Repository structure

```text
twinsbound/
  .python-version
  pyproject.toml
  uv.lock
  LICENSE
  CITATION.cff
  README.md
  spec/
    definitions.md
    assumptions.md
    theorem_targets.md
    observation_profiles.md
  src/
    twinsbound/
      model/
        types.py
        causality.py
        canonical.py
      protocols/
        base.py
        toy_locking.py
        streamlet_like.py
        hotstuff_like.py
      adversaries/
        correct.py
        byzantine.py
        equivocation.py
        twins_k.py
        mutation.py
      engine/
        enabled.py
        step.py
        explorer.py
        reductions.py
        store.py
      oracle/
        safety.py
        observation.py
        language.py
      analysis/
        minimize.py
        width.py
        decision.py
        render.py
      adapters/
        twins_simulator.py
        relab_hotstuff.py
        byzzbench.py
  configs/
    pilot.toml
    ablations/
    protocols/
  experiments/
    e0_definition_audit.py
    e1_byzantine_equivocation.py
    e2_clone_hierarchy.py
    e3_width.py
    e4_ablations.py
    e5_lifecycle.py
    e6_cross_protocol.py
    e7_conformance.py
    e8_sensitivity.py
  tests/
    unit/
    property/
    metamorphic/
    differential/
    regression/
  data/
    manifests/
    external/
  results/
    raw/
    processed/
    pilot/
  figures/
    source/
    rendered/
  proof/
    manual/
    vlsm/
  notebooks/
    exploratory_only/
  containers/
    Dockerfile
    compose.yaml
  docs/
    artifact_evaluation.md
    disclosure.md
    limitations.md
  scripts/
    run_pilot.py
    run_all.py
    verify_manifest.py
    make_figures.py
    report_environment.py
  third_party/
    README.md
```

Notebooks are explicitly non-authoritative. Every final result must be generated by versioned scripts.

## 16. Main exploration pseudocode

```text
procedure Explore(model, bounds, reductions):
    initial = Canonicalize(model.initial_state())
    frontier = queue containing initial
    seen = map initial to empty predecessor
    observations = empty set
    unsafe_witnesses = empty map

    while frontier is not empty:
        state = frontier.pop_front()
        observation = ProjectSafety(state)
        observations.add(observation)

        if ViolatesAgreement(observation):
            witness = ReconstructTrace(seen, state)
            unsafe_witnesses.keep_smallest(observation, witness)

        if AtBound(state, bounds):
            continue

        actions = model.enabled_actions(state)
        actions = ReductionsFilter(state, actions, reductions)

        for action in DeterministicOrder(actions):
            next_state = model.apply(state, action)
            AssertSemanticInvariants(state, action, next_state)
            canonical = Canonicalize(next_state)
            if canonical not in seen:
                seen.insert(canonical, predecessor = state and action)
                frontier.push_back(canonical)

    return CompleteExplorationManifest(observations, unsafe_witnesses, seen)
```

## 17. Minimum-clone pseudocode

```text
procedure MinimumClone(witness_observation, protocol, profile, max_k, bounds):
    for k from 1 through max_k:
        manifest = Explore(TwinsModel(protocol, profile, k), bounds, reductions = verified)
        if witness_observation is in manifest.observations:
            return finite result with k and constructive trace
    if max_k covers proven finite upper bound:
        return infinity within profile
    return unknown beyond tested cap
```

The procedure must never return infinity merely because an arbitrary `max_k` was reached.

## 18. Witness minimization pseudocode

```text
procedure Minimize(trace, predicate):
    current = trace
    repeat:
        changed = false
        for removable causal slice in CandidateSlices(current):
            trial = RemoveAndRepair(current, slice)
            if IsValidTrace(trial) and predicate(trial):
                current = trial
                changed = true
                break
    until not changed
    return current
```

`RemoveAndRepair` may delete only causally closed slices and must not synthesize new messages.

## 19. Minimal vertical slice

The smallest end-to-end path is:

1. parse `configs/pilot.toml`;
2. instantiate four-node toy locking protocol;
3. enumerate `AE` to the first complete bound with unsafe observation;
4. enumerate `AT(2)` under same bound;
5. project both through `ObsSafety`;
6. compute exact difference;
7. emit one human-readable unmatched or matched witness;
8. write `results/pilot/decision.md` with incomplete or complete status.

This slice excludes width analysis, second protocol, SMT, Coq and external adapters. It is the first integration acceptance test.

## 20. Performance constraints

- no assumption of GPU acceleration;
- memory use must be bounded and reported;
- state serialization should be compact but readable in debug mode;
- explorer may checkpoint complete BFS layers;
- disk spilling is a later optimization;
- no approximate Bloom-filter deduplication for decisive runs;
- every optimization must preserve tiny-bound languages exactly;
- if a completed decisive bound cannot be reached on one workstation, the pilot returns inconclusive and triggers abstraction review rather than cloud escalation by default.

## 21. Security threats to the artifact

- untrusted external trace files may be large or malformed;
- deserialization must use JSON, not executable pickle;
- no private keys or live node credentials are accepted;
- adapters operate only on local test fixtures;
- subprocess calls use fixed argument arrays;
- path traversal is rejected in manifests;
- generated HTML, if any, escapes message contents;
- dependency hashes and licenses are recorded;
- no arbitrary protocol plug-in code is loaded in artifact-evaluation mode.

## 22. Extension path after pilot

Only after GO:

1. stabilize theorem definitions;
2. add causal-width and minimization modules;
3. add second protocol model;
4. add concrete adapter;
5. add optional symbolic backend;
6. mechanize core embedding and lower-bound lemmas;
7. package one-command reproduction and artifact-evaluation documentation.

No production blockchain platform or global network is added at any stage.

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
````

## File: 07_ROADMAP_RISKS_REPRODUCIBILITY.md

````markdown
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
````

## File: 08_PAPER_SKELETON.md

````markdown
# Paper Skeleton and Publication Package

**Working title:** *Completeness Boundaries of Finite-Clone Twins Testing for Validated BFT Protocols: Relating Abstract State Equivocation to Executable Fault Injection*  
**Publication status:** no submission claim is justified before Gate 3 and Gate 5.  
**Likely audiences:** formal methods, distributed systems, software testing, dependable computing and blockchain-specific systems security.

## 1. Audience and venue type fit

### 1.1. Distributed systems audience

Will expect:

- a clearly defined BFT protocol class;
- adversary powers and network model;
- a theorem or separation result that changes how fault-injection coverage is interpreted;
- evidence beyond one toy protocol;
- practical meaning for consensus testing.

A mere model checker implementation is insufficient.

### 1.2. Formal methods audience

Will expect:

- precise transition systems;
- simulation or refinement relation;
- necessary and sufficient assumptions;
- machine-checked or carefully structured proof;
- sound abstraction from concrete harness;
- explicit bounded versus unbounded claims.

A systems-only replay study is insufficient.

### 1.3. Software testing audience

Will expect:

- a fault-model completeness question grounded in real test techniques;
- comparison with Twins, ByzzFuzz, ByzzBench, communication closure and causal testing;
- executable artifact;
- evidence that result affects test design, not only protocol semantics;
- realistic harness capabilities and regression witnesses.

A theorem with no actionable testing consequence may be seen as too abstract.

### 1.4. Blockchain-specific research audience

Will expect relevance to BFT consensus used in blockchain systems, but network name or token ecosystem cannot substitute for contribution. A strong fit requires an instantiation on a HotStuff-, Streamlet- or Tendermint-like model and a clear safety-testing implication.

### 1.5. Candidate venue types, not guarantees

- OPODIS, DISC or PODC-associated tracks for distributed-algorithm theory;
- FMBC or a formal-methods workshop for a narrower mechanized or counterexample result;
- CAV, TACAS or a related formal-methods venue only if proof and artifact rigor are high enough;
- ICST, ISSTA or software-testing venues if concrete harness and evaluation are substantial;
- dependable-computing venue if the focus becomes fault-model assurance;
- blockchain-focused security or systems workshop for an initial scoped result.

The venue is chosen after Gate 3 based on actual contribution shape, not prestige.

## 2. Three-point contribution statement

The paper may claim the following only if all evidence is obtained:

1. **A precise operational relation** between abstract validator state equivocation and a concrete finite-clone Twins adversary with explicit lifecycle and scheduler capabilities.
2. **A nontrivial characterization or separation result** for bounded safety observations, including a clone upper or lower bound, a no-uniform-cutoff theorem, or a minimized counterexample family.
3. **A reproducible exact checker and cross-protocol validation** that generates, minimizes and replays witnesses and makes every assumption auditable.

The first point alone is insufficient because generic refinement theory and S05 already provide much of the conceptual foundation.

## 3. Minimum publishable unit

The minimum publishable unit is one of the following:

### Positive route

- theorem for a non-vacuous class of validated deterministic BFT protocols;
- proof of finite-clone realization plus a nontrivial bound or exact condition;
- bounded checker validating the theorem on at least two non-isomorphic protocol models;
- explicit demonstration that result is not ordinary chain cover or S05 restatement.

### Negative route

- minimal protocol and trace satisfying declared validator assumptions;
- proof that an abstract state-equivocation safety witness is not realizable by a specified finite-clone harness or no fixed cutoff exists;
- necessary-condition analysis and minimized family of counterexamples;
- second example or structural generalization showing it is not a toy bug.

A pilot equality table without theorem, lower bound or separation is not a publishable unit.

## 4. Stretch contribution

One stretch contribution is enough; all are not required:

- Coq mechanization of embedding and finite-realization theorem using S06 concepts;
- a fixed clone cutoff for a meaningful locking BFT class;
- proof that snapshot capability changes the fault-model hierarchy;
- verified adapter showing a maintained HotStuff Twins implementation conforms to the formal profile;
- automated synthesis of minimal clone scenarios from abstract counterexamples;
- a reusable fault-model refinement framework beyond Twins.

## 5. Draft abstract for the pivoted topic

Clone-based testing systems such as Twins emulate Byzantine equivocation by running multiple correct protocol instances under a shared identity. The practical method is intentionally narrower than arbitrary message mutation, while formal validator models already show that Byzantine effects on honest components can be represented by abstract state equivocation. What remains unclear is whether an executable harness with a fixed number of simultaneously active clones realizes all safety-relevant behaviors of that abstract model and which harness capabilities determine the boundary. This work defines accepted-message Byzantine, dynamic state-equivocation and finite-clone adversaries over a common deterministic BFT transition system. It then studies observational language inclusion for bounded agreement violations, searches for the minimum clone number, and isolates the roles of causal branching, snapshot lifecycle and selective delivery. Depending on the result, the paper establishes either a finite-clone realization condition and bound or a minimized separation counterexample showing a principled blind spot. An exact, reproducible checker validates the result on a minimal locking protocol and an independent BFT model. The contribution concerns fault-model expressiveness rather than scenario count, throughput or a new consensus protocol.

This abstract is conditional and must be rewritten after the central result is known.

## 6. Expected Reviewer 2 objections and required answers

| Objection | Why it is serious | Required evidence or response |
|---|---|---|
| “VLSM already proves this.” | S05 kills the original theorem | State exactly that S05 is prior art; isolate fixed-`k` lifecycle gap; prove a bound or separation not present there |
| “This is just a refinement mapping.” | S18 and S28 provide generic theory | Show BFT-specific necessary conditions, clone lower bound or nontrivial impossibility; do not sell trace inclusion itself |
| “Minimum clones is just Dilworth or chain cover.” | Could make mathematical core trivial | Formal reduction and comparison; identify additional protocol validity, snapshot or scheduler constraints; reject paper if none remain |
| “Two clones are enough for equivocation.” | Common Twins intuition | Provide a valid more-than-two witness or prove a scoped two-clone theorem with nontrivial assumptions and literature audit |
| “Your Byzantine adversary is weakened until theorem is true.” | Accepted-message boundary may exclude important faults | Justify validator model through S05; provide separate mutation comparison; state excluded bug classes explicitly |
| “The toy protocol is not representative.” | External validity threat | Validate unchanged definitions on a second protocol family and map assumptions to an open HotStuff or Streamlet artifact |
| “Bounded exploration proves nothing general.” | Exact finite search cannot imply unbounded theorem | Use bounded search only for falsification and proof discovery; provide analytic theorem or clearly claim bounded separation only |
| “Your observation function hides divergences.” | Coarse projection can force equality | Report decision, state and causal-trace projections; justify primary property; show sensitivity to observation level |
| “The scheduler gives Twins unrealistic power.” | Asymmetric powers can fabricate completeness | Parameterize scheduler and lifecycle; prove equal network assumptions; include restrictive profile ablations |
| “The concrete harness does not implement your machine.” | Practical interpretation may fail | E7 conformance study or remove production-harness claim |
| “ByzzFuzz already shows Twins is incomplete.” | S07 demonstrates broader faults | Explain validator-valid versus arbitrary mutation distinction; reproduce a boundary witness and avoid universal Twins coverage claim |
| “No real bug is found.” | Systems venues may seek practical impact | Argue theoretical coverage assurance and blind spots; include concrete test-design implications; target appropriate venue |
| “No fixed cutoff is useful only negatively.” | Negative theorem may seem narrow | Provide counterexample family, necessary capabilities and consequences for test campaign interpretation |
| “State-space reductions may be unsound.” | Could invalidate all empirical evidence | Reduced/unreduced equality at tiny bounds, preservation lemmas and independent replay |
| “Hidden prior art under other terminology.” | Audit already missed S05 once | Publish exhaustive source map, citation search, S20 review and restrained novelty wording |
| “Coq and Python models diverge.” | Mechanized proof may not match executable artifact | Define shared schemas and cross-check example traces; state which artifact is normative |

## 7. Validity threats

### 7.1. Internal validity

- defects in transition implementation;
- unsound state canonicalization;
- asymmetric scheduler power;
- incorrect language comparison;
- counterexample minimizer changing semantics;
- optional solver returning unknown or invalid model.

Mitigation: independent oracles, reductions-off tiny runs, trace replay, exact manifests and solver-model replay.

### 7.2. External validity

- one Byzantine identity;
- finite traces;
- deterministic protocols;
- ideal authentication;
- safety only;
- two protocol models rather than production diversity;
- clone lifecycle profiles may not match all implementations.

Mitigation: scope claims, second model, capability mapping and no universal production conclusion.

### 7.3. Construct validity

- “completeness” may refer to all traces, unsafe traces, decisions or full state;
- “equivocation” may include message mutation in some literature;
- “full causal disclosure” may be vague or vacuous;
- `k_min` may depend on observation projection;
- causal width may be circular.

Mitigation: definitions in `03_FORMAL_MODEL.md`, multiple observations, validator boundary and chain-cover kill test.

### 7.4. Conclusion validity

- bounded equality mistaken for theorem;
- failure to find witness mistaken for absence;
- performance count mistaken for scientific effect;
- protocol-specific counterexample overgeneralized;
- incomplete full-text search mistaken for novelty.

Mitigation: proof obligations, incomplete markers, atomic claim ledger and date-limited novelty statement.

## 8. Paper outline by sections

### 1. Introduction

- practical role of clone-based BFT testing;
- exact gap between S04 and S05;
- why finite executable clones are not automatically dynamic state equivocation;
- research questions;
- contribution statement;
- one restrained result preview.

### 2. Background and motivating example

- authenticated BFT safety;
- Twins mechanism;
- accepted-message validator model;
- VLSM state equivocation theorem;
- a small example showing dynamic copy versus fixed clones;
- distinctions from ByzzFuzz mutation.

### 3. System and adversary models

- protocol transition system;
- messages and validation;
- network and observations;
- `AB`, `AE`, `AT(k)` and optional mutation model;
- clone lifecycle profiles;
- safety property.

### 4. Problem definitions

- bounded observation languages;
- finite-clone completeness;
- minimum clone number;
- cutoff;
- causal histories and candidate width;
- theorem targets and alternatives.

### 5. Theoretical result

One route only, according to actual finding:

- realization theorem and upper/lower bound; or
- separation theorem and counterexample family; or
- no-uniform-cutoff theorem; or
- lifecycle capability hierarchy.

Include assumptions, lemmas, proof sketch and limits.

### 6. Exact checker

- architecture;
- state exploration;
- reductions;
- observations;
- counterexample minimization;
- trusted computing base;
- reproducibility.

### 7. Evaluation

- definition sanity;
- pilot protocol;
- fixed-`k` hierarchy;
- structural predictor or separation;
- ablations;
- second protocol model;
- optional concrete harness conformance;
- resource cost as secondary result.

### 8. Discussion

- meaning for negative Twins campaigns;
- relation to message mutation;
- design implications for snapshot and scheduler;
- what the result does not guarantee;
- liveness and multiple Byzantine identities as future work.

### 9. Related work

Separate categories:

- Twins and BFT testing;
- VLSM and equivocation theory;
- communication closure and systematic testing;
- parameterized verification and cutoff bounds;
- refinement and I/O automata;
- fault injection and failure reproduction;
- BFT forensics and non-equivocation.

### 10. Threats to validity

Use the four-way validity analysis above.

### 11. Conclusion

State exactly which fault-model relation was proved or refuted and what a test engineer may infer.

### Appendices

- full transition tables;
- proofs;
- trace schema;
- additional witnesses;
- environment and license manifest;
- artifact instructions.

## 9. Mandatory tables

1. **Table 1:** fault-model capability matrix for `AB`, `AE`, `AT(k)` and mutation model.
2. **Table 2:** assumptions and their status: necessary, sufficient, convenience or untested.
3. **Table 3:** nearest prior art and exact remaining claims.
4. **Table 4:** language sizes and set differences by bound and `k`.
5. **Table 5:** `k_min` versus causal predictors for every minimal witness family.
6. **Table 6:** semantic ablation results.
7. **Table 7:** cross-protocol assumption mapping.
8. **Table 8:** concrete harness conformance, only if E7 is completed.
9. **Table 9:** validity threats and mitigations.
10. **Table 10:** artifact files, hashes and reproduction times.

No table may imply percentages of novelty or publication probability.

## 10. Mandatory figures

1. **Figure 1:** three-level model relation: Byzantine validator, dynamic equivocation, finite-clone harness.
2. **Figure 2:** motivating causal history showing why fixed clone cap matters or why two clones suffice.
3. **Figure 3:** formal event and observation pipeline.
4. **Figure 4:** language-inclusion lattice across `k` and harness profiles.
5. **Figure 5:** minimized decisive counterexample causal DAG or constructive realization mapping.
6. **Figure 6:** assumption-ablation boundary map.
7. **Figure 7:** cross-protocol transfer diagram.
8. **Figure 8:** repository and reproducibility workflow, optional for artifact appendix.

Every figure must be regenerated from source data or formal diagram specification.

## 11. Artifact-evaluation checklist

### Availability

- public or anonymized repository;
- permanent archive prepared;
- open-source license;
- CITATION file;
- external dependency license list.

### Functional

- smoke test completes;
- unit and metamorphic tests pass;
- one pilot trace generated and replayed;
- manifest verification succeeds;
- no network credential required.

### Reusable

- protocol interface documented;
- adversary interface documented;
- new protocol example;
- schema versioning;
- modular observations and oracles;
- no undocumented manual step.

### Reproducible

- exact environment pinning;
- raw and processed results;
- one-command core reproduction;
- hardware report;
- expected output checksums;
- completed and incomplete bounds distinguished;
- figure regeneration.

### Scientifically auditable

- assumptions linked to code;
- trace replay;
- reductions-off validation;
- decisive witnesses minimized;
- claim-evidence ledger;
- no stochastic result labeled complete.

### Safe

- local-only configurations;
- no mainnet endpoints;
- no private keys;
- responsible disclosure instructions;
- malicious mutation comparator disabled by default outside toy model.

## 12. Claims that must not appear without extra evidence

Do not claim:

- “Twins is complete for Byzantine behavior.”
- “This is the first formal model of equivocation.”
- “VLSM leaves the general Byzantine-to-equivocation question open.”
- “Two clones are sufficient for all BFT protocols.”
- “A fixed cutoff exists for all traces.”
- “Bounded model checking proves the unbounded theorem.”
- “The artifact verifies production HotStuff.”
- “No prior work studies this problem.”
- “ByzzFuzz faults are invalid in real systems.”
- “Full causal disclosure is standard and unambiguous.”
- “The result generalizes to liveness.”
- “The result applies to multiple Byzantine identities.”
- “The checker finds all bugs.”
- “More scenarios imply stronger safety assurance.”
- “The approach improves security by a numerical percentage.”
- “The paper is guaranteed to fit or be accepted at a named venue.”

## 13. Permitted restrained novelty language

A defensible formulation after successful Gate 5 is:

> Prior work introduces practical shared-identity clones and separately proves an abstract equivalence between Byzantine and equivocation behavior for validator systems. In the sources surveyed through 11 August 2026, we did not find a result that characterizes when a concrete harness with at most `k` active correct-code clones realizes bounded safety observations of dynamic state equivocation under explicit lifecycle and scheduler restrictions. Our contribution is limited to the theorem or separation statement proved here, the stated protocol class and the evaluated bounds.

This statement must be updated if Gate 0 finds additional prior art.

## 14. Result-dependent title variants

### Positive cutoff theorem

*Finite-Clone Realization of State Equivocation in Validated BFT Protocols*

### No-uniform-cutoff theorem

*No Fixed Clone Cutoff for State-Equivocation Testing of Validated BFT Protocols*

### Lifecycle separation

*When Twins Need Snapshots: Expressiveness Boundaries of Clone-Based BFT Fault Injection*

### Two-clone theorem

*When Two Twins Suffice: A Safety Coverage Theorem for a Restricted Class of Locking BFT Protocols*

### Counterexample route

*Beyond Twins: A Minimal State-Equivocation Behavior Not Realizable by a Finite-Clone BFT Harness*

A title is selected only after the result, not before.

## 15. Claim-evidence publication gate

The manuscript may enter Gate 8 only when every proposed contribution satisfies:

- one precise statement;
- one proof or exact counterexample;
- one executable reproduction;
- one nearest-alternative test;
- one scope limitation;
- one prior-art comparison;
- one negative-result interpretation;
- one artifact file path.

If any contribution lacks one item, it is removed or downgraded to discussion.

## 16. Paper writing order

1. Write definitions and theorem statement.
2. Write proof or counterexample derivation.
3. Freeze claim-evidence ledger.
4. Write evaluation from generated manifests.
5. Write related work with S05 prominently acknowledged.
6. Write validity threats.
7. Write introduction and abstract last.
8. Perform a forbidden-claims search.
9. Run artifact from clean environment.
10. Obtain supervisor and one distributed-systems/formal-methods expert review.

## 17. Submission readiness checklist

- original novelty claim explicitly withdrawn;
- residual result nontrivial and prior-art-safe;
- theorem assumptions non-vacuous;
- bounded and unbounded statements separated;
- at least two formal protocol models or an explicitly narrow theorem;
- every decisive trace minimized and replayed;
- no mainnet experiment;
- artifact license and dependencies documented;
- reviewer objections answered with evidence;
- figures and tables generated automatically;
- abstract matches actual result;
- venue type matches contribution;
- no publication promise.

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
````
