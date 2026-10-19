"""Check the executable specialization bridge, not just equal optimum formulas."""

from dataclasses import replace
from itertools import permutations, product

import pytest

from twins_scheduler.refinement_synthesis import Problem as PivotProblem, synthesize as structured
from twins_scheduler.repair_frontier import Domain, execute, from_graph
from twins_scheduler.transition_pivot_adapter import AdapterLimit, build_pivot_model, normalize_witness
from twins_scheduler.transition_synthesis import replay_trace, synthesize, verify_certificate


def path_for_policy_order(model, policy, order):
    events = tuple(("E", i) for i in range(model.source.domain.k)) + tuple(order)
    state = model.problem.initial
    indices = []
    for event in events:
        expected = None if event[0] == "V" else policy[2 * event[1] + (event[0] == "R")]
        index, edge = next((index, edge) for index, edge in enumerate(model.problem.transitions)
                           if edge.source == state and model.edge_events[index] == event
                           and edge.value == expected)
        indices.append(index)
        state = edge.target
    return indices


def test_every_raw_order_and_all_four_boolean_patterns_execute_exactly():
    source = PivotProblem(Domain((1, 2)), 0, 0, (5, 2))
    model = build_pivot_model(source)
    for policy, order in product(product((False, True), repeat=4), permutations(source.domain.events)):
        indices = path_for_policy_order(model, policy, order)
        witness = replay_trace(model.problem, indices)
        state = model.states[witness["terminal"]]
        repaired, emitted = set(), set()
        for kind, i in order:
            if kind == "R" and policy[2 * i + 1]:
                repaired.add(i)
            if kind == "V" and i not in repaired:
                emitted.add(i)
        assert state.first == sum(1 << i for i in range(2) if policy[2 * i])
        assert state.repaired == sum(1 << i for i in repaired)
        assert state.second == sum(1 << i for i in emitted)
        assert state.completed == 15
        normalized = normalize_witness(model, indices)
        run = execute(source.domain, normalized["opened"],
                      (tuple(event) for event in normalized["order"]), normalized["split"])
        assert run.first_weight >= sum(w for i, w in enumerate(source.domain.weights) if state.first >> i & 1)
        assert run.second_weight >= sum(w for i, w in enumerate(source.domain.weights) if state.second >> i & 1)
        assert normalized["cost"] == witness["cost"]


def test_reversed_mixed_pattern_normalizes_to_both_signatures():
    source = PivotProblem(from_graph(1, [(0, 0)]), 0, 0, (7,))
    model = build_pivot_model(source)
    path = path_for_policy_order(model, (False, True), (("R", 0), ("V", 0)))
    actual = replay_trace(model.problem, path)
    final = model.states[actual["terminal"]]
    assert (final.first, final.repaired, final.second) == (0, 1, 0)
    normalized = normalize_witness(model, path)
    assert normalized == {"opened": [0], "split": [0], "order": [["R", 0], ["V", 0]], "cost": 7}
    run = execute(source.domain, normalized["opened"], map(tuple, normalized["order"]), normalized["split"])
    assert run.first_weight == run.second_weight == 1


def test_required_split_is_preserved_even_without_observed_disagreement():
    source = PivotProblem(Domain((1,)), 0, 1, (4,), required_split=frozenset({0}))
    model = build_pivot_model(source)
    path = path_for_policy_order(model, (False, False), (("R", 0), ("V", 0)))
    normalized = normalize_witness(model, path)
    assert normalized["opened"] == normalized["split"] == [0]
    assert normalized["cost"] == 4
    assert synthesize(model.problem)["minimum_cost"] == structured(source)["minimum_cost"] == 4


def test_repair_after_issuance_cannot_remove_second_signature():
    source = PivotProblem(Domain((1,), frozenset({(("V", 0), ("R", 0))})), 1, 1, (3,))
    model = build_pivot_model(source)
    path = path_for_policy_order(model, (True, True), (("V", 0), ("R", 0)))
    result = replay_trace(model.problem, path)
    final = model.states[result["terminal"]]
    assert (final.first, final.repaired, final.second) == (1, 1, 1)
    assert result["split"] == []
    assert result["cost"] == 0
    # Even when both signatures already exist, the goal requires the last slot.
    penultimate = model.problem.transitions[path[-1]].source
    assert penultimate not in model.problem.unsafe
    assert result["terminal"] in model.problem.unsafe


def test_suppressed_opportunity_preserves_transitive_precedence():
    domain = Domain((1, 1), frozenset({(("R", 0), ("R", 1)), (("R", 1), ("V", 0))}))
    source = PivotProblem(domain, 2, 2, (5, 2), frozenset({1}))
    model = build_pivot_model(source)
    result = synthesize(model.problem)
    assert result["status"] == "infeasible"
    assert structured(source)["status"] == "infeasible"
    assert verify_certificate(result, model.problem)["status"] == "PASS"
    for index, edge in enumerate(model.problem.transitions):
        if model.edge_events[index] == ("V", 0):
            assert model.states[edge.source].completed & 3 == 3


def test_weighted_quotas_costs_and_permissions_are_bound_to_input():
    source = PivotProblem(from_graph(2, [(0, 0), (1, 1)], weights=(1, 2)), 2, 3, (5, 0))
    model = build_pivot_model(source)
    result = synthesize(model.problem)
    assert result["minimum_cost"] == structured(source)["minimum_cost"] == 0
    assert result["witness"]["split"] == [1]
    restricted = replace(source, allowed_split=frozenset({0}))
    changed = model.with_objective(restricted)
    assert changed.problem.transitions is model.problem.transitions
    assert synthesize(changed.problem)["minimum_cost"] is None
    with pytest.raises(ValueError, match="fresh exported model"):
        model.with_objective(replace(source, domain=Domain((1, 2))))


def test_exporter_never_calls_repair_graph_capacity_order_or_optimizer(monkeypatch):
    source = PivotProblem(from_graph(2, [(0, 1), (1, 0)]), 2, 2, (3, 1))

    def forbidden(*args, **kwargs):
        raise AssertionError("adapter depends on a specialized solution procedure")

    for name in ("repair_graph", "acyclic_capacity", "orders"):
        monkeypatch.setattr(Domain, name, forbidden)
    monkeypatch.setattr("twins_scheduler.repair_frontier.execute", forbidden)
    monkeypatch.setattr("twins_scheduler.refinement_synthesis.synthesize", forbidden)
    model = build_pivot_model(source)
    result = synthesize(model.problem)
    assert result["minimum_cost"] == 1
    assert verify_certificate(result)["status"] == "PASS"


def test_exporter_limit_and_missing_readiness_cannot_claim_infeasibility():
    source = PivotProblem(Domain((1,)), 1, 1, (2,))
    with pytest.raises(AdapterLimit, match="no complete model.*unknown"):
        build_pivot_model(source, max_states=1)
    # Domain historically allows this truthy non-Boolean; the adapter requires
    # the exact declared True readiness contract.
    noncanonical = replace(source, domain=Domain((1,), initially_ready=1))
    with pytest.raises(ValueError, match="initial readiness"):
        build_pivot_model(noncanonical)
