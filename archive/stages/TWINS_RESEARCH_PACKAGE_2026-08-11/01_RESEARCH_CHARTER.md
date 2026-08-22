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
