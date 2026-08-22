# Закрытие Gate 0–3 для темы о конечной полноте Twins

**Дата решения:** 11 августа 2026 года  
**Исходный кандидат:** формальные границы полноты finite-clone Twins testing для детерминированных BFT-протоколов с раскрываемой причинной историей.  
**Итог по исходному кандидату:** **ОТКЛОНИТЬ**.  
**Допустимый дальнейший ход:** только **новый существенный pivot** к conformance конкретного scenario language; он не получает автоматического GO.

---

## 1. Executive decision

Gate 0–3 закрыты не положительным подтверждением темы, а решающим отрицательным результатом.

| Gate | Статус выполнения | Решение |
|---|---|---|
| Gate 0 — novelty delta | Закрыт | **NO-GO** для finite-clone cutoff/width; допустим отдельный harness-conformance pivot |
| Gate 1 — minimum formal model | Закрыт | Модель исполнима, но центральный тезис либо ill-posed, либо сводится к определению/chain cover |
| Gate 2 — tools/resources | Закрыт | **PASS** для точного блокирующего пилота; внешние клиенты не нужны |
| Gate 3 — blocking pilot | Закрыт | **NO-GO** по заранее заданному правилу: обычный chain cover и двухветвевое safety-ядро |

### Главный вывод

Предыдущее обозначение `AT(k)` смешивало два различных ресурса:

1. число **всех persistent clone histories** за execution;
2. число **одновременно активных физических slots**, которые можно перезапускать или восстанавливать.

После разделения получаются два разных, но одинаково неблагоприятных для новизны результата:

- для persistent histories минимальное `k` является minimum chain cover несовместимых корректных локальных историй;
- для reusable active slots при произвольной конечной задержке и replay достаточно одного slot для любого конечного trace.

Следовательно, исходная тема не даёт нового BFT-specific bound. Продолжение к Gate 4 означало бы инженерно развивать уже опровергнутую заявку.

---

## 2. Что именно проверялось

Независимый аудит выбрал тему потому, что статья Twins явно оставляет строгую теорию coverage открытой. Gate 0–3 проверяли более узкое остаточное утверждение после учёта prior art:

> Для валидируемого deterministic message-level Byzantine behavior существует содержательная и нетривиальная граница по конечному числу correct-code clones, а минимальное число clones отражает BFT-specific causal structure.

Проверка сознательно не включала malformed messages, forged correct identities, произвольную порчу памяти и mutation faults, которые не являются outputs немодифицированного correct protocol code.

### Рабочие adversary models

- `AB`: accepted-message Byzantine — произвольный выбор validator-admissible histories/messages.
- `AE`: dynamic state equivocation — копирование reachable correct states и продолжение каждой копии правильной transition function.
- `AT_total(k)`: не более `k` различных correct-code histories за весь execution.
- `AT_active(k)`: не более `k` одновременно активных физических slots, но разрешены restart/replay/snapshot reuse.

### Основное наблюдение

Наблюдаются состояния корректных replicas и их решения; physical clone IDs и недоставленные сообщения стираются. Safety — agreement: два корректных узла не должны решить разные values.

---

## 3. Gate 0 — окончательная novelty delta

### 3.1. Что уже известно

1. Twins создаёт несколько автономных correct-code instances с общей identity и credentials, а scenario executor управляет доставкой сообщений. Авторы прямо оставляют строгую теорию coverage будущей работе и признают, что некоторые deviating behaviors и timing attacks могут не покрываться.
2. VLSM уже формализует equivocation и доказывает совпадение traces, наблюдаемых non-Byzantine validators, для Byzantine и equivocation behavior при validator assumptions. Поэтому общий тезис `arbitrary Byzantine ≡ equivocation` не является новым.
3. Minimum chain cover конечного DAG/poset является стандартной задачей; его размер равен width, то есть размеру максимальной antichain, по Dilworth.
4. Конкретные Twins implementations используют scenario languages. В просмотренной документации `relab/hotstuff` scenario задаётся replicas/twins, partitions и leaders для каждого view; generator строит последовательности пар leader/partition. Это отличается от идеального scheduler только потенциально и требует отдельного refinement audit.

### 3.2. Конструктивный novelty kill

Решение Gate 0 не зависит от аргумента «не найдено статьи». Оно следует из собственной семантики кандидата.

#### G0-T1 — static unfolding

Пусть `t` — конечный `AE` trace. Рассмотрим все требуемые faulty local histories, частично упорядоченные отношением совместимости в одной deterministic correct execution. Разобьём их на минимальное число chains. Для каждого chain запускается один persistent clone, которому replay-ятся только соответствующие inputs. Scheduler доставляет корректным replicas только сообщения, присутствующие в `t`, и удерживает остальные.

При deterministic replay, clone-specific delivery, suppressible undelivered messages, arbitrary finite delay и стирании физических clone IDs получается та же observation. Значит:

`AE finite trace -> AT_total(cc(t)) trace`,

где `cc(t)` — minimum chain-cover size.

#### G0-T2 — lower bound

Если observation сохраняет все требуемые ветви, один persistent clone может пройти только одну causally consistent local history. Любая реализация должна покрыть все несовместимые histories chains; поэтому нужно не меньше `cc(t)` clones.

Итак, `k_min = cc(t) = width(t)`. Это стандартная poset identity, а не новая BFT-граница.

#### G0-T3 — active-slot collapse

Если `k` означает только одновременные physical slots, один slot последовательно replay-ит каждую требуемую branch, а сообщения остаются отложенными в сети. После генерации всех sources scheduler доставляет их correct replicas в нужном causal order. При safety-only observation физическое одновременное существование ветвей не требуется.

Следовательно, для любого конечного trace:

`AE ⊆ AT_active(1)`,

а обратное включение следует из того, что slot исполняет correct branches. Иерархия по active `k` вырождается.

### 3.3. Gate 0 decision

**NO-GO.** Сработал заранее установленный criterion: direct generic theorem subsumes claim.

Два пункта первоначального process plan не завершены буквально: open full text статьи S20 не был найден, и live subject-matter expert не привлекался. Это не создаёт неопределённости в решении, потому что positive GO потребовал бы отсутствия subsuming result, тогда как no-go получен конструктивным доказательством из явных assumptions. Эти ограничения остаются релевантными только для нового pivot.

---

## 4. Gate 1 — исправленная формальная модель

### 4.1. Диагностический протокол

Пилот использует одну faulty leader identity и три correct replicas, то есть минимальную конфигурацию `n=4, f=1` по ролям. Correct-code leader branch:

1. принимает один явно заданный value;
2. эмитирует authenticated `PROPOSE(value)`;
3. после matching correct vote эмитирует `COMMIT(value, vote-reference)`.

Correct replica принимает первый valid proposal, locks/votes value и решает только после matching commit. Кворум намеренно слаб; система создана для порождения различающего agreement witness, а не как production BFT protocol.

### 4.2. Validity

Допускаются только сообщения с authenticated sender, value из конечного domain и causally valid commit, который ссылается на соответствующую proposal branch и matching correct vote. Malformed bytes, подделка correct identity и необоснованные internal-state claims исключены.

### 4.3. Сеть

- asynchronous safety semantics;
- arbitrary finite delay и reordering;
- clone-specific delivery;
- emitted message можно не доставлять;
- нет fairness, GST или real-time deadline;
- physical clone IDs не наблюдаются.

### 4.4. Observation language

Для каждого labeled correct replica:

- `N` — proposal не получен;
- `P(v)` — proposal получен и locked/voted, commit не получен;
- `D(v)` — matching commit получен и `v` решён.

Unsafe observation содержит не менее двух различных decided values.

### 4.5. Discharged obligations

| Obligation | Статус | Результат |
|---|---|---|
| `AT_total(k) ⊆ AE` | PASS | одинаковые transitions, ограниченное множество branches |
| `AB = AE` в pilot validator model | PASS | exact language equality для binary и ternary bounds |
| observation non-vacuous | PASS | различает `N`, `P`, `D` и agreement violation |
| completeness event BFS относительно independent quotient | PASS | equality для каждого branch set |
| static `k_min` meaningful | Формально PASS, novelty FAIL | совпадает с width/chain cover |
| active-slot `k` meaningful | FAIL | reusable slot collapse к `1` |
| central theorem non-definitional | FAIL | static construction — one chain per history |
| concrete harness conformance | UNKNOWN | другая задача, не моделировалась |

### 4.6. Gate 1 decision

Формальная модель завершена и исполнима, но научный GO не пройден. Исходная `AT(k)` была неоднозначной. Обе корректировки устраняют неоднозначность и одновременно уничтожают центральный contribution claim.

---

## 5. Gate 2 — инструменты и ресурсы

### 5.1. Mandatory local environment

- Python `3.13.5`;
- uv `0.10.0`;
- `uv.lock` и `.python-version`;
- standard-library-only executable pilot;
- deterministic TOML configuration;
- `unittest` regression suite;
- source, license и environment manifests;
- no RPC, no dataset, no cloud, no external solver, no mainnet/testnet interaction.

### 5.2. Reproduction command

```bash
./gate2/reproduce.sh
```

Script runs nine tests, rewrites deterministic pilot outputs and verifies them against the reviewed SHA-256 baseline. Environment and timing records are excluded from scientific result hashes.

### 5.3. External artifacts

Official pages and licenses of Twins simulator, VLSM, ByzzBench and `relab/hotstuff` were inspected. The isolated execution runtime could not clone external repositories because outbound DNS was unavailable. Since Gate 3 ends in no-go without them, no mandatory evidence is missing.

Any concrete-harness pivot must reopen Gate 2, acquire one repository at an exact commit and validate the actual executor—not infer semantics solely from documentation.

### 5.4. Clean reproduction

A second run was performed from a copied package with no pre-existing virtual environment or Python caches. uv created the environment, all nine tests passed, all manifest checks passed, and the five decisive deterministic result files were byte-identical to the reviewed run. The record is in `gate2/clean_reproduction.md`.

### 5.5. Gate 2 decision

**PASS for the blocking Gate 0–3 decision.** The pilot can be reproduced offline from this package.

---

## 6. Gate 3 — exact blocking pilot

### 6.1. Design

- one faulty protocol identity;
- three labeled correct replicas;
- binary domain `{0,1}` and ternary ablation `{0,1,2}`;
- all subsets of correct-code branches enumerated;
- event-level BFS explores every reachable state for every branch set;
- independent closed-form quotient enumerates all products of `N`, `P(v)`, `D(v)` and is asserted equal to BFS;
- compared models: `AB`, `AE`, static persistent `k=0..3`, reusable active `k=0..1`;
- no sampling, random seed or statistical inference.

### 6.2. Exact results

| Domain | Model | Language size | Unsafe | Missing unsafe vs `AE` |
|---|---:|---:|---:|---:|
| binary | `AB` | 125 | 24 | 0 |
| binary | `AE` | 125 | 24 | 0 |
| binary | static `k=1` | 53 | 0 | 24 |
| binary | static `k=2` | 125 | 24 | 0 |
| binary | active-reuse `k=1` | 125 | 24 | 0 |
| ternary | `AB` | 343 | 96 | 0 |
| ternary | `AE` | 343 | 96 | 0 |
| ternary | static `k=1` | 79 | 0 | 96 |
| ternary | static `k=2` | 295 | 72 | 24 |
| ternary | static `k=3` | 343 | 96 | 0 |
| ternary | active-reuse `k=1` | 343 | 96 | 0 |

### 6.3. Decisive machine checks

Для обоих domains автоматически подтверждены:

- `AB_equals_AE = true`;
- `AT_embeds_in_AE = true`;
- `static_k_min_equals_width_for_all_AE_observations = true`;
- `snapshot_active_one_equals_AE = true`;
- `every_unsafe_observation_has_two_branch_subwitness = true`.

Nine regression tests pass, including independent BFS/quotient equivalence.

### 6.4. Minimal witness

Бинарный unsafe witness:

`D0 | D1 | N`.

Он требует branches `0` и `1`. Static `k=1` не способен его породить, static `k=2` способен. В reusable-slot semantics один physical slot сначала replay-ит branch `0`, удерживает её messages, затем branch `1`, после чего scheduler доставляет сообщения в causally valid order.

Тернарное observation `D0 | D1 | P2` требует three persistent branches только потому, что observation сохраняет третью proposal branch. Его agreement violation имеет core `D0 | D1 | N`, то есть two-branch witness. Поэтому strict `k=2<k=3` не является более сильной safety boundary.

### 6.5. Alternative explanations eliminated

- **Implementation bug:** event BFS сравнивается с независимой closed-form language и покрыт tests.
- **AB получил скрытую силу:** AB ограничен тем же validator-admissible branch language; `AB=AE` проверено exact enumeration.
- **Случайный workload:** все finite branch sets перечислены.
- **Недостаток repetitions:** отсутствует probabilistic sampling.
- **Особый canonicalizer:** raw labeled node statuses сохраняются; equivalence only canonical string serialization.
- **Strict hierarchy скрывает новый safety result:** every unsafe observation имеет two-branch core.

### 6.6. Gate 3 decision

**NO-GO.** Gate rule прямо предписывал остановку, если результат повторяет VLSM, обычный chain cover или trivial two-clone behavior. Пилот подтвердил последние два условия, а Gate 0 показал общий collapse независимо от finite bound.

---

## 7. Что стало известно при неверной исходной гипотезе

Отрицательный результат не означает просто «метрика не улучшилась».

1. **Clone count нельзя обсуждать без lifecycle semantics.** Total histories и simultaneous slots — разные ресурсы с противоположным поведением.
2. **В ideal asynchronous model persistent `k` измеряет decomposition histories, а не специальное свойство BFT protocol.** Его точное значение задаётся minimum chain cover выбранного observation.
3. **Active `k` бессодержателен при replay и unbounded delay.** Один slot достаточно для любого finite safety trace.
4. **Safety violations agreement имеют двухветвевое ядро в диагностическом protocol.** Дополнительные branches могут увеличивать exact observation width, но не минимальный violating core.
5. **Настоящая неизвестная находится не в числе абстрактных clones, а в разрыве между ideal scheduler и конкретным scenario language/lifecycle.** Именно там ограничения partitions, views, timers, transport observability или non-replayable resources могут создать nontrivial separation.

---

## 8. Ограничения результата

### Что доказано аналитически

Static unfolding, exact-history lower bound и active-slot collapse следуют для любого finite trace при перечисленных assumptions A1–A7. Они не зависят от binary/ternary pilot.

### Что подтверждено только пилотом

Конкретные language sizes, двухветвевое unsafe core и equality `AB=AE` относятся к diagnostic two-phase model и указанным domains. Они не являются theorem для HotStuff, Tendermint или DiemBFT.

### Что не проверено

- actual executor semantics конкретного production/research harness;
- timers, bounded delay, fairness и synchronous attacks;
- non-suppressible transport logs;
- signatures/nonces или external resources, связанные с physical process lifecycle;
- multiple faulty identities;
- liveness properties;
- полный текст S20;
- expert review связи с refinement/I/O-automata literature.

Эти пробелы не позволяют заявлять conformance pivot новым, но не отменяют no-go исходного ideal-model claim.

---

## 9. Решение о дальнейшем исполнении

### Запрещённый следующий шаг

Не переходить к Gate 4 исходного проекта: не интегрировать production HotStuff client, не строить общий BFT framework и не начинать mechanized proof finite-clone cutoff.

### Единственный рациональный pivot

Новый вопрос:

> Каков trace-language gap между ideal per-message state equivocation и конкретным view-partition Twins scenario language, и существует ли safety-relevant trace, не кодируемый этим language?

Этот вопрос должен начать новый Gate 0 с audit communication closure, refinement, scenario-language expressiveness и фактической executor semantics. Charter находится в `docs/CONCRETE_HARNESS_PIVOT_CHARTER.md`.

---

## 10. Artifact map

| Путь | Назначение |
|---|---|
| `GATE_STATUS.csv` | machine-readable итог Gates 0–3 |
| `gate0/claim_map.md` | classification каждого core claim |
| `gate0/theorem_candidate.md` | constructive collapse proofs |
| `gate0/prior_art_matrix.csv` | ближайший academic/engineering prior art |
| `gate1/assumption_map.csv` | powers и их scientific effect |
| `spec/definitions.md` | executable formal vocabulary |
| `spec/proof_obligations.md` | obligation ledger |
| `gate2/environment_report.md` | environment и deviations |
| `gate2/source_manifest.csv` | sources/versions/checksums |
| `gate2/clean_reproduction.md` | clean-environment reproduction record |
| `gate2/license_inventory.csv` | licenses |
| `gate2/reproduce.sh` | clean reproduction command |
| `src/twinsbound/` | exact model/explorer/oracles |
| `tests/` | nine regression tests |
| `results/pilot/language_summary.csv` | exact language counts |
| `results/pilot/k_min.csv` | per-observation bounds and unsafe cores |
| `results/pilot/unmatched_traces.jsonl` | minimized witnesses absent at lower caps |
| `results/pilot/theorem_checks.json` | machine-readable decisive predicates |
| `results/pilot/state_space.json` | complete state-space accounting |
| `results/pilot/manifest.sha256` | reviewed deterministic baseline |

---

## 11. Source register

1. Bano et al. *Twins: BFT Systems Made Robust*. OPODIS 2021. DOI `10.4230/LIPIcs.OPODIS.2021.7`; arXiv `2004.10617`.
2. Zamfir et al. *Validating Labelled State Transition and Message Production Systems*. arXiv `2202.12662v4`, especially state/message equivocation and Theorem 7.1.
3. Cáceres. *Minimum Chain Cover in Almost Linear Time*. ICALP 2023. DOI `10.4230/LIPIcs.ICALP.2023.31`.
4. Drăgoi et al. *Testing Consensus Implementations Using Communication Closure*. PACMPL/OOPSLA 2020. DOI `10.1145/3428278`.
5. Abadi and Lamport. *The Existence of Refinement Mappings*. TCS 1991. DOI `10.1016/0304-3975(91)90224-P`.
6. Liang et al. *Node-Centric Systematic Testing for Distributed Systems*. ACM TOSEM 2026. DOI `10.1145/3831368`; metadata/abstract only in this run.
7. `asonnino/twins-simulator`, Apache-2.0, official repository documentation.
8. `relab/hotstuff`, MIT, official repository and `docs/twins.md` documentation.

Full identifiers and resource status are recorded in `gate2/source_manifest.csv` and `gate0/search_log.md`.

---

# Final verdict

**Gate 0–3 are closed. The finite-clone Twins candidate is rejected.**

The result is scientifically useful: it identifies the exact modeling error, proves why the proposed bound collapses, supplies an executable counter-audit, and prevents costly implementation of a non-novel claim. A concrete-harness conformance question remains possible, but it is a new candidate with status **ТРЕБУЕТ СУЩЕСТВЕННОГО PIVOT**, not a continuation already approved for implementation.
