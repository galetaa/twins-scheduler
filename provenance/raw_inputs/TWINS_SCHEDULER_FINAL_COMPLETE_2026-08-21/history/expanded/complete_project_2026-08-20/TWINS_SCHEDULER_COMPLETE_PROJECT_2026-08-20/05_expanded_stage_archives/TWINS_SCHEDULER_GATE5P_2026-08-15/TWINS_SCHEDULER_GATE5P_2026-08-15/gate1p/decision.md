# Gate 1′ — formal-model decision

**Статус: PASS.**

Формальная модель достаточна для блокирующего вопроса: является ли partition grammar универсально safety-complete относительно более богатых scheduler grammars даже в простом конечном детерминированном классе?

Модель намеренно минимальна. Она отделяет три вида потери выразительности:

1. symmetry/transitive closure узлов;
2. стирание message type;
3. стирание identity/order отдельных message instances.

Присвоение PASS не означает conformance с полной operational semantics `relab/hotstuff`. Этот перенос остаётся отдельным proof obligation.
