# Executive decision — Gate 6′

**Дата:** 17 августа 2026 года  
**Решение:** **PASS / GO TO GATE 7′**  
**Статус темы:** **ГОТОВО К СОЗДАНИЮ ВОСПРОИЗВОДИМОГО АРТЕФАКТА И РУКОПИСИ В СУЖЕННОМ SCOPE**  
**Публикационный статус:** **ЕЩЁ НЕ ГОТОВО К ПОДАЧЕ**

## Итог

Gate 6′ закрыл два блокера предыдущего этапа:

1. T1–T3 получили проверяемые proof assets с явной доверенной базой;
2. phase-coupled separation воспроизведена в более полном локальном consensus
   event loop, а не только в конечной формуле или phase-barrier kernel.

Центральный результат сохранился:

> В явном классе certificate-driven locking schemas стирание phase/type
> различий до одного type-uniform directed endpoint graph может удалить
> agreement-violating witness. Причина — добавленное closure repair evidence
> лишает второй конфликтующий quorum единственного честного pivot. Точный replay
> устраним только при stable-key idempotence.

## Закрытые обязательства

| Обязательство | Результат |
|---|---|
| T1 replay erasure | checked induction certificate — PASS |
| T2 relational closure lifting | checked induction certificate — PASS |
| T3 `n=3f+1`, `q=2f+1` separation | exact arithmetic/branch certificate — PASS |
| Независимый T3 cross-check | Go `math/big`, 1 028 значений `f`, включая 400-значное — PASS |
| Fuller event loop | Go proposal/prevote/POLKA/precommit/COMMIT fixture — PASS |
| Независимая реализация | Python mirror, 6/6 terminal cases совпали — PASS |
| Event-order sensitivity | FIFO, LIFO, 256 seeds; 1 548 case runs — PASS |
| Necessity check | все `2^7=128` комбинаций premises; точная Boolean characterization — PASS |
| Pinned-source recheck | Gate 5′ source obligations — PASS |

## Новый результат Gate 6′

Для семифлаговой абстракции strict separation возникает ровно при условии:

```text
second_base_short_by_one
AND repair_disables_pivot
AND repair_precedes_second_quorum_opportunity
AND enabling_and_repair_share_endpoint_edge
AND phase_specific_grammar_can_split_E_and_R
AND (first_base_short_by_one
     OR second_pivot_requires_enabling_evidence)
```

Из 128 возможных assignments strict separation дают только три:

```text
0111111
1101111
1111111
```

Это точная граница **для данной construction**, а не универсальная
characterization BFT-протоколов.

## Fuller-loop результат

| Вариант | `G_T` | `G_D` edge off | `G_D` edge on |
|---|---|---|---|
| Correct baseline | safe | safe | safe |
| Missing lock update | **unsafe** | safe: первый quorum отсутствует | safe: terminal repair блокирует второй quorum |

В unsafe execution корректные replicas принимают решения `0` и `1`.
Type-uniform edge-off не пропускает enabling evidence, а edge-on вместе с ним
вынужденно пропускает COMMIT evidence к pivot.

## Что разрешено утверждать

- существует явный certificate-driven locking schema с safety separation между
  type-uniform directed и phase-specific delivery;
- separation определяется repair/pivot mechanism, а не числом schedules;
- replay erasure верна под перечисленными idempotence assumptions;
- bounded local event loop воспроизводит mechanism;
- Boolean premise boundary точна для поставленной малой модели.

## Что утверждать нельзя

Нельзя заявлять production vulnerability, универсальную неполноту partitions
или directed graphs, универсальную минимальность `G_T`, результат о liveness,
unbounded partial synchrony, вероятность нахождения bugs или абсолютную
новизну.

## Оставшийся блокер

Перед подачей статьи требуется независимый human proof review либо перенос
T1–T3 в зрелый proof assistant. Текущий 503-строчный dependency-free proof
kernel существенно сильнее prose sketch, но честно не приравнивается к
Lean/Coq/Isabelle.

## Следующий этап

Gate 7′ должен:

1. выделить минимальный artifact archive;
2. провести независимую clean-copy reproduction;
3. получить proof review или mature-prover check;
4. автоматически генерировать все figures и tables;
5. заморозить manuscript evidence package.
