# Executive decision — Gate 5′

**Дата:** 15 августа 2026 года  
**Решение:** **PASS / GO TO GATE 6′**  
**Статус темы:** **ГОТОВО К ПОЛНОЙ ИССЛЕДОВАТЕЛЬСКОЙ РЕАЛИЗАЦИИ В СУЖЕННОМ SCOPE**

## Итог

Gate 5′ превратил наблюдение Gate 4′ о различиях scheduler grammars в узкий
переносимый формальный результат. Получены:

1. replay-erasure theorem для logical-key-idempotent vote processing;
2. relational closure-lifting theorem как локальное достаточное условие
   сохранения unsafe traces при добавлении сообщений;
3. параметрическая phase-coupled separation construction для
   `n=3f+1`, `q=2f+1`;
4. условная граница, когда one-view terminal delay заменяет phase filtering;
5. constructive separation для non-idempotent instance counting.

Главная граница воспроизвелась на втором, независимо названном
Tendermint-style prevote/precommit locking kernel. Correct baseline осталась
безопасной во всех проверенных grammars. Lock omission и valid-round guard error
не видны type-uniform directed graph, но видны phase-specific scheduler;
duplicate-vote-counting defect требует replay.

## Проверенная реализация

- точный finite-state search второго kernel;
- 15 минимальных unsafe witnesses, каждый повторно проверен независимым oracle;
- параметрическая конструкция проверена для `f=1…8`;
- replay theorem проверена на 364 последовательностях;
- Go/Python vote-processing correspondence проверена на 728 случаях;
- pinned CometBFT `v0.40.0`, commit
  `0880b4d378f347ab16e54ec677ff50d803f37d62`;
- controlled Go fixture подтверждает duplicate idempotence и lock-before-
  precommit correspondence без заявления о production bug.

## Допустимый paper claim

> **Safety-observation closure boundaries of scheduler grammars for
> certificate-driven locking BFT protocols.**

Это theorem-and-counterexample paper, а не новый testing DSL, не benchmark и не
отчёт об уязвимости CometBFT.

## Оставшийся риск

До submission-level готовности нужно mechanize или существенно ужесточить
proof T3 и провести одну controlled mutation через более полный consensus event
loop. Это задачи Gate 6′, а не скрытые концептуальные решения.

## Запрещённые заявления

Нельзя утверждать универсальную неполноту partitions, универсальную
минимальность phase-specific scheduling, наличие дефекта в CometBFT, liveness
completeness или абсолютную новизну.
