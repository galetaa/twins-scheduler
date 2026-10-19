import pytest

from twins_scheduler.repair_frontier import (
    Domain, acyclic, coarse_boundary, common_deadline, execute, from_graph,
    minimum_phase_splits, subsets, weighted_common_boundary,
)


def test_repair_after_signature_cannot_revoke_output():
    domain = from_graph(1, [])
    run = execute(domain, {0}, (("V", 0), ("R", 0)))
    assert run.repaired_at_end == {0}
    assert run.second_signers == {0}
    assert run.violates(1, 1)
    assert not execute(domain, {0}, (("R", 0), ("V", 0))).violates(1, 1)


def test_closed_channel_keeps_initially_ready_pivot_available():
    domain = from_graph(1, [(0, 0)])
    run = execute(domain, set(), next(domain.orders()))
    assert run.first_signers == set()
    assert run.second_signers == {0}
    assert not run.violates(1, 1)


def test_readiness_changes_multi_pivot_reachability():
    initial = from_graph(2, [(0, 0), (1, 1)])
    gated = Domain(initial.weights, initial.precedence, initially_ready=False)
    assert any(execute(initial, opened, order).violates(1, 1)
               for order in initial.orders() for opened in subsets(2))
    assert all(not execute(gated, opened, order).violates(1, 1)
               for order in gated.orders() for opened in subsets(2))


def test_individually_delayable_repairs_can_conflict_jointly():
    domain = from_graph(2, [(0, 1), (1, 0)])
    assert domain.acyclic_capacity() == 1
    assert all(not execute(domain, {0, 1}, order).violates(2, 2) for order in domain.orders())
    for i in range(2):
        assert any(i in execute(domain, {0, 1}, order).second_signers for order in domain.orders())
    assert any(execute(domain, {0, 1}, order, {0}).violates(2, 2) for order in domain.orders())


def test_weighted_granularity_blocks_total_weight_shortcut():
    weights = (2, 2)
    domain = common_deadline(2, {0, 1}, weights)
    assert 1 + 3 == sum(weights)
    assert not weighted_common_boundary(weights, {0, 1}, 1, 3)
    assert all(
        not execute(domain, opened, order).violates(1, 3)
        for order in domain.orders() for opened in subsets(2)
    )


def test_order_and_delivery_legality_are_checked():
    domain = from_graph(1, [(0, 0)])
    with pytest.raises(ValueError, match="linear extension"):
        execute(domain, {0}, (("V", 0), ("R", 0)))
    with pytest.raises(ValueError, match="exactly once"):
        execute(domain, {0}, (("R", 0), ("R", 0)))
    with pytest.raises(ValueError, match="split channels"):
        execute(domain, set(), next(domain.orders()), {0})
    with pytest.raises(ValueError, match="acyclic"):
        Domain((1,), frozenset({(("R", 0), ("V", 0)), (("V", 0), ("R", 0))}))


def test_transitive_order_is_used_in_repair_graph():
    domain = Domain((1, 1), frozenset({(("R", 0), ("R", 1)), (("R", 1), ("V", 0))}))
    assert (0, 0) in domain.repair_graph()
    assert not acyclic({0}, domain.repair_graph())


def test_phase_budget_and_infeasible_fine_witness():
    assert minimum_phase_splits(3, 1, 3, 3) == 2
    assert minimum_phase_splits(3, 1, 2, 2) == 0
    assert minimum_phase_splits(3, 1, 4, 1) is None
    assert not coarse_boundary(3, 1, 3, 3)
    assert coarse_boundary(3, 1, 2, 2)
