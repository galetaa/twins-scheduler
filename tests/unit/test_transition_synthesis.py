"""Static-policy enumeration, interacting transitions, and hostile proof edits."""

from copy import deepcopy
from itertools import product

import pytest

from twins_scheduler import transition_synthesis as implementation
from twins_scheduler.transition_examples import set_cover_problem
from twins_scheduler.transition_synthesis import (
    Problem, ProductState, SynthesisLimit, Transition, product_successors,
    replay_trace, synthesize, verify_certificate,
)


def independent_policy_minimum(problem):
    """Enumerate TOTAL policies and split subsets, then ordinary graph reachability.

    This oracle has no product states, partial-policy inference, Dijkstra,
    closed-set certificates, or calls to optimizer/replay helpers.
    """
    best = None
    for selected in product((False, True), repeat=len(problem.costs)):
        splits = {fibre for fibre, present in enumerate(selected) if present}
        if not problem.required_split <= splits <= problem.allowed_split:
            continue
        cost = sum(problem.costs[fibre] for fibre in splits)
        for policy in product((False, True), repeat=len(problem.key_fibres)):
            valid = True
            for first, second in product(range(len(policy)), repeat=2):
                if (problem.key_fibres[first] == problem.key_fibres[second]
                        and problem.key_fibres[first] not in splits
                        and policy[first] != policy[second]):
                    valid = False
            if not valid:
                continue
            reachable = {problem.initial}
            changed = True
            while changed:
                changed = False
                for edge in problem.transitions:
                    if (edge.source in reachable and edge.target not in reachable
                            and (edge.key is None or policy[edge.key] == edge.value)):
                        reachable.add(edge.target)
                        changed = True
            if reachable & problem.unsafe:
                best = cost if best is None else min(best, cost)
    return best


def two_routes(costs=(7, 3), allowed=None):
    # Both routes need a genuine split; protocol state chooses which route exists.
    return Problem(("initial", "first-A", "first-B", "unsafe"), 0, frozenset({3}), (
        Transition(0, 1, 0, True, "enable A"),
        Transition(1, 3, 1, False, "withhold A repair"),
        Transition(0, 2, 2, False, "withhold B repair"),
        Transition(2, 3, 3, True, "enable B"),
    ), (0, 0, 1, 1), costs, allowed)


def test_minimum_uses_state_dependent_alternative_route():
    problem = two_routes()
    result = synthesize(problem)
    assert result["minimum_cost"] == 3
    assert result["witness"]["transitions"] == [2, 3]
    assert result["witness"]["split"] == [1]
    assert result["witness"]["policy"] == [False, False, False, True]
    assert verify_certificate(result, problem)["status"] == "PASS"
    assert independent_policy_minimum(problem) == 3
    assert synthesize(two_routes(allowed=frozenset({0})))["minimum_cost"] == 7
    forbidden = two_routes(allowed=frozenset())
    assert synthesize(forbidden)["status"] == "infeasible"
    assert verify_certificate(synthesize(forbidden), forbidden)["claim"] == "infeasible"


def test_repeated_fine_key_never_becomes_an_adaptive_policy():
    problem = Problem(("initial", "after true", "unsafe"), 0, frozenset({2}), (
        Transition(0, 1, 0, True), Transition(1, 2, 0, False),
    ), (0,), (0,))
    result = synthesize(problem)
    assert result["status"] == "infeasible"
    assert independent_policy_minimum(problem) is None
    assert verify_certificate(result)["status"] == "PASS"
    with pytest.raises(ValueError, match="policy-consistent"):
        replay_trace(problem, [0, 1])


def test_reaching_same_protocol_state_with_two_policies_preserves_both():
    problem = Problem(("initial", "merged", "after repeat", "unsafe"), 0, frozenset({3}), (
        Transition(0, 1, 0, True), Transition(0, 1, 0, False),
        Transition(1, 2, 0, False), Transition(2, 3, 1, True),
    ), (0, 0), (4,))
    result = synthesize(problem)
    assert result["minimum_cost"] == 4
    assert result["witness"]["transitions"] == [1, 2, 3]
    merged = [node for node in result["proof"]["states"] if node["state"] == 1]
    assert sorted(node["assignment"] for node in merged) == [[0, -1], [1, -1]]
    assert verify_certificate(result)["status"] == "PASS"


def test_four_phases_and_repeated_use_pay_one_fibre_once():
    problem = Problem(tuple(f"state {i}" for i in range(7)), 0, frozenset({6}), (
        Transition(0, 1, 0, True), Transition(1, 2, 1, False),
        Transition(2, 3, 2, True), Transition(3, 4, 3, False),
        Transition(4, 5, 0, True), Transition(5, 6, 1, False),
    ), (0, 0, 0, 0), (9,))
    result = synthesize(problem)
    assert result["minimum_cost"] == 9
    assert result["witness"]["split"] == [0]
    assert verify_certificate(result)["replayed_transitions"] == 6
    node = ProductState(1, (1, -1, -1, -1))
    assert product_successors(problem, node)[0][2] == 9
    assert product_successors(problem, ProductState(4, (1, 0, 1, 0)))[0][2] == 0


def test_required_splits_are_paid_when_unused_and_initial_is_unsafe():
    problem = Problem(("already unsafe",), 0, frozenset({0}), (), (0, 1), (5, 7),
                      required_split=frozenset({1}))
    result = synthesize(problem)
    assert result["minimum_cost"] == 7
    assert result["proof"]["states"] == []
    assert result["witness"]["transitions"] == []
    assert result["witness"]["split"] == [1]
    assert verify_certificate(result)["status"] == "PASS"


def test_unseen_phase_completion_preserves_unsplit_true_value():
    problem = Problem(("initial", "unsafe"), 0, frozenset({1}), (Transition(0, 1, 1, True),),
                      (0, 0, 0), (8,))
    result = synthesize(problem)
    assert result["minimum_cost"] == 0
    assert result["witness"]["policy"] == [True, True, True]
    assert result["witness"]["split"] == []
    assert verify_certificate(result)["status"] == "PASS"


def test_zero_cost_cycles_and_nondeterminism_are_finite_and_exact():
    problem = Problem(("initial", "safe loop", "enabled", "unsafe"), 0, frozenset({3}), (
        Transition(0, 0), Transition(0, 1), Transition(1, 0),
        Transition(0, 2, 0, True), Transition(0, 1, 0, True),
        Transition(2, 2, 0, True), Transition(2, 3, 1, False),
    ), (0, 0), (0,))
    result = synthesize(problem)
    assert result["minimum_cost"] == 0
    assert result["witness"]["split"] == [0]
    assert result["proof"]["states"] == []
    assert result["statistics"]["discovered_product_states"] <= 10
    assert verify_certificate(result)["status"] == "PASS"


def test_no_fine_keys_reduces_to_reachability_with_tau_cycles():
    problem = Problem(("initial", "cycle", "unreachable unsafe"), 0, frozenset({2}), (
        Transition(0, 1), Transition(1, 0), Transition(1, 1),
    ), (), ())
    result = synthesize(problem)
    assert result["status"] == "infeasible"
    assert len(result["proof"]["states"]) == 2
    assert verify_certificate(result)["checked_input_transitions"] == 3


def test_exhaustive_small_graphs_match_total_policy_and_split_enumeration():
    edges = (
        Transition(0, 1, 0, False), Transition(0, 1, 0, True),
        Transition(1, 2, 1, False), Transition(1, 2, 1, True),
        Transition(1, 0, 0, False), Transition(1, 0, 0, True),
        Transition(2, 1), Transition(0, 0),
    )
    constraints = ((frozenset(), frozenset()),
                   (frozenset({0}), frozenset()),
                   (frozenset({0, 1}), frozenset({1})),
                   (frozenset({0, 1}), frozenset({0, 1})))
    checked = 0
    for mask in range(1 << len(edges)):
        selected = tuple(edge for index, edge in enumerate(edges) if mask >> index & 1)
        for costs, (allowed, required) in product(((2, 3), (0, 3)), constraints):
            problem = Problem(("initial", "middle", "unsafe"), 0, frozenset({2}),
                              selected, (0, 0, 1), costs, allowed, required)
            result = synthesize(problem)
            assert result["minimum_cost"] == independent_policy_minimum(problem)
            assert verify_certificate(result, problem)["status"] == "PASS"
            checked += 1
    assert checked == 2048


def test_expensive_feasible_witness_cannot_forge_optimality():
    problem = two_routes()
    forged = synthesize(problem)
    forged["minimum_cost"] = 7
    forged["proof"]["bound"] = 7
    forged["witness"] = replay_trace(problem, [0, 1])
    # The witness is valid, but the cheaper reachable unsafe state is omitted.
    with pytest.raises(ValueError, match="closed-set successor"):
        verify_certificate(forged, problem)


def test_closed_set_rejects_missing_initial_successor_and_unsafe_state():
    problem = two_routes(allowed=frozenset())
    certificate = synthesize(problem)
    missing_initial = deepcopy(certificate)
    missing_initial["proof"]["states"] = [
        node for node in missing_initial["proof"]["states"] if node["state"] != 0]
    with pytest.raises(ValueError, match="initial product state"):
        verify_certificate(missing_initial)
    missing_successor = deepcopy(certificate)
    missing_successor["proof"]["states"] = [
        node for node in missing_successor["proof"]["states"] if node["state"] != 1]
    with pytest.raises(ValueError, match="closed-set successor"):
        verify_certificate(missing_successor)
    unsafe = deepcopy(certificate)
    unsafe["proof"]["states"].append({"state": 3, "assignment": [-1] * 4})
    with pytest.raises(ValueError, match="contains an unsafe state"):
        verify_certificate(unsafe)


def test_deleted_input_edge_requires_hash_and_external_problem_binding():
    problem = two_routes()
    changed = deepcopy(problem.to_dict())
    changed["transitions"] = changed["transitions"][:2]
    altered_problem = Problem.from_dict(changed)
    certificate = synthesize(altered_problem)
    with pytest.raises(ValueError, match="different problem"):
        verify_certificate(certificate, problem)
    wrong_hash = synthesize(problem)
    wrong_hash["problem"]["transitions"].pop()
    with pytest.raises(ValueError, match="input hash"):
        verify_certificate(wrong_hash)


def test_false_infeasibility_and_incomplete_witness_are_rejected():
    problem = two_routes()
    original = synthesize(problem)
    forged = deepcopy(original)
    forged.update(status="infeasible", minimum_cost=None, witness=None)
    forged["proof"] = {"kind": "closed-reachable-set", "states": forged["proof"]["states"]}
    with pytest.raises(ValueError, match="closed-set successor"):
        verify_certificate(forged)
    missing = deepcopy(original)
    missing["witness"]["product_states"].pop()
    with pytest.raises(ValueError, match="every path product state"):
        verify_certificate(missing)
    policy = deepcopy(original)
    policy["witness"]["policy"][3] = False
    with pytest.raises(ValueError, match="used fine-key value"):
        verify_certificate(policy)
    repeated = deepcopy(original)
    repeated["proof"]["states"].append(deepcopy(repeated["proof"]["states"][0]))
    with pytest.raises(ValueError, match="duplicate"):
        verify_certificate(repeated)


def test_checker_is_independent_of_all_optimizer_transition_helpers(monkeypatch):
    problem = two_routes()
    certificate = synthesize(problem)

    def forbidden(*args, **kwargs):
        raise AssertionError("the checker invoked optimizer transition code")

    for name in ("synthesize", "replay_trace", "product_successors", "_optimizer_step",
                 "_product_cost", "_split_set"):
        monkeypatch.setattr(implementation, name, forbidden)
    assert verify_certificate(certificate, problem)["status"] == "PASS"


def test_resource_exhaustion_never_produces_infeasibility():
    problem = two_routes(allowed=frozenset())
    with pytest.raises(SynthesisLimit, match="product-state limit"):
        synthesize(problem, max_product_states=1)
    with pytest.raises(SynthesisLimit, match="wall-clock"):
        synthesize(problem, time_budget_seconds=1e-12)
    certificate = synthesize(problem)
    with pytest.raises(SynthesisLimit, match="certificate-state limit"):
        verify_certificate(certificate, max_checked_states=1)
    with pytest.raises(SynthesisLimit, match="wall-clock"):
        verify_certificate(certificate, time_budget_seconds=1e-12)


@pytest.mark.parametrize("field,value", [
    ("initial", True), ("unsafe", [True]), ("costs", [7, False]),
    ("costs", [7, -1]), ("costs", [7, 3.0]), ("key_fibres", [0, 0, 1, True]),
    ("required_split", [False]), ("allowed_split", [0, 0]),
])
def test_json_integer_fields_reject_booleans_and_noncanonical_values(field, value):
    data = two_routes().to_dict()
    data[field] = value
    with pytest.raises(ValueError):
        Problem.from_dict(data)


@pytest.mark.parametrize("field,value", [
    ("source", True), ("target", False), ("key", True), ("value", 1),
    ("value", "true"), ("label", 3),
])
def test_json_transition_values_are_typed(field, value):
    data = two_routes().to_dict()
    data["transitions"][0][field] = value
    with pytest.raises(ValueError):
        Problem.from_dict(data)


def test_malformed_certificate_booleans_cannot_pass_as_numbers():
    original = synthesize(two_routes())
    malformed = deepcopy(original)
    malformed["minimum_cost"] = True
    with pytest.raises(ValueError, match="nonnegative integer"):
        verify_certificate(malformed)
    malformed = deepcopy(original)
    malformed["proof"]["states"][0]["assignment"][0] = False
    with pytest.raises(ValueError, match="integers -1, 0, or 1"):
        verify_certificate(malformed)
    malformed = deepcopy(original)
    malformed["witness"]["policy"][0] = 0
    with pytest.raises(ValueError, match="total Boolean"):
        verify_certificate(malformed)


def test_problem_copies_mutable_input_and_roundtrips_exactly():
    states = ["initial", "unsafe"]
    transitions = [Transition(0, 1, 0, True)]
    costs = [2]
    problem = Problem(states, 0, [1], transitions, [0], costs)
    digest = problem.digest()
    states[1] = "changed"
    transitions.clear()
    costs[0] = 999
    assert problem.digest() == digest
    assert Problem.from_dict(problem.to_dict()) == problem


def test_set_cover_reduction_preserves_all_small_family_optima():
    universe = frozenset(range(3))
    subsets = tuple(frozenset(i for i in range(3) if mask >> i & 1) for mask in range(8))
    for chosen in product(range(8), repeat=3):
        family = tuple(subsets[index] for index in chosen)
        costs = (4, 2, 1)
        direct = None
        for selected in product((False, True), repeat=3):
            cover = frozenset().union(*(members for members, yes in zip(family, selected) if yes))
            if cover == universe:
                cost = sum(c for c, yes in zip(costs, selected) if yes)
                direct = cost if direct is None else min(direct, cost)
        problem = set_cover_problem(3, family, costs)
        assert all(edge.source < edge.target for edge in problem.transitions)
        assert problem.key_fibres == (0, 0, 1, 1, 2, 2)
        result = synthesize(problem)
        assert result["minimum_cost"] == direct
        assert verify_certificate(result, problem)["status"] == "PASS"


def test_empty_universe_uncovered_element_and_large_integer_costs():
    empty = synthesize(set_cover_problem(0, ((),), (10,)))
    assert empty["minimum_cost"] == 0
    impossible = synthesize(set_cover_problem(1, (), ()))
    assert impossible["status"] == "infeasible"
    assert verify_certificate(impossible)["status"] == "PASS"
    exact = 2 ** 128 + 17
    huge = synthesize(set_cover_problem(2, ((0, 1), (0,), (1,)), (exact, exact - 1, exact)))
    assert huge["minimum_cost"] == exact
    assert verify_certificate(huge)["status"] == "PASS"
