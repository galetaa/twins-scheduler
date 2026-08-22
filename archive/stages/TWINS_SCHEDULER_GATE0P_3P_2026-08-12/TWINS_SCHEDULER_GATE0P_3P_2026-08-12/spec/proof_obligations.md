# Proof obligations после блокирующего пилота

## Закрыто пилотом

### PO-1. Sound embeddings

Для каждой пары соседних грамматик задано конструктивное вложение policy/execution. Исчерпывающие тесты подтверждают inclusion наблюдений на четырёх моделях.

### PO-2. Strictness over the declared finite class

Три минимальных counterexample protocols показывают строгие включения по unsafe observations:

- `ECHO_GATE`: `G_P ⊊ G_D`;
- `TYPE_SPLIT`: `G_D ⊊ G_T`;
- `INSTANCE_ORDER`: `G_T ⊊ G_M`.

### PO-3. Positive control

`TWIN_BRANCH_CONTROL` показывает, что partition grammar не является заведомо бессильной: она воспроизводит классический branch-separable split.

### PO-4. Mechanism check

Для каждого separation witness наименее усиливающий естественный closure уничтожает unsafe observation. Это связывает разницу языков именно с symmetry/transitivity, type erasure или instance completion, а не только с разным количеством policies.

## Открытые блокирующие обязательства

### PO-5. Natural protocol class

Нужно определить непустой и практически узнаваемый класс view-based BFT implementations, для которого closure-preservation проверяемо синтаксически или семантически. Нельзя определять класс как «протоколы, для которых требуемое равенство уже выполняется».

### PO-6. Locking-protocol instantiation

Нужна одна корректная small-step locking model и набор заранее объяснённых implementation mutants. Должно быть показано, какие scheduler boundaries открывают или не открывают safety witnesses.

### PO-7. Actual harness conformance

Требуется доказать refinement между абстрактным `G_P` и зафиксированной operational semantics executor: sender view, pending queue, event-loop order, uncontrolled message types, block fetches и view advancement.

### PO-8. Cross-view semantics

Нужно расширить `G_M` и слабые грамматики поздней доставкой, replay и view-indexed policy sequence. Одновьюовый theorem не следует называть theorem для partial synchrony.

### PO-9. Closure theorem or natural separation

Публикационный результат должен быть одним из:

1. нетривиальное достаточное/необходимое условие partition closure preservation;
2. минимальный естественный BFT mutant/witness, недоступный partition grammar;
3. минимальное расширение grammar, восстанавливающее completeness для заданного класса.

### PO-10. Prior-art non-absorption

Нужно показать, что результат не является прямой подстановкой в communication-closure, Heard-Of/message-adversary или generic refinement theory.

## Stop conditions

Проект останавливается, если:

- differences сохраняются только на искусственных machines и исчезают на locking kernel/mutants;
- positive theorem сводится к определению closure-monotonicity;
- actual executor уже допускает необходимую выразительность через механизм, пропущенный model extraction;
- найден существующий necessary-and-sufficient theorem с той же property projection;
- результат остаётся только предложением нового DSL/API.
