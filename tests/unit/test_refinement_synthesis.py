"""Behavioral, optimizer/oracle and malicious-certificate controls."""

from copy import deepcopy
from itertools import permutations, product

import pytest

from twins_scheduler.repair_frontier import Domain, from_graph
from twins_scheduler.refinement_synthesis import (
    Problem, SynthesisLimit, fixed_split_capacity, fixed_split_feasible,
    synthesize, verify_certificate,
)


def independent_minimum(domain, deficits, costs, allowed=None):
    """Enumerate event permutations and 3-state admissions, without H or DP."""
    allowed = set(range(domain.k)) if allowed is None else set(allowed)
    best = None
    for order in permutations(domain.events):
        index = {event: j for j, event in enumerate(order)}
        if any(index[a] >= index[b] for a, b in domain.precedence):
            continue
        for modes in product(range(3), repeat=domain.k):
            if any(mode == 2 and i not in allowed for i, mode in enumerate(modes)):
                continue
            first = sum(w for i, w in enumerate(domain.weights) if modes[i] != 0)
            repaired, issued = [False] * domain.k, [False] * domain.k
            for kind, i in order:
                if kind == "R" and modes[i] == 1:
                    repaired[i] = True
                if kind == "V" and not repaired[i]:
                    issued[i] = True
            second = sum(w for i, w in enumerate(domain.weights) if issued[i])
            if first >= deficits[0] and second >= deficits[1]:
                cost = sum(c for i, c in enumerate(costs) if modes[i] == 2)
                best = cost if best is None else min(best, cost)
    return best


def test_one_pivot_forced_and_post_signature_repair():
    forced = Problem(from_graph(1, [(0, 0)]), 1, 1, (1,))
    late = Problem(Domain((1,), frozenset({(("V", 0), ("R", 0))})), 1, 1, (1,))
    early_result, late_result = synthesize(forced), synthesize(late)
    assert early_result["minimum_cost"] == 1
    assert early_result["witness"]["split"] == [0]
    assert late_result["minimum_cost"] == 0
    assert late_result["witness"]["split"] == []
    assert late_result["witness"]["repaired_at_end"] == [0]
    assert late_result["witness"]["second_signers"] == [0]
    assert verify_certificate(early_result, forced)["status"] == "PASS"
    assert verify_certificate(late_result, late)["replayed_events"] == 2


def test_prescribed_sets_of_same_size_can_succeed_or_fail():
    domain = from_graph(3, [(0, 1), (1, 0)])
    assert fixed_split_capacity(domain, {2}) == 2
    assert fixed_split_capacity(domain, {1}) == 3
    assert not fixed_split_feasible(domain, {2}, 3, 3)
    assert fixed_split_feasible(domain, {1}, 3, 3)
    unavailable = synthesize(Problem(domain, 3, 3, (7, 2, 1), frozenset({2})))
    available = synthesize(Problem(domain, 3, 3, (7, 2, 1), frozenset({1})))
    assert unavailable["status"] == "infeasible"
    assert available["minimum_cost"] == 2
    assert verify_certificate(unavailable)["status"] == "PASS"
    assert verify_certificate(available)["status"] == "PASS"


def test_cost_optimal_can_use_more_keys_than_cardinality_optimal():
    domain = from_graph(3, [(0, 1), (1, 0), (0, 2), (2, 0)])
    result = synthesize(Problem(domain, 3, 3, (10, 1, 1)))
    cardinality = synthesize(Problem(domain, 3, 3, (1, 1, 1)))
    assert result["minimum_cost"] == 2
    assert result["witness"]["split"] == [1, 2]
    assert cardinality["minimum_cost"] == 1
    assert cardinality["witness"]["split"] == [0]
    assert verify_certificate(result)["status"] == "PASS"


def test_refinement_capacity_is_not_submodular():
    domain = from_graph(3, [(0, 1), (1, 0), (0, 2), (2, 0)])
    values = {frozenset(s): fixed_split_capacity(domain, s)
              for s in ((), (1,), (2,), (1, 2))}
    assert values[frozenset()] == 2
    assert values[frozenset({1})] == values[frozenset({2})] == 2
    assert values[frozenset({1, 2})] == 3
    # Submodularity would require the reverse weak inequality.
    assert values[frozenset({1})] + values[frozenset({2})] < (
        values[frozenset()] + values[frozenset({1, 2})]
    )


def test_weighted_granularity_and_zero_cost_are_supported():
    domain = from_graph(2, [(0, 0), (1, 1)], weights=(2, 2))
    assert synthesize(Problem(domain, 1, 3, (7, 1)))["minimum_cost"] == 1
    free = synthesize(Problem(domain, 1, 3, (7, 0)))
    assert free["minimum_cost"] == 0
    assert free["witness"]["split"] == [1]
    assert verify_certificate(free)["status"] == "PASS"


def test_suppressed_opportunity_keeps_transitive_constraints():
    domain = Domain((1, 1), frozenset({
        (("R", 0), ("R", 1)), (("R", 1), ("V", 0)),
    }))
    # Suppressing R_1 cannot remove the forced R_0 < V_0 path through its slot.
    result = synthesize(Problem(domain, 2, 2, (1, 1), frozenset({1})))
    assert result["status"] == "infeasible"
    assert verify_certificate(result)["status"] == "PASS"


def test_required_split_is_paid_even_for_zero_quotas():
    problem = Problem(from_graph(2, []), 0, 0, (5, 3), required_split=frozenset({0}))
    result = synthesize(problem)
    assert result["minimum_cost"] == 5
    assert result["witness"]["split"] == [0]
    assert verify_certificate(result, problem)["status"] == "PASS"


def test_independent_permutation_oracle_for_every_two_vertex_graph():
    edges = tuple(product(range(2), repeat=2))
    for mask in range(16):
        domain = from_graph(2, [edge for j, edge in enumerate(edges) if mask >> j & 1], weights=(1, 2))
        for deficits in ((1, 2), (2, 2), (3, 3), (0, 3), (4, 0)):
            for allowed in (frozenset(), frozenset({0}), frozenset({0, 1})):
                problem = Problem(domain, *deficits, (3, 1), allowed)
                result = synthesize(problem)
                assert result["minimum_cost"] == independent_minimum(domain, deficits, (3, 1), allowed)
                assert verify_certificate(result, problem)["status"] == "PASS"


def test_feasible_expensive_witness_cannot_forge_optimality():
    domain = from_graph(3, [(0, 1), (1, 0), (0, 2), (2, 0)])
    problem = Problem(domain, 3, 3, (10, 1, 1))
    forged = synthesize(problem)
    expensive = synthesize(Problem(domain, 3, 3, (10, 1, 1), required_split=frozenset({0})))
    forged["witness"] = expensive["witness"]  # This is a genuinely feasible cost-10 order.
    forged["minimum_cost"] = 10
    forged["proof"]["potentials"][0][-1] = 10
    with pytest.raises(ValueError, match="lower-bound inequality"):
        verify_certificate(forged, problem)


def test_checker_rejects_wrong_problem_missing_slot_and_forged_terminal():
    problem = Problem(from_graph(1, [(0, 0)]), 1, 1, (2,))
    result = synthesize(problem)
    with pytest.raises(ValueError, match="different problem"):
        verify_certificate(result, Problem(problem.domain, 1, 1, (3,)))
    missing = deepcopy(result)
    missing["witness"]["order"].pop(0)
    with pytest.raises(ValueError, match="opportunity slot"):
        verify_certificate(missing)
    terminal = deepcopy(result)
    terminal["proof"]["potentials"][-1][0] = 1
    with pytest.raises(ValueError, match="terminal potentials"):
        verify_certificate(terminal)


def test_unknown_contract_and_resource_exhaustion_are_not_unsat():
    with pytest.raises(ValueError, match="initially-ready"):
        Problem(Domain((1,), initially_ready=False), 1, 1, (1,))
    with pytest.raises(ValueError, match="nonnegative integer cost"):
        Problem(from_graph(1, []), 1, 1, (-1,))
    with pytest.raises(ValueError, match="unknown split key"):
        fixed_split_feasible(from_graph(1, []), {9}, 3, 3)
    domain = from_graph(3, [(0, 1), (1, 2), (2, 0)])
    with pytest.raises(SynthesisLimit, match="largest component"):
        synthesize(Problem(domain, 3, 3, (1, 1, 1)), max_component_size=2)
    with pytest.raises(SynthesisLimit, match="cell limit"):
        synthesize(Problem(domain, 3, 3, (1, 1, 1)), max_potential_cells=1)
    with pytest.raises(SynthesisLimit, match="wall-clock budget"):
        synthesize(Problem(domain, 3, 3, (1, 1, 1)), time_budget_seconds=1e-12)


def test_loop_vertices_are_removed_only_from_reversible_search():
    k = 24
    domain = from_graph(k, [(i, j) for i in range(k) for j in range(k)])
    result = synthesize(Problem(domain, k, k, (1,) * k), max_component_size=1)
    assert result["statistics"]["largest_component"] == 1
    assert result["minimum_cost"] == k
    assert len(result["witness"]["order"]) == 2 * k
    assert verify_certificate(result)["status"] == "PASS"
