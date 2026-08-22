# Gate 0′ — novelty decision

**Статус: CONDITIONAL PASS.**

## Что уничтожено prior art

- «Мы добавили per-message filters» — уже инженерно реализовано в более богатых testing DSL.
- «Мы вводим directed communication graph per round/view» — стандартный message-adversary/Heard-Of объект.
- «Мы сокращаем asynchronous schedules до простых executions» — communication closure является ближайшей общей теорией.
- «Мы измеряем coverage нескольких BFT testers» — benchmark frameworks уже существуют.

## Остаточная novelty delta

Защищаемым остаётся только результат вида:

> Для чётко заданного natural class `C` view-based BFT implementations установить условия, при которых closure от более богатого scheduler к view partition сохраняет все safety-violating observations; при нарушении условий дать минимальный separation witness и минимальное grammar extension.

Пилот может подтвердить, что такой механизм нетривиален, но не доказывает новизну общего theorem.

## Kill conditions

Gate 0′ будет переоткрыт и закрыт NO-GO, если:

- результат окажется прямым corollary communication-closure/Heard-Of theorem;
- класс `C` будет определён циклически;
- единственным вкладом останется новый API;
- separation будет существовать только на искусственных machines без natural locking instantiation;
- скрытый conformance/refinement prior art даст ту же characterization.
