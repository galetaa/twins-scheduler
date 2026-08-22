# Gate 5′ — формальная характеризация и межпротокольная проверка

**Дата закрытия:** 15 августа 2026 года  
**Пакет:** `TWINS_SCHEDULER_GATE5P_2026-08-15`  
**Решение:** **PASS / GO TO GATE 6′**  
**Статус суженной темы:** **ГОТОВО К ПОЛНОЙ ИССЛЕДОВАТЕЛЬСКОЙ РЕАЛИЗАЦИИ В
ОГРАНИЧЕННОМ SCOPE**

---

## 1. Executive decision

Gate 5′ закрыт положительно. Бounded-наблюдения Gate 4′ удалось превратить в
повторно используемый theorem-and-counterexample package и перенести на второй
certificate-driven locking kernel.

Окончательная рабочая тема:

> **Границы сохранения safety-наблюдений при замыкании грамматик планировщика в
> certificate-driven locking BFT-протоколах**

> **Safety-Observation Closure Boundaries of Scheduler Grammars for
> Certificate-Driven Locking BFT Protocols**

Главный научный объект — не API тестировщика и не количество найденных ошибок, а
отношение между языками конечных executions после проекции на agreement
observations:

\[
UnsafeObs(L_{G_x}(P)).
\]

Gate 5′ даёт пять ограниченных результатов:

1. replay-erasure theorem при stable-key idempotence;
2. relational closure-lifting theorem для closure-added messages;
3. параметрическое quorum-pivot separation между `G_D` и `G_T`;
4. условный bounded terminal-delay corollary;
5. constructive replay separation при message-instance counting.

Главный оставшийся риск — не реализуемость, а публикационная строгость: T3 нужно
независимо проверить или механизировать, а одну controlled mutation желательно
провести через более полный consensus event loop. Это задача Gate 6′.

---

## 2. Почему Gate 5′ был необходим

Gate 4′ показал, что в bounded locking model типо-однородный directed graph
может пропускать phase-sensitive safety witnesses. Этого было недостаточно для
статьи по трём причинам:

1. результат мог быть артефактом одной staging model;
2. условия separation были выражены именами мутантов;
3. richer message filters уже существуют в Netrix, randomized BFT testing и
   других инструментах.

Поэтому Gate 5′ отвечал на один decision question:

> Можно ли выразить обнаруженную границу как theorem, separation condition или
> impossibility result, не зависящий от названий конкретных мутантов?

Ответ: **да, но только в суженной форме**.

---

## 3. Нормализованная спецификация темы

### 3.1. Исследовательский вопрос

При каких локальных свойствах protocol transitions стирание phase/type labels и
переход от per-phase delivery к одному directed graph на view сохраняет finite
agreement observations, и какой структурный механизм делает такое стирание
неполным?

### 3.2. Основной тезис

При R-monotone closure добавленные сообщения не уничтожают unsafety. Однако в
locking BFT protocol repair или terminal evidence может удалить единственного
честного quorum pivot, необходимого для позднего conflicting certificate. Тогда
phase-specific schedule способен доставить enabling evidence и удержать repair,
а type-uniform directed edge вынужден доставить оба или ни одного.

### 3.3. Ближайшая альтернатива

Все safety-relevant per-phase schedules нормализуются к одному directed graph на
view; различия richer grammar касаются только внутренних traces или лишних
вариантов одного и того же witness.

### 3.4. Фальсификатор

Сильная версия separation отвергается, если:

- T3 сводится к предположению полного language inequality;
- второй protocol kernel не сохраняет zero/nonzero detection classes;
- type-erasure closure не уничтожает минимальные witnesses;
- correct baseline становится unsafe при richer grammar;
- найден prior-art theorem с той же closure и safety projection.

### 3.5. Scope

Включено:

- deterministic finite executions;
- agreement observations;
- certificate-driven view/round protocols;
- `n=4,f=1` exact kernels;
- параметрическая quorum arithmetic для `n=3f+1`;
- phase/type erasure, terminal-time erasure и replay erasure;
- локальные controlled mutations;
- pinned source mapping и local Go fixtures.

Не включено:

- liveness;
- unbounded partial synchrony;
- вероятность обнаружения ошибки;
- production vulnerability claims;
- public-network experiments;
- новый scheduler DSL;
- universal minimality одной grammar.

---

## 4. Реализованный артефакт

Артефакт состоит из шести слоёв.

### 4.1. Frozen Gate 4′ evidence

`archive/gate4p_frozen/` содержит immutable baseline для первого locking kernel:
language matrix, separations, witnesses, closures и theorem checks.

### 4.2. Второй Tendermint-style kernel

`src/schedcheck/tendermint/` реализует:

- proposal;
- prevote;
- POLKA как +2/3 prevote evidence;
- persistent locked value/round;
- valid value/round;
- precommit;
- commit;
- independent agreement oracle.

Модель использует `n=4`, `f=1`, quorum 3, honest replicas `H1–H3` и одну
Byzantine identity, физически представленную twins `T0/T1`.

### 4.3. Шесть scheduler grammars

\[
G_P,\ G_D,\ G_{D1},\ G_T,\ G_M,\ G_R.
\]

- `G_P`: симметричная partition relation;
- `G_D`: type-uniform directed graph на view;
- `G_D1`: `G_D` плюс one-view terminal delay;
- `G_T`: отдельная endpoint policy для каждой phase/type;
- `G_M`: per-message choice;
- `G_R`: `G_M` плюс один bounded replay.

### 4.4. Формальные executable checks

- `src/schedcheck/gate5/closure.py` — локальные premises closure theorem и
  failed-premise counterexample;
- `src/schedcheck/gate5/phase.py` — малая finite phase model;
- `src/schedcheck/gate5/phase_coupled.py` — параметрическая quorum construction;
- `src/schedcheck/formal/vote_processing.py` — replay erasure и strict boundary.

### 4.5. Implementation correspondence

Pinned CometBFT source:

- release `v0.40.0`;
- commit `0880b4d378f347ab16e54ec677ff50d803f37d62`;
- `consensus.md`, `state.go`, `vote_set.go` и Apache-2.0 license;
- SHA-256 manifest и source registry.

Два dependency-free Go fixtures проверяют:

- extensional equality Python/Go vote processing;
- duplicate-vote inertness;
- lock-before-precommit ordering;
- controlled lock-omission и instance-counting boundaries.

### 4.6. Reproducibility layer

- deterministic exact search;
- no runtime Python dependencies;
- pinned source snapshots;
- source and artifact manifests;
- independent oracle;
- one-command reproduction;
- clean-copy verification.

---

## 5. Формальные результаты

## 5.1. T1 — replay-erasure theorem

Если повторная доставка одного replay key является protocol-state stutter, не
добавляет voting power и не создаёт новых messages, то удаление duplicates
сохраняет terminal state и safety observation:

\[
O(L_{G_R}(P))=O(L_{G_M}(P)).
\]

Доказательство — induction по числу duplicate occurrences.

Граница строгая. При подсчёте message instances последовательность

```text
B, H1, H1
```

достигает трёх instances, но содержит только две validator contributions.

Executable evidence:

- 364 sequences до длины 5;
- 0 idempotence counterexamples;
- минимальный one-replay non-idempotent witness `B,H1,H1`;
- 728 Go/Python conformance cases;
- strict `G_M` versus `G_R` separation в двух kernels.

## 5.2. T2 — relational closure lifting

Пусть `R` — preorder по protocol-relevant states. Если:

1. closure-added message является R-increasing;
2. original transitions forward-simulate `R`;
3. unsafe predicate upward closed по `R`;

то вставка closure-added messages с сохранением порядка original transitions не
может превратить unsafe trace в safe.

Gate 5′ содержит положительный finite example, где все premises выполнены, и
locking counterexample, где repair message удаляет future action pivot. В
counterexample:

```text
unsafe_before = true
unsafe_after_type_closure = false
```

Следовательно, ключевая причина separation — не «больше вариантов», а
немонотонность будущей safety-relevant enabledness относительно добавленных
messages.

## 5.3. T3 — parametric quorum-pivot separation

Для каждого `f≥1` строятся:

\[
n=3f+1,\qquad q=2f+1,
\]

и два conflicting supports:

\[
Q_0=B\cup A\cup\{p\},\qquad Q_1=B\cup C\cup\{p\},
\]

где `|B|=|A|=|C|=f`, а `p` — единственный честный участник пересечения.

Base support каждого quorum равен `2f`, то есть на единицу меньше threshold.

- `G_T` доставляет enabling evidence `e` к `p`, но удерживает repair/terminal
  message `r`; defect оставляет `p` доступным обеим ветвям; оба quorum достигают
  `2f+1`.
- `G_D` связывает `e` и `r` на одном edge. Если edge закрыт, первый quorum имеет
  `2f`. Если открыт, `r` отключает `p` до второй ветви, и второй quorum имеет
  `2f`.

Отсюда существует family `P_f` с:

\[
UnsafeObs(G_D)=\varnothing,
\qquad
UnsafeObs(G_T)\ne\varnothing.
\]

Алгебра задаёт результат для любого положительного `f`; executable regression
проверяет `f=1…8`.

## 5.4. T4 — terminal-delay boundary

Если coupled repair message является terminal evidence и его one-view deferral
не меняет прочие enabling transitions, `G_D1` воспроизводит phase-specific
witness. Immediate-delivery closure уничтожает его.

Это не означает `G_T⊆G_D1`: discrimination между двумя non-terminal phases может
по-прежнему требовать `G_T`.

## 5.5. T5 — strict non-idempotent replay boundary

Если accumulator считает instances вместо contribution identities, один replay
может создать certificate, отсутствующий после replay erasure. Exact kernels
демонстрируют agreement violation только в `G_R` для controlled duplicate-count
mutation.

---

## 6. Результаты второго exact kernel

Correct baseline безопасна во всех 24 комбинациях `4 cases × 6 grammars`.

| Controlled obligation violation | `G_P` | `G_D` | `G_D1` | `G_T` | `G_M` | `G_R` |
|---|---:|---:|---:|---:|---:|---:|
| Omitted POLKA lock update | 0 | 0 | **12** | **9** | **9** | **9** |
| Wrong valid-round value/strictness guard | 0 | 0 | **12** | **9** | **9** | **9** |
| Duplicate vote instances counted | 0 | 0 | 0 | 0 | 0 | **12** |
| Receiver validation omission, positive control | **1** | 1 | 3 | 3 | 3 | 3 |

Значения — число различных agreement-violating decision observations, а не
число schedules.

Дополнительные проверки:

- 15 serialized minimal witnesses;
- все 15 проходят повторное исполнение;
- все 15 проходят независимо написанный mutable-state oracle;
- 5 selected closure counterfactuals уничтожают соответствующий witness;
- standard grammar inclusions выполняются;
- `G_D⊆G_D1` выполняется;
- positive control обнаруживается уже `G_P`.

---

## 7. Межпротокольный перенос

Сопоставлены четыре mechanisms:

1. persistent lock omission;
2. justification guard error;
3. duplicate-vote instance counting;
4. receiver-validation omission control.

Для каждого mechanism и каждой из шести grammars сравнивалась бинарная class:
`unsafe observations = 0` либо `>0`.

Результат:

```text
24 / 24 mapped mechanism-grammar pairs preserve the zero/nonzero class.
```

Это не доказывает универсальность. Оно исключает более слабое объяснение, что
Gate 4′ separation был только следствием названий стадий первого kernel.

---

## 8. Соответствие официальной CometBFT semantics

На дату исследования официальная pinned версия — CometBFT `v0.40.0`.
Source mapping проверяет пять obligations:

1. exact duplicate vote возвращает `added=false, err=nil`;
2. voting power добавляется при первом заполнении validator slot;
3. +2/3 prevotes приводят к persistent lock assignment;
4. proposal несёт `ValidRound`;
5. official specification использует Propose → Prevote → Precommit и PoLC lock
   transition.

Все пять source obligations имеют статус PASS.

Implementation correspondence намеренно ограничено:

- lock assignment precedes the abstract precommit action in pinned source;
- duplicate vote is inert at VoteSet layer;
- controlled fixture показывает, что удаление lock либо instance counting
  меняет abstract safety-relevant enabledness.

Это **не** full CometBFT conformance и **не** security finding.

---

## 9. Prior art и novelty delta

Gate 5′ не заявляет новизну следующих компонентов:

- directed communication graphs;
- Heard-Of/message-adversary representations;
- communication closure;
- message filters;
- drop, delay, reorder и replay;
- randomized BFT testing;
- mutation testing;
- Twins scenarios;
- Tendermint locking;
- duplicate-vote rejection;
- checker implementation.

Ограниченная novelty delta:

> property-preserving closure condition плюс parametric quorum-pivot separation
> для перехода от per-phase delivery к одному directed graph на view, совместно
> с replay-erasure boundary по stable-key idempotence.

Поиск не обнаружил источник с той же полной комбинацией. Это ограниченное
отрицательное утверждение, а не доказательство абсолютной новизны.

---

## 10. Threats to validity

### 10.1. Internal validity

- Kernels bounded и barrier-based.
- Mutations controlled, а не найденные production defects.
- Exact counts зависят от выбранной observation projection.
- Второй kernel структурно родственен первому.

Меры: correct baselines, positive control, independent oracle, closure
counterfactuals, frozen cross-kernel comparison и source mapping.

### 10.2. Construct validity

`G_D` означает один type-uniform directed graph на view, а не любой реалистичный
network adversary. `G_T` различает phases/kinds, но не моделирует произвольное
время. `G_D1` добавляет только one-view terminal delay.

### 10.3. External validity

Результат пока не переносится автоматически на:

- production HotStuff/CometBFT event loops;
- protocols без explicit phases;
- asynchronous DAG consensus;
- liveness;
- dynamic validator sets;
- weighted non-uniform quorum geometry;
- unbounded executions.

### 10.4. Conclusion validity

Количество unsafe observations не является effect size или bug probability.
Решение основано на strict set difference, mechanism closure и theorem premises.

---

## 11. Gate decision table

| Work package | Статус | Основание |
|---|---|---|
| WP5.0 novelty refresh | CONDITIONAL PASS | Результат отличен от DSL/API claim; hidden prior art остаётся риском |
| WP5.1 abstract protocol class | PASS | Grammars, closures, observations и boundaries заданы |
| WP5.2 theorem/counterexample | PASS | T1–T5, positive theorem premises и structural separation |
| WP5.3 second natural kernel | PASS | Tendermint-style exact model переносит key classes |
| WP5.4 implementation correspondence | CONDITIONAL PASS | Pinned source + local fixtures; не full event-loop conformance |
| WP5.5 publication kill test | PASS WITH NARROW CLAIM | Вклад формулируется theorem/separation, не tool |
| **Gate 5′** | **PASS / GO TO GATE 6′** | Formal result + independent bounded instantiation получены |

---

## 12. Что стало известно при отрицательных исходах

Даже если Gate 6′ опровергнет широкую публикационную интерпретацию, Gate 5′ уже
устанавливает:

- richer scheduler API не является вкладом;
- replay power исчезает при explicit idempotence premise;
- added messages не всегда монотонны относительно safety witness;
- terminal delay и phase discrimination — разные виды expressiveness;
- один directed graph на view может быть неполон для конкретной parameterized
  protocol family;
- bounded witness counts нельзя трактовать как prevalence.

Отрицательный результат сохраняет требуемую научную ценность.

---

## 13. Gate 6′

Следующий gate должен закрыть не ещё один benchmark, а три риска:

1. proof hardening T1–T3;
2. model-to-event-loop correspondence;
3. external validity и reviewer-proof novelty statement.

Gate 6′ не должен включать public-network experiments, exploit development,
большой DSL или случайное наращивание mutants.

Подробный план находится в `ROADMAP_GATE6P.md`.

---

## 14. Воспроизводимость

Основная команда:

```bash
./scripts/reproduce.sh
```

Она выполняет:

1. exact Gate 5′ runner;
2. Tendermint language enumeration;
3. formal family/replay/closure checks;
4. source obligation checks;
5. 728 Go/Python conformance cases;
6. controlled Go fixture tests;
7. regression tests;
8. independent self-check;
9. manifest verification.

Эксперимент полностью локален и не обращается к mainnet, testnet, RPC или
external services.

---

## 15. Итог

**Gate 5′ закрыт: PASS / GO TO GATE 6′.**

Суженная тема достигла уровня, на котором можно продолжать полноценную
реализацию без повторного концептуального выбора. При этом публикационная заявка
остаётся условной: Gate 6′ обязан укрепить доказательства и связь с более полным
implementation execution, иначе результат следует публиковать только как
bounded formal characterization.
