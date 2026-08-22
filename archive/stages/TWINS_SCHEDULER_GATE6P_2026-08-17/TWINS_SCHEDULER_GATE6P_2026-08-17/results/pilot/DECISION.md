# Gate 0′–3′ decision

**Overall status:** ТРЕБУЕТ СУЖЕНИЯ

The unrestricted partition-normal-form completeness hypothesis is falsified in the declared finite deterministic protocol class. The exact pilot establishes a strict safety-observation hierarchy:

`G_P_PARTITION ⊊ G_D_DIRECTED_VIEW ⊊ G_T_TYPE_SPECIFIC ⊊ G_M_PER_MESSAGE`.

This is a GO only for the narrowed closure-preservation research question. It is not evidence of a production HotStuff vulnerability and not a license to build a large new testing framework before protocol-class validation.

## Gate statuses

- **gate_0_prime: CONDITIONAL_PASS** — The implementation-specific partition restriction is real and richer schedulers are known; novelty survives only as a property-preserving characterization for a natural protocol class, not as a richer fault-injection API.
- **gate_1_prime: PASS** — Four scheduler grammars, safety observations, embeddings, counterexamples, and explicit abstraction limits are formalized.
- **gate_2_prime: PASS** — The exact checker is standard-library-only, locally reproducible, source-pinned, and does not require a blockchain node, solver, network service, or dataset.
- **gate_3_prime: PASS_GO_WITH_NARROWING** — Every adjacent grammar inclusion is strict on safety observations, and each least natural closure destroys its designated witness.

## Next admissible claim

Necessary and sufficient (or sharply sufficient plus separation) closure-preservation conditions under which view-partition schedules preserve all safety-violating observations of richer message schedulers for a natural class of view-based BFT protocol implementations.

## Next gate

Gate 4': instantiate one correct locking protocol plus seeded implementation mutants, check actual executor conformance, and seek a protocol-class closure theorem or a natural minimal separation.
