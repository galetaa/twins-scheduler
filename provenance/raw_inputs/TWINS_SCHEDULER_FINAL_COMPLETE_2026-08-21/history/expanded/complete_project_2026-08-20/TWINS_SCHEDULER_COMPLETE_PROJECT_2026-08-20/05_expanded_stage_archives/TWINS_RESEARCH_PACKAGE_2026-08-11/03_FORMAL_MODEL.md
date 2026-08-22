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
