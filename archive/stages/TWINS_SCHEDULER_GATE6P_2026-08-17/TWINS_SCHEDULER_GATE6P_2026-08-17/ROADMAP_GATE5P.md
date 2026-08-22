# Roadmap Gate 5′ — formal characterization and cross-protocol validation

## Entry condition

Gate 4′ is closed with bounded natural separations. Entry to Gate 5′ is permitted
only because the correct baseline is safe, the selected witnesses survive an
independent oracle, counterfactual closures isolate the mechanism, and pinned
network semantics pass executable conformance.

## Gate 5′ decision question

Can the bounded observations be stated as a reusable theorem, separation
condition, or impossibility result independent of the five named mutants?

## Work packages

### WP5.0 — novelty refresh

**Effort:** 1–2 focused person-days  
**Tasks:** search message-adversary normal forms, communication closure,
refinement/conformance, fault-model expressiveness, phase-specific omission, and
idempotent quorum processing.  
**Output:** `gate5p/prior_art_delta.md`.  
**GO:** no source already gives the same closure/separation characterization.  
**NO-GO:** closest work contains the same property and proof.

### WP5.1 — abstract protocol class

**Effort:** 2–4 days  
**Tasks:** define certificate-driven view protocol, phase-labelled messages,
state constraints established by evidence, repair/terminal messages, and safety
observation.  
**Output:** `spec/protocol_class.md`.  
**GO:** conditions can be checked without mentioning a particular mutant.  
**PIVOT:** conditions are circular or equivalent to assuming the conclusion.

### WP5.2 — closure-preservation theorem or counterexample

**Effort:** 3–6 days  
**Tasks:** formalize `C_type`, `C_time`, and `C_dup`; attempt sufficient theorem
for closure preservation; search minimal counterexample when monotonicity fails.  
**Output:** proof manuscript plus executable checks.  
**GO:** at least one non-definitional theorem/separation result.  
**NO-GO:** only case-by-case enumeration remains.

### WP5.3 — second natural protocol kernel

**Effort:** 3–5 days  
**Primary choice:** a Tendermint-style prevote/precommit locking kernel with
valid-round justification.  
**Reserve:** a chained three-phase HotStuff core.  
**Output:** separate state machine and cross-protocol result matrix.  
**GO:** theorem conditions or a natural separation transfer.  
**NO-GO:** all effects rely on the first kernel's artificial staging.

### WP5.4 — implementation-level correspondence

**Effort:** 4–7 days  
**Tasks:** select one safe local mutation in an open implementation or a faithful
executable model; map implementation events to abstract phases; compare the
actual scenario language with the abstract scheduler.  
**Output:** conformance/refinement table and controlled local witness.  
**Safety:** local execution only; no public network.  
**GO:** abstract preconditions are observable in executable code.  
**PIVOT:** implementation mapping requires changing the scientific claim.

### WP5.5 — publication kill test

**Effort:** 1–2 days  
**Tasks:** write three contribution bullets, strongest Reviewer 2 objection,
negative-result statement, and novelty claim limited by searched sources.  
**Output:** `gate5p/PUBLICATION_DECISION.md`.  
**GO:** contribution is theorem/bound/separation plus artifact.  
**NO-GO:** contribution is only a scheduler DSL or a mutant benchmark.

## Critical path

```text
WP5.0 → WP5.1 → WP5.2 → WP5.3 → WP5.5
                         ↘ WP5.4 ↗
```

Estimated critical-path effort: **10–19 focused person-days**. WP5.4 may run in
parallel after the abstract class is stable.

## First fifteen tasks

| # | Action | Acceptance artifact | Size | Parallel |
|---:|---|---|:---:|:---:|
| 1 | Freeze Gate 4′ theorem-check JSON and hashes | immutable manifest | S | no |
| 2 | Define type-uniform closure on labelled view traces | formal definition + examples | M | no |
| 3 | Define safety-monotone additional-message relation | non-circular definition | M | no |
| 4 | Search exact closure terminology in adjacent literature | source matrix | M | yes with 2–3 |
| 5 | Prove standard grammar embeddings at trace level | lemma draft | S | yes |
| 6 | Generalize lock-omission witness symbolically | parametric trace | M | no |
| 7 | Generalize QC-guard witness symbolically | parametric trace | M | yes with 6 |
| 8 | State inbound-phase exception from timeout case | lemma/counterexample | M | yes |
| 9 | Prove replay/idempotence lemma | proof + tests | M | yes |
| 10 | Specify Tendermint-style second kernel | executable spec | L | after 2–3 |
| 11 | Re-run six grammars on second kernel | result matrix | M | after 10 |
| 12 | Minimize cross-protocol witnesses | JSONL + diagrams | M | after 11 |
| 13 | Map pinned Go network rules to abstract grammar | refinement table | M | after 2 |
| 14 | Implement one controlled implementation mutation | local test only | L | after 13 |
| 15 | Run publication kill test | GO/NO-GO memo | M | after 4, 9, 11 |

## First three work sessions

### Session 1

Write `C_type`, `C_time`, and `C_dup` as relations over labelled traces and
translate the three Gate 4′ counterfactuals into symbolic obligations.

### Session 2

Attempt the replay/idempotence lemma and a sufficient closure-preservation lemma.
Record the first counterexample rather than strengthening assumptions silently.

### Session 3

Implement the smallest Tendermint-style kernel that distinguishes proposal
valid-round evidence, prevote, precommit, lock update, and decision. Run only the
correct baseline and one phase-coupled mutant initially.

## Final decision rule

Gate 5′ passes only with at least one reusable formal result and one independent
protocol instantiation. More mutants, more schedules, higher coverage, or a new
DSL do not satisfy the gate.
