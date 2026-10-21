#!/usr/bin/env python3
"""Recompute the seven-validator study, certificates and full-policy controls."""
from __future__ import annotations
import csv
from dataclasses import replace
import gzip
from hashlib import sha256
import itertools
import json
import os
from pathlib import Path
from time import perf_counter

from twins_scheduler.scaled_protocol import (build_model, replay, Engine, GuardedReplay,
    STAGES, FINE_KEYS, FIBRES, OPPORTUNITY_BOUND, advance, EnumerationLimit, initial_partition, flow_partition)
from twins_scheduler.transition_synthesis import synthesize, verify_certificate, SynthesisLimit
from twins_scheduler.transition_abstraction import synthesize_via_abstraction, verify_abstraction_run


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".gz" else
                     (json.dumps(data, sort_keys=True, indent=2) + "\n").encode())


def policy_oracle(problem):
    """Independent ordinary BFS for each total assignment; no search helper."""
    outgoing = [[] for _ in problem.states]
    for edge in problem.transitions:
        outgoing[edge.source].append(edge)
    rows = []
    for integer in range(1 << len(problem.key_fibres)):
        policy = tuple(bool(integer >> k & 1) for k in range(len(problem.key_fibres)))
        reached, pending, found, examined = {problem.initial}, [problem.initial], False, 0
        while pending:
            state = pending.pop()
            if state in problem.unsafe:
                found = True
                break
            for edge in outgoing[state]:
                examined += 1
                if edge.key is not None and policy[edge.key] != edge.value:
                    continue
                if edge.target not in reached:
                    reached.add(edge.target)
                    pending.append(edge.target)
        mixed = {f for f in range(len(problem.costs)) if
                 len({policy[k] for k, owner in enumerate(problem.key_fibres) if owner == f}) > 1}
        split = mixed | problem.required_split
        feasible = found and split <= problem.allowed_split
        rows.append({"policy_bits": integer, "unsafe": found, "feasible": feasible,
                     "split": sorted(split), "cost": sum(problem.costs[f] for f in split),
                     "reached_states": len(reached), "examined_edges": examined})
    feasible = [r["cost"] for r in rows if r["feasible"]]
    return {"problem_sha256": problem.digest(), "total_policies": len(rows),
            "unsafe_policies": sum(r["unsafe"] for r in rows),
            "minimum_cost": min(feasible, default=None), "policies": rows}


def run_schedule(variant, policy, orders=None, dependency="NONE"):
    compact = Engine(variant, dependency)
    full = GuardedReplay(variant, dependency, policy)
    steps = 0
    for stage, actions in enumerate(STAGES):
        order = (orders or {}).get(stage, tuple(range(len(actions))))
        if set(order) != set(range(len(actions))) or len(order) != len(actions):
            raise ValueError("not a stage permutation")
        for slot in order:
            action = actions[slot]
            key = compact.control_key(action)
            compact.apply(action, None if key is None else policy[key])
            full.apply(action)
            assert compact.freeze() == full.freeze(), (stage, slot, variant)
            steps += 1
    audit = full.loop.audit()
    audit.pop("all_other_transport_edges_have_type_uniform_delivery", None)
    assert all(audit.values()), audit
    return {"unsafe": compact.unsafe(), "decisions": {n: s.committed for n, s in full.loop.replicas.items()
             if s.committed is not None}, "matched_successors": steps, "audits": audit}


def main():
    root = Path(__file__).resolve().parents[1]
    output = Path(os.environ.get("TWINS_OUTPUT_ROOT", root))
    dest = output / "results/scaled"
    logs = Path(os.environ.get("TWINS_LOG_DIR", output / "build_logs"))
    rows, times, corpus = [], [], {}
    models = {}
    for variant in ("BASELINE", "ONLY_P0_MUTATED", "MISSING_LOCK_UPDATE"):
        started = perf_counter()
        models[variant] = model = build_model(variant)
        print(f"EXPORTED {variant}: {len(model.problem.states)} states", flush=True)
        times.append({"task": f"export:{variant}", "seconds": perf_counter() - started})
        write(dest / f"models/{variant.lower()}.json.gz", model.problem.to_dict())
        corpus[variant] = oracle = policy_oracle(model.problem)
        write(dest / f"oracles/{variant.lower()}.json.gz", oracle)
        if variant != "MISSING_LOCK_UPDATE":
            assert not model.problem.unsafe and oracle["minimum_cost"] is None
    mutant = models["MISSING_LOCK_UPDATE"]
    cases = (("unit", (1,)*6, frozenset(range(6))),
             ("weighted", (2,5,9,3,7,11), frozenset(range(6))),
             ("p1_controls_fixed", (1,)*6, frozenset(range(3))))
    for name, costs, allowed in cases:
        problem = replace(mutant.problem, costs=costs, allowed_split=allowed)
        model = replace(mutant, problem=problem)
        oracle = policy_oracle(problem)
        write(dest / f"oracles/{name}.json.gz", oracle)
        write(dest / f"models/{name}.json.gz", problem.to_dict())
        t = perf_counter(); direct = synthesize(problem)
        direct_seconds = perf_counter()-t
        t = perf_counter(); direct_check = verify_certificate(direct, expected_problem=problem)
        direct_check_seconds = perf_counter()-t
        assert direct_check["minimum_cost"] == oracle["minimum_cost"]
        write(dest / f"certificates/{name}.direct.json.gz", direct)
        t = perf_counter(); refinement = synthesize_via_abstraction(problem, initial_map=initial_partition(model))
        refinement_seconds = perf_counter()-t
        t = perf_counter(); checked = verify_abstraction_run(refinement, expected_concrete=problem)
        refinement_check_seconds = perf_counter()-t
        assert checked["minimum_cost"] == oracle["minimum_cost"]
        write(dest / f"certificates/{name}.refinement.json.gz", refinement)
        history = refinement["iterations"]
        history_rows = []
        for i, item in enumerate(history):
            cert = item["abstract_certificate"]
            audit = verify_certificate(cert)
            history_rows.append({"iteration": i+1, "states": len(item["abstract"]["states"]),
                "edges": len(item["abstract"]["transitions"]), "lower_bound": audit["minimum_cost"],
                "action": item["action"], "certificate_product_states": audit["checked_product_states"],
                "certificate_edge_checks": audit["checked_input_transitions"],
                "policy_reachable_states": len(item.get("policy_reachable_states", [])),
                "solver_statistics": cert["statistics"]})
        write(dest / f"histories/{name}.json", history_rows)
        replay_summary = None
        if direct["status"] == "optimal":
            for mode, witness in (("direct", direct["witness"]),
                                  ("refinement", refinement["bridge"]["concrete_witness"])):
                record = replay(model, witness["transitions"], witness["policy"])
                assert record["unsafe"] and record["decisions"]["A"] != record["decisions"]["C"]
                write(dest / f"replays/{name}.{mode}.json.gz", record)
                replay_summary = {"messages": len(record["messages"]), "events": len(record["log"]),
                                 "checks": len(record["audit"]), "decisions": record["decisions"]}
        row = {"case": name, "states": len(problem.states), "edges": len(problem.transitions),
               "minimum_cost": oracle["minimum_cost"], "oracle_policies": oracle["total_policies"],
               "unsafe_policies": oracle["unsafe_policies"],
               "initial_abstract_states": len(set(initial_partition(model))),
               "iterations": checked["iterations"], "false_policies": checked["eliminated_policies"],
               "final_abstract_states": checked["final_abstract_states"],
               "final_abstract_edges": history_rows[-1]["edges"],
               "direct_certificate_states": direct_check["checked_product_states"],
               "direct_certificate_edge_checks": direct_check["checked_input_transitions"],
               "refinement_discovered_product_states_total": sum(r["solver_statistics"]["discovered_product_states"] for r in history_rows),
               "refinement_discovered_product_states_peak": max(r["solver_statistics"]["discovered_product_states"] for r in history_rows),
               "final_certificate_states": history_rows[-1]["certificate_product_states"],
               "lower_bound_history": [r["lower_bound"] for r in history_rows],
               "refinement_certificate_states_total": sum(r["certificate_product_states"] for r in history_rows),
               "refinement_certificate_edge_checks_total": sum(r["certificate_edge_checks"] for r in history_rows),
               "all_edge_simulation_checks_total": len(problem.transitions)*len(history_rows),
               "policy_reachable_states_total": sum(r["policy_reachable_states"] for r in history_rows),
               "direct_statistics": direct["statistics"], "guarded_replay": replay_summary}
        rows.append(row)
        times.append({"task": name, "direct_seconds": direct_seconds,
                      "direct_check_seconds": direct_check_seconds,
                      "refinement_seconds": refinement_seconds,
                      "refinement_check_seconds": refinement_check_seconds})
        print(f"CERTIFIED {name}: cost={row['minimum_cost']} iterations={row['iterations']}", flush=True)
    dependencies = []
    for control in ("NO_CROSS_PREVOTE", "NO_NIL_TIMEOUT_SUPPORT", "NO_ROUND1_P1_PREVOTE"):
        model = build_model(dependency=control)
        assert not model.problem.unsafe, control
        write(dest / f"models/{control.lower()}.json.gz", model.problem.to_dict())
        dependencies.append({"control": control, "states": len(model.problem.states),
                             "edges": len(model.problem.transitions), "unsafe_states": 0,
                             "complete_graph": True})
    # Complete fixed assignment checks, using independent graph reachability.
    unsafe_masks = [set(r['split']) for r in corpus['MISSING_LOCK_UPDATE']['policies'] if r['unsafe']]
    assert unsafe_masks and min(map(len, unsafe_masks)) == 2
    assert all(s & set(range(3)) and s & set(range(3,6)) for s in unsafe_masks)
    # Same policy, different timeout/repair orders: new support is essential.
    late_policy = (True,False,True,False,True,True)*2
    guard_controls = []
    for name, orders in (("support_before_timeouts", {}), ("timeouts_before_support", {9:(1,0),10:(1,0)})):
        result = run_schedule('MISSING_LOCK_UPDATE', late_policy, orders)
        guard_controls.append({"case": name, **result})
    assert guard_controls[0]['unsafe'] and not guard_controls[1]['unsafe']
    # Check deterministic dictionary-rule replay on safe and mixed cases too.
    replay_checks = 0
    for variant in models:
        for mask in (0, 4095, 1365, 2730, 2013, 3965):
            policy = tuple(bool(mask >> i & 1) for i in range(12))
            run_schedule(variant, policy)
            replay_checks += 1
    try:
        build_model(max_states=3)
    except EnumerationLimit:
        cutoff = "unknown"
    else:
        raise AssertionError("an incomplete graph was returned")
    # Sensitivity control: a guard-blind seed is not presumed to scale.
    # Its fixed, deterministic resource cutoff is unknown, never infeasible.
    try:
        synthesize_via_abstraction(mutant.problem, initial_map=flow_partition(mutant),
                                  max_refinements=8, max_product_states=10000)
    except SynthesisLimit as exc:
        seed_control = {"status": "unknown", "reason": str(exc),
                        "initial_states": len(set(flow_partition(mutant))),
                        "max_refinements": 8, "max_product_states": 10000}
    else:
        raise AssertionError("guard-blind control unexpectedly completed; review recorded claim")
    summary = {"status": "PASS", "schema": "scaled-study/v2", "validators": 7, "quorum": 5,
        "fine_keys": list(FINE_KEYS), "coarse_fibres": list(FIBRES),
        "stages": len(STAGES), "opportunities": OPPORTUNITY_BOUND,
        "cases": rows, "dependency_controls": dependencies,
        "baseline": {v: {"states": len(models[v].problem.states),
                         "edges": len(models[v].problem.transitions), "unsafe_states": len(models[v].problem.unsafe),
                         "oracle_policies": corpus[v]['total_policies']} for v in models if v != 'MISSING_LOCK_UPDATE'},
        "guard_controls": guard_controls, "additional_independent_replays": replay_checks,
        "all_total_policy_queries": sum(v['total_policies'] for v in corpus.values()),
        "minimum_requires_both_targets": True, "oracle_mismatches": 0,
        "resource_limit": cutoff, "coarse_seed_control": seed_control,
        "source_sha256": {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                          for p in (root/"src/python/twins_scheduler/scaled_protocol.py",
                                    root/"src/python/twins_scheduler/concrete_trace.py")},
        "scope": "complete stated finite staged environment, fixed batches, static controls; no client-wide claim"}
    write(dest / "summary.json", summary)
    write(logs / "scaled_timings.json", times)
    print('SCALED STUDY PASS', flush=True)


if __name__ == '__main__':
    main()
