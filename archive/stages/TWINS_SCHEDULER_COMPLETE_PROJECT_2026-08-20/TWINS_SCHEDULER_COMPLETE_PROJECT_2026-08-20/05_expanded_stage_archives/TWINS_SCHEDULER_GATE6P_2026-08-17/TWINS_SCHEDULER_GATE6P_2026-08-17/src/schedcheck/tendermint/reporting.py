from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

from schedcheck.tendermint.cases import CASES, ExperimentCase, case_by_id
from schedcheck.tendermint.explorer import (
    PolicyMemory,
    _apply_delivery_sequence,
    _message_allowed_by_memory,
    explore_case,
    replay_witness,
)
from schedcheck.tendermint.kernel import complete_stage, emit_stage, finish_view, initial_runtime
from schedcheck.tendermint.model import (
    Grammar,
    HONEST_NODES,
    KernelState,
    KernelWitness,
    VARIANTS,
    Variant,
    VariantName,
    ViewTrace,
)
from schedcheck.tendermint.oracle import verify_witness

GRAMMARS: tuple[Grammar, ...] = tuple(Grammar)
_TOKEN_EDGE = re.compile(r":(?P<sender>[^-:]+)->(?P<receiver>[^:]+):")


def _observation_id(observation: tuple[int | None, ...]) -> str:
    return "|".join(
        f"{node}={'-' if value is None else value}"
        for node, value in zip(HONEST_NODES, observation, strict=True)
    )


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _minimal_unsafe(result: Any) -> KernelWitness | None:
    candidates = [result.witnesses[o] for o in result.unsafe_observations]
    return min(candidates, key=lambda witness: witness.rank()) if candidates else None


def _edge_masks(view: ViewTrace) -> tuple[int, int]:
    outbound = 0
    inbound = 0
    for stage in view.stages:
        for token in stage.delivered + stage.deferred:
            match = _TOKEN_EDGE.search(token)
            if match is None:
                raise AssertionError(f"cannot parse edge: {token}")
            sender, receiver = match.group("sender"), match.group("receiver")
            if sender == view.leader:
                node, direction = receiver, "out"
            elif receiver == view.leader:
                node, direction = sender, "in"
            else:
                raise AssertionError(f"non-star message: {token}")
            bit = 1 << HONEST_NODES.index(node)
            if direction == "out":
                outbound |= bit
            else:
                inbound |= bit
    return outbound, inbound


def simulate_type_erasure(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> tuple[KernelState, list[str]]:
    """Erase message kinds to one directed endpoint graph per round."""
    plans = {plan.view: plan for plan in case.plans}
    state = KernelState()
    policies: list[str] = []
    for view_trace in witness.views:
        plan = plans[view_trace.view]
        outbound, inbound = _edge_masks(view_trace)
        memory = PolicyMemory(outbound_mask=outbound, inbound_mask=inbound)
        policies.append(memory.descriptor(Grammar.DIRECTED, plan.leader))
        runtime = initial_runtime(state)
        for stage in range(5):
            messages = emit_stage(runtime, plan, stage, variant)
            delivered = tuple(
                message
                for message in sorted(messages, key=lambda item: item.uid)
                if _message_allowed_by_memory(
                    message, Grammar.DIRECTED, plan.leader, memory
                )
            )
            runtime = _apply_delivery_sequence(runtime, delivered, plan, variant)
            runtime = complete_stage(runtime, stage, variant)
        state = finish_view(runtime)
    return state, policies


def simulate_replay_erasure(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> tuple[KernelState, list[str]]:
    """Collapse duplicate instances and respect resulting causal unavailability."""
    plans = {plan.view: plan for plan in case.plans}
    state = KernelState()
    unavailable: list[str] = []
    for view_trace in witness.views:
        plan = plans[view_trace.view]
        runtime = initial_runtime(state)
        for stage_trace in view_trace.stages:
            messages = emit_stage(runtime, plan, stage_trace.stage, variant)
            by_token = {message.token(): message for message in messages}
            requested = tuple(dict.fromkeys(stage_trace.delivered))
            delivered = []
            for token in requested:
                message = by_token.get(token)
                if message is None:
                    unavailable.append(token)
                else:
                    delivered.append(message)
            runtime = _apply_delivery_sequence(runtime, tuple(delivered), plan, variant)
            runtime = complete_stage(runtime, stage_trace.stage, variant)
        state = finish_view(runtime)
    return state, unavailable


def run(output: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    results: dict[tuple[str, VariantName, Grammar], Any] = {}
    log: list[str] = []

    for case in CASES:
        for variant_name in (VariantName.BASELINE, case.variant):
            for grammar in GRAMMARS:
                result = explore_case(case, VARIANTS[variant_name], grammar)
                results[(case.case_id, variant_name, grammar)] = result
                log.append(
                    ",".join(
                        (
                            case.case_id,
                            variant_name.value,
                            grammar.value,
                            f"states={len(result.states)}",
                            f"observations={len(result.observations)}",
                            f"unsafe={len(result.unsafe_observations)}",
                        )
                    )
                )

    matrix_rows: list[dict[str, Any]] = []
    witness_rows: list[dict[str, Any]] = []
    for case in CASES:
        for role, variant_name in (("baseline", VariantName.BASELINE), ("mutant", case.variant)):
            for grammar in GRAMMARS:
                result = results[(case.case_id, variant_name, grammar)]
                witness = _minimal_unsafe(result)
                matrix_rows.append(
                    {
                        "case_id": case.case_id,
                        "role": role,
                        "variant": variant_name.value,
                        "grammar": grammar.value,
                        "states": len(result.states),
                        "observations": len(result.observations),
                        "unsafe_observations": len(result.unsafe_observations),
                        "unsafe_ids": ";".join(
                            sorted(_observation_id(o) for o in result.unsafe_observations)
                        ),
                        "minimal_unsafe_deliveries": "" if witness is None else witness.delivered_count,
                        "symbolic_nodes": result.stats.symbolic_nodes,
                        "delivery_choices": result.stats.delivery_choices,
                    }
                )
                if witness is not None:
                    replayed = replay_witness(case, VARIANTS[variant_name], witness)
                    oracle = verify_witness(case, VARIANTS[variant_name], witness)
                    row = witness.as_dict()
                    row.update(
                        {
                            "replay_status": "PASS" if replayed.observation() == witness.observation else "FAIL",
                            "independent_oracle_status": "PASS" if oracle == witness.observation else "FAIL",
                        }
                    )
                    witness_rows.append(row)

    _write_csv(
        output / "tendermint_language_matrix.csv",
        [
            "case_id", "role", "variant", "grammar", "states", "observations",
            "unsafe_observations", "unsafe_ids", "minimal_unsafe_deliveries",
            "symbolic_nodes", "delivery_choices",
        ],
        matrix_rows,
    )
    with (output / "tendermint_witnesses.jsonl").open("w", encoding="utf-8") as handle:
        for row in sorted(witness_rows, key=lambda x: (x["case_id"], x["grammar"], x["observation"])):
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    comparisons = (
        (Grammar.PARTITION, Grammar.DIRECTED, "directionality"),
        (Grammar.DIRECTED, Grammar.DIRECTED_DELAY1, "one-round terminal delay"),
        (Grammar.DIRECTED, Grammar.TYPE_SPECIFIC, "phase separation"),
        (Grammar.TYPE_SPECIFIC, Grammar.PER_MESSAGE, "message-instance choice"),
        (Grammar.PER_MESSAGE, Grammar.PER_MESSAGE_REPLAY1, "bounded replay"),
    )
    separation_rows: list[dict[str, Any]] = []
    for case in CASES:
        for weaker, stronger, capability in comparisons:
            left = results[(case.case_id, case.variant, weaker)]
            right = results[(case.case_id, case.variant, stronger)]
            new = right.unsafe_observations - left.unsafe_observations
            separation_rows.append(
                {
                    "case_id": case.case_id,
                    "variant": case.variant.value,
                    "weaker": weaker.value,
                    "stronger": stronger.value,
                    "capability": capability,
                    "weaker_unsafe": len(left.unsafe_observations),
                    "stronger_unsafe": len(right.unsafe_observations),
                    "new_unsafe": len(new),
                    "new_unsafe_ids": ";".join(sorted(_observation_id(o) for o in new)),
                    "strict_safety_separation": str(bool(new)).lower(),
                }
            )
    _write_csv(
        output / "tendermint_separations.csv",
        [
            "case_id", "variant", "weaker", "stronger", "capability",
            "weaker_unsafe", "stronger_unsafe", "new_unsafe", "new_unsafe_ids",
            "strict_safety_separation",
        ],
        separation_rows,
    )

    baseline_safe = all(
        not results[(case.case_id, VariantName.BASELINE, grammar)].unsafe_observations
        for case in CASES
        for grammar in GRAMMARS
    )

    closure_checks: list[dict[str, Any]] = []
    for case_id, variant_name in (
        ("TM_LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("TM_VALID_ROUND_GUARD", VariantName.WRONG_VALID_ROUND_GUARD),
    ):
        case = case_by_id(case_id)
        variant = VARIANTS[variant_name]
        source = results[(case_id, variant_name, Grammar.TYPE_SPECIFIC)]
        witness = _minimal_unsafe(source)
        assert witness is not None
        closed_state, policies = simulate_type_erasure(case, variant, witness)
        closure_checks.append(
            {
                "case_id": case_id,
                "closure": "erase_phase_labels_to_directed_round_graph",
                "source_observation": witness.observation_id(),
                "closed_observation": closed_state.observation_id(),
                "source_unsafe": True,
                "closed_unsafe": closed_state.unsafe(),
                "mechanism_confirmed": not closed_state.unsafe(),
                "closed_policies": policies,
            }
        )

        delayed = results[(case_id, variant_name, Grammar.DIRECTED_DELAY1)]
        delayed_witness = _minimal_unsafe(delayed)
        assert delayed_witness is not None
        immediate_state, policies = simulate_type_erasure(case, variant, delayed_witness)
        closure_checks.append(
            {
                "case_id": case_id,
                "closure": "erase_terminal_delay_by_immediate_delivery",
                "source_observation": delayed_witness.observation_id(),
                "closed_observation": immediate_state.observation_id(),
                "source_unsafe": True,
                "closed_unsafe": immediate_state.unsafe(),
                "mechanism_confirmed": not immediate_state.unsafe(),
                "closed_policies": policies,
            }
        )

    duplicate_case = case_by_id("TM_DUPLICATE_REPLAY")
    duplicate_variant = VARIANTS[VariantName.DUPLICATE_VOTE_COUNTING]
    replay_result = results[(
        duplicate_case.case_id,
        duplicate_case.variant,
        Grammar.PER_MESSAGE_REPLAY1,
    )]
    replay_w = _minimal_unsafe(replay_result)
    assert replay_w is not None
    dedup_state, unavailable = simulate_replay_erasure(
        duplicate_case, duplicate_variant, replay_w
    )
    closure_checks.append(
        {
            "case_id": duplicate_case.case_id,
            "closure": "deduplicate_logical_votes",
            "source_observation": replay_w.observation_id(),
            "closed_observation": dedup_state.observation_id(),
            "source_unsafe": True,
            "closed_unsafe": dedup_state.unsafe(),
            "mechanism_confirmed": not dedup_state.unsafe(),
            "causally_unavailable_after_deduplication": unavailable,
        }
    )
    (output / "tendermint_closure_counterfactuals.json").write_text(
        json.dumps(closure_checks, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    def unsafe(case_id: str, variant: VariantName, grammar: Grammar) -> int:
        return len(results[(case_id, variant, grammar)].unsafe_observations)

    checks = {
        "tendermint_baseline_safe_in_all_bounded_grammars": baseline_safe,
        "grammar_lattice_inclusions_hold": all(
            results[(case.case_id, variant, weaker)].observations
            <= results[(case.case_id, variant, stronger)].observations
            for case in CASES
            for variant in (VariantName.BASELINE, case.variant)
            for weaker, stronger in (
                (Grammar.PARTITION, Grammar.DIRECTED),
                (Grammar.DIRECTED, Grammar.TYPE_SPECIFIC),
                (Grammar.TYPE_SPECIFIC, Grammar.PER_MESSAGE),
                (Grammar.PER_MESSAGE, Grammar.PER_MESSAGE_REPLAY1),
            )
        ),
        "directed_embeds_in_terminal_delay": all(
            results[(case.case_id, variant, Grammar.DIRECTED)].observations
            <= results[(case.case_id, variant, Grammar.DIRECTED_DELAY1)].observations
            for case in CASES
            for variant in (VariantName.BASELINE, case.variant)
        ),
        "lock_omission_phase_separation": (
            unsafe("TM_LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.DIRECTED) == 0
            and unsafe("TM_LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.TYPE_SPECIFIC) > 0
        ),
        "valid_round_guard_phase_separation": (
            unsafe("TM_VALID_ROUND_GUARD", VariantName.WRONG_VALID_ROUND_GUARD, Grammar.DIRECTED) == 0
            and unsafe("TM_VALID_ROUND_GUARD", VariantName.WRONG_VALID_ROUND_GUARD, Grammar.TYPE_SPECIFIC) > 0
        ),
        "bounded_terminal_delay_exposes_both_phase_coupled_mutants": (
            unsafe("TM_LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.DIRECTED_DELAY1) > 0
            and unsafe("TM_VALID_ROUND_GUARD", VariantName.WRONG_VALID_ROUND_GUARD, Grammar.DIRECTED_DELAY1) > 0
        ),
        "replay_is_required_for_non_idempotent_vote_counting": (
            unsafe("TM_DUPLICATE_REPLAY", VariantName.DUPLICATE_VOTE_COUNTING, Grammar.PER_MESSAGE) == 0
            and unsafe("TM_DUPLICATE_REPLAY", VariantName.DUPLICATE_VOTE_COUNTING, Grammar.PER_MESSAGE_REPLAY1) > 0
        ),
        "partition_positive_control": unsafe(
            "TM_VALIDATION_CONTROL",
            VariantName.RECEIVER_VALIDATION_OMISSION,
            Grammar.PARTITION,
        ) > 0,
        "selected_closures_destroy_witnesses": all(
            check["mechanism_confirmed"] for check in closure_checks
        ),
        "all_serialized_witnesses_pass_independent_oracle": all(
            row["independent_oracle_status"] == "PASS" for row in witness_rows
        ),
    }
    (output / "tendermint_theorem_checks.json").write_text(
        json.dumps(checks, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output / "tendermint_run_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "results": results,
        "witnesses": witness_rows,
        "closure_checks": closure_checks,
    }
