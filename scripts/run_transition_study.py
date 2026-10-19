#!/usr/bin/env python3
"""Reproduce general finite-LTS synthesis and the state-coupled quorum model.

All result files are deterministic.  Wall-time observations go to build_logs.
The oracle enumerates total fine policies and permitted split subsets before
ordinary graph reachability; it never calls product-state synthesis helpers.
"""

from __future__ import annotations

import csv
from dataclasses import replace
import gzip
from hashlib import sha256
import itertools
import json
import os
from pathlib import Path
import random
from time import perf_counter

from twins_scheduler.coupled_protocol import (
    EnumerationLimit, FINE_KEYS, STAGES, build_model,
    direct_policy_reachability, execution_record, exhaustive_policy_oracle, graph_policy_reachability,
    quotient_audit_order, replay_protocol_witness, run_policy_schedule, semantic_examples, spurious_quotient,
)
from twins_scheduler.transition_synthesis import Problem, Transition, synthesize, verify_certificate


def write_json(path: Path, value, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True,
                      separators=(",", ":") if compact else None,
                      indent=None if compact else 2) + "\n").encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".gz" else raw)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def oracle_family():
    """Every six-way labelling of four positions, six input configurations.

    Three states; initial 0 and unsafe 2.  The possible directed positions
    are 0->1, 1->2, 1->0 and 0->0.  Each is absent, tau, or one of the four
    Boolean labels at two fine keys.  Thus all 6**4=1296 graphs are checked
    under zero/positive split cost and free/forbidden/required splitting.
    """
    positions = ((0, 1), (1, 2), (1, 0), (0, 0))
    labels = (None, (None, None), (0, False), (0, True), (1, False), (1, True))
    for code, choices in enumerate(itertools.product(range(len(labels)), repeat=len(positions))):
        transitions = tuple(Transition(source, target, *labels[choice], f"position{index}")
                            for index, ((source, target), choice) in enumerate(zip(positions, choices))
                            if labels[choice] is not None)
        for cost in (0, 3):
            for mode, allowed, required in (
                ("free", frozenset({0}), frozenset()),
                ("forbidden", frozenset(), frozenset()),
                ("required", frozenset({0}), frozenset({0})),
            ):
                yield f"exhaustive:{code}:cost{cost}:{mode}", Problem(
                    ("start", "middle", "unsafe"), 0, frozenset({2}), transitions,
                    (0, 0), (cost,), allowed, required)


def random_family(count: int = 128):
    """Fixed-seed wider graphs with cycles, multiple fibres and internal edges."""
    rng = random.Random(20261019)
    for index in range(count):
        count_states = rng.randrange(4, 9)
        count_keys = rng.randrange(3, 7)
        fibres = tuple(rng.randrange(3) for _ in range(count_keys))
        costs = tuple(rng.randrange(9) for _ in range(3))
        allowed = frozenset(i for i in range(3) if rng.randrange(4) != 0)
        required = frozenset(i for i in sorted(allowed) if rng.randrange(5) == 0)
        transitions = []
        for edge_index in range(rng.randrange(count_states, 4 * count_states)):
            source, target = rng.randrange(count_states), rng.randrange(count_states)
            key = None if rng.randrange(4) == 0 else rng.randrange(count_keys)
            transitions.append(Transition(source, target, key,
                                          None if key is None else bool(rng.randrange(2)),
                                          f"edge{edge_index}"))
        unsafe = frozenset({count_states - 1})
        if index % 17 == 0:
            unsafe |= {0}
        yield f"random:{index}", Problem(tuple(f"q{i}" for i in range(count_states)), 0,
                                        unsafe, tuple(transitions), fibres, costs, allowed, required)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_root = Path(os.environ.get("TWINS_OUTPUT_ROOT", root))
    output = output_root / "results" / "transition"
    log_dir = Path(os.environ.get("TWINS_LOG_DIR", output_root / "build_logs"))
    started = perf_counter()
    observations = []
    oracle_rows = []
    checked_product_states = 0
    for name, problem in itertools.chain(oracle_family(), random_family()):
        oracle = exhaustive_policy_oracle(problem)
        certificate = synthesize(problem)
        verification = verify_certificate(certificate, problem)
        if certificate["minimum_cost"] != oracle["minimum_cost"]:
            raise AssertionError(f"independent total-policy oracle mismatch: {name}")
        checked_product_states += verification["checked_product_states"]
        oracle_rows.append({"case": name, "states": len(problem.states),
                            "transitions": len(problem.transitions),
                            "fine_keys": len(problem.key_fibres), "fibres": len(problem.costs),
                            "minimum_cost": "infeasible" if oracle["minimum_cost"] is None else oracle["minimum_cost"],
                            "policies": oracle["total_policies"],
                            "policy_split_pairs": oracle["compatible_policy_split_pairs"],
                            "certificate_checked_states": verification["checked_product_states"],
                            "input_sha256": problem.digest(), "mismatch": False})
    print(f"general LTS oracle: {len(oracle_rows)} cases, zero mismatches", flush=True)
    observations.append({"phase": "small_graph_oracle", "wall_seconds": perf_counter() - started})
    write_csv(output / "oracle_cases.csv", oracle_rows)

    examples = []
    for name, problem in semantic_examples().items():
        certificate = synthesize(problem)
        check = verify_certificate(certificate, problem)
        oracle = exhaustive_policy_oracle(problem)
        assert certificate["minimum_cost"] == oracle["minimum_cost"]
        examples.append({"name": name, "problem": problem.to_dict(), "certificate": certificate,
                         "verification": check, "oracle": oracle})
    write_json(output / "semantic_examples.json", examples)
    spurious_input = semantic_examples()["spurious_state_merge"]
    spurious, mapping = spurious_quotient(spurious_input)
    write_json(output / "spurious_abstraction.json", {
        "concrete": spurious_input.to_dict(), "abstract": spurious.to_dict(), "state_map": list(mapping),
        "concrete_certificate": synthesize(spurious_input), "abstract_certificate": synthesize(spurious),
        "meaning": "Every concrete edge maps to an abstract edge, but the abstract cost-0 path has no concrete lift.",
    })

    model_started = perf_counter()
    mutant = build_model()
    baseline = build_model("BASELINE")
    abstract, mapping = quotient_audit_order(mutant)
    abstract_baseline, _ = quotient_audit_order(baseline)
    observations.append({"phase": "two_complete_protocol_graphs", "wall_seconds": perf_counter() - model_started})
    write_json(output / "coupled_mutant.json.gz", mutant.problem.to_dict(), compact=True)
    write_json(output / "coupled_baseline.json.gz", baseline.problem.to_dict(), compact=True)
    write_json(output / "coupled_audit_quotient.json.gz", abstract.to_dict(), compact=True)
    write_json(output / "coupled_audit_quotient_map.json", list(mapping))
    write_json(output / "coupled_protocol_states.json.gz", {
        "states": mutant.snapshots, "edge_actions": mutant.edge_actions,
        "stages": [[{"kind": action.kind, "args": list(action.args)} for action in stage]
                   for stage in STAGES],
    }, compact=True)
    model_cases = (
        ("mutant_free", mutant, mutant.problem),
        ("baseline_free", baseline, baseline.problem),
        ("mutant_forbid_all", mutant, replace(mutant.problem, allowed_split=frozenset())),
        ("mutant_only_B_to_P", mutant, replace(mutant.problem, allowed_split=frozenset({0}))),
        ("mutant_only_A_to_P", mutant, replace(mutant.problem, allowed_split=frozenset({1}))),
        ("mutant_require_B_to_P", mutant, replace(mutant.problem, required_split=frozenset({0}))),
        ("mutant_require_both", mutant, replace(mutant.problem, required_split=frozenset({0, 1}))),
    )
    model_rows = []
    main_execution = None
    for name, model, problem in model_cases:
        certificate = synthesize(problem)
        check = verify_certificate(certificate, problem)
        oracle = exhaustive_policy_oracle(problem)
        if certificate["minimum_cost"] != oracle["minimum_cost"]:
            raise AssertionError(f"protocol total-policy optimum mismatch: {name}")
        execution = None
        if certificate["status"] == "optimal":
            execution = replay_protocol_witness(model, certificate["witness"]["transitions"],
                                                certificate["witness"]["policy"])
            if not execution["unsafe"] or not all(execution["audit"].values()):
                raise AssertionError(f"guarded protocol replay failed: {name}")
            if name == "mutant_free":
                main_execution = execution
        write_json(output / "certificates" / f"{name}.json.gz", certificate, compact=True)
        model_rows.append({"case": name, "status": certificate["status"],
                           "minimum_cost": "infeasible" if certificate["minimum_cost"] is None else certificate["minimum_cost"],
                           "states": len(problem.states), "transitions": len(problem.transitions),
                           "unsafe_states": len(problem.unsafe),
                           "checked_product_states": check["checked_product_states"],
                           "total_policies": oracle["total_policies"],
                           "compatible_policy_split_pairs": oracle["compatible_policy_split_pairs"],
                           "input_sha256": problem.digest(), "witness_guard_audit": execution is None or all(execution["audit"].values())})
    assert main_execution is not None
    write_csv(output / "model_cases.csv", model_rows)
    write_json(output / "coupled_protocol_witness.json.gz", main_execution, compact=True)
    print(f"coupled quorum: {len(mutant.problem.states)} states, {len(mutant.problem.transitions)} transitions; minimum2; baseline infeasible", flush=True)

    mixed_policy = (True, True, True, True, False, False)
    order_controls = []
    for name, policy, order in (
        ("repair_before_timeout_unsafe", mixed_policy, (0, 1, 2)),
        ("timeout_before_enabling_quorum_safe", mixed_policy, (1, 0, 2)),
        ("late_repair_block_delivered", (True,) * len(FINE_KEYS), (1, 0, 2)),
        ("late_repair_block_suppressed", (True, True, True, True, True, False), (1, 0, 2)),
        ("both_precommits_suppressed_no_round_advance", (True, False, True, True, False, False), (0, 1, 2)),
    ):
        execution = execution_record(run_policy_schedule(policy, stage_orders={6: order}))
        if not all(execution["audit"].values()):
            raise AssertionError(f"order/block control guard audit failed: {name}")
        order_controls.append({"name": name, "policy": list(policy), "stage6_order": list(order),
                               "execution": execution})
    if not order_controls[0]["execution"]["unsafe"] or order_controls[1]["execution"]["unsafe"]:
        raise AssertionError("the fixed-policy order boundary was not reproduced")
    if (order_controls[2]["execution"]["decisions"].get("P") != 0
            or "P" in order_controls[3]["execution"]["decisions"]):
        raise AssertionError("missing-block data dependency was not reproduced")
    if order_controls[4]["execution"]["decisions"] != {"A": 0}:
        raise AssertionError("closed-precommit readiness boundary was not reproduced")
    write_json(output / "coupled_order_controls.json.gz", order_controls, compact=True)

    # Check exporter completeness independently of exported adjacency.  Every
    # total fine policy is re-executed from empty replicas through the guarded
    # transition generator, and state/edge counts and bad reachability match.
    direct_started = perf_counter()
    direct_rows = []
    for model, graph in ((mutant, abstract), (baseline, abstract_baseline)):
        for policy in itertools.product((False, True), repeat=len(FINE_KEYS)):
            direct = direct_policy_reachability(model.variant, policy)
            exported = graph_policy_reachability(graph, policy)
            if direct != exported:
                raise AssertionError(f"direct protocol/export mismatch: {model.variant}, {policy}")
            direct_rows.append({"variant": model.variant, "policy": "".join(str(int(bit)) for bit in policy),
                                "unsafe": direct["unsafe"], "states": direct["states"],
                                "transitions": direct["transitions"], "mismatch": False})
        print(f"direct guarded protocol comparison: {model.variant},64 total policies, zero mismatches", flush=True)
    observations.append({"phase": "direct_protocol_all_policies", "wall_seconds": perf_counter() - direct_started})
    write_csv(output / "direct_policy_checks.csv", direct_rows)

    limit_unknown = False
    try:
        build_model(max_states=3)
    except EnumerationLimit:
        limit_unknown = True
    assert limit_unknown
    aggregate_input_hash = sha256("\n".join(row["input_sha256"] for row in oracle_rows).encode()).hexdigest()
    summary = {
        "status": "PASS", "schema_version": 1,
        "exhaustive_graphs": 6 ** 4, "exhaustive_cost_permission_configurations": 6,
        "exhaustive_oracle_cases": 6 ** 4 * 6, "random_oracle_cases": 128,
        "oracle_cases": len(oracle_rows), "oracle_mismatches": 0,
        "oracle_total_policies": sum(row["policies"] for row in oracle_rows),
        "oracle_compatible_policy_split_pairs": sum(row["policy_split_pairs"] for row in oracle_rows),
        "oracle_certificate_checked_product_states": checked_product_states,
        "oracle_input_manifest_sha256": aggregate_input_hash,
        "random_seed": 20261019,
        "semantic_examples": len(examples),
        "protocol_model_cases": len(model_rows),
        "protocol": {"mutant": mutant.summary(), "baseline": baseline.summary(),
                     "audit_quotient_states": len(abstract.states),
                     "audit_quotient_transitions": len(abstract.transitions),
                     "minimum_cost": 2, "selected_fibre": "A->P:H1:R0",
                     "costs": list(mutant.problem.costs),
                     "witness_decisions": main_execution["decisions"],
                     "witness_messages": len(main_execution["messages"]),
                     "witness_log_events": len(main_execution["log"]),
                     "witness_certificates": len(main_execution["certificates"]),
                     "all_witness_guard_audits_pass": all(main_execution["audit"].values()),
                     "block_phase_labelled_edges": sum(edge.key == 5 for edge in mutant.problem.transitions),
                     "same_fixed_policy_has_safe_and_unsafe_orders": True,
                     "late_repair_commit_waits_for_received_block": True,
                     "suppressing_both_precommits_can_remove_round_advance": True,
                     "order_and_block_controls": len(order_controls)},
        "direct_protocol_policy_checks": len(direct_rows), "direct_protocol_mismatches": 0,
        "direct_protocol_generated_states": sum(row["states"] for row in direct_rows),
        "direct_protocol_generated_transitions": sum(row["transitions"] for row in direct_rows),
        "resource_limit_is_unknown": limit_unknown,
        "scope": "Complete finite opportunity-domain model: n=4, one Byzantine B, two rounds, twelve stages and 32 once-only opportunity slots; all permutations within each stage, including repair versus precommit timeouts. Guarded missing-block catchup is included. Unsafe means the unmutated observers A and C decide different blocks. Test-only HMAC. Not all CometBFT executions.",
    }
    write_json(output / "summary.json", summary)
    observations.append({"phase": "whole_study", "wall_seconds": perf_counter() - started})
    write_json(log_dir / "transition_synthesis_observations.json", observations)
    print(json.dumps({"status": "PASS", "oracle_cases": len(oracle_rows),
                      "direct_protocol_policy_checks": len(direct_rows),
                      "protocol_minimum_cost": 2}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
