# Executive decision — Gate 0′–3′

## Выбранный pivot

**Safety-preserving completeness of view-partition schedules for view-based BFT testing.**

Уточнённая рабочая тема:

**«Условия сохранения safety-свидетельств при замене message-level scheduler на partition schedule в тестировании view-based BFT-протоколов».**

## Итоговый статус

**ТРЕБУЕТ СУЖЕНИЯ.**

Gate 0′–3′ дают условный GO не на разработку нового framework, а на один следующий формальный этап: найти protocol-class closure theorem либо естественный BFT separation.

## Главный результат пилота

Для заявленного класса конечных детерминированных protocol machines исчерпывающе подтверждена строгая иерархия по agreement-violating observations:

```text
G_P_PARTITION
  ⊊ G_D_DIRECTED_VIEW
  ⊊ G_T_TYPE_SPECIFIC
  ⊊ G_M_PER_MESSAGE
```

Минимальные разделения:

| Граница | Модель | Unsafe observation, отсутствующее в слабой грамматике |
|---|---|---|
| partition → directed | `ECHO_GATE` | `A=0|B=1` |
| directed → type-specific | `TYPE_SPLIT` | `A=0|B=1` и `A=1|B=0` |
| type-specific → per-message | `INSTANCE_ORDER` | `A=0|B=1` и `A=1|B=0` |

`TWIN_BRANCH_CONTROL` служит положительным контролем: обычный branch-separable Twins witness уже доступен partition grammar.

## Механизм

Три natural closure counterfactuals уничтожили соответствующие violations:

1. directed star → weak-component partition closure добавляет обратные/транзитивные связи;
2. type-specific schedule → endpoint-union стирает различие типов;
3. per-message schedule → type-edge completion доставляет все same-type instances в каноническом порядке.

Это показывает, что разделения вызваны не просто большим числом schedules, а конкретной потерей causal control.

## Что результат опровергает

Опровергнута **неограниченная** гипотеза:

> Любое конечное safety violation, доступное message-level scheduler в детерминированном view protocol, имеет partition-normal-form witness.

## Что результат не доказывает

- что production HotStuff небезопасен;
- что текущий `relab/hotstuff` пропускает известную реальную ошибку;
- что partitions неполны для всех естественных BFT protocols;
- что найден новый scheduler API;
- что одновьюовый результат переносится на liveness, timing, replay или late delivery.

## Главный блокирующий риск

Текущие separators являются минимальными diagnostic machines, а не стандартным locking protocol. Без natural protocol class вклад останется корректным, но недостаточно сильным для статьи.

## Следующий необратимый шаг

Реализовать Gate 4′:

1. small-step locking kernel с `n=4, f=1`;
2. safe baseline и заранее мотивированные implementation mutants;
3. те же четыре grammars;
4. actual-executor conformance layer;
5. решение: theorem, natural separation или NO-GO.

Полный план находится в `ROADMAP_GATE4P.md`.
