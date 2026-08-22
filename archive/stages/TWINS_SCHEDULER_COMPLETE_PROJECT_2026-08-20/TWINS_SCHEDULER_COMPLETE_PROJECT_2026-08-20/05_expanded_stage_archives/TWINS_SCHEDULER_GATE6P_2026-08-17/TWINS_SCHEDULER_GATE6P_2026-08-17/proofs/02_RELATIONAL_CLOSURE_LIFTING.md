# Relational closure-lifting theorem

## Purpose

A stronger scheduler can omit a phase-labelled message that a coarser scheduler
must deliver after phase labels are erased. Closing a trace therefore inserts
additional deliveries. This theorem gives a local sufficient condition under
which those insertions cannot repair an unsafe execution.

## Definitions

Let `S` be a state space, `A` the actions retained from an original trace, `C`
the closure-added actions, `δ` a deterministic transition function, `U⊆S` an
unsafe set, and `R⊆S×S` a relation.

The local obligations are:

1. **Closure growth:** for every reachable `s` and `c∈C`,
   `R(s, δ(s,c))`.
2. **Forward simulation of retained actions:** if `R(s,t)`, then for every
   retained action `a∈A`, `R(δ(s,a), δ(t,a))`.
3. **Upward closure of unsafety:** if `R(s,t)` and `s∈U`, then `t∈U`.

A closed trace is obtained by inserting any finite number of actions from `C`
while preserving the order of retained actions.

## Theorem T2

Under obligations 1–3, every closed trace ending unsafe whenever its retained
projection ends unsafe.

## Proof

Couple the retained execution and the closed execution. Initially the states are
identical, so they are related. Every inserted closure action preserves the
relation by closure growth. Every shared retained action preserves it by
forward simulation. Induction over the closed trace therefore relates the final
retained state to the final closed state. Upward closure of `U` transfers
unsafety. ∎

## Strong equality special case

If `R` is an observation-preserving bisimulation and every closure action is
stuttering modulo `R`, then closure preserves the complete observation, not only
unsafety. Gate 5′ does not assume this stronger condition.

## Why locking implementations violate the premise

A repair or terminal message can make an honest quorum-intersection pivot
unavailable for a later conflicting certificate. Such a message is not
`R`-increasing for a relation that preserves future safety-relevant actions.
The executable counterexample uses:

```text
original: E0, D0, E1, D1       -> decisions {0,1}
closed:   E0, R0, D0, E1, D1   -> decision {0}
```

`R0` both records the first decision and disables the pivot's later conflicting
action. Thus the theorem explains exactly why type erasure is safe for monotone
message accumulation but can repair a defective locking trace.

## Executable evidence

`results/gate5p/closure_theorem_checks.json` contains:

- a finite monotone system satisfying all local premises and preserving
  unsafety after insertion;
- a finite locking-fragility system where the closure-growth premise fails and
  the inserted repair action destroys the unsafe observation.

## Scope

T2 is sufficient, not necessary. Failure of a premise does not imply that every
trace changes under closure; it identifies where a protocol-specific proof or
counterexample is required.
