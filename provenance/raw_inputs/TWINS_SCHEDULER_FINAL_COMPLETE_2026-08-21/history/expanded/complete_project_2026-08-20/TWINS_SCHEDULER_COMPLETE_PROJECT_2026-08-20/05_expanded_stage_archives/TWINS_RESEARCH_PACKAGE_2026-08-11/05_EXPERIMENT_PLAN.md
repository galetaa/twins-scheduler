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
