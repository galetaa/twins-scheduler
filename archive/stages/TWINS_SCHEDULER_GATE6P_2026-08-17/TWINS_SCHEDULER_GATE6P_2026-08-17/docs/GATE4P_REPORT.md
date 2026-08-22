# Gate 4′ — естественный locking-kernel, временные расширения и conformance

**Дата завершения:** 15 августа 2026 года  
**Исследовательская линия:** safety-preserving completeness scheduler grammars
для Twins-based BFT testing  
**Решение Gate 4′:** **PASS / CONDITIONAL GO TO GATE 5′**  
**Общий статус темы:** **ТРЕБУЕТ СУЖЕНИЯ**

# 1. Executive decision

Gate 4′ закрыт положительно. Строгие различия scheduler grammars, найденные на
диагностических машинах Gate 0′–3′, сохраняются на bounded locking protocol с
quorum certificates, locks, двумя конфликтующими views и корректной безопасной
baseline-версией.

Главный результат:

> Три семантически мотивированных locking mutants имеют agreement-violating
> observations при phase/type-specific scheduler, но не при одном
> type-uniform directed graph на view. Одновьюовая задержка terminal commit
> evidence выявляет два из этих mutants, однако не заменяет phase separation
> для timeout-classification defect. Отдельный duplicate-counting mutant требует
> replay. Корректная baseline остаётся безопасной во всех проверенных моделях.

Это поддерживает научный вопрос о **минимальной scheduler capability,
необходимой для обнаружения разных классов safety defects**. Результат ещё не
является theorem для класса HotStuff-like protocols и не доказывает уязвимость
`relab/hotstuff`.

# 2. Что было реализовано

## 2.1. Exact locking checker

Добавлен модуль `src/schedcheck/locking/`:

- `model.py` — роли, состояния, сообщения, grammars и variants;
- `kernel.py` — детерминированная small-step semantics;
- `explorer.py` — исчерпывающий symbolic explorer;
- `oracle.py` — независимый mutable-state witness checker;
- `cases.py` — пять диагностических экспериментов;
- `reporting.py` — генерация machine-readable результатов.

Модель использует `n=4`, `f=1`, quorum `3`, одну Byzantine identity `B`,
представленную twins `T0/T1`, и honest replicas `H1/H2/H3`. View 1 предлагает
`0`, view 2 — `1`. Свойство safety нарушено, если две корректные реплики приняли
разные значения.

## 2.2. Scheduler grammars

Проверены шесть моделей:

```text
G_P_PARTITION
G_D_DIRECTED_VIEW
G_D1_DIRECTED_DELAY1
G_T_TYPE_SPECIFIC
G_M_PER_MESSAGE
G_R_PER_MESSAGE_REPLAY1
```

Стандартная вложенность

```text
G_P ⊆ G_D ⊆ G_T ⊆ G_M ⊆ G_R
```

подтверждена для всех baseline/mutant cases в bounded state space. Отдельно
подтверждено `G_D ⊆ G_D1`. `G_D1` и `G_T` не считаются упорядоченными: первое
добавляет время, второе — различение фаз/типов.

## 2.3. Независимая проверка

Каждый сохранённый unsafe witness:

1. воспроизводится executable kernel replay;
2. проверяется независимым oracle, который парсит serialized trace и не вызывает
   transition functions explorer;
3. проходит counterfactual closure, уничтожающую предполагаемый механизм.

Все 18 сериализованных минимальных unsafe witnesses прошли обе проверки.

# 3. Протокольные варианты

| Variant | Изменение | Научная роль |
|---|---|---|
| `BASELINE` | правильные locks, QC guards, signer de-duplication | negative control; должен быть safe |
| `MISSING_LOCK_UPDATE` | replica precommits, но не сохраняет lock | phase/terminal-repair defect |
| `WRONG_QC_GUARD` | certified value игнорируется; сравнение view нестрогое | unlock-validation defect |
| `TIMEOUT_AS_PRECOMMIT` | timeout certificate трактуется как precommit evidence без lock | certificate-type confusion |
| `DUPLICATE_VOTE_COUNTING` | считаются message instances, не logical signer IDs | replay/idempotence defect |
| `RECEIVER_VALIDATION_OMISSION` | `H3` принимает forged one-signer commit certificate | positive control, видимый partition scheduler |

Это intentional semantic mutations bounded reference model. Они не являются
утверждениями о найденных дефектах в production-клиенте.

# 4. Основные результаты

## 4.1. Correct baseline

Для каждого из пяти experiment plans и всех шести grammars число unsafe
observations равно нулю. Это исключает объяснение, что richer scheduler просто
ломает саму корректную protocol semantics.

## 4.2. Mutant language matrix

| Case / mutant | `G_P` | `G_D` | `G_D1` | `G_T` | `G_M` | `G_R` |
|---|---:|---:|---:|---:|---:|---:|
| Lock omission | 0 | 0 | **12** | **9** | **9** | **9** |
| Wrong QC guard | 0 | 0 | **12** | **9** | **9** | **9** |
| Timeout classification | 0 | 0 | 0 | **9** | **9** | **9** |
| Duplicate vote counting | 0 | 0 | 0 | 0 | 0 | **12** |
| Validation omission control | **1** | 1 | 3 | 3 | 3 | 3 |

Ячейки содержат число различных agreement-violating decision observations, а
не число raw schedules.

Минимальные unsafe traces требуют:

- 18 доставок для type-specific lock/QC-guard witnesses;
- 19 доставок для их delayed-commit witnesses;
- 14 доставок для timeout-classification witness;
- 14 доставок для replay witness;
- 13 доставок для partition-visible positive control.

## 4.3. Строгие различения

Получены четыре содержательно разные границы.

### A. Type-uniform directed graph недостаточен

Для `MISSING_LOCK_UPDATE`, `WRONG_QC_GUARD` и `TIMEOUT_AS_PRECOMMIT`:

```text
UnsafeObs(G_D) = ∅
UnsafeObs(G_T) ≠ ∅
```

В первых двух случаях scheduler должен доставить промежуточное evidence, но
удержать terminal evidence на том же leader-to-replica edge. В timeout case
необходимо отдельно управлять входящими `PREVOTE` и `PRECOMMIT` фазами.

### B. Bounded terminal delay частично заменяет type filtering

Для lock omission и wrong QC guard:

```text
UnsafeObs(G_D1) ≠ ∅
```

Commit certificate первого view допускается сетью, но приходит после второго
view. Replica успевает участвовать в конфликтующем quorum до получения terminal
evidence.

Для timeout-classification mutant `G_D1` остаётся безопасным. Причина: единый
inbound directed mask не может одновременно подавить `PREVOTE` и пропустить
`PRECOMMIT` на том же endpoint. Следовательно, временная власть и phase/type
власть различаются семантически.

### C. Replay необходим для non-idempotent quorum processing

Для duplicate-counting mutant:

```text
UnsafeObs(G_M) = ∅
UnsafeObs(G_R) ≠ ∅
```

Одной копии честного vote недостаточно: вместе с голосом Byzantine identity это
только два signer contributions. Повтор одного signed message ошибочно считается
третьим вкладом и создаёт certificate.

### D. Не каждый defect является scheduler gap

Validation-omission control обнаруживается уже `G_P`. Это подтверждает, что
oracle не навязывает вывод «richer всегда нужен» и способен отделять обычный
protocol-validation bug от scheduler-expressiveness blind spot.

# 5. Mechanism falsification через closures

## 5.1. Type erasure

Для каждого из трёх `G_T` witnesses построена closure: все message types
разрешаются на любом endpoint/direction, использованном хотя бы одним типом.
После closure:

```text
Lock omission:          unsafe → H1=0 | H2=0 | H3=-
Wrong QC guard:         unsafe → H1=0 | H2=0 | H3=-
Timeout classification: unsafe → H1=0 | H2=0 | H3=-
```

Дополнительные сообщения устанавливают lock, доставляют terminal evidence или
ломают conflicting quorum. Все closed observations безопасны.

## 5.2. Delay erasure

Для двух `G_D1` witnesses delayed commit certificates доставляются немедленно при
тех же directed endpoint masks. В обоих случаях unsafe observation исчезает и
получается `H1=0 | H2=0 | H3=-`.

## 5.3. Replay erasure

Повторы vote/precommit instances заменяются одной копией. После de-duplication
prepare/commit certificates причинно не возникают; итог `H1=- | H2=- | H3=-`.

Эти counterfactuals показывают, что separation вызывается именно заявленной
scheduler capability, а не случайным выбором другого workload.

# 6. Conformance с pinned Go harness semantics

## 6.1. Зафиксированный источник

Использован commit:

```text
3179c6e62929294961acbfd9bf8445769716a121
```

`inputs/hotstuff_snapshot/network.go` имеет SHA-256:

```text
4419845a04729c23ba31cd2fb37daf792e1c1a10fba32f29163f60c6506f3c55
```

На дату проверки официальный `main` всё ещё указывал на этот commit.

## 6.2. Проверенная семантика

Исполнимая Go fixture и Python abstraction сравнивались по:

- same-partition bypass;
- cross-partition filtering по runtime message type;
- drop-all для views вне scenario;
- sender-effective-view tagging;
- future-view pending queue;
- advancement global view только на idle tick.

Проверено 134 cases: 6 фиксированных edge cases и 128 seeded random cases,
`seed=20260815`. Результаты совпали полностью.

## 6.3. Граница conformance

Fixture не запускает node event loops и consensus protocol. Поэтому она не
доказывает, что abstract locking witness исполним в текущем Chained HotStuff
implementation. Она закрывает только mapping сетевой admission/queue semantics.
Следующий gate должен либо построить implementation-level mutation, либо дать
строгое refinement argument.

# 7. Что теперь можно и нельзя заявлять

## Допустимо

- В bounded locking model type-uniform view graph пропускает три класса
  phase-sensitive safety defects.
- Bounded late terminal delivery воспроизводит два из них, но не заменяет
  phase-specific inbound control.
- Replay строго необходим для выбранного non-idempotent signer-counting defect.
- Correct baseline safe во всём проверенном finite state space.
- Pinned Go network-admission semantics согласуется с Python abstraction на
  проверенном corpus.

## Недопустимо

- partitions неполны для любого HotStuff-like protocol;
- `relab/hotstuff` содержит один из mutants;
- найден production safety bug;
- `G_T` является универсально минимальным scheduler;
- 9 или 12 observations оценивают реальную вероятность обнаружения ошибки;
- новый fault-injection API сам по себе является научным вкладом.

# 8. Решение по воротам

| Подворота Gate 4′ | Статус | Основание |
|---|---|---|
| Natural locking kernel | PASS | certificate/lock/quorum semantics реализована; baseline safe |
| Semantic mutants | PASS | четыре mechanism-specific mutants плюс positive control |
| Phase/type separation | PASS | три strict safety separations `G_D → G_T` |
| Temporal extension | PASS | два positive и один discriminating negative result |
| Replay extension | PASS | strict `G_M → G_R` separation |
| Independent witness oracle | PASS | все 18 witnesses воспроизведены |
| Go network conformance | CONDITIONAL PASS | admission/queue PASS; consensus loop вне scope |
| Protocol-class theorem | FAIL / BLOCKING | ещё не сформулирован и не доказан |
| Second natural protocol | UNKNOWN / BLOCKING | ещё не реализован |

**Gate 4′: PASS / CONDITIONAL GO TO GATE 5′.**

**Общий статус темы: ТРЕБУЕТ СУЖЕНИЯ.**

# 9. Следующий этап

Gate 5′ должен исследовать не новый framework, а formal characterization:

1. type-uniform closure и условия сохранения unsafe witness;
2. phase-coupled separation lemma;
3. terminal-delay simulation boundary;
4. replay/idempotence theorem;
5. second protocol instantiation;
6. mapping хотя бы одной implementation-level mutation к формальным условиям.

NO-GO наступает, если формулировка остаётся перечислением пяти mutants либо
второй protocol model не воспроизводит ни theorem condition, ни natural
separation.

# 10. Воспроизводимость

Основная команда:

```bash
./scripts/reproduce_gate4p.sh
```

Она заново выполняет:

1. Go/Python conformance;
2. exact language enumeration;
3. counterfactual closures;
4. independent witness checking;
5. fast regression suite; exhaustive state-space assertions already run inside
   `run_gate4p.py`;
6. self-check machine-readable результатов.

Runtime dependencies Python-модуля отсутствуют; conformance требует Go toolchain.
В зафиксированной среде использованы CPython 3.13.5, Go 1.23.2,
`PYTHONHASHSEED=0`.
