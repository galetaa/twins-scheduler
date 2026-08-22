# Implementation Specification

**Artifact name:** `twinsbound`  
**Purpose:** executable formal model and exact bounded checker for comparing accepted-message Byzantine behavior, dynamic state equivocation and finite-clone Twins behavior.  
**Status:** architecture ready for blocking pilot; full implementation conditional on Gate 0 and Gate 1.

## 1. Artifact purpose and non-purpose

The artifact must answer exact semantic questions:

- which correct-node observations are reachable under each adversary model;
- whether one observation language includes another;
- minimum clone cap needed to reproduce an abstract-equivocation witness;
- which assumption or harness capability explains an unmatched trace.

It is not:

- a new blockchain client;
- a production consensus implementation;
- a high-throughput simulator;
- a mainnet attack tool;
- a general-purpose fuzzer;
- a performance benchmark;
- a dashboard or hosted service.

## 2. Architecture

The architecture has seven layers:

1. **Pure protocol semantics** — immutable local states, messages, transition function and validation.
2. **Adversary semantics** — correct, accepted-message Byzantine, dynamic equivocation, finite-clone and optional mutation models.
3. **Execution engine** — enabled-event generation, state transition and bounded exploration.
4. **Canonicalization and reduction** — symmetry, causal normalization and partial-order reduction.
5. **Oracles** — safety, observation projection, language inclusion and minimum-clone search.
6. **Analysis** — witness minimization, causal-history extraction, width predictors and decision rules.
7. **Adapters** — optional import/export to S21, S22, S08 and S06.

The core remains single-process and deterministic. Parallel search may be added only after correctness is established because parallel enumeration complicates reproducibility and state deduplication.

## 3. Components and responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| `model.types` | Frozen data types for identity, state, message, event and observation | Contain protocol-specific rules |
| `model.causality` | Dependency DAG, histories and incompatibility operations | Infer validity from implementation logs |
| `protocols.base` | Protocol interface and transition contracts | Schedule network events |
| `protocols.toy_locking` | Minimal pilot protocol | Encode adversary shortcuts |
| `protocols.streamlet_like` | Post-pilot independent model | Change common observation definitions |
| `protocols.hotstuff_like` | Conditional validation model | Depend on production client internals |
| `adversaries.correct` | No-process-fault baseline | Mutate messages |
| `adversaries.byzantine` | Accepted-message abstract generator | Emit messages rejected by declared `Valid` |
| `adversaries.equivocation` | Dynamic state-copy semantics | Impose finite clone cap |
| `adversaries.twins_k` | Concrete finite-clone lifecycle and scheduler | Execute non-protocol transitions |
| `adversaries.mutation` | Optional stronger comparator | Enter main coverage theorem |
| `engine.enabled` | Enumerate enabled semantic events | Canonicalize observations |
| `engine.step` | Apply one event and verify invariants | Hide invalid transitions |
| `engine.explorer` | BFS or layered DFS under explicit bounds | Treat partial search as complete |
| `engine.store` | Deduplicate canonical global states | Merge states without preservation proof |
| `oracle.safety` | Detect agreement violation | Use model-specific clone internals |
| `oracle.observation` | Project correct-node observable semantics | Include physical clone IDs |
| `oracle.language` | Compute exact inclusion and differences | Estimate set inclusion statistically |
| `analysis.minimize` | Delta-debug decisive traces | Change observation class silently |
| `analysis.width` | Extract competing structural predictors | Define width using already known `k_min` |
| `analysis.decision` | Apply predeclared GO, NO-GO, PIVOT rules | Override rules for a preferred outcome |
| `adapters` | Concrete artifact conformance and trace normalization | Become a required core dependency |

## 4. Interfaces

### 4.1. Protocol interface

A protocol module supplies:

```text
initial_local_state(identity, config) -> LocalState
validate(recipient, local_state, message, context) -> ValidationResult
step(actor, local_state, input_event, context) -> TransitionResult
observe_local(local_state) -> LocalObservation
is_value_compatible(value_a, value_b) -> bool
```

`TransitionResult` contains new state, emitted messages and disclosed causal dependencies. It is a pure value; no network I/O or global mutation is permitted.

### 4.2. Adversary interface

```text
initial_adversary_state(protocol, config) -> AdversaryState
enabled_actions(global_state, bounds) -> iterable of AdversaryAction
apply_action(global_state, action) -> GlobalState
profile_metadata() -> Mapping
```

Every action must identify semantic authority: scheduler action, correct local step, abstract message production, state copy or clone lifecycle.

### 4.3. Explorer interface

```text
explore(model, bounds, reductions, sink) -> ExplorationSummary
```

The summary must state whether enumeration is complete, which bound frontier was reached, number of unique states, number of transitions, unsafe observations and termination reason.

### 4.4. Oracle interface

```text
project(trace_or_state, observation_profile) -> CanonicalObservation
violates_safety(observation) -> SafetyResult
compare_languages(left_manifest, right_manifest) -> LanguageDifference
minimum_clone(witness, clone_range, profile) -> CloneSearchResult
```

## 5. Data model

### 5.1. Immutable identifiers

All identities, messages, events and states receive deterministic content hashes. Hashes are conveniences for storage and comparison; semantic equality is defined by canonical serialized content, not collision-prone assumptions.

### 5.2. Message record

Contains:

- schema version;
- protocol identity of sender;
- message type;
- round;
- value identifier;
- justification identifiers;
- disclosed choice;
- abstract signature token;
- payload fields;
- causal dependency identifiers.

### 5.3. Event record

Contains:

- trace-local event number;
- event kind;
- actor or recipient;
- clone identifier only in internal execution record;
- input message identifier;
- emitted-message identifiers;
- pre-state and post-state hashes;
- direct causal parents;
- semantic rule identifier.

### 5.4. Observation record

Contains only declared correct-node states, accepted certificates, decisions and delivered evidence. Internal clone IDs are replaced by shared protocol identity.

## 6. File formats

- **TOML:** human-authored configurations, parsed by Python standard library `tomllib`.
- **JSON Lines:** event traces and witness corpora; one deterministic record per line.
- **JSON:** exploration summary, environment and manifests.
- **CSV:** language sizes, parameter matrices, `k_min` tables and ablation results.
- **Markdown:** decision memos, proof sketches and human-readable witness explanation.
- **Graphviz DOT:** optional causal DAG rendering; source DOT is canonical, rendered images are derived.
- **Coq source:** optional proof development after theorem stabilization.

Every format contains a schema version. A migration script is required before breaking a stored schema.

## 7. Configuration schema

`configs/pilot.toml` contains:

```text
schema_version = 1
experiment_id = "BP-TWINS-FC-01"
protocol = "toy_locking"
identities = 4
byzantine_identities = 1
values = 2
round_bound = 4
delivery_bound = 24
local_step_bound = 32
certificate_bound = 8
clone_caps = "1,2,3,4"
observation_profile = "safety_state"
clone_profile = "genesis_static"
search_order = "breadth_first"
symmetry_reduction = true
partial_order_reduction = true
stop_after_complete_bound = true
```

Numerical defaults are not scientific thresholds. Before execution they are derived from protocol emission rules and minimum decision depth, then recorded in `decision.md`. If the minimum unsafe witness requires a larger bound, the configuration is versioned rather than edited in place.

## 8. Logging and observability

### 8.1. Human logs

Structured text records:

- phase start and finish;
- active configuration hash;
- completed frontier;
- resource use;
- reduction statistics;
- invariant violations;
- incomplete-search reason.

### 8.2. Machine logs

JSON event logs include exact timestamps only for operational diagnostics. Timestamps never enter semantic equality.

### 8.3. Progress reporting

Progress is based on completed BFS layers and canonical states, not estimated percentage. Explorer must never print “complete” when a resource cap stopped enumeration.

## 9. Error handling

Error classes:

- configuration error;
- invalid protocol transition;
- invalid adversary action;
- canonicalization collision or nondeterminism;
- bound overflow;
- resource exhaustion;
- schema mismatch;
- external-adapter mismatch;
- proof or invariant violation.

Policy:

- semantic errors stop the run immediately;
- resource exhaustion writes an incomplete manifest and exits nonzero;
- external adapter failures do not invalidate core results but block practical-conformance claims;
- no exception is converted into an empty language.

## 10. Reproducibility mechanism

- `.python-version` pins Python 3.14.7;
- `pyproject.toml` pins direct dependencies;
- `uv.lock` pins the resolved graph;
- `environment.json` records OS, architecture, CPU, RAM, Python, uv and optional solver versions;
- every run stores Git commit and dirty-tree status;
- configuration and source hashes are embedded in result manifests;
- exploration order is deterministic;
- generated figures are recreated from committed CSV or JSON;
- raw traces are immutable;
- processed outputs name their raw-manifest dependency;
- external repos are recorded by commit hash, license and local patch checksum.

## 11. Test strategy

### 11.1. Unit tests

- local transition rules;
- message validity;
- certificate construction;
- event causality;
- safety oracle;
- observation projection;
- canonical serialization.

### 11.2. Property-based tests

Using S24 only for software validation:

- canonicalization idempotence;
- identity-renaming invariance;
- value-renaming invariance;
- `AT(k)` language monotonicity in `k` within same profile;
- every finite-clone trace embeds into dynamic equivocation;
- replay of serialized trace yields same observation.

Property-based tests do not establish the research theorem.

### 11.3. Metamorphic tests

- adding an undelivered message does not change `ObsDecision`;
- renaming physical clone IDs does not change observation;
- disabling reductions yields same tiny-bound languages;
- expanding a bound cannot remove a previously reachable observation;
- increasing clone cap cannot reduce finite-clone language.

### 11.4. Differential tests

- two independent safety-oracle implementations;
- two serializers produce identical semantic hashes;
- optional Python versus SMT witness check;
- formal trace versus S21, S22 or S08 adapter.

### 11.5. Regression corpus

Every decisive counterexample is committed as minimized JSONL plus a human derivation and a test asserting its classification.

## 12. Trusted computing base

Scientific trust depends on:

1. protocol transition implementation;
2. message-validity predicate;
3. adversary semantics;
4. canonicalizer and reductions;
5. observation projection;
6. safety oracle;
7. set-comparison code;
8. Python runtime and standard-library serialization.

Hypothesis, pytest, uv, plotting tools and external Twins implementations are outside the semantic TCB. Z3 joins the TCB only for results it decides; therefore all decisive solver witnesses must be replayed concretely.

## 13. External dependencies and licenses

| Tool or artifact | Purpose | Official status on 11 Aug 2026 | License | Maturity | Limitations | Simpler fallback |
|---|---|---|---|---|---|---|
| Python 3.14.7, S23 | Core implementation | Official maintenance release, 5 Aug 2026 | PSF | High | New patch line may not be installed on all systems | Python 3.13 pinned after compatibility test |
| uv, S26 | Environment and lockfile | Official Astral docs, universal lockfile | Apache-2.0 or MIT dual project licensing as distributed | High and actively maintained | Exact CLI version must be recorded; lock format uv-specific | Standard `venv` plus hashed requirements export |
| pytest 9.1.1, S25 | Test runner | Official stable changelog, 19 Jun 2026 | MIT | High | Major-version deprecations; avoid private APIs | Standard-library `unittest` |
| Hypothesis 6.165.3, S24 | Property-based software tests | Official PyPI, 11 Aug 2026 | MPL-2.0 | High | Not a formal proof and may find only sampled cases | Exhaustive tiny-domain generators |
| Z3 5.0.0, S27 | Optional symbolic backend | Official release, 17 Jul 2026 | MIT | High but recent release has publicly reported edge-case issues | Never accept `unknown`; set timeout; replay models; avoid experimental parallel mode | Explicit enumeration or stable earlier pinned solver after audit |
| VLSM repo, S06 | Prior-art verification and optional Coq reuse | 325 commits; Coq 8.16+; recommended 8.18 | BSD-3-Clause | Research-grade formal library | Nontrivial Coq learning cost; abstract model not concrete harness | Manual theorem plus executable Python model |
| twins-simulator, S21 | External scenario replay | Small research repo; Streamlet and Fast-HotStuff | Apache-2.0 | Research prototype | Research-only, limited maintenance and scope | Internal formal models |
| relab/hotstuff, S22 | HotStuff conformance validation | Active framework, 1,849 commits, Go 1.18+ | MIT | Mature research framework | Complex production-style code and instrumentation gap | S21 or ByzzBench |
| ByzzBench, S08 | Controlled BFT testing baseline | Peer-reviewed tool paper and MIT repository | MIT | Early but purpose-built | Preliminary Twins integration; benchmark semantics may differ | Internal adapter and toy model |
| Graphviz | Derived DAG figures | Version fixed at Gate 2 | EPL-1.0 | Mature | Rendering nondeterminism across versions | Plain DOT and textual DAG tables |
| Coq 8.18 | Optional proof assistant matching S06 recommendation | Official ecosystem version required by pinned opam switch | LGPL family for Coq distribution | Mature | High human cost | Manual proof with checked executable lemmas |

## 14. Verified setup commands

The following commands were checked against official documentation available on 11 August 2026. Exact binary versions must still be recorded in the repository environment report.

### 14.1. Create project and dependencies

```text
mkdir twinsbound
cd twinsbound
uv init
uv add --dev pytest==9.1.1 hypothesis==6.165.3
uv lock
uv sync
uv run pytest
```

`uv init`, `uv add`, `uv lock`, `uv sync` and `uv run` are documented by S26. Python version is then pinned by setting `.python-version` to `3.14.7` and `requires-python` to the intended compatible range. The project must not rely on an unverified `uv init --python` variation.

### 14.2. Build VLSM formalization for independent prior-art inspection

Official S06 commands:

```text
opam repo add coq-released https://coq.inria.fr/opam/released
opam install coq.8.18.0 coq-stdpp.1.9.0 coq-itauto coq-equations
git clone https://github.com/runtimeverification/vlsm.git
cd vlsm
make
```

Before use, replace the floating repository state with a recorded commit checkout. The listed commands verify buildability of S06, not integration with `twinsbound`.

### 14.3. Twins simulator external validation

Official S21 commands:

```text
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest
pytest
python scripts/twins_executor.py scripts/test_scenarios.json
```

These commands belong to external validation only. The main project continues to use uv and does not copy S21 environment uncritically.

### 14.4. relab HotStuff validation

Official S22 minimum commands and requirements:

```text
make
./hotstuff help run
```

Go 1.18 or later is required. Exact experiment command must be selected from the repository documentation at the pinned commit; no unverified command is specified here.

## 15. Repository structure

```text
twinsbound/
  .python-version
  pyproject.toml
  uv.lock
  LICENSE
  CITATION.cff
  README.md
  spec/
    definitions.md
    assumptions.md
    theorem_targets.md
    observation_profiles.md
  src/
    twinsbound/
      model/
        types.py
        causality.py
        canonical.py
      protocols/
        base.py
        toy_locking.py
        streamlet_like.py
        hotstuff_like.py
      adversaries/
        correct.py
        byzantine.py
        equivocation.py
        twins_k.py
        mutation.py
      engine/
        enabled.py
        step.py
        explorer.py
        reductions.py
        store.py
      oracle/
        safety.py
        observation.py
        language.py
      analysis/
        minimize.py
        width.py
        decision.py
        render.py
      adapters/
        twins_simulator.py
        relab_hotstuff.py
        byzzbench.py
  configs/
    pilot.toml
    ablations/
    protocols/
  experiments/
    e0_definition_audit.py
    e1_byzantine_equivocation.py
    e2_clone_hierarchy.py
    e3_width.py
    e4_ablations.py
    e5_lifecycle.py
    e6_cross_protocol.py
    e7_conformance.py
    e8_sensitivity.py
  tests/
    unit/
    property/
    metamorphic/
    differential/
    regression/
  data/
    manifests/
    external/
  results/
    raw/
    processed/
    pilot/
  figures/
    source/
    rendered/
  proof/
    manual/
    vlsm/
  notebooks/
    exploratory_only/
  containers/
    Dockerfile
    compose.yaml
  docs/
    artifact_evaluation.md
    disclosure.md
    limitations.md
  scripts/
    run_pilot.py
    run_all.py
    verify_manifest.py
    make_figures.py
    report_environment.py
  third_party/
    README.md
```

Notebooks are explicitly non-authoritative. Every final result must be generated by versioned scripts.

## 16. Main exploration pseudocode

```text
procedure Explore(model, bounds, reductions):
    initial = Canonicalize(model.initial_state())
    frontier = queue containing initial
    seen = map initial to empty predecessor
    observations = empty set
    unsafe_witnesses = empty map

    while frontier is not empty:
        state = frontier.pop_front()
        observation = ProjectSafety(state)
        observations.add(observation)

        if ViolatesAgreement(observation):
            witness = ReconstructTrace(seen, state)
            unsafe_witnesses.keep_smallest(observation, witness)

        if AtBound(state, bounds):
            continue

        actions = model.enabled_actions(state)
        actions = ReductionsFilter(state, actions, reductions)

        for action in DeterministicOrder(actions):
            next_state = model.apply(state, action)
            AssertSemanticInvariants(state, action, next_state)
            canonical = Canonicalize(next_state)
            if canonical not in seen:
                seen.insert(canonical, predecessor = state and action)
                frontier.push_back(canonical)

    return CompleteExplorationManifest(observations, unsafe_witnesses, seen)
```

## 17. Minimum-clone pseudocode

```text
procedure MinimumClone(witness_observation, protocol, profile, max_k, bounds):
    for k from 1 through max_k:
        manifest = Explore(TwinsModel(protocol, profile, k), bounds, reductions = verified)
        if witness_observation is in manifest.observations:
            return finite result with k and constructive trace
    if max_k covers proven finite upper bound:
        return infinity within profile
    return unknown beyond tested cap
```

The procedure must never return infinity merely because an arbitrary `max_k` was reached.

## 18. Witness minimization pseudocode

```text
procedure Minimize(trace, predicate):
    current = trace
    repeat:
        changed = false
        for removable causal slice in CandidateSlices(current):
            trial = RemoveAndRepair(current, slice)
            if IsValidTrace(trial) and predicate(trial):
                current = trial
                changed = true
                break
    until not changed
    return current
```

`RemoveAndRepair` may delete only causally closed slices and must not synthesize new messages.

## 19. Minimal vertical slice

The smallest end-to-end path is:

1. parse `configs/pilot.toml`;
2. instantiate four-node toy locking protocol;
3. enumerate `AE` to the first complete bound with unsafe observation;
4. enumerate `AT(2)` under same bound;
5. project both through `ObsSafety`;
6. compute exact difference;
7. emit one human-readable unmatched or matched witness;
8. write `results/pilot/decision.md` with incomplete or complete status.

This slice excludes width analysis, second protocol, SMT, Coq and external adapters. It is the first integration acceptance test.

## 20. Performance constraints

- no assumption of GPU acceleration;
- memory use must be bounded and reported;
- state serialization should be compact but readable in debug mode;
- explorer may checkpoint complete BFS layers;
- disk spilling is a later optimization;
- no approximate Bloom-filter deduplication for decisive runs;
- every optimization must preserve tiny-bound languages exactly;
- if a completed decisive bound cannot be reached on one workstation, the pilot returns inconclusive and triggers abstraction review rather than cloud escalation by default.

## 21. Security threats to the artifact

- untrusted external trace files may be large or malformed;
- deserialization must use JSON, not executable pickle;
- no private keys or live node credentials are accepted;
- adapters operate only on local test fixtures;
- subprocess calls use fixed argument arrays;
- path traversal is rejected in manifests;
- generated HTML, if any, escapes message contents;
- dependency hashes and licenses are recorded;
- no arbitrary protocol plug-in code is loaded in artifact-evaluation mode.

## 22. Extension path after pilot

Only after GO:

1. stabilize theorem definitions;
2. add causal-width and minimization modules;
3. add second protocol model;
4. add concrete adapter;
5. add optional symbolic backend;
6. mechanize core embedding and lower-bound lemmas;
7. package one-command reproduction and artifact-evaluation documentation.

No production blockchain platform or global network is added at any stage.

## Реестр источников и проверяемых идентификаторов

Дата проверки веб-источников и состояния инструментов: 11 августа 2026 года.

| ID | Источник | Тип и статус | Идентификатор, артефакт и фактическая роль |
|---|---|---|---|
| S01 | `00_RESEARCH_BRIEF_BLOCKCHAIN_CS.md`, версия 2.0 | Локальный исходный бриф | SHA-256 `fa0ee734ff7f09690ee4e3e5b520d7a9d2d6485bef07b89e19128ba2dd5a660e`. Определяет область, ограничения, ресурсы, требования к вкладу, отрицательному результату и безопасности. |
| S02 | `Исследовательский анализ брифа.txt` | Локальный первый исследовательский проход | SHA-256 `723ac880390123aae20396d2bd8911c04560548ebda3dc3d5f69ba235f195b45`. Две загруженные копии имеют одно и то же имя и содержание; положительные оценки не использованы как доказательства. |
| S03 | `independent_audit_blockchain_topics_2026-08-11.md` | Локальный независимый аудит | SHA-256 `b541b2fdfa1470caaf0a2dcd62a7b97db9257232637460a25e787f2346a70742`. Источник выбранного кандидата, но не источник истины о новизне. |
| S04 | Shehar Bano, Alberto Sonnino, Andrey Chursin, Dmitri Perelman, Zekun Li, Avery Ching, Dahlia Malkhi. *Twins: BFT Systems Made Robust*. OPODIS 2021 | Рецензированная конференционная статья | DOI `10.4230/LIPIcs.OPODIS.2021.7`; arXiv `2004.10617`. Вводит correct-code clones с общей identity, оставляет строгую теорию coverage открытой и формулирует conjecture для deterministic full-disclosure protocols. Артефакты заявлены открытыми; статья CC-BY 4.0. |
| S05 | Vlad Zamfir, Mihai Calancea, Denisa Diaconescu, Wojciech Kołowski, Brandon Moore, Karl Palmskog, Traian Florin Șerbănuță, Michael Stay, Dafina Trufaș, Jan Tušil. *Validating Labelled State Transition and Message Production Systems: A Theory for Modelling Faulty Distributed Systems* | Препринт с машинно проверенной формализацией | arXiv `2202.12662v4`, 15 декабря 2023 года. Определяет validators, state/message equivocation и доказывает совпадение traces, наблюдаемых honest validators, под Byzantine и equivocation behavior при указанных предположениях. Все результаты проверены в Coq. Это главный novelty-killer исходного кандидата. |
| S06 | `runtimeverification/vlsm` | Открытый Coq-репозиторий | Лицензия BSD-3-Clause; Coq 8.16 и новее; рекомендован Coq 8.18; зависимости `coq-stdpp` 1.9 и новее, Itauto, Equations. Содержит формализацию S05. Commit hash должен быть зафиксирован в Gate 2. |
| S07 | Levin N. Winter, Florena Buse, Daan de Graaf, Klaus von Gleissenthall, Burcu Kulahcioglu Ozkan. *Randomized Testing of Byzantine Fault Tolerant Algorithms* | Рецензированная статья PACMPL OOPSLA1 2023 | DOI `10.1145/3586053`. Вводит ByzzFuzz; показывает fault executions с future-round field mutation, которые обычный Twins не порождает. Эти случаи не автоматически принадлежат validator-only модели S05. |
| S08 | João Miguel Louro Neto, Burcu Kulahcioglu Ozkan. *A Benchmark Framework for Byzantine Fault Tolerance Testing Algorithms* | Рецензированная tool paper, FMBC 2025 | DOI `10.4230/OASIcs.FMBC.2025.13`. Описывает ByzzBench, контролируемую среду и начальные реализации random tester, ByzzFuzz и Twins. Репозиторий `joaomlneto/byzzbench`, лицензия MIT; commit hash фиксируется в Gate 2. |
| S09 | Cezara Drăgoi, Constantin Enea, Burcu Kulahcioglu Ozkan, Rupak Majumdar, Filip Nikšić. *Testing Consensus Implementations Using Communication Closure* | Рецензированная статья PACMPL OOPSLA 2020 | DOI `10.1145/3428278`. Ближайший prior art по schedule reduction и представительным executions, но не по эквивалентности двух Byzantine fault models. |
| S10 | Ognjen Marić, Christoph Sprenger, David Basin. *Cutoff Bounds for Consensus Algorithms* | Рецензированная статья CAV 2017 | DOI `10.1007/978-3-319-63390-9_12`. Ближайший prior art по process cutoffs; не даёт clone cutoff для Twins. |
| S11 | Igor Konnov, Marijana Lazić, Helmut Veith, Josef Widder. *A Short Counterexample Property for Safety and Liveness Verification of Fault-tolerant Distributed Algorithms* | Рецензированная статья POPL 2017 | DOI `10.1145/3009837.3009860`. Даёт bounded-witness reasoning для класса fault-tolerant algorithms, но не реализацию Byzantine witness finite-clone adversary. |
| S12 | Nathalie Bertrand, Vincent Gramoli, Igor Konnov, Marijana Lazić, Pierre Tholoniat, Josef Widder. *Holistic Verification of Blockchain Consensus* | Рецензированная статья DISC 2022 | DOI `10.4230/LIPIcs.DISC.2022.10`. Систематическая формальная проверка blockchain consensus; полезна для abstraction strategy, но объектом является protocol safety, а не completeness fault injector. |
| S13 | Ruijie Meng, George Pîrlea, Abhik Roychoudhury, Ilya Sergey. *Greybox Fuzzing of Distributed Systems* | Рецензированная статья ACM CCS 2023 | DOI `10.1145/3576915.3623097`. MALLORY использует causal behavior summaries для guided fault injection. Угрожает любому claim о новом causal coverage metric, но не решает trace-language inclusion Twins. |
| S14 | Peiyao Sheng, Gerui Wang, Kartik Nayak, Sreeram Kannan, Pramod Viswanath. *BFT Protocol Forensics* | Рецензированная статья ACM CCS 2021 | DOI `10.1145/3460120.3484566`. Формализует forensic evidence после нарушений BFT. Релевантна observations и evidence, но не clone expressiveness. |
| S15 | João Soares, Ricardo Fernandez, Miguel Silva, Tadeu Freitas, Rolando Martins. *ZERMIA: A Fault Injector Framework for Testing Byzantine Fault Tolerant Protocols* | Рецензированная глава, NSS 2021 | DOI `10.1007/978-3-030-92708-0_3`. Инженерный prior art по fault injection; не даёт coverage theorem. |
| S16 | Mads Frederik Madsen, Søren Debois. *On the Subject of Non-Equivocation: Defining Non-Equivocation in Synchronous Agreement Systems* | Рецензированная статья PODC 2020 | DOI `10.1145/3382734.3405731`. Уточняет понятие non-equivocation и границы fault assumptions; соседняя теория, не finite-clone testing theorem. |
| S17 | Prince Mahajan, Lorenzo Alvisi, Mike Dahlin. *Consistency, Availability, and Convergence* | Технический отчёт UTCS TR-11-22, 2011 | Соседний prior art: Byzantine inconsistencies представлены через forked или virtual views. Не рецензирован как основная статья по Twins; угрожает claims о самой идее виртуальных копий и fork counting. |
| S18 | Martín Abadi, Leslie Lamport. *The Existence of Refinement Mappings* | Рецензированная теоретическая статья, TCS 1991 | DOI `10.1016/0304-3975(91)90224-P`. Соседняя дисциплина: refinement и implementation mapping. Требует доказать соответствие abstract equivocation и concrete harness как refinement, а не только сравнить outputs. |
| S19 | Sebastião Amaro, Pedro Fonseca, Miguel Matos. *Rose: Reproducing External-Fault-Induced Failures in Distributed Systems with Lightweight Instrumentation* | Рецензированная статья EuroSys 2026 | DOI `10.1145/3767295.3803625`; открытый artifact DOI `10.5281/zenodo.18862553`, размер опубликованного архива 812.6 MB. Ближайший новый engineering prior art по воспроизведению fault-induced traces; не формализует Twins completeness. |
| S20 | Yu Liang, Yu Gao, Wensheng Dou, Wenhan Feng, Zheng Qin, Zhen Tang, Hui Li, Wen Wang, Jun Wei. *Node-Centric Systematic Testing for Distributed Systems* | Рецензированная статья ACM TOSEM 2026 | DOI `10.1145/3831368`; online publication 17 июля 2026 года. Официальные metadata и abstract доступны; полный текст через открытый источник не подтверждён. Работа вводит node-centric equivalence и NodeExplore, поэтому угрожает claims о новом behavior-preserving reduction, но не подтверждает finite-clone theorem. |
| S21 | `asonnino/twins-simulator` | Открытый research artifact | Apache-2.0; Streamlet и Fast-HotStuff; documented commands `pip install -e .`, `pytest`, `python scripts/twins_executor.py scripts/test_scenarios.json`. Research-only, 20 commits на дату проверки. Использовать только для внешней валидации. |
| S22 | `relab/hotstuff` | Открытый systems artifact | MIT; Go не ниже 1.18; включает Twins safety testing и три HotStuff variants. На дату проверки 1,849 commits. Использовать после абстрактного пилота, не как trusted reference semantics. |
| S23 | Python 3.14.7 | Официальный runtime | Выпуск 5 августа 2026 года. Основной язык explicit-state pilot; точная patch version фиксируется `.python-version` и environment report. |
| S24 | Hypothesis 6.165.3 | Официальный пакет PyPI | Выпущен 11 августа 2026 года; MPL-2.0; Python 3.10 и новее; source archive SHA-256 `687c5abb1a9c11478577c2cf18685c0eb82150d278477d3e14da290a1ef2a098`. Используется только для генеративных regression tests, не как научный oracle. |
| S25 | pytest 9.1.1 | Официальная документация | Выпущен 19 июня 2026 года. Используется для unit, metamorphic и regression tests. |
| S26 | uv | Официальная документация и репозиторий Astral | Лицензия Apache-2.0 OR MIT; поддерживает universal lockfile; проверенные команды `uv init`, `uv add`, `uv lock`, `uv sync`, `uv run`. Точная версия бинарника фиксируется в environment report. |
| S27 | Z3 5.0.0 | Официальный релиз GitHub | Выпущен 17 июля 2026 года; MIT. Резервный symbolic backend; не входит в минимальный пилот и подключается только при доказанной необходимости. |
| S28 | Nancy A. Lynch, Mark R. Tuttle. *An Introduction to Input/Output Automata* | Классическая работа по distributed-system semantics | CWI Quarterly 2(3), 1989. Определяет compositional state-machine view и external traces; соседняя основа для observation and simulation relation. |

## Ограничение поискового вывода

Фраза «источник не найден» означает только отсутствие результата в обследованных англоязычных научных базах, официальных репозиториях, citation searches и доступном инженерном prior art на 11 августа 2026 года. Она не доказывает абсолютного отсутствия работы, unpublished result, dissertation lemma, private engineering note или новой публикации после даты поиска.
