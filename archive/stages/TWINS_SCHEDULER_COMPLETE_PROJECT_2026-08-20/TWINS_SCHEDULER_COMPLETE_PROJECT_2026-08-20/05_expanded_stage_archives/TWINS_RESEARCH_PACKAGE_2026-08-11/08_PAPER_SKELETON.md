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
