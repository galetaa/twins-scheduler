# Gate 7′ — executive decision

## Вердикт

**PASS / GO TO GATE 8′ MANUSCRIPT; SUBMISSION HOLD.**

Центральный theorem-and-counterexample package заморожен в минимальном,
самодостаточном и офлайн-воспроизводимом артефакте. Все manuscript figures и
таблицы генерируются из machine-readable evidence. Концептуальных решений,
блокирующих начало рукописи, больше нет.

Финальная подача статьи пока не разрешена. До submission необходимо закрыть
proof-assurance одним из двух путей: независимая построчная проверка специалистом
или реально собранная kernel-checked формализация в Lean, Coq либо Isabelle.
Также требуется обновить novelty review на дату подачи и проверить mapping
конкретного protocol instance к абстрактным premises.

## Замороженный научный тезис

Для явно определённого класса конечных certificate-driven locking schemas
стирание различий message phase/type до одного type-uniform directed endpoint
graph может удалить agreement-violating witness. Механизм — non-monotone repair:
добавленное при closure evidence отключает единственного честного участника,
общего двум конфликтующим quorum, до формирования второго certificate.

Точный replay устраним относительно safety-наблюдений только при stable replay
key, stuttering duplicate transition, отсутствии нового voting power и
protocol-relevant output, а также state-based observation.

Это existence/separation result для явной schema family, а не универсальное
утверждение о неполноте partition или directed schedulers.

## Решающее evidence

| Route | Результат | Что поддерживает |
|---|---:|---|
| Z3 4.13.3.0 SMT/CHC | 5 positive files, 8 `UNSAT` | T1, условные obligations T2, параметрическая арифметика T3 и symbolic equivalence T6 |
| Damaged controls | 4/4 `SAT` | чувствительность formal harness к существенным premises |
| Small certificate kernel | T1–T3 PASS | независимо аудируемые induction/arithmetic certificates |
| Exact Boolean checker | 128 assignments, 0 mismatches | точная seven-flag граница T6 |
| Go `math/big` | 1 028 cases PASS | отсутствие small-integer artifact в T3 |
| Go/Python fuller event loop | 6/6 exact terminal matches | перенос separation mechanism в две независимо написанные реализации |
| Event-order sensitivity | 1 548 runs, 0 classification changes | результат не является FIFO-only artifact в bounded fixture |
| Gate 6′ equivalence | 15/15 files byte-identical | минимизация не изменила решающее evidence |
| Paper generator | 24/24 outputs | 3 SVG figures и 7 таблиц в CSV/Markdown/LaTeX |
| Unit tests | 17/17 PASS | certificates, negative tamper path, models, outputs и source mapping |

## Что готово

- standalone artifact archive;
- one-command offline reproduction;
- SHA-256 core и full-artifact manifests;
- abstract draft, populated paper skeleton и claim-to-evidence index;
- автоматически создаваемые figures/tables;
- artifact-evaluation guide, environment contract, license inventory и
  third-party notices;
- Gate 8′ roadmap без скрытых концептуальных решений.

## Что не готово

Пакет не доказывает production vulnerability, full-client refinement, liveness,
unbounded partial-synchrony result, универсальную минимальность `G_T`,
распространённость реальных bugs или абсолютную научную новизну. Lean scaffold
приложен только как маршрут миграции и **не был kernel-checked**.

## Следующий необратимый шаг

Написать sections 2–6 полной статьи вокруг уже замороженных definitions,
conditional closure theorem, quorum-pivot separation, exact premise boundary и
replay-erasure theorem. Расширение числа mutants, scheduler features или scope
на этом этапе считается регрессией.
