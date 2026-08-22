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
