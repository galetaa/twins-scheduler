# Независимый аудит научных тем по blockchain systems

**Дата завершения аудита и поиска:** 11 августа 2026 года  
**Исходный бриф:** `00_RESEARCH_BRIEF_BLOCKCHAIN_CS.md`, версия 2.0  
**Проверяемый материал:** `Исследовательский анализ брифа.txt`  
**Статус:** независимый prior-art, novelty и execution audit

## Условные пометки

- **[Бриф]** — прямо следует из исходного файла брифа.
- **[Первый отчёт]** — утверждение или кандидат из первого исследовательского прохода; не считается проверенным.
- **[Независимо проверено]** — подтверждено заново первичным либо официальным источником.
- **[Вывод аудита]** — методологический вывод из сопоставления источников и требований.
- **[Рабочее предположение, не содержащееся в брифе]** — минимальное консервативное допущение, без которого проверка невозможна.
- **[Спекулятивная гипотеза]** — проверяемое утверждение предлагаемой темы, а не установленный факт.

## Итог в одном абзаце

Пять исходных кандидатов **не выдержали аудит в исходном виде**. Тема диагностируемости finality stalls оказалась плотным пересечением общей diagnosability theory, failure detectors, BFT accountability/forensics и новой distributed diagnosis при задержках. Тема temporal composition rollups пока не содержит результата, отличимого от общей L2 formal framework и стандартного assume–guarantee reasoning. Causal differential oracle является в основном новым применением зрелой partial-order/causal testing техники в уже насыщенной fuzzing-области. Тема parallel execution практически поглощается формальной теорией 2021 года, параметризованной по наблюдаемым компонентам состояния. DAS-тема пересекается с formal DAS, Robust Distributed Arrays, targeted sampling и network-aware DAS; её новизна не может быть установлена по доступным материалам. После поиска заменяющих тем сохранён **один** кандидат: формальная проверка или опровержение явно оставленной авторами Twins гипотезы о полноте clone-based Byzantine fault injection для детерминированных протоколов с полным раскрытием причинной истории.

---

# РАЗДЕЛ 1. НЕЗАВИСИМО ИЗВЛЕЧЁННЫЕ ТРЕБОВАНИЯ БРИФА

## 1.1. Обязательные требования

| Параметр | Независимо извлечённое требование |
|---|---|
| Область | Блокчейн и распределённые реестры как объект Computer Science; основной уровень — protocol/system, а не рынок токенов. |
| Уровень | Магистр прикладной информатики; результат должен быть пригоден для научной статьи. |
| Тип исследования | Теоретико-вычислительное: формальная или математическая постановка плюс самостоятельная вычислительная проверка, model checking, симуляция либо прототип. |
| Вид вклада | Новый механизм, модель, abstraction, формализация, bound, impossibility/equivalence result или новое различающее предсказание. |
| Механизм | Тема должна объяснять, какое свойство протокола, сети, состояния, программы или модели противника определяет исследуемую гарантию. |
| Различимость | Нужен тест, следствие или свидетельство, отличающее предлагаемое объяснение от ближайшей альтернативы. |
| Фальсифицируемость | Должны быть явные условия опровержения, ослабления сильной версии и границы применимости. |
| Обобщаемость | Основной тезис не должен исчезать при смене одной сети, клиента, dataset, workload или ML-архитектуры. |
| Реализуемость | Один мощный компьютер; открытый код и данные; локальная сеть, симулятор, forked state или testnet; без крупной инфраструктуры. |
| Отрицательный результат | Должен устанавливать границу, невозможность, эквивалентность, недостаточность механизма либо контрпример, а не только отсутствие прироста метрики. |
| Масштаб | Один узкий исследовательский вопрос, достаточный для статьи; не разработка новой полноценной blockchain platform. |
| Публикационность | Повтор опубликованной работы, локальный engineering prototype или неразличимый механизм являются основаниями для отказа. |

## 1.2. Запреты и нежелательные направления

Прямо исключены трейдинг, price prediction, инвестиционные и арбитражные задачи. Также не подходят: очередная GNN над transaction graph, классификация адресов, benchmark-only comparison, сравнение TPS, dApp/token/explorer, новая ML-архитектура без системного механизма, новый consensus с отличием только в параметрах и результат, оцениваемый только по throughput/latency/accuracy.

## 1.3. Доступные ресурсы

- Сильное программирование и ML; опыт графовых представлений и вычислительных экспериментов.
- Собственный мощный компьютер и GPU.
- Возможность локальных multi-node testnets, fault injection, симуляции, model checking, fuzzing, symbolic execution и differential testing.
- Открытые protocol specifications, клиенты, test suites, vulnerability corpora и самостоятельно сгенерированные traces.
- Доступ к научному руководителю или предметному эксперту.

## 1.4. Срок, этика и формальные требования

Жёсткий срок и точный объём в страницах не заданы, но бриф прямо запрещает превращать отсутствие deadline в чрезмерно широкую программу. Специальных требований кафедры, журнала или конференции пока нет. Опасные эксперименты допустимы только локально, в симуляторе, forked state или контролируемой testnet; эксплуатация live-систем, DoS, front-running, кража активов и несанкционированный доступ запрещены.

## 1.5. Критерии подходящей темы

Тема должна одновременно пройти пять ворот:

1. содержательная научная проблема, формальный объект и механизм;
2. независимость от одной реализации или dataset;
3. локальная воспроизводимость;
4. ясный публикационный тезис и аудитория;
5. содержательный отрицательный результат.

## 1.6. Неуказанные сведения

В брифе не указаны: конкретная подобласть; permissionless/permissioned setting; Layer 1/Layer 2/cross-chain focus; сеть, клиент, VM и consensus family; требуемая глубина криптографии; необходимость полного mechanized proof; целевая площадка; точный срок; допустимое время одного вычислительного эксперимента; доступ к archive nodes, облаку, платной литературе или закрытым данным; текущий практический опыт с blockchain clients, smart-contract languages, model checkers и proof assistants.

## 1.7. Противоречия и напряжения

Строгих логических противоречий не обнаружено. Есть два напряжения:

- high-risk/high-reward необходимо совместить с одним проверяемым минимальным результатом;
- широкий первый поиск необходимо завершить одной узкой статьёй.

## 1.8. Рабочие предположения

- **Рабочее предположение, не содержащееся в брифе:** закрытые данные, commercial archive nodes, платный cloud и корпоративная telemetry считаются недоступными.
- **Рабочее предположение, не содержащееся в брифе:** базовая среда — Linux workstation, контейнеры, локальные виртуальные узлы и open-source model checker.
- **Рабочее предположение, не содержащееся в брифе:** для первой статьи допустим абстрактный theorem/counterexample с валидацией на одной малой reference model; интеграция production client является расширением, а не условием успеха.
- **Рабочее предположение, не содержащееся в брифе:** ML не является обязательной частью вклада.

---

# РАЗДЕЛ 2. ВЕРДИКТЫ ПО ВСЕМ ИСХОДНЫМ ТЕМАМ

## 2.1. Сводная таблица

| Исходная тема | Соответствие брифу | Главный ближайший аналог | Главная угроза новизне | Главная угроза реализуемости | Отрицательный результат | Novelty kill test | Итоговый вердикт |
|---|---|---|---|---|---|---|---|
| A. Идентифицируемость причин finality stall | Полное по области; требуется сильное сужение | Lewis-Pye et al., **Accountable Liveness**, CCS 2025 | Общая diagnosability + accountable liveness уже формализуют причинную атрибуцию и пределы наблюдения | Минимальность telemetry требует строгой trust/logging model; state explosion | Формально ценен, но значительная часть вывода уже известна в общем виде | **C — существенное, но инкрементальное расширение** | **Отклонить** в исходном виде |
| B. Временная композиция optimistic rollup | Соответствие после существенного сужения | Avarikioti et al., **A Security Framework for General Blockchain L2 Protocols**, 2025 | Общая framework уже включает stateful L2 machines, adversarial scheduling, timing, safety/liveness | Слишком много компонентов и не задана точная property; легко получить тривиальный counterexample несовместимых deadlines | Может быть ценен, но только при нетривиальном necessary/sufficient theorem | **C — существенное, но инкрементальное расширение** | **Отклонить**: слабая конкретизация и очевидная композиция |
| C. Каузально-инвариантный differential oracle | Соответствие после сужения | FORKY, ICSE 2025; SpecTrum, ASE 2026 | Mazurkiewicz/happens-before/causal summaries и differential testing уже зрелы; неизвестен полный текст SpecTrum | Требуется ground truth для false positives/false negatives и сложная client integration | Если oracle ничего не меняет, остаётся только отрицательный engineering result | **D — только учебная/прикладная работа** | **Отклонить** |
| D. Conflict specifications и consensus-visible semantics | Полное формальное соответствие | Bartoletti et al., **A Theory of Transaction Parallelism in Blockchains**, LMCS 2021 | Теория уже параметризована по observables и доказывает observational/Mazurkiewicz equivalence | Реализуемость высокая, но научный вклад исчезает | Подтверждение известной sufficiency почти не добавляет знания | **E — практически уже опубликована** | **Отклонить** |
| E. Correlation-robust DAS soundness | Соответствие после сужения | Feist et al., **Robust Distributed Arrays**, 2025; Madisetti et al., **Targeted Sampling**, 2025 | Formal DAS, secure networking, targeted sampling и network-aware DAS уже покрывают пространство | Криптографическая model fidelity; самый опасный текст недоступен полностью | Потенциально ценен, но нельзя отделить от уже опубликованного | **F — новизна не устанавливается без специализированного поиска** | **Не включать в финал; требуется отдельный crypto-аудит** |

## 2.2. Кандидат A — идентифицируемость причин остановки финализации

### Исходное содержание кандидата

**[Первый отчёт]** Предлагалось различать selective Byzantine withholding и admissible network delay по проекциям timed protocol traces, доказать недостаточность ledger-only observation и найти минимальный набор authenticated receive/timeout/QC events после GST.

### Соответствие брифу

Тема находится на protocol/system level, использует formal methods, adversarial scheduling и синтетические traces; закрытые данные не требуются. Соответствие полное. Проблема темы не в брифе, а в литературном приоритете и в том, что различение причины зависит от доверенной evidence model, не сформулированной достаточно строго.

### Ближайшие работы, ранжированные по угрозе новизне

| Ближайшая работа | Совпадающая проблема | Совпадающий механизм/тезис | Совпадающая гипотеза | Совпадающее предсказание | Совпадающий способ проверки | Реальное отличие темы | Содержательно? | Только терминология? | Угроза новизне |
|---|---|---|---|---|---|---|---|---|---|
| [Lewis-Pye et al., *Accountable Liveness*, CCS 2025](https://doi.org/10.1145/3719027.3765032) | Атрибуция виновных при liveness failure | Формальная сеть между synchrony и partial synchrony; число идентифицируемых нарушителей | Liveness accountability достижима только в определённом режиме | Exact if-and-only-if regime и near-optimal accountability | Теоремы и protocol construction | Минимальный набор telemetry для пары delay/withholding | Частично | Нет | **Критическая** |
| [Wang et al., *Distributed Fault Diagnosis ... with Transmission Delay Impairments*, IEEE TAC 2024 / arXiv 2026](https://arxiv.org/abs/2608.06035) | Диагноз faults при частичном наблюдении и задержках | Distributed diagnosability, delay recorder, finite-step diagnosis | Задержки меняют различимость faults | Условие диагностируемости при transmission delays | Формальная verification structure | BFT-specific fault classes и authenticated messages | Частично | Нет | **Критическая** |
| [Sampath et al., *Diagnosability of Discrete-Event Systems*, IEEE TAC 1995](https://doi.org/10.1109/9.412626) | Различение скрытых faults по observable events | Diagnoser/twin-plant и observational equivalence | Fault должен стать однозначно диагностируемым за конечное число событий | Наличие/отсутствие indistinguishable faulty/non-faulty runs | Automata analysis | Частичная синхронность и Byzantine semantics | В основном инстанцирование | Да, если нет нового theorem | **Очень высокая** |
| [Doudou et al., *Muteness Failure Detectors*, EDCC 1999](https://doi.org/10.1007/3-540-48254-7_7) | Отсутствие ожидаемых сообщений | Failure detector для mute/omission behavior | Молчание можно обнаруживать при заданных timing assumptions | Подозрение процесса после отсутствия сообщений | Формальная спецификация и implementation | Отличить malicious withholding от benign delay | Ограниченно | Частично | Высокая |
| [Chandra & Toueg, *Unreliable Failure Detectors for Reliable Distributed Systems*, JACM 1996](https://doi.org/10.1145/226643.226647) | Неразличимость slow/failed process | Failure-detector abstractions | В asynchronous model delay и failure неотделимы без дополнительной oracle assumption | Impossibility/solvability boundaries | Теоремы | Byzantine finality и telemetry minimization | Инкрементально | Нет | Высокая |
| [Haeberlen et al., *PeerReview*, SOSP 2007](https://doi.org/10.1145/1294261.1294279) | Доказуемая атрибуция faulty behavior | Tamper-evident logs и cross-checking | Достаточные authenticated logs дают accountability | Observable deviation можно предъявить как evidence | Протокол и prototype | Минимальность неполной telemetry; liveness stall | Да, но узко | Нет | Высокая |
| [Sheng et al., *BFT Protocol Forensics*, CCS 2021](https://doi.org/10.1145/3460120.3484566) | Выявление Byzantine replicas по protocol transcripts | Forensic support и evidence after violations | Разные protocol designs дают разные forensic guarantees | Количество идентифицируемых виновных | Формальный анализ BFT protocols | Liveness, а не safety; delay/withholding pair | Да, но близко | Нет | Высокая |
| [Decouchant et al., *Liveness Checking of the HotStuff Protocol Family*, PRDC 2023](https://arxiv.org/abs/2310.09006) | Non-progress executions HotStuff | State abstraction, temperature/lasso detection | Liveness violation обнаружима без фиксированного timeout bound | Lasso/temperature distinguishes real non-progress | Model checking/testing | Причина stall и minimal evidence | Да | Нет | Средне-высокая |

### Novelty kill test

1. **Работа с той же комбинацией:** одной статьи с точной парой `selective withholding versus admissible delay + minimal event set` не найдено, однако *Accountable Liveness* уже решает более общий вопрос достижимости liveness attribution, а DES literature задаёт стандартный formalism диагностируемости.
2. **Все элементы по отдельности известны:** да — partial synchrony, indistinguishability, failure detectors, diagnosability, authenticated logs, BFT forensics, HotStuff liveness checking.
3. **Неочевидность соединения:** ограниченная. Само утверждение «без send evidence задержка и withholding неразличимы» следует из классической indistinguishability argument.
4. **Научная значимость соединения:** возможна только при нетривиальном theorem о минимальном cryptographically verifiable evidence set, общем для класса протоколов.
5. **Меняет ли понимание:** исходная формулировка — нет; узкий evidence-minimality result — возможно.
6. **Различает ли объяснения:** только после добавления доверенной evidence model; без неё это невозможно по определению.
7. **Новое применение известного подхода:** в текущем виде — в значительной степени да.
8. **Максимальная угроза:** *Accountable Liveness* плюс общая diagnosability theory.
9. **Минимальное доказательство для сохранения новизны:** necessary-and-sufficient characterization минимального набора cryptographically verifiable messages, не выводимая напрямую из generic diagnosability/accountability.
10. **Возможные пропуски:** accountability gadgets, slashing evidence, omission accountability, failure-detector lower bounds, control-theory sensor-selection literature.

**Novelty verdict: C — существенное, но инкрементальное расширение.**

### Execution kill test

- Получить ожидаемое различение можно из простого факта наличия доверенного send receipt, не подтверждая proposed causal model.
- Более простая альтернатива: различение задаётся не protocol mechanism, а trust boundary логов.
- Конструкт «причина» не измеряется по ledger trace; он вводится через model assumptions.
- Данных достаточно, поскольку traces синтетические; статистическая выборка не является проблемой.
- Минимальный pilot реалистичен, но не доказывает general minimality.
- Go/no-go: тема имеет смысл только если найден неочевидный protocol-independent lower bound; иначе это application of diagnosability.
- Опровергающее наблюдение: generic diagnosability/accountability theorem после простой подстановки даёт весь заявленный результат либо minimal set сводится к одному очевидному trusted send event.
- **Что станет известно, если гипотеза неверна?** Что выбранная telemetry не различает причины. Без нового lower bound это лишь неуспех конкретной операционализации; научный вклад слабее, чем заявлялось.

### Итоговый вердикт

**Отклонить исходную тему.** Точная причина: заявленная novelty delta не выдерживает сочетания *Accountable Liveness*, DES diagnosability и классической slow-versus-failed indistinguishability. Переработка возможна только в новый вопрос о минимальных cryptographic evidence certificates; такой вопрос требует отдельного prior-art и не сохранён автоматически.

---

## 2.3. Кандидат B — композиция временных гарантий optimistic rollup

### Исходное содержание кандидата

**[Первый отчёт]** Каждый компонент rollup задаётся timed assume–guarantee contract; предполагалось найти traces, где forced inclusion, sequencing, L1 inclusion и challenge subsystem локально live, но end-to-end settlement не live из-за несовместимых deadlines.

### Соответствие брифу

После сужения до одного класса optimistic rollups тема соответствует modular blockchain architecture, composability и model checking. В исходном виде она слишком широка: не заданы точные интерфейсы компонентов, временная модель, observable completion event и adversary.

### Ближайшие работы

| Ближайшая работа | Совпадающая проблема | Совпадающий механизм/тезис | Совпадающая гипотеза | Совпадающее предсказание | Совпадающий способ проверки | Реальное отличие темы | Содержательно? | Только терминология? | Угроза новизне |
|---|---|---|---|---|---|---|---|---|---|
| [Avarikioti et al., *A Security Framework for General Blockchain Layer 2 Protocols*, 2025](https://arxiv.org/abs/2504.14965) | End-to-end L2 security/liveness | Stateful L2 machines, subroutines, adversarial scheduling, timing and composability | L2 guarantees depend on composed assumptions | Safety/liveness/data-availability trace properties | Formal composable framework | Closed-form deadline compatibility theorem | Потенциально | Нет | **Критическая** |
| [Chaliasos et al., *Towards a Formal Foundation for Blockchain ZK Rollups*, CCS 2025](https://doi.org/10.1145/3719027.3765115) | Forced transactions, censorship, liveness | Alloy model with malicious operator/admin | Mechanism design determines weak liveness/censorship resistance | Counterexamples to rollup guarantees | Alloy/model checking | Optimistic timing composition, не ZK mechanisms | Да, но узко | Нет | Очень высокая |
| [Kalodner et al., *Arbitrum: Scalable, Private Smart Contracts*, USENIX Security 2018](https://www.usenix.org/conference/usenixsecurity18/presentation/kalodner) | Dispute/fallback and progress | Interactive protocol and on-chain advancement | Honest party can advance state despite disagreement | Eventual VM progress under assumptions | Protocol construction/analysis | General temporal assume–guarantee boundary | Частично | Нет | Высокая |
| [Li et al., *Finding Finalization Failure Bugs in Polygon zkRollup*, CCS 2024](https://doi.org/10.1145/3658644.3690243) | Finalization failure | Behavior model and guided fuzzing | Certain execution paths prevent finalization | Concrete failure traces | Model-guided fuzzing | Necessary/sufficient cross-component timing theorem | Да | Нет | Высокая |
| [Li et al., *Denial of Sequencing Attacks in Ethereum Layer 2 Rollups*, CCS 2025](https://doi.org/10.1145/3719027.3765100) | Sequencer liveness/DoS | Exploitation of legality checks | Adversary can prevent sequencing at low cost | Reproducible non-progress | Attack construction/experiments | Deadline incompatibility rather than one bug class | Да | Нет | Высокая |
| [Tas et al., *Proof of Diligence: Cryptoeconomic Security for Rollups*, AFT 2024](https://doi.org/10.4230/LIPIcs.AFT.2024.5) | Timely challenge/watchtower behavior | Incentivized checking and challenge process | Diligent actors preserve rollup security | Security depends on checking timing/incentives | Formal/economic analysis | Pure timed composition independent of incentives | Частично | Нет | Средне-высокая |
| [Motepalli et al., *SoK: Decentralized Sequencers for Rollups*, 2023](https://arxiv.org/abs/2310.03616) | Sequencer assumptions and liveness | Component taxonomy and ideal properties | Sequencer design affects inclusion/finality | Trade-offs and failure modes | SoK/spec analysis | Formal theorem across interfaces | Да | Нет | Средняя |
| [Derka et al., *Sequencer Level Security*, 2024](https://arxiv.org/abs/2405.01819) | Security at sequencing layer | Explicit sequencer-level protocol/property | Sequencing guarantees require extra layer | Attack resistance under protocol assumptions | Protocol design/analysis | Composition with challenge and L1 clocks | Да | Нет | Средняя |

### Novelty kill test

- Общий тезис «локальная liveness не гарантирует end-to-end liveness» является стандартным результатом композиционного reasoning, а не новой blockchain-specific hypothesis.
- Existing general L2 framework уже предоставляет язык для timing, adversarial scheduling и composed subroutines.
- Отличие становится содержательным только при наличии **нетривиального necessary-and-sufficient symbolic relation**, общего для чётко определённого класса rollups и не являющегося простым условием вида «каждый upstream deadline меньше downstream deadline».
- Самая опасная работа — general L2 security framework; вторая — formal rollup foundation.
- Минимальное доказательство новизны: theorem, который не является прямой инстанциацией framework, плюс реальный protocol counterexample, удовлетворяющий локальным assumptions каждого компонента.

**Novelty verdict: C — существенное, но инкрементальное расширение.**

### Execution kill test

- Тривиальный counterexample можно получить, просто выбрав несовместимые числовые deadlines; это не подтверждает новый механизм.
- Конкурирующее объяснение: failure вызван нарушением assumption одного компонента, а не composition gap.
- Операционализация должна различать inclusion, execution, proof/challenge completion, L1 finality и withdrawal finality; первый отчёт этого не делает.
- Полный rollup stack слишком велик; abstraction risk высок.
- Опровергающий результат: при минимальных стандартных assumptions local liveness всегда компонуется либо proposed inequality следует непосредственно из existing framework.
- **Что станет известно, если гипотеза неверна?** Что выбранный класс компонентов имеет compositional liveness. Это может быть полезно, но без общего theorem останется проверкой одной abstraction.

### Итоговый вердикт

**Отклонить.** Точная причина: слабая конкретизация научной проблемы и высокая вероятность того, что заявленный вклад является очевидной инстанциацией general L2 framework и assume–guarantee reasoning.

---
## 2.4. Кандидат C — каузально-инвариантный differential oracle

### Исходное содержание кандидата

**[Первый отчёт]** Protocol traces переводятся из total order в labelled partial order; допустимые permutations независимых events quotient-ятся по Mazurkiewicz-style relation. Предлагалось отличать genuine semantic divergence клиентов от различий raw logs, вызванных допустимым расписанием.

### Соответствие брифу

Тема формально относится к protocol diagnostics, cross-client validation и event representations; она локально воспроизводима. Однако вклад должен быть теорией семантической divergence, а не новым feedback/oracle модулем для fuzzing. В исходной формулировке эта граница не проведена.

### Ближайшие работы

| Ближайшая работа | Совпадающая проблема | Совпадающий механизм/тезис | Совпадающая гипотеза | Совпадающее предсказание | Совпадающий способ проверки | Реальное отличие темы | Содержательно? | Только терминология? | Угроза новизне |
|---|---|---|---|---|---|---|---|---|---|
| [Jeong et al., *SpecTrum: Specification-Guided Differential Fuzzing for Ethereum Consensus Clients*, ASE 2026](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/76/SpecTrum-Specification-Guided-Differential-Fuzzing-for-Ethereum-Consensus-Clients) | Differential oracle для consensus clients | Specification-guided comparison | Specification separates permissible and erroneous behavior | Client discrepancies against spec | Differential fuzzing | Causal quotient вместо specification-guided oracle | Неизвестно без полного текста | Возможно | **Критическая; текст недоступен** |
| [FORKY, *Fork State-Aware Differential Fuzzing for Blockchain Consensus*, ICSE 2025](https://doi.org/10.1109/ICSE55347.2025.00085) | False/true divergence между consensus clients | Fork-state-aware oracle and generation | Fork context необходим для meaningful comparison | Discrepancies in fork handling | Differential fuzzing | Partial-order equivalence instead of fork-state abstraction | Ограниченно | Нет | Очень высокая |
| [Yang et al., *Finding Consensus Bugs in Ethereum via Multi-transaction Differential Fuzzing (Fluffy)*, OSDI 2021](https://www.usenix.org/conference/osdi21/presentation/yang) | Cross-client consensus divergence | Multiple clients as differential oracles | Inconsistent outcomes reveal consensus bugs | Divergent block states/results | Differential fuzzing | Trace equivalence beyond final state | Да, но как oracle refinement | Нет | Высокая |
| [Tyr, IEEE S&P 2023](https://doi.org/10.1109/SP46215.2023.10179450) | Consensus-failure bugs | Behaviour-divergent model | Behavioural divergence guides bug discovery | Distinct protocol behaviours expose bugs | Model-guided fuzzing | Formal causal equivalence relation | Частично | Нет | Высокая |
| [LOKI, NDSS 2023](https://www.ndss-symposium.org/ndss-paper/loki-state-aware-fuzzing-framework-for-the-implementation-of-blockchain-consensus-protocols/) | Stateful consensus testing | Dynamic state model and state-aware messages | State context is required for valid/deep tests | Bugs under particular state transitions | Fuzzing with state model | Quotient of schedules rather than state-aware generation | Частично | Нет | Высокая |
| [Meng et al., *Greybox Fuzzing of Distributed Systems (MALLORY)*, CCS 2023](https://doi.org/10.1145/3576915.3623097) | Causal behavioral abstraction in distributed testing | Lamport timelines and happens-before summaries | Causal summaries are useful feedback | Different causal histories imply different behavior classes | Greybox fault injection | Use as correctness oracle, not coverage feedback | Да, но narrow | Нет | Высокая |
| [Drăgoi et al., *Testing Consensus Implementations Using Communication Closure*, OOPSLA 2020](https://doi.org/10.1145/3428278) | Controlling asynchronous schedules in consensus testing | Communication closure/round reduction | Certain async runs reduce to canonical round-based runs | Representative schedules preserve bugs | Testing reduction and implementation | General causal equivalence across clients | Да | Нет | Средне-высокая |
| [Scott et al., *Minimizing Faulty Executions of Distributed Systems*, NSDI 2016](https://www.usenix.org/conference/nsdi16/technical-sessions/presentation/scott) | Redundant event orderings in failure traces | Causal minimization/replay | Many schedules are equivalent for a failure | Smaller causally sufficient trace | Execution analysis | Online differential oracle | Ограниченно | Нет | Средняя |

### Novelty kill test

- Partial-order reduction, Mazurkiewicz equivalence, happens-before summaries and causal minimization являются зрелыми методами concurrency/distributed testing.
- Blockchain-specific contribution пока сводится к помещению этих методов в differential oracle.
- Нужное различающее следствие — доказательство soundness/completeness oracle относительно формальной protocol property — не сформулировано. Простое снижение false positives не является новым системным механизмом.
- SpecTrum принят на ASE 2026, но публичного полного описания на дату поиска не обнаружено; прямое совпадение исключить нельзя.
- Минимальное доказательство новизны: новая coarsest property-preserving equivalence для конкретного formal semantics, с theorem о сохранении safety/liveness violations и контрпримером к existing oracles. Это уже другая, существенно более сложная тема.

**Novelty verdict: D — подходит только как учебная, репликационная или прикладная работа.**

### Execution kill test

- Улучшение может объясняться обычной canonical sorting либо reduction state space, а не корректностью causal oracle.
- Ground truth для semantic equivalence production clients отсутствует; disagreement не сообщает, какой клиент прав.
- Client integration и instrumentation могут поглотить работу.
- Минимальный pilot на двух toy implementations реалистичен, но почти не доказывает переносимость.
- Опровергающий результат: quotient не меняет классы false positives/false negatives по сравнению с простым final-state/spec oracle.
- **Что станет известно, если гипотеза неверна?** Что causal quotient не улучшает выбранный oracle. Это в основном отрицательный результат инструмента, прямо нежелательный по брифу.

### Итоговый вердикт

**Отклонить.** Точная причина: тема является преимущественно новым применением mature partial-order/causal testing methods; различающее научное предсказание и независимый от инструмента mechanism отсутствуют.

---

## 2.5. Кандидат D — достаточность conflict specifications для consensus-visible semantics

### Исходное содержание кандидата

**[Первый отчёт]** Предлагалось ввести `resource-observable serializability`: parallel execution должно совпадать с prescribed sequential execution по tuple `(state, status, return data, receipts, logs, resource accounting)`. Гипотеза: key-level conflicts и final-state serializability недостаточны.

### Соответствие брифу

Формально тема идеально соответствует брифу: semantics, parallel execution, theory plus counterexamples, открытые VM tests. Но соответствие брифу не спасает тему от прямого prior art.

### Ближайшие работы

| Ближайшая работа | Совпадающая проблема | Совпадающий механизм/тезис | Совпадающая гипотеза | Совпадающее предсказание | Совпадающий способ проверки | Реальное отличие темы | Содержательно? | Только терминология? | Угроза новизне |
|---|---|---|---|---|---|---|---|---|---|
| [Bartoletti, Galletta, Murgia, *A Theory of Transaction Parallelism in Blockchains*, LMCS 2021](https://doi.org/10.46298/lmcs-17(4:10)2021) | Семантически корректная перестановка/параллельность transactions | Общая blockchain model, параметризованная по observables; swappability; Mazurkiewicz equivalence | Read/write observable approximations suffice for strong swappability | Concurrent execution observationally equivalent to serial | Формальные определения, theorems, Ethereum instantiation | Выбрать observables `status/logs/receipts/gas` и проверить conflict specs | Почти нет | **Да** | **Уничтожающая** |
| [Gelashvili et al., *Block-STM*, PPoPP 2023](https://doi.org/10.1145/3572848.3577524) | Deterministic parallel execution | Optimistic STM with preset transaction order | Parallel result equals ordered sequential result | Deterministic block outcome | System design and evaluation | Расширенная observation relation | Ограниченно | Нет | Очень высокая |
| [Anjana et al., *Efficient Parallel Execution ... Leveraging Conflict Specifications*, AFT 2025](https://doi.org/10.4230/LIPIcs.AFT.2025.29) | Declared conflicts and parallel execution | Conflict specifications for EVM/MoveVM | Specifications expose parallelism safely | Speedup under specified conflicts | Prototype/benchmarks | Formal soundness audit of declarations | Да, но как verification | Нет | Очень высокая |
| [Xu et al., *Vegeta*, NSDI 2025](https://www.usenix.org/conference/nsdi25/presentation/xu-tianjing) | Correct deterministic parallel EVM | Operation-level concurrency | Fine-grained execution preserves semantics | Higher concurrency with deterministic outcome | System evaluation | No new scheduler; semantics boundary | Частично | Нет | Высокая |
| [Lin et al., *ParallelEVM*, EuroSys 2025](https://doi.org/10.1145/3689031.3696063) | Parallel EVM execution | Concurrent engine and dependency handling | Engine preserves canonical result | Deterministic equivalence and speedup | Implementation/benchmark | Abstract observable tuple | Ограниченно | Нет | Высокая |
| [Chen et al., *Forerunner*, SOSP 2021](https://doi.org/10.1145/3477132.3483564) | Speculative smart-contract execution | Constraints and prediction | Dependencies can be anticipated for safe execution | Correct speculation/rollback | System prototype | Proof of conflict-spec sufficiency | Частично | Нет | Средне-высокая |
| [Hildenbrandt et al., *KEVM*, CSF 2018](https://doi.org/10.1109/CSF.2018.00022) | Exact EVM semantics including exceptional behavior | Executable formal semantics in K | EVM outcomes can be formally derived/verified | Reference execution outcomes | Formal semantics/tool | Parallel composition theorem | Да | Нет | Средняя |
| [Dickerson et al., *Adding Concurrency to Smart Contracts*, PODC 2017](https://doi.org/10.1145/3087801.3087835) | Commutativity/conflicts for smart contracts | Abstract locks and transactional boosting | Semantic commutativity enables concurrency | Equivalent concurrent histories | Protocol/system design | Blockchain-specific full observable tuple | Ограниченно | Нет | Средняя |

### Novelty kill test

- Bartoletti et al. прямо вводят general model **parameterized over observables** и semantics transactions, определяют observational equivalence, swappability, safe approximations read/write observables и Mazurkiewicz equivalence.
- Поэтому добавление `status`, `return data`, `receipts`, `logs` и gas/resource accounting является, без нового mathematical obstruction, выбором конкретного набора observables в уже существующей теории.
- Исходный термин `resource-observable serializability` переименовывает известный framework.
- Возможный остаток — найти bug в конкретной conflict specification либо mechanize one VM instantiation — является verification/application work, не новым общим construct.

**Novelty verdict: E — практически уже опубликована.**

### Execution kill test

- Counterexample final-state equivalence versus log divergence может быть построен, но existing theory ожидает именно выбор релевантных observables.
- Более простое объяснение: ошибочно выбран observation function, а не новый concurrency mechanism.
- Реализация пилота проста; именно это увеличивает риск получить лишь учебную демонстрацию известной теории.
- Опровергающий результат: все effects входят в existing observable set, а theorem 2021 напрямую обеспечивает требуемую sufficiency.
- **Что станет известно, если гипотеза неверна?** Что известная observable-equivalence abstraction достаточна для выбранной VM. Это полезная инженерная верификация, но не заявленный новый научный вклад.

### Итоговый вердикт

**Отклонить.** Точная причина: существование почти идентичной и более общей публикации; реальное отличие сводится к выбору observable tuple и проверке конкретной VM.

---

## 2.6. Кандидат E — correlation-robust DAS soundness

### Исходное содержание кандидата

**[Первый отчёт]** Предлагалось связать cryptographic DAS soundness с joint distribution фактически полученных peer/index observations; гипотеза — одинаковые marginals и nominal sample count могут давать разные false-accept probabilities из-за correlation/adaptive censorship.

### Соответствие брифу

Тема соответствует data availability, cryptography, networking и adversarial simulation; данные синтетические. Однако текущая глубина cryptographic game analysis у автора не подтверждена, а prior-art риск существенно выше, чем оценено в первом отчёте.

### Ближайшие работы

| Ближайшая работа | Совпадающая проблема | Совпадающий механизм/тезис | Совпадающая гипотеза | Совпадающее предсказание | Совпадающий способ проверки | Реальное отличие темы | Содержательно? | Только терминология? | Угроза новизне |
|---|---|---|---|---|---|---|---|---|---|
| [Feist et al., *Robust Distributed Arrays: Provably Secure Networking for DAS*, 2025](https://arxiv.org/abs/2504.13757) | Связь DAS security с реальной P2P network | Формальная robustness property и provably secure network construction | Cryptographic DAS недостаточен без secure networking layer | Availability access under malicious permissionless network | Definitions, construction, proofs | Общий joint-distribution/correlation bound вместо новой storage network | Да, но близко | Нет | **Критическая** |
| [Madisetti et al., *Data Availability Attacks: Targeted Sampling for 2-D Reed–Solomon Codes*, ITW 2025](https://doi.org/10.1109/ITW62417.2025.11240529) | Adversarial sampling and DA failure | Targeted sample selection against 2-D RS | Strategic sampling weakens detection guarantee | Higher false acceptance under targeted pattern | Information-theoretic/attack analysis | General equal-marginal correlation model | Неизвестно без полного текста | Возможно | **Критическая; текст недоступен** |
| [Hall-Andersen et al., *Foundations of Data Availability Sampling*, IACR CiC 2025](https://doi.org/10.62056/a09qudhdj) | Formal DAS primitive and soundness | Cryptographic definitions/security notions/proofs | Security depends on exact verifier/adversary game | Formal acceptance/security bounds | Cryptographic games and proofs | Reduction from network observations to game | Да, если отсутствует | Нет | Очень высокая |
| [Minh et al., *Efficient DAS via Coded Distributed Arrays*, ICBC 2026](https://arxiv.org/abs/2606.16200) | Byzantine discovery/routing for sampled fragments | Coded distributed arrays and network coding | Network sampler quality affects DAS | Robust/efficient sampling under network faults | Design, analysis, evaluation | Architecture-independent correlation theorem | Да | Нет | Очень высокая |
| [Wagner & Zapico, *A Documentation of Ethereum’s PeerDAS*, 2024](https://eprint.iacr.org/2024/1362) | Реальный peer/index sampling process | Protocol documentation and sampling assumptions | Pseudorandom sampling and custody determine assurance | Detection probability under protocol parameters | Specification analysis | Abstract composition theorem | Да | Нет | Высокая |
| [Pigaglio et al., *PANDAS*, Middleware 2025](https://doi.org/10.1145/3721462.3770769) | Dissemination/sampling before consensus deadline | Network protocol for DAS | P2P design determines timely sample availability | Sampling success and deadlines | Protocol + evaluation | False-accept correlation bound | Частично | Нет | Высокая |
| [Zhang & Venkatakrishnan, *Honeybee*, MobiHoc 2025](https://doi.org/10.1145/3704413.3764424) | Byzantine-resistant peer sampling | Secure peer sampling | Peer diversity/Byzantine resistance affects observations | Robust peer selection | Protocol/proofs/evaluation | Direct linkage to cryptographic DAS soundness | Да | Нет | Средне-высокая |
| [Yu et al., *Coded Merkle Tree*, FC 2020](https://doi.org/10.1007/978-3-030-51280-4_8) | Probabilistic detection of unavailable coded data | Erasure coding + Merkle commitments + sampling | Random samples expose withholding with calculable probability | Sampling detection bound | Theory and prototype | Dependence/correlation of realized samples | Да | Нет | Средняя |
| [Al-Bassam et al., *Fraud and Data Availability Proofs*, FC 2021](https://doi.org/10.1007/978-3-662-64331-0_15) | Light-client probabilistic DA assurance | Fraud proofs plus sampling | Random sampling detects unavailable data | Security probability versus sample count | Formal protocol analysis | Network-induced joint law | Да | Нет | Средняя |
| [Hall-Andersen et al., *FRIDA*, CRYPTO 2024](https://eprint.iacr.org/2024/248) | Efficient cryptographic DAS | FRI-based construction | Transparent commitment/sampling can satisfy DAS notions | Soundness/efficiency bounds | Cryptographic proofs | Network composition | Да | Нет | Средняя |

### Novelty kill test

- Сам тезис «одинаковые marginals не определяют joint-event probability» является базовым фактом теории вероятностей; это не самостоятельная scientific novelty.
- Содержательная тема должна дать reduction/composition theorem между конкретным network sampler и formal DAS game либо impossibility/lower bound, который не покрыт RDA/Targeted Sampling.
- *Robust Distributed Arrays* уже прямо заявляет formal security definitions и provably secure networking layer for DAS.
- Полный текст *Targeted Sampling* не найден в открытом доступе; по названию и metadata он может содержать наиболее близкий attack model.
- Минимальное доказательство новизны: показать конкретное assumption gap в Foundations/RDA и theorem, не выводимый из их models, после полнотекстового аудита Targeted Sampling.

**Novelty verdict: F — новизна не может быть установлена без специализированного поиска.**

### Execution kill test

- Получить различие false-accept rates легко, изменив marginals или effective unique samples; это не подтверждает заявленный cross-layer mechanism.
- Нужно доказать, что correlation возникает из реалистичного network process, а не введена произвольно.
- Crypto game fidelity и adaptive adversary существенно сложнее обычной Monte Carlo simulation.
- Минимальный pilot реалистичен, но демонстрирует только elementary probability unless tied to formal security game.
- Опровергающий результат: existing DAS definition already quantifies over the proposed dependence, либо RDA supplies the required reduction.
- **Что станет известно, если гипотеза неверна?** Что existing cryptographic notion already absorbs network correlation under its assumptions. Это содержательный reduction result, но его prior art сейчас не отделён от RDA.

### Итоговый вердикт

**Сначала провести дополнительный специализированный поиск; не включать в финал.** Точная причина: novelty cannot be established because the closest public work already formalizes secure DAS networking, а самый опасный targeted-sampling paper не проверен полнотекстово.

---
# РАЗДЕЛ 3. ОТКЛОНЁННЫЕ ТЕМЫ И ПРОВЕРКА ЗАМЕН

## 3.1. Отклонённые исходные темы

1. **Идентифицируемость finality stalls** — отклонена из-за недостаточной novelty delta: общий механизм уже покрыт diagnosability/failure-detector/accountability literature, а точный вклад зависит от неформализованной trust model telemetry.
2. **Временная композиция optimistic rollup** — отклонена как чрезмерно широкая и близкая к general L2 formal framework; без нетривиального necessary-and-sufficient theorem контрпример несовместимых deadlines очевиден.
3. **Каузально-инвариантный differential oracle** — отклонён как application of mature partial-order/causal testing methods; нет независимого от инструмента distinguishing prediction, а SpecTrum 2026 может напрямую пересекаться.
4. **Conflict specifications и consensus-visible semantics** — отклонена из-за почти идентичной более общей публикации Bartoletti et al. 2021; отличие преимущественно терминологическое.
5. **Correlation-robust DAS** — исключена из финала, потому что новизна не устанавливается на фоне Foundations, Robust Distributed Arrays, Targeted Sampling и CDA; требуется отдельный crypto prior-art audit.

## 3.2. Новые кандидаты, созданные после kill tests

Поскольку ни одна исходная тема не прошла аудит, были сформированы три более узких замены из явно обнаруженных gaps.

| Новый кандидат | Источник gap | Главная проверка prior art | Execution kill test | Вердикт |
|---|---|---|---|---|
| **R1. Формальные границы полноты Twins-based fault injection для deterministic full-disclosure BFT protocols** | Авторы Twins прямо оставили открытой rigorous characterization coverage и conjecture о полноте для full-disclosure protocols | Exact-phrase, mechanism, citation и related-work search не обнаружили theorem/counterexample, разрешающий conjecture; ByzzFuzz/ByzzBench/communication closure решают другие задачи | Возможны theorem, minimal counterexample и finite model pilot; положительный и отрицательный исходы информативны | **Сохранить; достаточно сильна для обсуждения с руководителем** |
| **R2. Conformance PeerDAS network sampler формальной DAS security game** | Необходимость связать реальный peer/index process и cryptographic verifier | Robust Distributed Arrays уже формализует provably secure networking for DAS; CDA 2026 и Targeted Sampling усиливают overlap | Реалистичная reduction сложна; без неё pilot лишь иллюстрирует probability | **Отклонить** |
| **R3. Полнота конечного набора message-mutation operators для BFT testing** | ByzzFuzz и другие testers не дают общей гарантии coverage | Randomized Testing of BFT Algorithms, ByzzBench, generic mutation testing и arbitrary Byzantine-message model делают либо universality тривиальной, либо ограниченный basis заведомо incomplete | Результат зависит от языка сообщений и implementation; легко сводится к tool-specific benchmark | **Отклонить** |

## 3.3. Почему в финале только одна тема

Требование пользователя допускает от одной до трёх финальных тем. Сохранять R2 или R3 ради формального количества означало бы нарушить исходное правило аудита «не сохранять все варианты из вежливости». Бриф первого прохода желал две центральные темы, но текущая задача — независимый аудит — прямо разрешает оставить одну, если только она выдерживает проверку.

---

# РАЗДЕЛ 4. ОКОНЧАТЕЛЬНАЯ ТЕМА

## Тема 1 — основная и единственная прошедшая аудит

### 1. Окончательное название на русском языке

**Формальные границы полноты метода Twins для safety-тестирования BFT-протоколов блокчейн-систем: детерминированные протоколы с полным раскрытием причинной истории**

### 2. Окончательное название на английском языке

**Formal Completeness Boundaries of Twins-Based Safety Testing for Blockchain BFT Protocols: Deterministic Protocols with Full Causal Disclosure**

### 3. Формулировка для титульного листа

**Формализация и проверка полноты clone-based Byzantine fault injection при обнаружении нарушений safety в детерминированных BFT-консенсусах с полным раскрытием причинной истории**

### 4. Краткий тезис из одного предложения

Работа должна установить, при каких формальных условиях любое конечное safety-нарушающее поведение произвольного Byzantine process наблюдательно воспроизводимо набором корректно исполняющихся clones с общей identity и adversarial message schedule, либо построить минимальный контрпример к этой гипотезе.

### 5. Актуальность

Twins позволяет эмулировать Byzantine behavior без написания вредоносной версии protocol code: несколько корректных instances используют одну identity, получают разные subsets сообщений и тем самым могут equivocate, double-vote или демонстрировать state loss. Метод практически масштабируется, но его авторы прямо указывают, что он покрывает многие, но не все attacks, и оставляют открытой строгую теорию coverage; отдельно формулируется conjecture о полноте для deterministic protocols, где каждое сообщение раскрывает entire causal past и nondeterminism. После публикации появились randomized BFT testing и ByzzBench, однако они оценивают bug-finding и benchmark coverage, а не доказывают equivalence arbitrary Byzantine adversary и clone adversary.

### 6. Научная проблема

Для clone-based BFT testing отсутствует формальная граница expressiveness:

- какие arbitrary Byzantine executions могут быть воспроизведены только корректным protocol code, клонированием identity и control of message delivery;
- какие свойства message validity, causal disclosure и determinism достаточны для completeness;
- сколько clones необходимо для воспроизведения конечного safety witness;
- какие minimal counterexamples возникают при ослаблении каждого условия.

Без такой границы отсутствие найденной ошибки в Twins campaign нельзя интерпретировать как содержательное coverage evidence.

### 7. Объект исследования

Детерминированные authenticated Byzantine fault-tolerant consensus protocols, применимые в blockchain state-machine replication.

### 8. Предмет исследования

Отношение наблюдательной симуляции между:

1. executions с произвольным Byzantine adversary, способным выбирать сообщения и локальные действия;
2. executions с Twins adversary, который использует только несколько корректных protocol instances с общей identity и adversarially controlled message delivery.

### 9. Цель

Дать формальное necessary/sufficient characterization либо строгую separation boundary для полноты Twins-based safety testing в классе deterministic full-causal-disclosure BFT protocols.

### 10. Задачи

1. Задать trace semantics authenticated deterministic BFT protocol и формализовать accepted-message validity, causal past и observable safety state.
2. Определить arbitrary Byzantine adversary, finite-clone Twins adversary и требуемую observation/simulation relation.
3. Формализовать класс `full causal disclosure` так, чтобы условие было проверяемым, а не словесным.
4. Доказать coverage theorem для ограниченного класса либо построить минимальный counterexample к conjecture Twins.
5. Получить upper/lower bound на число clones или distinct causal histories, необходимых для finite safety witness.
6. Проверить theorem/counterexample посредством bounded model checking и small protocol instances, затем провести controlled validation на одной открытой HotStuff/Tendermint-like model.

### 11. Основной исследовательский вопрос

**При каких условиях на determinism, message validity и causal disclosure каждое конечное safety-нарушающее execution детерминированного BFT-протокола под произвольным Byzantine adversary имеет наблюдательно эквивалентное execution, генерируемое конечным числом корректно исполняющихся Twins clones и adversarial message scheduler?**

### 12. Дополнительные исследовательские вопросы

- Является ли full causal disclosure достаточным либо нужны proof-carrying transition validity и replayable nondeterminism?
- Должна ли equivalence сохранять только решения correct replicas или полный causal trace?
- Существует ли bound на число clones как функция числа Byzantine identities, protocol rounds или distinct adversarial causal histories?
- Какие условия необходимы: authentication, deterministic transition function, explicit parent references, disclosed random coins, monotonic local state?
- Какой минимальный counterexample возникает при удалении одного условия?
- Переносится ли theorem с round-based lock-step protocols на partially synchronous protocols для safety properties?

### 13. Основная гипотеза или тезис

**[Спекулятивная гипотеза]** Для конечных safety witnesses в authenticated deterministic BFT protocols, где каждое accepted message содержит проверяемое описание своего causal past и всех sources of nondeterminism, arbitrary Byzantine execution observationally simulable конечным набором correct-code clones с общей identity; число clones ограничивается числом distinct Byzantine causal histories в witness.

### 14. Предполагаемый механизм или объяснительная рамка

Протокол задаётся labelled transition system:

\[
P=(S,M,\delta,V,O),
\]

где `S` — local states, `M` — authenticated messages, `δ` — deterministic transition relation, `V` — predicate accepted-message validity, `O` — observation function correct replicas.

Arbitrary Byzantine adversary `A_B` может выбирать любые actions/messages, удовлетворяющие внешней cryptographic validity. Twins adversary `A_T(k)` запускает `k` copies корректного `δ` под одной identity, доставляет каждой copy разные causally consistent message subsets и выбирает, какие produced messages доставлять correct replicas.

Coverage означает language inclusion modulo observation:

\[
O(L_{A_B}^{unsafe}(P))\subseteq O(L_{A_T(k)}^{unsafe}(P)).
\]

Сильная версия требует существования конечного `k` для каждого finite unsafe trace. Более практичная версия ищет bound `k=f(r,h,|M|)` либо показывает, что fixed `k` недостаточен.

### 15. Ближайшая альтернативная гипотеза

Full causal disclosure недостаточно: Byzantine process способен сформировать accepted message или последовательность state transitions, не являющуюся output ни одной корректной execution history; следовательно, существует finite safety violation, которое никакое конечное число Twins, выполняющих немодифицированный code, не воспроизводит.

### 16. Ключевое различающее предсказание

- **Coverage hypothesis:** для каждого bounded arbitrary-Byzantine safety witness model checker находит Twins witness с той же observation correct replicas; при удалении causal-disclosure condition появляется counterexample.
- **Alternative:** существует protocol, удовлетворяющий заявленным full-disclosure conditions, и finite arbitrary-Byzantine safety witness, для которого Twins language inclusion нарушается.

Это различает механизм полноты от простой эмпирической эффективности: речь идёт не о числе найденных bugs, а о formal inclusion двух adversary-generated trace languages.

### 17. Эксперимент или анализ, различающий объяснения

1. Определить toy locking BFT protocol с signed messages, explicit parent/lock proofs и deterministic transition function.
2. Exhaustively enumerate bounded traces двух adversary models при `n=4`, `f=1`, 3–5 rounds.
3. Сравнить unsafe observation languages.
4. Автоматически искать unmatched arbitrary-Byzantine trace.
5. Повторить после controlled mutations условий: удалить parent hash, скрыть coin, разрешить unverifiable local-state claims, ограничить число clones.
6. Если inclusion устойчиво, извлечь inductive simulation invariant и доказать theorem; если нарушается, минимизировать counterexample.

### 18. Окончательная формулировка novelty delta

Twins вводит практический clone-based generator и **явно оставляет открытой** rigorous characterization его coverage, формулируя conjecture о полном покрытии Byzantine behavior для deterministic full-disclosure protocols. Более поздние BFT testing works предлагают randomized exploration, message mutation, communication-closure reductions и benchmark frameworks, но в обследованной литературе не обнаружено theorem или counterexample, устанавливающего observational equivalence arbitrary Byzantine adversary и finite-clone Twins adversary для указанного класса.

**Проверяемая формулировка:**  
*В обследованной литературе по состоянию на 11 августа 2026 года не обнаружено работы, которая одновременно рассматривает формальную полноту clone-based Byzantine fault injection, задаёт класс deterministic full-causal-disclosure BFT protocols и доказывает либо опровергает сохранение всех finite safety-violating observations относительно arbitrary Byzantine adversary. Ближайшие работы вводят Twins, randomized/message-mutation testing, controlled schedule reductions и benchmark frameworks, но не разрешают эту комбинацию целиком. Заключение ограничено использованными базами, английскими поисковыми терминами, доступностью источников и возможным engineering prior art.*

**Novelty verdict: A — потенциально содержательно новая тема.** Это не утверждение абсолютной новизны.

### 19. Наиболее опасные ближайшие публикации

1. Bano et al., *Twins: BFT Systems Made Robust*, OPODIS 2021/2022.
2. Winter et al., *Randomized Testing of Byzantine Fault Tolerant Algorithms*, OOPSLA 2023.
3. Louro Neto & Kulahcioglu Ozkan, *A Benchmark Framework for BFT Testing Algorithms*, FMBC 2025.
4. Drăgoi et al., *Testing Consensus Implementations Using Communication Closure*, OOPSLA 2020.
5. Marić et al., *Cutoff Bounds for Consensus Algorithms*, CAV 2017.
6. Konnov et al., *A Short Counterexample Property...*, POPL 2017.
7. Tholoniat & Gramoli, *Formal Verification of Blockchain Byzantine Fault Tolerance*, 2019.
8. Meng et al., *Greybox Fuzzing of Distributed Systems*, CCS 2023.

### 20. Точное отличие от каждой опасной работы

| Работа | Что уже сделано | Что остаётся в финальной теме |
|---|---|---|
| Twins | Clone-based method, implementation, empirical attacks, explicit coverage conjecture | Formal adversary-language definition, theorem/counterexample, clone bound |
| Randomized Testing of BFT Algorithms | Message-mutation/randomized test generation and bug detection | Expressiveness equivalence of correct-code clones versus arbitrary Byzantine processes |
| ByzzBench | Unified benchmark and controlled environment | Scientific coverage criterion independent of benchmark bug set |
| Communication Closure | Reduction of asynchronous consensus executions to canonical communication-closed schedules | Reduction between two Byzantine **fault models**, not only schedules |
| Cutoff Bounds | Process-count cutoff for verification | Number-of-clones/causal-histories bound and coverage of adversary actions |
| Short Counterexample Property | Bounded witness length for threshold protocols | Reproducibility of witness by clone adversary |
| Formal Verification of Blockchain BFT | Automatic safety verification of protocol models | Verification of testing-method completeness, not protocol safety itself |
| MALLORY | Causal summaries as feedback for fault injection | Formal soundness/completeness relation, not heuristic coverage metric |

### 21. Необходимые данные, выборка, корпус или материалы

- Formal specifications of one minimal locking BFT protocol and one HotStuff/Tendermint-like protocol.
- Synthetic bounded executions; historical mainnet data не нужны.
- Model checker or SMT-based trace enumerator.
- Open-source Twins/ByzzBench artifacts where compatible.
- Protocol message schemas with signatures, parent/justification references and local transition rules.
- Mutation set for ablation of disclosure conditions.

### 22. Методология

- labelled transition systems and trace semantics;
- observational simulation/language inclusion;
- causal DAGs and authenticated histories;
- theorem proving by induction on accepted messages/causal histories;
- bounded model checking and counterexample generation;
- symmetry reduction and cutoff reasoning;
- property-based generation of adversary traces;
- delta debugging/minimization of counterexamples;
- controlled instantiation on small BFT protocol models.

### 23. План анализа

1. **Definition audit:** separate signature validity, semantic validity, causal disclosure and correct-node observations.
2. **Adversary comparison:** define `A_B` and `A_T(k)` without hiding extra power in scheduler.
3. **Small-model search:** calculate whether unsafe observation-language inclusion holds at bounded depth.
4. **Condition ablation:** identify which conditions are necessary.
5. **Theorem route:** construct simulation mapping from each Byzantine causal branch to a clone.
6. **Counterexample route:** minimize unmatched trace and prove non-simulability.
7. **Clone-bound analysis:** derive upper/lower bound or prove no uniform fixed bound.
8. **Protocol instantiation:** map formal assumptions to one open BFT design.

### 24. Минимальный пилот

A four-replica (`n=4, f=1`) two-phase locking protocol:

- messages carry signer, round, value, parent/justification hash and disclosed nondeterministic choices;
- arbitrary Byzantine generator enumerates all accepted signed messages under bounded rounds;
- Twins generator runs 1–4 correct copies under one identity and varies deliveries;
- checker compares sets of correct-replica decision pairs that violate agreement;
- ablations remove causal references or permit unverifiable state claims.

Пилот считается успешным, если найден хотя бы один из двух результатов:

1. bounded inclusion plus a plausible inductive invariant; или
2. minimal counterexample separating adversary models.

### 25. Критерий go/no-go после пилота

**Go:**

- обнаружена стабильная inclusion pattern и нетривиальная simulation invariant; или
- найден минимальный counterexample, который сохраняется после проверки корректности formal conditions; или
- выявлена нетривиальная lower bound на число clones.

**No-go как самостоятельная статья:**

- theorem является одношаговым следствием определения `full disclosure` и не даёт границы/clone bound;
- counterexamples возникают только из ошибок toy semantics;
- coverage relation требует столь сильной validity oracle, что класс protocols становится пустым или практически нерелевантным;
- exact result уже найден в specialised literature после expert citation search.

### 26. Критерий опровержения или пересмотра гипотезы

Сильная гипотеза опровергнута, если существует finite protocol `P`, удовлетворяющий согласованным full-disclosure/determinism/authentication conditions, и safety-violating trace `τ` под arbitrary Byzantine adversary, для которого ни при каком конечном наборе clones в установленной model не существует trace с той же observation correct replicas.

Ослабление потребуется, если simulation существует только:

- с числом clones, неограниченно растущим с trace length;
- при более сильной proof-carrying validity;
- только для round-based safety, но не partial synchrony/liveness;
- только modulo более грубой observation relation.

### 27. Вклад при положительном результате

- первый formal coverage theorem для Twins-defined adversary class;
- precise sufficient conditions on protocol/message design;
- bound на число clones или causal branches;
- principled interpretation negative testing result;
- reusable formal model and model-checking artifact;
- design guidance: какие causal proofs делают BFT implementation amenable to complete clone-based testing.

### 28. Вклад при отрицательном результате

- minimal counterexample к опубликованной conjecture;
- separation theorem между arbitrary Byzantine and Twins adversaries;
- necessary conditions, отсутствующие в исходном понятии full disclosure;
- lower bound или impossibility of fixed-clone completeness;
- точная граница того, какие bug classes Twins принципиально не может обнаружить.

Отрицательный результат не сводится к «tester не нашёл bug» и полностью соответствует требованию брифа.

### 29. Основные риски

1. **Тривиальность:** после сильной формализации theorem может стать почти definitional.
2. **Пустота класса:** `full disclosure` может потребовать unrealistically strong message verification.
3. **Unbounded clones:** finite-trace completeness может не давать practically useful fixed bound.
4. **Model mismatch:** arbitrary Byzantine power и accepted-message validity легко определить несбалансированно.
5. **Hidden prior art:** сходный result может находиться в protocol-testing, I/O automata, refinement, conformance testing или dissertation literature без слова Twins.
6. **Proof difficulty:** general theorem может превысить масштаб магистерской статьи.

### 30. Способ сузить тему

Первичная статья должна ограничиться:

- safety/agreement, не liveness;
- finite traces;
- one Byzantine identity;
- deterministic round-based authenticated protocols;
- messages with explicit causal justification DAG;
- observational equivalence только по states/decisions correct replicas;
- theorem либо counterexample без production-client integration.

Partial synchrony, multiple Byzantine identities, liveness и fixed universal clone bound оставить расширением.

### 31. Реалистичная последовательность выполнения

1. Полностью формализовать terminology Twins и exact conjecture.
2. Провести backward/forward citation search по Twins, ByzzFuzz и communication closure.
3. Определить smallest nontrivial protocol class и observation relation.
4. Реализовать dual-adversary bounded trace generator.
5. Провести pilot и condition ablations.
6. Выбрать theorem route или counterexample route по результату pilot.
7. Доказать основной result и clone bound/limitation.
8. Проверить на второй minimal protocol либо open model.
9. Подготовить reproducible artifact.
10. После expert review сформулировать restrained novelty claim и target venue.

### 32. Стартовые источники

1. [Bano et al. *Twins: BFT Systems Made Robust*. OPODIS 2021, DOI 10.4230/LIPIcs.OPODIS.2021.7](https://doi.org/10.4230/LIPIcs.OPODIS.2021.7)
2. [Bano et al. *Brief Announcement: Twins – BFT Systems Made Robust*. DISC 2021, DOI 10.4230/LIPIcs.DISC.2021.46](https://doi.org/10.4230/LIPIcs.DISC.2021.46)
3. [Winter et al. *Randomized Testing of Byzantine Fault Tolerant Algorithms*. PACMPL/OOPSLA 2023, DOI 10.1145/3586053](https://doi.org/10.1145/3586053)
4. [Louro Neto & Kulahcioglu Ozkan. *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms*. FMBC 2025, DOI 10.4230/OASIcs.FMBC.2025.13](https://doi.org/10.4230/OASIcs.FMBC.2025.13)
5. [Drăgoi et al. *Testing Consensus Implementations Using Communication Closure*. PACMPL/OOPSLA 2020, DOI 10.1145/3428278](https://doi.org/10.1145/3428278)
6. [Marić, Sprenger, Basin. *Cutoff Bounds for Consensus Algorithms*. CAV 2017, DOI 10.1007/978-3-319-63390-9_12](https://doi.org/10.1007/978-3-319-63390-9_12)
7. [Konnov et al. *A Short Counterexample Property for Safety and Liveness Verification of Fault-tolerant Distributed Algorithms*. POPL 2017, DOI 10.1145/3009837.3009860](https://doi.org/10.1145/3009837.3009860)
8. [Tholoniat & Gramoli. *Formal Verification of Blockchain Byzantine Fault Tolerance*. arXiv:1909.07453](https://arxiv.org/abs/1909.07453)
9. [Bertrand et al. *Holistic Verification of Blockchain Consensus*. DISC 2022, DOI 10.4230/LIPIcs.DISC.2022.10](https://doi.org/10.4230/LIPIcs.DISC.2022.10)
10. [Meng et al. *Greybox Fuzzing of Distributed Systems*. CCS 2023, DOI 10.1145/3576915.3623097](https://doi.org/10.1145/3576915.3623097)
11. [ZERMIA: A Fault Injector Framework for Testing Byzantine Fault Tolerance Systems, 2021](https://doi.org/10.1007/978-3-030-92708-0_3)
12. [Decouchant et al. *Liveness Checking of the HotStuff Protocol Family*. PRDC 2023, arXiv:2310.09006](https://arxiv.org/abs/2310.09006)
13. [Sheng et al. *BFT Protocol Forensics*. CCS 2021, DOI 10.1145/3460120.3484566](https://doi.org/10.1145/3460120.3484566)
14. [Haeberlen et al. *PeerReview: Practical Accountability for Distributed Systems*. SOSP 2007, DOI 10.1145/1294261.1294279](https://doi.org/10.1145/1294261.1294279)
15. [Lynch. *Distributed Algorithms*. Morgan Kaufmann, 1996](https://dl.acm.org/doi/book/10.5555/525656)

### Вопросы, которые необходимо проверить у предметного специалиста

- Является ли `full disclosure` устойчивым научным термином или его нужно заменить на `causally self-verifying messages`/proof-carrying history?
- Как правильно ограничить arbitrary Byzantine adversary: любые signed bytes, любые accepted messages или любые semantically valid transitions?
- Достаточно ли equivalence по decisions correct nodes для publication-level theorem?
- Нужен ли fixed clone cutoff либо trace-dependent bound уже содержателен?
- Известен ли похожий theorem в I/O automata, refinement, conformance testing, Byzantine epistemic logic или unpublished Diem/Aptos engineering work?
- Какой protocol instance лучше: HotStuff core, Tendermint locking protocol или специально минимальная abstract machine?
- Какой venue разумен: OPODIS/DISC/PODC workshop, FMBC, formal methods venue или software testing venue?
- Требуется ли mechanized proof, либо theorem plus bounded checker artifact достаточны?

---
# РАЗДЕЛ 5. СРАВНЕНИЕ ФИНАЛИСТОВ

После kill tests остался один финалист. Таблица намеренно не дополнена более слабыми темами.

| Тема | Соответствие брифу | Научная содержательность | Защищаемость novelty delta | Реализуемость | Доступность данных | Сила различающей проверки | Вклад при отрицательном результате | Главный риск | Рекомендация |
|---|---|---|---|---|---|---|---|---|---|
| Формальные границы полноты Twins для deterministic full-causal-disclosure BFT protocols | Полное после сужения до safety и finite traces | Очень высокая: equivalence/separation двух adversary models | Сильная, но условная; основана на явно открытой conjecture и отсутствии найденного решения | Высокая для small-model theorem/counterexample; средняя для общего результата | Полная: synthetic traces, open specs/code | Очень сильная: language inclusion theorem или unmatched minimal trace | Очень высокий: refutation, necessary condition, lower bound | Тривиальность либо слишком сильный/пустой protocol class | **Основная тема; обсуждать с руководителем после pilot definition audit** |

---

# РАЗДЕЛ 6. ОСНОВНАЯ РЕКОМЕНДАЦИЯ

## Выбор

**Выбрать тему о формальной полноте Twins-based safety testing.**

### 1. Научная содержательность

Тема задаёт самостоятельный теоретический объект — отношение expressiveness между arbitrary Byzantine adversary и clone-based correct-code adversary. Это не benchmark, не новый fuzzer и не прирост coverage metric. Результатом может быть simulation theorem, separation theorem, counterexample или clone bound.

### 2. Отличие от ближайшей литературы

Twins формулирует conjecture, но не доказывает её. Randomized BFT testing, ByzzBench, communication closure и formal verification проверяют эффективность, schedules или protocol safety, но не дают coverage theorem для clone adversary. Exact-phrase и mechanism searches не выявили разрешения conjecture по состоянию на дату аудита.

### 3. Соответствие брифу и реализуемость

Тема protocol-level, generalizable beyond one chain, формальная и вычислительно проверяемая. Все traces генерируются локально; production infrastructure, mainnet funds и historical dataset не нужны. Минимальный pilot возможен на четырёх репликах и bounded rounds.

### 4. Информативность отрицательного результата

Контрпример к conjecture или impossibility of fixed-clone completeness является самостоятельным научным результатом: он строго определяет, какие Byzantine bugs метод не способен воспроизвести и какие условия protocol design необходимы.

## Почему не выбраны остальные исходные темы

- **Finality diagnosability:** слишком близко к accountable liveness и generic diagnosability; without evidence-minimality theorem вклад инкрементален.
- **Rollup temporal composition:** нет нетривиальной property; general L2 framework уже задаёт нужный язык.
- **Causal differential oracle:** mature causal/POR machinery плюс saturated client-fuzzing literature; outcome likely tool-specific.
- **Parallel semantics:** general observable-parametric theory уже опубликована.
- **DAS correlation:** novelty cannot be established на фоне RDA/Targeted Sampling/CDA.

## Условие, способное изменить рекомендацию

Рекомендация изменится, если предметный специалист или forward-citation search найдёт уже опубликованный proof/counterexample Twins coverage conjecture либо если formal definition full disclosure делает theorem тривиальным или protocol class практически пустым. В этом случае тему следует отклонить, а не расширять искусственно.

## Что необходимо проверить до окончательного утверждения

1. Полный backward/forward citation graph Twins.
2. Dissertations и unpublished technical reports авторов Twins/Diem/Aptos.
3. I/O automata, refinement, conformance и Byzantine epistemic-logic literature.
4. Точное definition accepted-message validity.
5. Bounded pilot language inclusion на toy protocol.
6. Наличие нетривиального result после condition ablation.
7. Target venue и ожидаемый уровень proof mechanization.

---

# РАЗДЕЛ 7. ГОТОВЫЙ ТЕКСТ ДЛЯ НАУЧНОГО РУКОВОДИТЕЛЯ

## Тема

**Формальные границы полноты метода Twins для safety-тестирования BFT-протоколов блокчейн-систем: детерминированные протоколы с полным раскрытием причинной истории**

## Актуальность

Метод Twins эмулирует Byzantine behavior посредством нескольких корректно исполняющихся copies одного узла с общей network identity. Разным copies доставляются разные subsets сообщений, благодаря чему они могут порождать equivocation, double voting и другие конфликтующие действия без модификации protocol code. Метод практически применим, но его авторы прямо указывают, что строгая теория coverage остаётся открытой, и формулируют conjecture о полном покрытии Byzantine behaviors для deterministic protocols, где сообщения раскрывают causal past и источники nondeterminism. Без решения этого вопроса отрицательный результат Twins testing не даёт формально обоснованной гарантии о непокрытых классах attacks.

## Научная проблема

Не установлено, при каких условиях множество safety-violating observations, генерируемых произвольным Byzantine adversary, совпадает с множеством observations, воспроизводимых конечным числом correct-code clones с общей identity и adversarial message scheduler. Неизвестны также необходимые условия full causal disclosure и bound на число clones.

## Объект исследования

Детерминированные authenticated Byzantine fault-tolerant consensus protocols для blockchain state-machine replication.

## Предмет исследования

Наблюдательная эквивалентность и границы expressiveness arbitrary Byzantine fault model и Twins-based clone fault model относительно finite safety violations.

## Цель

Формально доказать полноту Twins для ограниченного класса deterministic full-causal-disclosure BFT protocols либо построить минимальный counterexample и уточнить необходимые условия coverage.

## Задачи

1. Формализовать protocol traces, message validity, causal history и observations correct replicas.
2. Определить arbitrary Byzantine и finite-clone Twins adversary models.
3. Дать проверяемое определение full causal disclosure.
4. Установить simulation theorem либо separation counterexample.
5. Получить bound или lower bound на число clones/causal histories.
6. Подтвердить результат bounded model checking и controlled protocol instantiation.

## Основной исследовательский вопрос

При каких условиях каждое конечное safety-нарушающее execution детерминированного BFT protocol под произвольным Byzantine adversary имеет наблюдательно эквивалентное execution, генерируемое конечным числом correct-code Twins clones и adversarial message scheduler?

## Дополнительные исследовательские вопросы

- Достаточно ли ссылок на causal past или нужна proof-carrying transition validity?
- Какой observation level должен сохраняться: decisions, local states или full trace?
- Существует ли fixed clone cutoff?
- Какие условия являются necessary, а не только sufficient?
- Какой минимальный counterexample появляется при скрытом nondeterminism или неполной causal disclosure?

## Гипотеза или основной тезис

Для finite safety witnesses в authenticated deterministic protocols с проверяемой full causal disclosure любое accepted Byzantine behavior может быть разложено на набор causally consistent correct-code branches; каждому branch соответствует clone, поэтому unsafe observation произвольного adversary воспроизводима Twins execution. Число clones зависит от числа distinct Byzantine causal histories в witness.

## Предполагаемый механизм

Каждый accepted message несёт enough evidence для восстановления causally consistent local history. Byzantine node не получает дополнительной семантической возможности синтезировать accepted state transition, которой нет ни в одной корректной history; он может только показывать разным recipients разные consistent branches. Twins именно это и реализует посредством clones и selective delivery.

## Различающее предсказание или свидетельство

Если механизм верен, bounded unsafe trace language arbitrary Byzantine adversary включается в Twins unsafe trace language modulo observations correct replicas. Если full disclosure недостаточно, model checker должен найти finite unmatched safety witness. Controlled removal каждого disclosure condition должно либо сохранять inclusion, либо давать минимальный counterexample.

## Предполагаемая научная новизна

Предлагается впервые проверить формально открытую conjecture Twins coverage через explicit relation двух adversary trace languages, necessary/sufficient protocol conditions и clone bound. Формулировка предварительная и не является заявлением абсолютной новизны.

В обследованной литературе по состоянию на 11 августа 2026 года не обнаружено работы, которая одновременно формализует deterministic full-causal-disclosure BFT class и доказывает либо опровергает completeness finite-clone Twins adversary для всех finite safety-violating observations arbitrary Byzantine adversary. Заключение ограничено использованными базами, терминами и доступностью источников.

## Отличие от ближайших работ

Twins вводит method и conjecture, но не coverage theorem. Randomized Testing of BFT Algorithms разрабатывает message-mutation testing; ByzzBench — benchmark framework; communication closure — schedule reduction; cutoff и short-counterexample works — bounds for verification; formal BFT verification проверяет protocols, а не полноту fault injector. Предлагаемая работа исследует expressiveness relation fault models.

## Методы

Labelled transition systems, causal trace semantics, observational simulation, language inclusion, bounded model checking, counterexample generation, induction over causal histories, symmetry/cutoff reasoning и property-based adversary trace generation.

## Данные или материалы

Synthetic traces, minimal locking BFT model, open HotStuff/Tendermint-like specification, Twins/ByzzBench artifacts при совместимости и локальный model checker. Mainnet data и платная infrastructure не требуются.

## План анализа

Сначала фиксируются formal definitions и two adversary models. Затем bounded checker сравнивает unsafe observation languages. Condition ablations выявляют необходимые assumptions. По результату строится inductive simulation proof либо minimal separation counterexample. После этого вывод проверяется на второй protocol model и оформляется reproducible artifact.

## Минимальный пилот

Для `n=4, f=1` реализовать two-phase locking protocol с signed messages и causal justifications. Exhaustively enumerate bounded arbitrary-Byzantine and 1–4-clone Twins executions на 3–5 rounds, сравнить agreement-violating observations и минимизировать unmatched traces. Повторить после удаления parent references и скрытия nondeterministic choices.

## Критерий опровержения

Гипотеза опровергнута finite protocol и unsafe trace, удовлетворяющими согласованным full-disclosure conditions, но не имеющими observationally equivalent Twins trace при любом конечном числе clones в model. Гипотеза ослабляется, если требуется unbounded-with-trace clone count или более сильная validity oracle.

## Ожидаемый научный вклад

Coverage theorem, precise protocol conditions, clone bound и reusable checker artifact либо formal separation theorem и минимальный counterexample к conjecture.

## Вклад при отрицательном результате

Отрицательный результат задаст principled blind spot Twins, уточнит necessary disclosure conditions и не позволит интерпретировать отсутствие найденных bugs как широкое evidence of safety.

## Основные риски

Theorem может оказаться тривиальным при слишком сильной definition; protocol class — практически пустым; число clones — unbounded; похожий result может скрываться в refinement/conformance literature; general proof может быть слишком широк для первой статьи.

## Первый практический шаг

Записать machine-checkable definitions `arbitrary Byzantine trace`, `Twins trace`, `full causal disclosure` и `observation equivalence`, затем построить bounded language-inclusion checker для минимального four-node locking protocol.

## Что необходимо согласовать с научным руководителем

- accepted-message validity и power arbitrary adversary;
- safety-only scope;
- требуемая observation relation;
- необходимость fixed clone cutoff;
- выбор protocol instance;
- допустимый уровень mechanized proof;
- target venue;
- специалист, который проверит связь с I/O automata/refinement literature.

---

# РАЗДЕЛ 8. ОГРАНИЧЕНИЯ АУДИТА

## 8.1. Дата завершения поиска

**11 августа 2026 года.** Новые публикации после этой даты не учитывались.

## 8.2. Использованные базы и источники

- ACM Digital Library;
- IEEE Xplore;
- USENIX Open Access;
- arXiv и ar5iv;
- IACR Cryptology ePrint Archive и IACR Communications in Cryptology;
- SpringerLink;
- LIPIcs/DROPS;
- DBLP;
- NDSS proceedings;
- официальные conference pages ASE/ICSE/CCS/OPODIS/FMBC;
- institutional repositories и author copies;
- official protocol specifications/EIPs, где они являлись engineering prior art;
- citation and exact-phrase web search.

## 8.3. Основные поисковые запросы

### Тема A

- `BFT finality stall diagnosability network delay withholding`
- `accountable liveness partial synchrony identify violators`
- `distributed fault diagnosis transmission delay partial observation`
- `muteness failure detector omission Byzantine`
- `BFT protocol forensics liveness accountability`
- `minimal telemetry fault diagnosis distributed systems`

### Тема B

- `rollup end-to-end liveness timed composition forced inclusion challenge period`
- `formal security framework general blockchain layer 2 liveness`
- `rollup local liveness global liveness assume guarantee`
- `sequencer liveness forced transaction finalization failure`
- `rollup deadline compatibility model checking`

### Тема C

- `causal trace equivalence differential fuzzing blockchain consensus clients`
- `Mazurkiewicz equivalence distributed systems testing oracle`
- `fork state aware differential fuzzing consensus`
- `specification guided differential fuzzing Ethereum consensus clients`
- `happens-before summary distributed systems fuzzing`
- `partial-order reduction consensus client testing`

### Тема D

- `transaction parallelism blockchain observational equivalence observables`
- `conflict specifications parallel smart contract execution soundness`
- `Mazurkiewicz transaction swappability blockchain`
- `parallel EVM receipts logs gas semantics equivalence`
- `deterministic smart contract execution serializability`

### Тема E

- `data availability sampling correlated samples adaptive network adversary`
- `targeted sampling 2-D Reed Solomon data availability attack`
- `provably secure networking data availability sampling`
- `PeerDAS sampler security game network correlation`
- `coded distributed arrays DAS Byzantine routing`
- `DAS joint distribution false acceptance`

### Финальная тема

- `"Theory of Twins coverage"`
- `"full disclosure" Twins BFT coverage`
- `clone-based Byzantine fault injection completeness`
- `Twins BFT coverage theorem`
- `deterministic protocol causal past twins Byzantine`
- `correct-code clones arbitrary Byzantine adversary equivalence`
- `Byzantine fault injection mutation completeness`
- `BFT testing communication closure cutoff`

## 8.4. Использованные синонимы и старая терминология

- diagnosability, fault isolation, observability, codiagnosability, muteness, omission failure, failure detector, accountability, forensics;
- non-progress, liveness violation, finality stall, censorship, withholding, delayed delivery;
- assume–guarantee, compositional liveness, timed contracts, deadline compatibility, end-to-end progress;
- trace equivalence, partial order, happens-before, Mazurkiewicz traces, causal summaries, schedule reduction, communication closure;
- serializability, commutativity, swappability, observable equivalence, deterministic replay;
- data availability sampling, availability proofs, targeted sampling, peer sampling, distributed arrays, custody, adaptive withholding;
- twins, clones, replicas with shared identity, adversary emulation, Byzantine mutation, fault injection, conformance, refinement, trace-language inclusion.

## 8.5. Проверенные смежные дисциплины

- discrete-event-system diagnosis;
- classical distributed computing and failure detectors;
- accountability and protocol forensics;
- formal methods/model checking;
- concurrency theory and trace languages;
- database serializability and software transactional memory;
- software testing/fuzzing/mutation testing;
- cryptographic security games;
- coding theory and P2P peer sampling;
- parameterized verification and cutoff theorems;
- refinement, observational simulation and conformance testing.

## 8.6. Недоступные или неполностью проверенные источники

- полный текст *SpecTrum: Specification-Guided Differential Fuzzing for Ethereum Consensus Clients* на дату поиска публично не найден; подтверждены title/authors/acceptance only;
- полный текст *Data Availability Attacks: Targeted Sampling for 2-D Reed–Solomon Codes in Blockchain Systems* не был доступен через открытый официальный источник;
- возможные unpublished Diem/Aptos internal notes по Twins coverage;
- paywalled dissertations, patents, private audits и engineering incident reports;
- материалы, где relevant theorem скрыт как secondary lemma и не отражён в title/abstract.

## 8.7. Части литературы, которые могли быть пропущены

- работы не на английском языке;
- conformance/refinement papers без blockchain/BFT terminology;
- formal-language results под терминами adversarial I/O automata или implementation relation;
- doctoral theses и workshop technical reports;
- GitHub issues/design documents;
- новые papers, появившиеся в течение дня 11 августа 2026 года или после него;
- результаты, известные engineering community, но не опубликованные академически.

## 8.8. Утверждения, которые остаются спекулятивными

- strong Twins completeness hypothesis;
- sufficiency exact full-causal-disclosure conditions;
- existence of practical fixed clone cutoff;
- nontriviality theorem after rigorous validity definition;
- transfer from toy protocol to HotStuff/Tendermint-like systems;
- absence of hidden resolution of conjecture in non-indexed literature.

## 8.9. Что должен проверить живой предметный специалист

1. Correctness and non-vacuity of arbitrary Byzantine/accepted-message model.
2. Relationship to I/O automata simulation/refinement.
3. Whether full disclosure already implies local transition verifiability in a standard formalism.
4. Known unpublished work by Twins authors and successors.
5. Whether trace-dependent clone bound is publication-worthy.
6. Choice of protocol class and target venue.
7. Expected level of mechanization and proof rigor.

## 8.10. Что необходимо сделать до публичного заявления о научной новизне

- получить full texts всех critical closest works;
- провести backward/forward citation search from Twins;
- проверить dissertations, patents and technical reports;
- связаться либо обсудить с expert in BFT testing/formal verification;
- выполнить minimal pilot;
- зафиксировать exact theorem statement and assumptions;
- проверить claim по Google Scholar, Semantic Scholar, DBLP, ACM, IEEE, arXiv and author repositories повторно;
- написать novelty statement только относительно clearly enumerated works and search date;
- не использовать формулировку «тема совершенно новая».

---

# КРАТКИЙ ФИНАЛЬНЫЙ ВЕРДИКТ

**Все пять исходных тем исключены из окончательного списка.**  
**Одна заменяющая тема выдержала аудит:** formal completeness boundaries of Twins-based safety testing for deterministic full-causal-disclosure BFT protocols.  
**Рекомендуемый следующий исследовательский артефакт:** bounded dual-adversary trace checker для `n=4, f=1`, который либо обнаружит separation counterexample, либо даст invariant для proof route.
