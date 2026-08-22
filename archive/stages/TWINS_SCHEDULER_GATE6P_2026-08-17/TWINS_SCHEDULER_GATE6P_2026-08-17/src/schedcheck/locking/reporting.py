from __future__ import annotations

import csv
from dataclasses import replace
import hashlib
import json
import platform
import re
import sys
from pathlib import Path
from typing import Any

from schedcheck.locking.cases import CASES, ExperimentCase, case_by_id
from schedcheck.locking.explorer import (
    PolicyMemory,
    _apply_delivery_sequence,
    _message_allowed_by_memory,
    explore_case,
    replay_witness,
)
from schedcheck.locking.kernel import complete_stage, emit_stage, finish_view, initial_runtime
from schedcheck.locking.model import (
    Grammar,
    HONEST_NODES,
    KernelState,
    KernelWitness,
    StageDelivery,
    VARIANTS,
    Variant,
    VariantName,
    ViewTrace,
)
from schedcheck.locking.oracle import verify_witness

GRAMMARS: tuple[Grammar, ...] = (
    Grammar.PARTITION,
    Grammar.DIRECTED,
    Grammar.DIRECTED_DELAY1,
    Grammar.TYPE_SPECIFIC,
    Grammar.PER_MESSAGE,
    Grammar.PER_MESSAGE_REPLAY1,
)

_TOKEN_EDGE = re.compile(r":(?P<sender>[^-:]+)->(?P<receiver>[^:]+):")


def _observation_id(observation: tuple[int | None, ...]) -> str:
    return "|".join(
        f"{node}={'-' if value is None else value}"
        for node, value in zip(HONEST_NODES, observation, strict=True)
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _minimal_unsafe_witness(result: Any) -> KernelWitness | None:
    candidates = [
        result.witnesses[observation] for observation in result.unsafe_observations
    ]
    return min(candidates, key=lambda witness: witness.rank()) if candidates else None


def _edge_masks(view: ViewTrace) -> tuple[int, int]:
    outbound = 0
    inbound = 0
    for stage in view.stages:
        for token in stage.delivered + stage.deferred:
            match = _TOKEN_EDGE.search(token)
            if match is None:
                raise AssertionError(f"cannot parse witness edge: {token}")
            sender = match.group("sender")
            receiver = match.group("receiver")
            if sender == view.leader:
                node = receiver
                direction = "out"
            elif receiver == view.leader:
                node = sender
                direction = "in"
            else:
                raise AssertionError(f"non-star message in locking witness: {token}")
            bit = 1 << HONEST_NODES.index(node)
            if direction == "out":
                outbound |= bit
            else:
                inbound |= bit
    return outbound, inbound


def _simulate_directed_type_erasure(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> tuple[KernelState, list[str]]:
    """Close a type-specific witness to one directed graph per view."""
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


def _erase_delay(witness: KernelWitness) -> KernelWitness:
    """Deliver every deferred terminal certificate immediately."""
    views: list[ViewTrace] = []
    for view in witness.views:
        stages = tuple(
            replace(
                stage,
                delivered=stage.delivered + stage.deferred,
                deferred=(),
            )
            for stage in view.stages
        )
        views.append(replace(view, stages=stages, late_delivered=()))
    return replace(witness, grammar=Grammar.DIRECTED, views=tuple(views))


def _erase_replay(witness: KernelWitness) -> KernelWitness:
    views: list[ViewTrace] = []
    for view in witness.views:
        stages: list[StageDelivery] = []
        for stage in view.stages:
            delivered = tuple(dict.fromkeys(stage.delivered))
            stages.append(replace(stage, delivered=delivered))
        views.append(replace(view, stages=tuple(stages)))
    return replace(witness, grammar=Grammar.PER_MESSAGE, views=tuple(views))


def _simulate_replay_erasure(
    case: ExperimentCase,
    variant: Variant,
    witness: KernelWitness,
) -> tuple[KernelState, list[str]]:
    """Replay the same schedule after collapsing repeated message instances.

    Later certificates that depended on the duplicate-counting bug may no longer
    be emitted. Such tokens are recorded as causally unavailable rather than
    force-injected, which is the intended counterfactual.
    """
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
            runtime = _apply_delivery_sequence(
                runtime, tuple(delivered), plan, variant
            )
            runtime = complete_stage(runtime, stage_trace.stage, variant)
        state = finish_view(runtime)
    return state, unavailable


def run(root: Path, output: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    results: dict[tuple[str, VariantName, Grammar], Any] = {}
    log_lines: list[str] = []

    for case in CASES:
        for variant_name in (VariantName.BASELINE, case.variant):
            variant = VARIANTS[variant_name]
            for grammar in GRAMMARS:
                result = explore_case(case, variant, grammar)
                results[(case.case_id, variant_name, grammar)] = result
                log_lines.append(
                    ",".join(
                        (
                            case.case_id,
                            variant_name.value,
                            grammar.value,
                            f"states={len(result.states)}",
                            f"observations={len(result.observations)}",
                            f"unsafe={len(result.unsafe_observations)}",
                            f"symbolic_nodes={result.stats.symbolic_nodes}",
                        )
                    )
                )

    matrix_rows: list[dict[str, Any]] = []
    witness_rows: list[dict[str, Any]] = []
    for case in CASES:
        for role, variant_name in (
            ("baseline", VariantName.BASELINE),
            ("mutant", case.variant),
        ):
            for grammar in GRAMMARS:
                result = results[(case.case_id, variant_name, grammar)]
                witness = _minimal_unsafe_witness(result)
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
                            sorted(_observation_id(item) for item in result.unsafe_observations)
                        ),
                        "minimal_unsafe_deliveries": (
                            witness.delivered_count if witness is not None else ""
                        ),
                        "view_calls": result.stats.view_calls,
                        "symbolic_nodes": result.stats.symbolic_nodes,
                        "delivery_choices": result.stats.delivery_choices,
                    }
                )
                if witness is not None:
                    replayed = replay_witness(case, VARIANTS[variant_name], witness)
                    oracle_observation = verify_witness(
                        case, VARIANTS[variant_name], witness
                    )
                    row = witness.as_dict()
                    row.update(
                        {
                            "replay_status": (
                                "PASS"
                                if replayed.observation() == witness.observation
                                else "FAIL"
                            ),
                            "independent_oracle_status": (
                                "PASS"
                                if oracle_observation == witness.observation
                                else "FAIL"
                            ),
                        }
                    )
                    witness_rows.append(row)

    _write_csv(
        output / "language_matrix.csv",
        [
            "case_id",
            "role",
            "variant",
            "grammar",
            "states",
            "observations",
            "unsafe_observations",
            "unsafe_ids",
            "minimal_unsafe_deliveries",
            "view_calls",
            "symbolic_nodes",
            "delivery_choices",
        ],
        matrix_rows,
    )
    with (output / "witnesses.jsonl").open("w", encoding="utf-8") as handle:
        for row in sorted(
            witness_rows,
            key=lambda item: (
                item["case_id"], item["variant"], item["grammar"], item["observation"]
            ),
        ):
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    comparison_specs = (
        (Grammar.PARTITION, Grammar.DIRECTED, "directionality"),
        (Grammar.DIRECTED, Grammar.DIRECTED_DELAY1, "one-view commit delay"),
        (Grammar.DIRECTED, Grammar.TYPE_SPECIFIC, "message-phase separation"),
        (Grammar.TYPE_SPECIFIC, Grammar.PER_MESSAGE, "message-instance choice"),
        (Grammar.PER_MESSAGE, Grammar.PER_MESSAGE_REPLAY1, "one bounded replay"),
    )
    separation_rows: list[dict[str, Any]] = []
    for case in CASES:
        variant_name = case.variant
        for weaker, stronger, capability in comparison_specs:
            left = results[(case.case_id, variant_name, weaker)]
            right = results[(case.case_id, variant_name, stronger)]
            new_unsafe = right.unsafe_observations - left.unsafe_observations
            separation_rows.append(
                {
                    "case_id": case.case_id,
                    "variant": variant_name.value,
                    "weaker": weaker.value,
                    "stronger": stronger.value,
                    "capability": capability,
                    "weaker_unsafe": len(left.unsafe_observations),
                    "stronger_unsafe": len(right.unsafe_observations),
                    "new_unsafe": len(new_unsafe),
                    "new_unsafe_ids": ";".join(
                        sorted(_observation_id(item) for item in new_unsafe)
                    ),
                    "strict_safety_separation": str(bool(new_unsafe)).lower(),
                }
            )
    _write_csv(
        output / "separations.csv",
        [
            "case_id",
            "variant",
            "weaker",
            "stronger",
            "capability",
            "weaker_unsafe",
            "stronger_unsafe",
            "new_unsafe",
            "new_unsafe_ids",
            "strict_safety_separation",
        ],
        separation_rows,
    )

    baseline_checks = {
        case.case_id: {
            grammar.value: not results[
                (case.case_id, VariantName.BASELINE, grammar)
            ].unsafe_observations
            for grammar in GRAMMARS
        }
        for case in CASES
    }
    baseline_pass = all(
        status
        for case_checks in baseline_checks.values()
        for status in case_checks.values()
    )
    (output / "baseline_checks.json").write_text(
        json.dumps(
            {"status": "PASS" if baseline_pass else "FAIL", "checks": baseline_checks},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    closure_checks: list[dict[str, Any]] = []
    for case_id, variant_name in (
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("QC_GUARD", VariantName.WRONG_QC_GUARD),
        ("TIMEOUT_CLASSIFICATION", VariantName.TIMEOUT_AS_PRECOMMIT),
    ):
        case = case_by_id(case_id)
        variant = VARIANTS[variant_name]
        typed = results[(case_id, variant_name, Grammar.TYPE_SPECIFIC)]
        typed_witness = _minimal_unsafe_witness(typed)
        assert typed_witness is not None
        closed_state, policies = _simulate_directed_type_erasure(
            case, variant, typed_witness
        )
        closure_checks.append(
            {
                "case_id": case_id,
                "closure": "erase_message_type_to_one_directed_graph_per_view",
                "source_observation": typed_witness.observation_id(),
                "closed_observation": closed_state.observation_id(),
                "source_unsafe": True,
                "closed_unsafe": closed_state.unsafe(),
                "mechanism_confirmed": not closed_state.unsafe(),
                "closed_policies": policies,
            }
        )

    for case_id, variant_name in (
        ("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE),
        ("QC_GUARD", VariantName.WRONG_QC_GUARD),
    ):
        case = case_by_id(case_id)
        variant = VARIANTS[variant_name]
        delayed = results[(case_id, variant_name, Grammar.DIRECTED_DELAY1)]
        delayed_witness = _minimal_unsafe_witness(delayed)
        assert delayed_witness is not None
        immediate_state, policies = _simulate_directed_type_erasure(
            case, variant, delayed_witness
        )
        closure_checks.append(
            {
                "case_id": case_id,
                "closure": "erase_one_view_delay_by_immediate_delivery",
                "source_observation": delayed_witness.observation_id(),
                "closed_observation": immediate_state.observation_id(),
                "source_unsafe": True,
                "closed_unsafe": immediate_state.unsafe(),
                "mechanism_confirmed": not immediate_state.unsafe(),
                "closed_policies": policies,
            }
        )

    duplicate_case = case_by_id("DUPLICATE_REPLAY")
    duplicate_variant = VARIANTS[VariantName.DUPLICATE_VOTE_COUNTING]
    replay_result = results[
        (
            "DUPLICATE_REPLAY",
            VariantName.DUPLICATE_VOTE_COUNTING,
            Grammar.PER_MESSAGE_REPLAY1,
        )
    ]
    replay_w = _minimal_unsafe_witness(replay_result)
    assert replay_w is not None
    deduplicated_state, unavailable = _simulate_replay_erasure(
        duplicate_case, duplicate_variant, replay_w
    )
    closure_checks.append(
        {
            "case_id": "DUPLICATE_REPLAY",
            "closure": "deduplicate_message_instances",
            "source_observation": replay_w.observation_id(),
            "closed_observation": deduplicated_state.observation_id(),
            "source_unsafe": True,
            "closed_unsafe": deduplicated_state.unsafe(),
            "mechanism_confirmed": not deduplicated_state.unsafe(),
            "causally_unavailable_after_deduplication": unavailable,
        }
    )
    (output / "closure_counterfactuals.json").write_text(
        json.dumps(closure_checks, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    def unsafe_count(case_id: str, variant_name: VariantName, grammar: Grammar) -> int:
        return len(results[(case_id, variant_name, grammar)].unsafe_observations)

    theorem_checks = {
        "baseline_safe_in_all_bounded_models": baseline_pass,
        "directed_embeds_in_directed_delay1": all(
            results[(case.case_id, variant_name, Grammar.DIRECTED)].observations
            <= results[(case.case_id, variant_name, Grammar.DIRECTED_DELAY1)].observations
            for case in CASES
            for variant_name in (VariantName.BASELINE, case.variant)
        ),
        "standard_lattice_inclusions_hold": all(
            results[(case.case_id, variant_name, weaker)].observations
            <= results[(case.case_id, variant_name, stronger)].observations
            for case in CASES
            for variant_name in (VariantName.BASELINE, case.variant)
            for weaker, stronger in (
                (Grammar.PARTITION, Grammar.DIRECTED),
                (Grammar.DIRECTED, Grammar.TYPE_SPECIFIC),
                (Grammar.TYPE_SPECIFIC, Grammar.PER_MESSAGE),
                (Grammar.PER_MESSAGE, Grammar.PER_MESSAGE_REPLAY1),
            )
        ),
        "lock_omission_requires_more_than_directed": (
            unsafe_count("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.DIRECTED) == 0
            and unsafe_count("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.TYPE_SPECIFIC) > 0
        ),
        "qc_guard_requires_more_than_directed": (
            unsafe_count("QC_GUARD", VariantName.WRONG_QC_GUARD, Grammar.DIRECTED) == 0
            and unsafe_count("QC_GUARD", VariantName.WRONG_QC_GUARD, Grammar.TYPE_SPECIFIC) > 0
        ),
        "timeout_requires_phase_specific_not_commit_delay_only": (
            unsafe_count("TIMEOUT_CLASSIFICATION", VariantName.TIMEOUT_AS_PRECOMMIT, Grammar.DIRECTED_DELAY1) == 0
            and unsafe_count("TIMEOUT_CLASSIFICATION", VariantName.TIMEOUT_AS_PRECOMMIT, Grammar.TYPE_SPECIFIC) > 0
        ),
        "bounded_commit_delay_exposes_lock_and_qc_mutants": (
            unsafe_count("LOCK_OMISSION", VariantName.MISSING_LOCK_UPDATE, Grammar.DIRECTED_DELAY1) > 0
            and unsafe_count("QC_GUARD", VariantName.WRONG_QC_GUARD, Grammar.DIRECTED_DELAY1) > 0
        ),
        "replay_required_for_duplicate_counting": (
            unsafe_count("DUPLICATE_REPLAY", VariantName.DUPLICATE_VOTE_COUNTING, Grammar.PER_MESSAGE) == 0
            and unsafe_count("DUPLICATE_REPLAY", VariantName.DUPLICATE_VOTE_COUNTING, Grammar.PER_MESSAGE_REPLAY1) > 0
        ),
        "partition_positive_control": unsafe_count(
            "VALIDATION_OMISSION_CONTROL",
            VariantName.RECEIVER_VALIDATION_OMISSION,
            Grammar.PARTITION,
        ) > 0,
        "all_counterfactual_closures_destroy_selected_witness": all(
            item["mechanism_confirmed"] for item in closure_checks
        ),
        "all_serialized_witnesses_pass_independent_oracle": all(
            item["independent_oracle_status"] == "PASS" for item in witness_rows
        ),
    }
    checks_pass = all(theorem_checks.values())
    (output / "theorem_checks.json").write_text(
        json.dumps(theorem_checks, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    conformance_path = output / "conformance_summary.json"
    conformance = (
        json.loads(conformance_path.read_text(encoding="utf-8"))
        if conformance_path.exists()
        else {"status": "NOT_RUN"}
    )
    conformance_pass = conformance.get("status") == "PASS"

    decision = {
        "gate": "Gate 4'",
        "date": "2026-08-15",
        "status": (
            "PASS / CONDITIONAL GO TO GATE 5'"
            if checks_pass and conformance_pass
            else "FAIL"
        ),
        "overall_research_status": "ТРЕБУЕТ СУЖЕНИЯ",
        "primary_result": (
            "Natural locking mutants exhibit safety-relevant scheduler separations: "
            "type/phase control exposes three mutants hidden from a type-uniform "
            "directed view graph; bounded late commit delivery exposes two of those; "
            "bounded replay is necessary for a duplicate-signer-counting mutant."
        ),
        "blocking_unknown": (
            "The bounded results are not yet a protocol-class theorem and are not "
            "evidence of a vulnerability in HotStuff or relab/hotstuff."
        ),
        "go_condition": (
            "Proceed only to a formal characterization and second natural protocol "
            "instantiation; do not build a general-purpose fuzzer yet."
        ),
        "no_go_condition": (
            "Stop if the separation cannot be stated independently of these mutants, "
            "or if a second protocol instance reduces it to a modeling artifact."
        ),
        "checks_pass": checks_pass,
        "conformance_pass": conformance_pass,
    }
    (output / "gate4p_decision.json").write_text(
        json.dumps(decision, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "pythonhashseed_required": "0",
        "runtime_dependencies": [],
        "source_commit": "3179c6e62929294961acbfd9bf8445769716a121",
        "network_go_sha256": _sha256(
            root / "inputs" / "hotstuff_snapshot" / "network.go"
        ),
        "conformance": conformance,
    }
    (output / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "run_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    return {
        "decision": decision,
        "theorem_checks": theorem_checks,
        "closure_checks": closure_checks,
        "matrix_rows": matrix_rows,
    }
