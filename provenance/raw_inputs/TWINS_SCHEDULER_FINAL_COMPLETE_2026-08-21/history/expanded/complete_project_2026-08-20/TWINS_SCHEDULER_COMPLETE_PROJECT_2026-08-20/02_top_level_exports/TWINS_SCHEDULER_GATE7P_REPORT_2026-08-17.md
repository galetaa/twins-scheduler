# Gate 7′ — воспроизводимый артефакт и manuscript-ready evidence

**Дата закрытия:** 17 августа 2026 года  
**Рабочая тема:** границы сохранения safety-наблюдений при замыкании грамматик scheduler для certificate-driven locking BFT-протоколов  
**Вердикт:** **PASS / GO TO GATE 8′ MANUSCRIPT; SUBMISSION HOLD**

## 1. Executive decision

Gate 7′ закрыт. Центральный результат Gate 6′ извлечён в самостоятельный
минимальный пакет, повторно закодирован в зрелом SMT/CHC solver route, снабжён
falsifying controls, воспроизведён из чистой копии и связан с автоматически
генерируемым manuscript evidence.

Разрешён Gate 8′ — написание полной статьи и подготовка submission package.
Финальная подача остаётся заблокированной до независимой human proof review или
фактически собранной kernel-checked формализации, venue-specific novelty refresh
и финальной проверки protocol-to-schema assumption map.

## 2. Замороженный claim и границы

### 2.1. Основной claim

Для явно определённого класса конечных certificate-driven locking schemas
стирание message phase/type до одного type-uniform directed endpoint graph может
удалить agreement-violating witness. Closure добавляет repair evidence, которое
отключает единственного честного quorum pivot до второй конфликтующей quorum
opportunity.

### 2.2. Replay claim

Удаление повторной доставки одного logical message сохраняет terminal
protocol-relevant state и state-based safety observation только при явных
premises:

- stable replay key;
- duplicate processing является protocol-relevant stutter;
- duplicate не добавляет voting power;
- duplicate не создаёт relevant output;
- дальнейшие transitions детерминированы относительно relevant state.

### 2.3. Non-claims

Работа не устанавливает:

- production vulnerability в CometBFT, HotStuff, Tendermint или другом клиенте;
- universal incompleteness partition/directed schedulers;
- universal minimality phase/type-specific scheduling;
- liveness theorem;
- unbounded partial-synchrony completeness;
- bug prevalence или discovery probability;
- full refinement production client → abstract schema;
- абсолютную научную новизну.

## 3. WP7.1 — minimal artifact extraction

Из critical path исключены historical Gate 0′–5′ campaigns, временные notebooks,
старые альтернативные темы и дублирующие outputs. Сохранены:

- dependency-free Python core;
- независимый Go fuller event loop;
- независимый Go `math/big` checker;
- small certificate kernel и certificates T1–T3;
- SMT-LIB/CHC obligations и четыре damaged controls;
- exact 128-row premise model;
- pinned source fragments, licenses и source mapping;
- machine-readable result files;
- paper-data sources и generator;
- manuscript skeleton и evidence index;
- offline runner и manifests.

Минимальная выжимка заново вычисляет **15 решающих файлов Gate 6′** и совпадает
с ними побайтово по SHA-256. Frozen core manifest содержит **13 ключевых
Gate 7′ entries**, включая decision, theorem ledger, extraction equivalence,
SMT report, exact characterization, event-loop evidence и paper manifest.

## 4. WP7.2 — mature-prover migration

### 4.1. Positive obligations

Gate 6′ опирался на небольшой project-local proof checker. Gate 7′ добавляет
отдельную SMT-LIB 2 encoding route, исполненную Z3 4.13.3.0.

| Обязательство | Логика | Проверенный результат | Точная интерпретация |
|---|---|---:|---|
| T1 replay-erasure invariant | HORN/CHC | 1 `UNSAT` | unequal relevant states недостижимы при stable-key stuttering и одинаковых deterministic first-delivery transitions |
| T2 local VCs | AUFLIA | 4 `UNSAT` | transitivity, increasing insertion, forward simulation и upward closure действительно дают заявленные local consequences |
| T2 prefix skeleton | HORN/CHC | 1 `UNSAT` | finite-prefix relation не нарушается при предоставленных local obligations |
| T3 quorum-pivot arithmetic | QF_LIA | 1 `UNSAT` | branch counts верны символически для любого integer `f≥1` |
| T6 premise characterization | QF_LIA | 1 `UNSAT` | operational seven-flag model эквивалентна closed Boolean formula |

Итого: **5 positive source files и 8 `UNSAT` results**.

### 4.2. Negative controls

Четыре intentionally damaged encodings дали ожидаемый `SAT`:

1. duplicate перестаёт быть stutter;
2. closure insertion перестаёт быть `R`-increasing;
3. repair перестаёт отключать pivot;
4. из T6 ошибочно удаляется disjunct `Rq`.

Это не доказывает правильность statement-to-symbol mapping, но исключает
простейшую неисправность вида «harness всегда возвращает `UNSAT`».

### 4.3. Assurance boundary

Разрешённая формулировка: theorem obligations **independently re-encoded and
solver-checked with Z3**. Нельзя заявлять полную mechanization production
protocol semantics.

Trusted computing base включает:

- Z3 runtime и SMT/CHC engines;
- пять positive encodings и четыре controls;
- minimal C API loader;
- host compiler/dynamic linker;
- statement-to-symbol interpretation;
- для generic composition T2 — отдельный small certificate kernel;
- written abstraction mapping protocol events → schema premises.

Lean 4 scaffold приложен, но не собран и не участвует в PASS decision.

## 5. Формальные результаты

### 5.1. T1 — replay erasure

Для finite traces exact duplicate delivery можно удалить без изменения
protocol-relevant terminal state, если обработка duplicate является stutter и не
создаёт relevant side effects. Результат не распространяется на equivocation,
timers, callbacks, resource-visible effects и instance-counting quorum logic.

### 5.2. T2 — relational closure lifting

Пусть closure вставляет actions в исходный trace. Если существует preorder `R`,
для которого inserted actions `R`-increasing, retained actions forward-simulate
`R`, отношение транзитивно, а `Unsafe` upward-closed, то closure сохраняет finite
unsafety.

Это conditional theorem. Каждая protocol instantiation обязана предъявить
содержательный `R`. Quorum-pivot construction показывает границу: repair может
уменьшить множество будущих safety-relevant действий, поэтому нужная
monotonicity отсутствует.

### 5.3. T3 — parametric quorum-pivot separation

Для любого `f≥1`:

```text
n = 3f+1
q = 2f+1
Q0 = B ∪ A ∪ {p}
Q1 = B ∪ C ∪ {p}
```

где `|B|=|A|=|C|=f`, а `p` — единственный честный участник пересечения двух
conflicting quorum.

Phase-specific grammar доставляет enabling evidence `E`, но удерживает repair
`R`, позволяя `p` участвовать в обеих ветвях. Type-uniform directed edge имеет
только два выбора:

- edge-off: `E` и `R` отсутствуют, первый quorum остаётся на `q−1`;
- edge-on: доставляются `E` и `R`, repair отключает `p`, второй quorum остаётся
  на `q−1`.

Следовательно, для явной schema family phase-specific grammar имеет unsafe
observation, отсутствующее при обоих type-uniform directed choices. Это
existential separation, не universal scheduler theorem.

### 5.4. T6 — exact premise boundary

В supplied seven-flag operational model strict separation выполняется в
точности при:

```text
S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)
```

Проверены все `2^7=128` assignments. Strict patterns:

```text
0111111
1101111
1111111
```

Operational checker, closed Boolean characterization и symbolic Z3 encoding
дают **0 mismatches**.

## 6. Executable validation

Fuller two-round event loop реализует:

```text
PROPOSAL → PREVOTE → POLKA → PRECOMMIT → COMMIT
```

с dynamically generated events, unique logical vote keys, persistent locks,
quorum formation, irreversible decisions и независимым agreement oracle.
Controlled mutation удаляет только lock update после POLKA.

| Grammar / variant | Результат |
|---|---|
| `G_T_TYPE_SPECIFIC / BASELINE` | safe |
| `G_D_ROUND0_EDGE_OFF / BASELINE` | safe |
| `G_D_ROUND0_EDGE_ON / BASELINE` | safe |
| `G_T_TYPE_SPECIFIC / MISSING_LOCK_UPDATE` | **unsafe** |
| `G_D_ROUND0_EDGE_OFF / MISSING_LOCK_UPDATE` | safe: первый quorum не формируется |
| `G_D_ROUND0_EDGE_ON / MISSING_LOCK_UPDATE` | safe: repair приходит до второй ветви |

Go и независимо написанная Python mirror совпали по всем **6 terminal cases**.
FIFO, LIFO и 256 seeded random queue orders дали **1 548 case runs** без смены
classification или terminal signature.

Дополнительные exact checks:

- parameter sensitivity: 512 cases;
- Go `math/big`: 1 028 values `f`, включая 400-digit case;
- unit tests: 17/17 PASS;
- tampered T1 certificate: ожидаемо отвергается.

## 7. WP7.3 — manuscript assets

`scripts/generate_paper_assets.py` создаёт одной командой:

- Figure 1 — scheduler grammar embeddings;
- Figure 2 — parametric quorum-pivot construction;
- Figure 3 — exact premise characterization;
- 7 tables в CSV;
- те же 7 tables в Markdown;
- те же 7 tables в LaTeX.

Всего **24 generated files**. Каждый output имеет SHA-256 в
`paper_assets/MANIFEST.json`. Ручное изменение чисел в paper assets не требуется
и не допускается.

## 8. WP7.4 — reproducibility

Проверенный route:

```bash
./scripts/reproduce_gate7p.sh
```

Он работает без package downloads, RPC, blockchain nodes, public networks или
external datasets и выполняет:

1. core evidence regeneration;
2. сравнение 15 Gate 6′ hashes;
3. локальную компиляцию minimal Z3 loader;
4. 5 positive SMT/CHC files и 4 damaged controls;
5. paper generation;
6. 17 unit tests;
7. self-check;
8. verification core и full-artifact manifests.

Clean-copy run из распакованного archive candidate завершился с exit status 0:

```text
elapsed wall clock: 6.48 s
user CPU: 8.16 s
system CPU: 1.28 s
maximum resident set: 113 372 KiB
socket messages sent/received: 0/0
```

Это описание одного reference run, а не performance guarantee. Полный record
находится в `REPRODUCTION_VERIFICATION.md`; hardware/environment — в
`environment/HARDWARE_REPORT.md` и `environment/EXACT_HOST_INSTRUCTIONS.md`.

## 9. WP7.5 — manuscript package

Подготовлены:

- `manuscript/ABSTRACT_DRAFT.md`;
- `manuscript/PAPER_SKELETON.md`;
- `manuscript/EVIDENCE_INDEX.md`;
- claim-to-evidence table;
- validity table;
- prohibited-claims table;
- artifact evaluation guide;
- Gate 8′ roadmap.

Argument order заморожен:

```text
problem and observation language
→ conditional closure theorem
→ quorum-pivot separation
→ exact premise boundary
→ replay-erasure theorem
→ executable validation
→ related work
→ validity and reproducibility
```

## 10. Safety, ethics и disclosure

Эксперименты полностью локальны. Mainnet, public testnet, чужие assets, private
keys, network probing, DoS и эксплуатация live systems не используются.
Controlled mutations применяются только к абстрактным и локальным fixtures.
Production security finding не заявлен, поэтому disclosure не активирован.

## 11. Definition of Done

| Критерий Gate 7′ | Статус | Основание |
|---|---|---|
| Standalone minimal extraction | PASS | 15 Gate 6′ files byte-identical; все inputs внутри archive |
| Mature solver route | PASS WITH EXPLICIT TCB | 8 `UNSAT`, 4 damaged-control `SAT` |
| No blocking proof objection for manuscript construction | CONDITIONAL PASS | encoding obligations pass; human/kernel review остаётся submission blocker |
| Independent executable routes | PASS | Go/Python 6/6; Go big-int 1 028 cases |
| Exact premise boundary | PASS | 128 assignments, 0 mismatches |
| Event-order robustness in bounded fixture | PASS | 1 548 runs, 0 changes |
| Automated paper assets | PASS | 24 outputs, own manifest |
| Offline clean-copy reproduction | PASS | exit 0; core и artifact manifests pass |
| Complete manuscript | FAIL — Gate 8′ | skeleton готов, prose paper ещё не написан |
| Submission proof assurance | FAIL — submission hold | нет human review или kernel-checked mature assistant build |
| Venue-current novelty audit | FAIL — Gate 8′ | должен быть обновлён непосредственно перед submission |

## 12. Gate decision

| Work package | Статус |
|---|---|
| WP7.1 Minimal extraction | PASS |
| WP7.2 Mature-prover migration | PASS WITH EXPLICIT TCB AND SUBMISSION HOLD |
| WP7.3 Automated figures/tables | PASS |
| WP7.4 Offline reproducibility | PASS |
| WP7.5 Manuscript skeleton | PASS |
| **Gate 7′ overall** | **PASS / GO TO GATE 8′ MANUSCRIPT; SUBMISSION HOLD** |

## 13. Следующий этап

Gate 8′ должен:

1. написать полную связную рукопись без расширения frozen claim;
2. выполнить sentence-level claim-to-evidence audit;
3. закрыть proof assurance human review или kernel-checked development;
4. обновить communication-closure, message-adversary, refinement/conformance и
   BFT-testing prior art на дату submission;
5. выбрать научную аудиторию и адаптировать terminology/page budget;
6. подготовить anonymous artifact и appendix;
7. вынести окончательный submission-ready / pivot / no-go verdict.

Первый необратимый шаг — написать formal model и theorem sections вокруг уже
зафиксированных T1–T3/T6, а не добавлять новые mutants, scheduler features или
протоколы.
