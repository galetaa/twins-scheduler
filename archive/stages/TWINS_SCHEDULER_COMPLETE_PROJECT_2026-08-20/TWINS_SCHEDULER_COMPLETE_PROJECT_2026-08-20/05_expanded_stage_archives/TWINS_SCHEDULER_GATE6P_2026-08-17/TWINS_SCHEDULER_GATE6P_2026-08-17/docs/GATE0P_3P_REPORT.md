# Gate 0′–3′: реализация и проверка scheduler-grammar pivot

**Дата:** 12 августа 2026 года  
**Статус:** завершён блокирующий mechanism pilot  
**Итог:** **ТРЕБУЕТ СУЖЕНИЯ; CONDITIONAL GO к Gate 4′**

## 1. Executive decision

Исходная finite-clone тема была отклонена предыдущим пилотом. Новый pivot проверяет другой объект: может ли view-level partition grammar быть safety-complete относительно более богатого управления доставкой сообщений.

Пилот не подтвердил сильную partition-normal-form гипотезу. Напротив, в точно заданном конечном классе получена строгая лестница:

\[
G_P\subsetneq G_D\subsetneq G_T\subsetneq G_M
\]

по множествам agreement-violating observations.

Это **не** означает, что partition-based Twins бесполезен: положительный контроль воспроизводит классический split между twin branches. Результат означает, что полнота partition scenarios не может быть универсальной без дополнительных semantic conditions на protocol implementation.

Продолжение перспективно только в форме:

> characterization условий, при которых добавление доставок, вынужденное partition/type/instance closure, сохраняет safety witness.

Создание более богатого DSL или нового fault injector само по себе научным вкладом не является.

## 2. Проверенная operational semantics реального harness

Source snapshot зафиксирован на `relab/hotstuff` commit:

`3179c6e62929294961acbfd9bf8445769716a121`.

Из кода следует:

1. один элемент `View` содержит leader и коллекцию partitions;
2. sender/receiver в одном partition проходят;
3. иначе сообщение теряется, если его runtime type входит в `dropTypes`;
4. `ExecuteScenario` передаёт proposal, vote, hash, new-view и timeout types;
5. partition/leader pairs строятся по views;
6. встроенный safety checker исключает identities, имеющие twins, и помечает это TODO.

В комментарии `ExecuteScenario` указано, что Timeout/NewView разрешены, но фактический список `dropTypes` включает их. Поэтому source code, а не комментарий, принят как основание model extraction.

Точное соответствие event-loop semantics пока не доказано. Gate 1′ моделирует только ключевое closure-ограничение: одна symmetric partition relation на view и единое решение для контролируемых типов.

## 3. Gate 0′: prior art и novelty

### 3.1 Что уже известно

- Twins задаёт clone/partition testing family.
- Communication-closure work исследует reduction к lossy synchronous executions и testing hypothesis.
- Heard-Of/message-adversary theory использует per-round receive sets и directed communication graphs.
- Netrix-подобный DSL уже допускает message-level drop/delay/reorder/replay.
- Randomized BFT testing, distributed fuzzing и BFT benchmark frameworks уже существуют.

### 3.2 Что нельзя заявлять

Нельзя заявлять новизной:

- directed graphs;
- per-message filters;
- richer scheduler API;
- ещё один BFT benchmark;
- reduction к простым schedules без нового preservation theorem.

### 3.3 Остаточная заявка

В scoped search не найдена работа, одновременно задающая рассматриваемую grammar hierarchy, unsafe-observation projection и closure-preservation characterization для natural class of view-based BFT implementations.

Gate 0′ получает **CONDITIONAL PASS**, потому что ближайший скрытый prior art может находиться в generic refinement, conformance или communication-closed protocol theory.

## 4. Gate 1′: формальная модель

Полная спецификация находится в `spec/definitions.md`.

### 4.1 Protocol machine

Протокол конечен и детерминирован. Execution ограничен одним logical view с несколькими ordered micro-stages. Message instance имеет unique ID, type, endpoints и canonical emission order.

### 4.2 Safety observation

Наблюдаются решения designated correct replicas. Unsafe означает наличие двух различных non-bottom decisions.

### 4.3 Grammars

| Grammar | Управление |
|---|---|
| `G_P_PARTITION` | одна equivalence partition relation для view |
| `G_D_DIRECTED_VIEW` | один directed graph для view |
| `G_T_TYPE_SPECIFIC` | directed graph для каждого message type |
| `G_M_PER_MESSAGE` | arbitrary ordered subset конкретных instances на micro-stage |

### 4.4 Constructive inclusions

Каждая слабая policy конструктивно встраивается в следующую сильную. Checker проверил inclusion observation languages для всех четырёх pilot protocols.

### 4.5 Ограничения

Нет clocks, cross-view late delivery, replay, payload mutation, Byzantine transition generation или liveness. Static grammars используют canonical delivery order. Поэтому результат ограничен scheduler expressiveness в заявленной абстракции.

Gate 1′: **PASS**.

## 5. Gate 2′: resources и воспроизводимость

Артефакт использует только Python standard library. Внешние services и datasets отсутствуют.

Зафиксировано:

- CPython 3.13.5;
- uv 0.10.0;
- pytest 9.0.2 как дополнительный runner;
- authoritative stdlib self-check;
- `PYTHONHASHSEED=0`;
- upstream source SHA-256;
- MIT licenses.

Gate 2′: **PASS**.

## 6. Gate 3′: decisive mechanism pilot

### 6.1 Протоколы

#### `ECHO_GATE`

Leader запускает A и B. Запущенные реплики отправляют peer echo. В конце view реплика без peer echo принимает своё значение. Это intentional diagnostic machine для проверки asymmetric/non-transitive delivery.

#### `TYPE_SPLIT`

Leader отправляет primary certificate value 0 и fallback certificate value 1 обоим наблюдателям. Каждый принимает первый полученный certificate. Модель проверяет возможность different delivery by message type.

#### `INSTANCE_ORDER`

Leader отправляет два same-type certificate instances в canonical order. Статические grammars не различают instances; per-message scheduler может выбрать разные first certificates для A и B.

#### `TWIN_BRANCH_CONTROL`

Две физические twin branches T0/T1 отправляют conflicting certificates. Partition `{T0,A}/{T1,B}` воспроизводит split. Это positive control.

### 6.2 Исчерпывающие результаты

| Protocol | Grammar | Policies/executions | Observations | Unsafe observations |
|---|---:|---:|---:|---:|
| ECHO_GATE | partition | 5 | 3 | 0 |
| ECHO_GATE | directed | 64 | 4 | 1 |
| ECHO_GATE | type-specific | 4096 | 4 | 1 |
| ECHO_GATE | per-message | 15 | 4 | 1 |
| TYPE_SPLIT | partition | 5 | 4 | 0 |
| TYPE_SPLIT | directed | 64 | 4 | 0 |
| TYPE_SPLIT | type-specific | 4096 | 9 | 2 |
| TYPE_SPLIT | per-message | 65 | 9 | 2 |
| INSTANCE_ORDER | partition | 5 | 4 | 0 |
| INSTANCE_ORDER | directed | 64 | 4 | 0 |
| INSTANCE_ORDER | type-specific | 64 | 4 | 0 |
| INSTANCE_ORDER | per-message | 65 | 9 | 2 |
| TWIN_BRANCH_CONTROL | partition | 15 | 9 | 2 |
| TWIN_BRANCH_CONTROL | directed | 4096 | 9 | 2 |
| TWIN_BRANCH_CONTROL | type-specific | 4096 | 9 | 2 |
| TWIN_BRANCH_CONTROL | per-message | 65 | 9 | 2 |

Policy count не является метрикой качества: разные grammars имеют разные parameterizations. Решающий объект — наличие stronger-only unsafe observation.

### 6.3 Минимальные separating witnesses

#### Partition vs directed

```text
allowed directed edges: L→A, L→B
start delivered to A and B
A→B echo dropped
B→A echo dropped
result: A=0 | B=1
```

Partition closure объединяет L, A и B в один block, доставляет echoes и меняет результат на `A=-|B=-`.

#### Directed vs type-specific

```text
PRIMARY_CERT: L→A
FALLBACK_CERT: L→B
result: A=0 | B=1
```

Type erasure включает endpoint edges L→A и L→B для всех types. Оба наблюдателя видят primary first: `A=0|B=0`.

#### Type-specific vs per-message

```text
deliver cert0→A
then cert1→B
omit the other instances
result: A=0 | B=1
```

Instance completion доставляет обе certificate instances на обоих selected type-edges в canonical order: `A=0|B=0`.

### 6.4 Machine-checked claims

- every weak language is included in its stronger neighbor for each protocol;
- `G_P⊊G_D` on unsafe observations;
- `G_D⊊G_T` on unsafe observations;
- `G_T⊊G_M` on unsafe observations;
- all three designated closures destroy the designated unsafe witness;
- partition grammar finds the Twins positive control.

Gate 3′: **CONDITIONAL PASS / GO WITH NARROWING**.

## 7. Научный смысл отрицания strong hypothesis

Сильная гипотеза предсказывала, что различия raw schedules могут quotient-иться без потери safety witnesses. Пилот показывает три независимых причины отказа:

1. **topological closure effect:** partition adds links absent in a directed witness;
2. **type closure effect:** endpoint-level rule adds semantically different message types;
3. **instance closure effect:** type-level rule adds/reorders semantically distinct instances.

Дополнительные valid messages могут изменять locks, accepted certificates или timeout paths. Поэтому completeness требует protocol-level preservation condition, а не только combinatorial schedule embedding.

## 8. Что станет известно при дальнейшем отрицательном результате

Если natural locking model не даст separation и получится closure theorem, станет известно, что partitions достаточно expressive для указанного protocol class, несмотря на strictness в общем finite class.

Если natural separation будет найден, станет известно минимальное scheduler capability, необходимое для конкретного класса safety bugs.

Если не получится ни theorem, ни natural witness, проект должен быть остановлен: synthetic hierarchy сама по себе недостаточна как статья.

## 9. Verdict и next gate

### Разрешено

Продолжить к Gate 4′ с узким тезисом о closure preservation.

### Запрещено

- начинать новый production-grade framework;
- заявлять HotStuff vulnerability;
- заявлять universal incompleteness всех Twins campaigns;
- переходить к benchmark-only evaluation.

### Gate 4′

Нужны locking baseline, semantic mutants, view-indexed delays/replay и actual executor conformance. Подробный backlog находится в `ROADMAP_GATE4P.md`.

## 10. Reproduction contract

```bash
./scripts/reproduce.sh
```

Успешный запуск должен выдать:

```text
SELF-CHECK PASS
12 passed
REPRODUCTION PASS
core_files_byte_identical=9
```

Authoritative outputs:

- `results/pilot/language_summary.csv`;
- `results/pilot/adjacent_separations.csv`;
- `results/pilot/suite_hierarchy.json`;
- `results/pilot/closure_counterfactuals.json`;
- `results/pilot/witnesses.jsonl`;
- `results/pilot/gate_decision.json`.
