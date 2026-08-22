# Gate 6′ — proof hardening, fuller event-loop validation и анализ границ применимости

**Дата закрытия:** 17 августа 2026 года  
**Решение:** **PASS / GO TO GATE 7′**  
**Итоговый research status:** **READY FOR REPRODUCIBLE PAPER AND ARTIFACT BUILD IN NARROW SCOPE**

---

## 1. Executive decision

Gate 6′ закрыт положительно. Параметрическая phase-coupled separation не
оказалась артефактом малой phase-barrier модели и не распалась при уточнении
предпосылок. Она прошла четыре независимых маршрута проверки:

1. checked proof certificate для универсальной арифметики и двух ветвей `G_D`;
2. независимый Go `math/big` checker;
3. полный перебор всех Boolean premise configurations поставленной
   construction;
4. локальный двухраундовый consensus event loop с реальным порождением и
   обработкой proposal, vote и certificate events.

Основной тезис остаётся строго ограниченным:

> В явном классе конечных certificate-driven locking schemas closure,
> стирающее message phase/type и объединяющее их в один directed endpoint edge,
> может добавить repair evidence, которое устраняет agreement-violating witness
> путём отключения единственного честного quorum pivot.

Это existence/separation result, а не универсальная неполнота всех partition или
directed schedulers.

Полную реализацию статьи теперь можно продолжать без нового концептуального
решения. Однако подача статьи ещё преждевременна: текущий малый proof kernel
нуждается в независимом human review либо переносе в зрелый proof assistant.

---

## 2. Цель и критерии Gate 6′

Gate 5′ оставил два блокирующих риска:

- T3 был publication-grade proof sketch, но не checked proof;
- controlled mutation ещё не проходила через fuller consensus event loop.

Gate 6′ считался успешным только при одновременном выполнении условий:

1. T1–T3 имеют проверяемые доказательные assets без admitted lemmas;
2. T3 не является круговым следствием определения;
3. независимая арифметическая реализация подтверждает construction;
4. fuller-loop baseline остаётся safe;
5. controlled mutation даёт unsafe witness только в предсказанной grammar;
6. ближайшие directed closures уничтожают witness тем же mechanism;
7. хотя бы одно условие construction проходит necessity analysis;
8. результаты воспроизводятся локально без сети и внешних datasets.

Все восемь условий выполнены.

---

## 3. Замороженная научная постановка

Исследуются конечные agreement observations deterministic
certificate-driven, round/view-based BFT schemas.

Используются scheduler grammars:

- `G_D`: один directed endpoint graph на round для всех контролируемых phases;
- `G_T`: отдельная admission policy для каждой phase/type;
- `G_M`: per-message delivery;
- `G_R`: per-message delivery с bounded replay.

Главная closure:

\[
C_{type}:G_T\rightarrow G_D
\]

сохраняет использованные endpoint edges, но стирает phase labels: если edge
разрешён хотя бы для одной phase, он разрешается для всех контролируемых phases.

Safety observation:

\[
O(s)=(decision_i)_{i\in H},
\]

а state unsafe, если две correct identities имеют разные non-null decisions.

---

## 4. T1 — replay-erasure theorem

### 4.1. Утверждение

Пусть duplicate delivery определяется stable replay key. Если повторная
обработка:

- не меняет protocol-relevant state;
- не генерирует relevant output;
- не добавляет voting power;
- не влияет на последующие transitions;
- не меняет выбранное observation,

то удаление всех non-first occurrences сохраняет конечный результат:

\[
O(L_{G_R}(P))=O(L_{G_M}(P)).
\]

### 4.2. Проверенный proof route

Мера induction — число non-first replay-key occurrences. Base case является
identity. В step удаляется один duplicate stutter; suffix congruence сохраняет
остаток execution, а мера уменьшается на один.

Certificate проверяет:

- theorem не предполагается как premise;
- все rule dependencies доступны до применения;
- measure-decrease fact получен явно;
- base, step и final target согласованы.

### 4.3. Граница

Theorem заведомо неверна при instance counting, side-effectful callbacks,
observable resource counters, timer resets или иных non-stuttering duplicate
handlers. Поэтому T1 является условной границей, а не общим утверждением о
replay.

---

## 5. T2 — relational closure lifting

### 5.1. Утверждение

Пусть closed trace вставляет дополнительные actions, сохраняя порядок original
actions. Если существует preorder `R`, такой что:

1. inserted action является `R`-increasing;
2. original action forward-simulates `R`;
3. `Unsafe` upward-closed по `R`,

то unsafe original trace после closure остаётся unsafe.

### 5.2. Проверенный proof route

Induction выполняется по длине remaining merged suffix. На added action relation
сохраняется transitivity; на original action — forward simulation. В terminal
state upward closure переносит unsafety.

### 5.3. Почему T2 не уничтожает novelty

Locking repair message способен сделать состояние «более информированным», но
одновременно удалить будущую возможность pivot поддержать конфликтующий quorum.
Поэтому такой transition не является monotone относительно relation,
сохраняющего safety-relevant capabilities. Phase-coupled separation является
точной failed-premise boundary T2.

---

## 6. T3 — parametric quorum-pivot separation

### 6.1. Construction

Для каждого `f≥1`:

\[
n=3f+1,\qquad q=2f+1.
\]

Validators делятся на:

- `B`, `|B|=f` Byzantine identities;
- `A`, `|A|=f` honest left-only supporters;
- `C`, `|C|=f` honest right-only supporters;
- pivot `p`.

Конфликтующие supports:

\[
Q_0=B\cup A\cup\{p\},
\qquad
Q_1=B\cup C\cup\{p\}.
\]

Оба имеют размер `q`; fixed base каждой ветви имеет размер `2f=q-1`.

На одном edge к `p` находятся:

- enabling evidence `E`;
- более позднее repair/terminal evidence `R`.

### 6.2. `G_T`

`G_T` доставляет `E`, но удерживает `R`. Controlled defective transition
оставляет `p` доступным для обеих ветвей. Оба supports достигают `2f+1`, поэтому
unsafe observation достижимо.

### 6.3. `G_D`

Type-uniform edge имеет две возможности:

- edge absent: `E` и `R` отсутствуют, первый symmetric support остаётся `2f`;
- edge present: доставляются оба; первый quorum формируется, после чего `R`
  исключает `p` из второй ветви, оставляя `2f`.

Следовательно, для construction:

\[
UnsafeObs(G_D)=\varnothing,
\qquad
UnsafeObs(G_T)\neq\varnothing.
\]

### 6.4. Проверки

Exact proof certificate нормализует все polynomial equalities и доказывает
`q-2f=1`. Независимый Go checker использует arbitrary-precision integers и
проверил:

- `f=1…1024`;
- четыре особенно большие величины;
- всего 1 028 cases;
- максимальный `f` содержит 400 decimal digits.

Это не заменяет symbolic proof; оно исключает machine-word overflow и ошибку
одной реализации.

---

## 7. T6 — точная premise characterization

Gate 6′ не ограничился one-at-a-time ablation. Проверены все 128 assignments
семи Boolean premises.

Field order:

1. first base short by one;
2. second base short by one;
3. second pivot requires `E`;
4. `R` disables pivot;
5. `R` действует до second-quorum opportunity;
6. `E` и `R` используют один endpoint edge;
7. `G_T` может разделить `E` и `R`.

Strict separation возникает только для:

```text
0111111
1101111
1111111
```

Точная формула:

\[
S_2\land D\land T\land E\land X\land(S_1\lor R_q).
\]

Пять условий обязательны во всех strict assignments данной модели:

- second base short by one;
- effective repair;
- timely repair;
- shared endpoint edge;
- phase-splitting power.

`first_base_short_by_one` и `second_pivot_requires_E` по отдельности не
обязательны, но хотя бы одно из них необходимо.

Важно: это necessary-and-sufficient result для семифлаговой construction, не
для всего protocol class.

---

## 8. Fuller consensus event loop

### 8.1. Реализованные transitions

Go fixture содержит:

```text
PROPOSAL -> PREVOTE -> POLKA -> PRECOMMIT -> COMMIT
```

Сообщения порождаются handlers и помещаются в explicit FIFO queue. Leader
формирует certificates только после уникальных logical votes. Correct replicas
поддерживают persistent locks и irreversible decisions.

Участники: `B`, `H1`, pivot `P`, `H3`; quorum `3`. Round 0 предлагает `0`, round
1 — конфликтующее `1`.

### 8.2. Controlled mutation

`MISSING_LOCK_UPDATE` пропускает только assignment persistent lock после POLKA.
Остальная transition logic совпадает с baseline.

### 8.3. Scheduler policies

Контролируется round-0 edge `B→P`:

- `G_T`: proposal/POLKA проходят, COMMIT удерживается;
- `G_D off`: edge закрыт для всех phases;
- `G_D on`: edge открыт для всех phases.

### 8.4. Результаты

| Grammar | Baseline | Missing lock update |
|---|---|---|
| `G_T_TYPE_SPECIFIC` | safe; `H1` decides 0, pivot locks 0 | **unsafe**; `H1=0`, `P=1`, `H3=1` |
| `G_D_ROUND0_EDGE_OFF` | safe; round 1 decides 1 | safe; round 0 lacks quorum |
| `G_D_ROUND0_EDGE_ON` | safe; `H1=P=0` | safe; terminal evidence makes `P=0`, so round 1 lacks pivot |

Correct baseline безопасна во всех трёх grammars. Это исключает объяснение
«богатый scheduler сам создаёт нарушение».

### 8.5. Независимая conformance

Python implementation написана отдельно и не импортирует Gate 4′/5′ kernels.
Go и Python совпали по всем canonical terminal fields:

- unsafe flag;
- decisions;
- locks;
- POLKA rounds;
- COMMIT rounds.

Результат: **6/6 cases, 0 mismatches**.

---

## 9. Sensitivity analysis

### 9.1. Event order

Проверены:

- FIFO;
- LIFO;
- 256 seeded random queue selectors.

Всего:

- 258 scheduler runs;
- 1 548 grammar/mutation case runs;
- 0 classification failures;
- один terminal signature на каждый case.

Эта проверка относится только к bounded causal event-order variation внутри
fixture. Она не является liveness или arbitrary-asynchrony theorem.

### 9.2. Parameter sensitivity

Python construction проверена для:

- `f=1…256`;
- 256 random positive `f` до `10^18`;
- seed `60617`;
- 512 cases;
- 0 failures.

Go big-int route отдельно проверил 1 028 cases.

---

## 10. Proof assurance и trusted computing base

Использован 503-line dependency-free proof kernel:

- 431 nonblank/noncomment lines;
- SHA-256 закреплён в result file;
- runtime dependencies отсутствуют;
- malicious polynomial syntax и tampered certificates отклоняются tests.

Доверенными остаются:

- CPython;
- kernel implementation;
- semantic validity named Horn rules;
- standard induction principle;
- mapping proof fields to protocol premises.

Поэтому корректная формулировка статуса — **checked by a small trusted proof
script**, а не «fully mechanized theorem in Lean/Coq/Isabelle».

---

## 11. Focused prior-art refresh

Проверены communication closure, directed message adversaries, Twins,
ByzzFuzz, Netrix, ByzzBench и combinations terminology вокруг phase-specific
scheduling и safety projection.

Ближайшие работы уже дают:

- reduction к lossy synchronous executions;
- произвольные directed communication graph models;
- clone/partition testing;
- per-message drop/delay/reorder/replay filters;
- mutation-based BFT testing;
- benchmark infrastructure.

Поэтому новый API или богатый scheduler не является вкладом.

В проверенных источниках не найден результат, одновременно задающий
`C_type`, safety-observation preservation/separation и repair/pivot mechanism.
Отсутствие найденной работы не доказывает абсолютную новизну; остаётся риск
скрытого prior art в refinement, conformance, dissertations и engineering
material.

---

## 12. Validity assessment

### Internal validity

Сильные стороны:

- exact logical outcomes вместо statistical metric;
- baseline controls;
- controlled single mutation;
- independent Go/Python implementations;
- tamper tests;
- complete Boolean premise state space;
- arbitrary-precision arithmetic.

Оставшийся риск — shared specification error и ограниченная зрелость custom
proof kernel.

### Construct validity

Safety определена только как agreement among correct decisions. Repair model
представляет message-mediated decision/constraint restoration. Протоколы с
indirect repair, weighted quorums или локальными timer effects потребуют нового
mapping.

### External validity

Результат перенесён между двумя exact kernels и одним fuller fixture, но
production event loop не моделируется полностью. Нельзя переносить вывод на
любой HotStuff/Tendermint/PBFT client без refinement proof.

### Conclusion validity

Нет статистических claims. Количество schedules не трактуется как probability
или coverage quality. Решение основано на theorem/counterexample boundary.

---

## 13. Machine-readable gate decision

Все decisive checks равны `true`:

- Gate 5′ prerequisite;
- T1, T2, T3 proof checks;
- independent big-int check;
- one-at-a-time ablations;
- exact premise characterization;
- parameter sensitivity;
- Python and Go fuller loops;
- exact conformance;
- event-order sensitivity;
- pinned-source recheck.

Machine-readable verdict:

```text
PASS / GO TO GATE 7′
```

---

## 14. Claim freeze

Допустимый claim:

> Phase/type erasure can remove finite agreement-violation witnesses in an
> explicit certificate-driven locking schema because closure-added repair
> evidence disables a unique honest quorum pivot; exact replay is erasable only
> under stable-key idempotence.

Запрещённые claims:

- production vulnerability;
- universal scheduler incompleteness/minimality;
- liveness completeness;
- unbounded result;
- bug prevalence;
- absolute novelty.

---

## 15. Решение и следующий этап

### Gate 6′

**PASS / GO TO GATE 7′.**

### Статус темы

**ГОТОВО К СОЗДАНИЮ ВОСПРОИЗВОДИМОГО PAPER/ARTIFACT PACKAGE В СУЖЕННОМ SCOPE.**

### Что ещё блокирует submission

- независимый proof review или mature-prover migration;
- минимизация архива;
- чистое независимое воспроизведение final package;
- automated paper figures/tables;
- final venue-specific novelty refresh.

### Critical path Gate 7′

```text
proof review
→ minimal artifact extraction
→ clean offline reproduction
→ automated figures/tables
→ manuscript evidence freeze
```
