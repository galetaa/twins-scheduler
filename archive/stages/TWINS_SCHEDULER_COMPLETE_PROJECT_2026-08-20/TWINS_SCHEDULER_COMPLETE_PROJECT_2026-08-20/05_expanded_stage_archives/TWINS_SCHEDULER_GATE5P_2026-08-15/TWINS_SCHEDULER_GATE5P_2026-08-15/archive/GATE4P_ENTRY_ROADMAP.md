# Gate 4′ roadmap — natural BFT validation

## Цель

Проверить, сохраняется ли найденная hierarchy на достаточно естественной модели view-based locking BFT и можно ли сформулировать нециклическое closure-preservation condition.

## Entry conditions

- Gate 0′–3′ package воспроизводится побайтово;
- scope остаётся safety-only;
- richer API не считается вкладом;
- production integration не выполняется до natural-model decision.

## Work packages

### WP1. Locking kernel

Создать `LOCKING_BASELINE`:

- `n=4`, `f=1`;
- fixed proposer/twin proposer;
- proposal, vote, QC, timeout/new-view abstractions;
- explicit `locked_view`, `locked_value`, `highest_qc`;
- deterministic transition function;
- agreement oracle по трём корректным identities;
- bounded 2–4 views.

Baseline должен быть safe во всех четырёх грамматиках в пределах bound.

### WP2. Seeded mutants

Mutants выбираются по semantic fault, а не ради заранее нужного результата:

1. missing lock update;
2. wrong QC/view comparison;
3. timeout certificate accepted as commit evidence;
4. first-certificate-wins ordering bug;
5. receiver-specific validation omission;
6. stale proposal accepted after view change.

Для каждого mutant заранее фиксируются expected mechanism, strongest alternative explanation и falsifier.

### WP3. View-indexed grammars

Расширить policies до sequence per view. Добавить:

- delayed delivery into later view;
- explicit drop;
- bounded replay;
- canonical and adversarial event-loop ordering;
- controlled message-type set.

### WP4. Conformance

Построить adapter между abstract `G_P` и snapshot `relab/hotstuff`:

- sender effective view;
- `shouldDrop` decision;
- pending queue;
- global-view advance;
- per-node event-loop drain;
- leader schedule;
- controlled/uncontrolled message types.

Conformance tests должны сравнивать решения abstract adapter и executable Go micro-scenarios.

### WP5. Closure characterization

Проверить candidate conditions:

- receive-set monotonicity;
- certificate monotonicity;
- lock monotonicity;
- commutativity of extra valid messages;
- type-insensitivity;
- instance-order insensitivity;
- view-local communication closure.

Нужно определить условия, которые можно проверять независимо от equality of unsafe languages.

## Decision rules

### GO to paper

Хотя бы один результат:

- natural mutant имеет minimal safety witness в `G_D\G_P`, `G_T\G_D` или `G_M\G_T`;
- получен нетривиальный theorem, что specified locking class closure-preserving;
- установлена минимальная grammar extension для всего bounded mutant class;
- найден implementation-conformance gap, объясняющий систематический blind spot и подтверждённый independent oracle.

### NO-GO

- все separations остаются только на artificial diagnostic machines;
- candidate theorem является тавтологией;
- actual executor semantics существенно богаче абстрактного `G_P` и устраняет поставленный gap;
- prior art уже содержит тот же closure characterization;
- результаты зависят только от event-loop artifact одного клиента.

### PIVOT

- partition complete для safety, но неполна только для liveness/timing: открыть отдельный проект, не смешивать результаты;
- gap существует только для cross-view replay: сузить grammar hierarchy до temporal dimension;
- distinction зависит от message validity: перейти к fault-model conformance, а не scheduler conformance.

## Backlog первых 15 задач

| № | Действие | Артефакт | Acceptance | Размер | Параллельно |
|---:|---|---|---|---|---|
| 1 | Записать locking state и transition table | `spec/locking_kernel.md` | Все состояния/guards однозначны | M | нет |
| 2 | Реализовать baseline state machine | `protocols/locking.py` | Deterministic exhaustive run | L | нет |
| 3 | Добавить agreement/validity oracle | `oracles/locking.py` | Unit tests с ручными traces | M | да с 4 |
| 4 | Зафиксировать mutant catalog | `configs/mutants.toml` | Для каждого mechanism и falsifier | M | да с 3 |
| 5 | Реализовать missing-lock mutant | module + tests | Counterfactual against baseline | M | после 2 |
| 6 | Реализовать QC-view mutant | module + tests | Exact mutation diff documented | M | после 2 |
| 7 | Ввести per-view policy sequence | grammar module | Existing tests unchanged | L | после 2 |
| 8 | Ввести late-delivery queue | engine module | Deterministic replay tests | L | после 7 |
| 9 | Ввести bounded replay | engine module | No duplicate UID ambiguity | M | после 8 |
| 10 | Написать abstract Go-harness adapter | `conformance/relab.py` | Matches source snapshot cases | L | после 7 |
| 11 | Создать Go micro-scenario fixture | `conformance/go_fixture/` | Local deterministic output | L | после 10 |
| 12 | Сравнить abstract/executable traces | `results/conformance/` | Zero unexplained divergences | L | после 11 |
| 13 | Выполнить exhaustive mutant matrix | CSV/JSON results | All bounds/manifests recorded | L | после 5–12 |
| 14 | Минимизировать natural witnesses | witness corpus | Independent replay passes | M | после 13 |
| 15 | Сформулировать theorem/separation | `spec/main_result.md` | Non-circular, reviewer-testable | L | после 14 |

## Critical path

`locking spec → baseline → view-indexed engine → mutants → exhaustive matrix → witness minimization → theorem/NO-GO`.

Оценка: **12–20 фокусированных человеко-дней** до честного Gate 4′ decision, без production campaign.
