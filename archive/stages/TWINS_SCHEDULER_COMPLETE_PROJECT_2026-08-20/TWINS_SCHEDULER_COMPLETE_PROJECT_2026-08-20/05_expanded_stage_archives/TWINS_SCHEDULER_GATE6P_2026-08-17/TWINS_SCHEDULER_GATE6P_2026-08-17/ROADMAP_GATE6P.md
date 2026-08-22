# Roadmap — Gate 6′: proof hardening and implementation-level validation

## Gate objective

Convert the Gate 5′ analytical results and extracted source correspondence into
submission-grade evidence without widening the scientific claim.

## Work packages

### WP6.1 Mechanize T1 and T2 — 2–4 focused person-days

- encode stable logical keys, replay erasure, relation `R`, closure insertion,
  and unsafe upward closure in Lean, Isabelle, TLA+/TLAPS, or another selected
  proof environment;
- prove replay erasure by induction;
- prove relational closure lifting by induction over inserted actions.

**Acceptance:** checked proof or a small trusted proof script; no admitted
lemmas.

### WP6.2 Harden T3 — 3–6 days

- formalize the `n=3f+1`, `q=2f+1` quorum construction symbolically;
- separate the protocol schema premises from the witness construction;
- prove the directed impossibility and phase-specific reachability branches;
- prove the bounded-delay corollary separately.

**Acceptance:** machine-checked theorem or publication-grade proof reviewed
against the executable family `f=1…8`.

### WP6.3 Fuller event-loop mutation — 4–8 days

- choose one controlled mutation: missing lock update or duplicate instance
  counting;
- inject it only into a local fork or isolated test fixture;
- replay the minimal witness through a fuller consensus event loop;
- keep all experiments local; never target public networks.

**Acceptance:** baseline rejects the witness, controlled mutation accepts it,
and the result is replayable from a pinned commit and deterministic scenario.

### WP6.4 Third-instance or necessity check — 2–5 days

- either instantiate the phase-coupled schema in a third small protocol model,
  or prove that one existing premise is necessary via a minimal countermodel;
- avoid adding a large mutant catalogue.

**Acceptance:** one new theorem-relevant boundary, not merely more test cases.

### WP6.5 Artifact hardening — 2–4 days

- container or lockfile pinning;
- one-command reproduction;
- independent clean extraction check;
- machine-readable theorem ledger;
- automated figures/tables;
- complete source and license manifest.

### WP6.6 Paper skeleton — 3–5 days

- introduction centered on property-preserving scheduler closure;
- related work separating message adversaries, communication closure, testing
  DSLs, Twins, and mutation frameworks;
- theorem statements before systems results;
- limitations and non-claims explicit.

## Go/no-go rules

**GO to full paper:** T3 survives proof hardening and at least one fuller-loop
controlled mutation reproduces the predicted grammar boundary.

**PIVOT:** the proof requires a narrower protocol schema but remains non-vacuous
and the same boundary survives in both exact kernels.

**NO-GO:** T3 is found to be circular, the fuller-loop experiment contradicts
the mechanism, or a prior work is found with the same closure/separation result.

## Critical path

`T3 formalization → fuller event-loop mutation → independent reproduction →
paper claim freeze`.
