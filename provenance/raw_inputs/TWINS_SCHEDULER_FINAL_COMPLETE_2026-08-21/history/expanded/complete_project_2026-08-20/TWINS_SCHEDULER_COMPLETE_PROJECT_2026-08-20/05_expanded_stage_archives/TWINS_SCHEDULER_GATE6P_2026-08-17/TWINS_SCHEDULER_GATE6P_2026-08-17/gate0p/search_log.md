# Gate 0′ search log

**Дата поиска:** 12 августа 2026 года.

## Проверяемая заявка

Не искалась «новая система fault injection». Проверялось более узкое утверждение: существует ли опубликованная characterization того, когда один симметричный partition schedule на view сохраняет все safety-violating observations более сильного per-message scheduler для класса view-based BFT implementations.

## Поисковые группы

1. `partition normal form distributed protocol message schedule safety`
2. `symmetric partition per-message distributed systems testing`
3. `communication closure partition schedule consensus testing safety`
4. `message adversary partitions consensus communication graph`
5. `BFT testing scheduler grammar network partition per-message delivery completeness`
6. `Heard-Of communication predicate partition equivalence`
7. `fault injection expressiveness safety witness distributed consensus`
8. `Twins partition scenario coverage scheduler`
9. `Netrix message filter drop replay reorder consensus testing`
10. `view-based BFT partition schedule incomplete`

## Проверенные типы источников

- peer-reviewed distributed systems, formal-methods и testing papers;
- официальные proceedings/DOI pages;
- current open-source code и documentation `relab/hotstuff`;
- BFT testing frameworks и benchmark papers;
- message-adversary/Heard-Of literature.

## Что найдено

- Communication closure уже исследует property-preserving reduction от asynchronous к lossy synchronous executions и формулирует testing hypothesis.
- Heard-Of и message-adversary works уже используют per-round sets/graphs доставленных сообщений.
- Netrix уже реализует message-level filters, drop, delay, replay и ordering constraints.
- Twins и `relab/hotstuff` используют view-level partition scenarios.

## Что не обнаружено в обследованных источниках

Не обнаружена работа, одновременно:

1. задающая лестницу `partition → directed-view → type-specific → per-message`;
2. сравнивающая её по **unsafe observation languages**, а не по raw trace coverage;
3. дающая necessary/sufficient closure-preservation condition для natural class of view-based BFT implementations;
4. определяющая минимальное scheduler extension, восстанавливающее такую полноту.

Это ограниченное поисковое утверждение, а не доказательство отсутствия prior art. Наиболее вероятные скрытые аналоги находятся в refinement/conformance, communication-closed protocols, message-adversary и testing-theory literature.
