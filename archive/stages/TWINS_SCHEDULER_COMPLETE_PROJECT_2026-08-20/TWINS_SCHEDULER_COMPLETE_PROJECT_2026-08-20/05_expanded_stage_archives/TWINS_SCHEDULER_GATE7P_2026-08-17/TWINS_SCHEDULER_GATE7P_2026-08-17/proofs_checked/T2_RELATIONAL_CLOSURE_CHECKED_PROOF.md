# T2 — Relational closure lifting

## Statement

Let `τ` be a finite original execution ending in an unsafe state. Let `C(τ)` be
a trace obtained by inserting closure-added actions while preserving the order
of all original actions. Let `R` be a preorder over protocol-relevant states.
Assume:

1. initial original and closed states are `R`-related;
2. every closure-added action is `R`-increasing;
3. every original action forward-simulates `R`;
4. `Unsafe` is upward closed under `R`.

Then the terminal state of `C(τ)` is unsafe.

If `R` additionally preserves the complete selected observation, closure
preserves that observation, not merely unsafety.

## Checked induction

Traverse the merged trace and relate:

- the state after the original actions consumed so far; and
- the state after the corresponding merged prefix.

The measure is the length of the remaining merged suffix.

### Base case

The empty prefixes denote the same initial state; reflexivity establishes the
relation.

### Added-action case

The original side does not advance. The closed side executes an inserted action.
By the `R`-increasing premise and transitivity, the prefix relation is
preserved.

### Original-action case

Both sides execute the same original action. Forward simulation preserves the
relation.

The two cases exhaust each merged event and the suffix measure decreases.
At the terminal prefix, the original unsafe state is `R`-related to the closed
terminal state. Upward closure of `Unsafe` yields the theorem.

## Why this theorem does not trivialize the paper

Certificate-driven locking protocols may fail the premises. Closure can add a
repair or terminal message that removes the only honest validator capable of
participating in a later conflicting quorum. Such a message is not increasing
for any relation that preserves the relevant future actions. The Gate 4′–6′
separation is exactly a failed-premise boundary of T2.

## Machine-readable assets

- `t2_rules.json`;
- `t2_closure_lifting_certificate.json`;
- `results/gate6p/t2_closure_lifting_proof_check.json`.
