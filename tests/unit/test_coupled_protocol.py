"""Protocol, persistence and independent-oracle boundaries of the general LTS model."""

from dataclasses import replace
import pytest

from twins_scheduler.coupled_protocol import (
    Action, CoupledTrace, EnumerationLimit, FINE_KEYS, STAGES,
    apply_action, build_model, direct_policy_reachability,
    execution_record, exhaustive_policy_oracle, graph_policy_reachability, quotient_audit_order,
    replay_protocol_witness, run_policy_schedule, semantic_examples, spurious_quotient,
)
from twins_scheduler.transition_synthesis import synthesize, verify_certificate


@pytest.fixture(scope="module")
def coupled_model():
    return build_model()


def test_generated_quorums_require_both_controlled_prevote_contributions():
    for left, right, expected in ((True, False, False), (False, True, False), (True, True, True)):
        loop = CoupledTrace("MISSING_LOCK_UPDATE")
        apply_action(loop, STAGES[0][0])
        apply_action(loop, STAGES[1][0], True)
        apply_action(loop, Action("vote", ("A", "P", 0, "PREVOTE")), left)
        apply_action(loop, Action("vote", ("B", "P", 0, "PREVOTE")), right)
        emitted = loop.vote_envelope("P", "A", 0, "PRECOMMIT") is not None
        assert emitted is expected
        assert loop.replicas["P"].locked_value is None
        if expected:
            assert loop.replicas["P"].valid_value == 0
            certificate = next(row for row in loop.certificates if row["receiver"] == "P")
            assert certificate["signers"] == ["A", "B", "P"]


def test_proposal_uses_same_controlled_endpoint_fibre():
    loop = CoupledTrace("MISSING_LOCK_UPDATE")
    apply_action(loop, STAGES[0][0])
    apply_action(loop, STAGES[1][0], False)
    assert loop.replicas["P"].proposal_id is None
    assert loop.vote_envelope("P", "A", 0, "PREVOTE") is None
    assert FINE_KEYS[2] == "A->P:H1:R0:PROPOSAL"


def test_minimum_certificate_replays_real_guarded_votes(coupled_model):
    cert = synthesize(coupled_model.problem)
    assert cert["minimum_cost"] == 2
    assert cert["witness"]["split"] == [1]
    assert verify_certificate(cert, coupled_model.problem)["status"] == "PASS"
    execution = replay_protocol_witness(coupled_model, cert["witness"]["transitions"],
                                        cert["witness"]["policy"])
    assert execution["unsafe"]
    assert execution["decisions"] == {"A": 0, "C": 1}
    assert all(execution["audit"].values())
    commit_certificates = {(row["receiver"], row["value"]): row["signers"]
                           for row in execution["certificates"] if row["kind"] == "PRECOMMIT"}
    assert commit_certificates[("A", 0)] == ["A", "B", "P"]
    assert commit_certificates[("C", 1)] == ["B", "C", "P"]
    assert exhaustive_policy_oracle(coupled_model.problem)["minimum_cost"] == 2


def test_refinement_permissions_change_real_model_optimum(coupled_model):
    for allowed, expected in ((frozenset(), None), (frozenset({0}), 5), (frozenset({1}), 2)):
        problem = replace(coupled_model.problem, allowed_split=allowed)
        cert = synthesize(problem)
        assert cert["minimum_cost"] == expected
        assert exhaustive_policy_oracle(problem)["minimum_cost"] == expected
        assert verify_certificate(cert, problem)["status"] == "PASS"


def test_baseline_has_no_unsafe_states_in_complete_declared_domain():
    model = build_model("BASELINE")
    assert not model.problem.unsafe
    assert model.summary()["complete"]
    cert = synthesize(model.problem)
    assert cert["status"] == "infeasible"
    assert verify_certificate(cert, model.problem)["status"] == "PASS"


def test_audit_order_quotient_preserves_every_actual_transition(coupled_model):
    abstract, mapping = quotient_audit_order(coupled_model)
    assert len(abstract.states) < len(coupled_model.problem.states)
    edges = {(edge.source, edge.target, edge.key, edge.value) for edge in abstract.transitions}
    assert all((mapping[edge.source], mapping[edge.target], edge.key, edge.value) in edges
               for edge in coupled_model.problem.transitions)
    assert {mapping[state] for state in coupled_model.problem.unsafe} == abstract.unsafe
    assert synthesize(abstract)["minimum_cost"] == 2


@pytest.mark.parametrize("policy", [
    (False, False, False, False, False, False),
    (True, True, True, True, True, True),
    (True, True, True, True, False, False),
    (True, False, True, True, True, True),
])
def test_exported_graph_matches_independently_generated_guarded_run(coupled_model, policy):
    abstract, _ = quotient_audit_order(coupled_model)
    assert direct_policy_reachability(coupled_model.variant, policy) == graph_policy_reachability(abstract, policy)


def test_static_fine_key_cannot_change_after_cycle():
    problem = semantic_examples()["static_key_cycle"]
    # A graph-only search would take edges 0,1; a fixed policy cannot.
    assert problem.transitions[0].target == problem.transitions[1].source
    assert problem.transitions[1].target in problem.unsafe
    assert exhaustive_policy_oracle(problem)["minimum_cost"] is None
    assert synthesize(problem)["status"] == "infeasible"


def test_three_phases_and_repeated_key_pay_one_fibre_cost():
    problem = semantic_examples()["three_phase_paid_once"]
    cert = synthesize(problem)
    assert cert["minimum_cost"] == 7
    assert cert["witness"]["split"] == [0]
    assert len(cert["witness"]["transitions"]) == 4
    assert exhaustive_policy_oracle(problem)["minimum_cost"] == 7


def test_spurious_state_abstraction_is_only_a_lower_bound():
    concrete = semantic_examples()["spurious_state_merge"]
    abstract, mapping = spurious_quotient(concrete)
    assert mapping == (0, 0, 1)
    assert synthesize(concrete)["minimum_cost"] == 3
    assert synthesize(abstract)["minimum_cost"] == 0


def test_state_limit_returns_unknown_not_partial_safe_model():
    with pytest.raises(EnumerationLimit, match="unknown:.*no complete transition graph"):
        build_model(max_states=3)


def test_fixed_policy_has_safe_and_unsafe_orders_due_to_quorum_enabled_timeout():
    policy = (True, True, True, True, False, False)
    before = execution_record(run_policy_schedule(policy, stage_orders={6: (0, 1, 2)}))
    after = execution_record(run_policy_schedule(policy, stage_orders={6: (1, 0, 2)}))
    assert before["unsafe"]
    assert not after["unsafe"]
    assert all(before["audit"].values()) and all(after["audit"].values())
    assert any(row["action"] == "NO_ENABLED_TIMEOUT" and row["actor"] == "P"
               and row["timer"] == "PRECOMMIT" for row in after["log"])


def test_suppressing_both_precommits_removes_round_advance_despite_first_certificate():
    policy = (True, False, True, True, False, False)
    execution = execution_record(run_policy_schedule(policy))
    assert execution["decisions"] == {"A": 0}
    assert not execution["unsafe"]
    assert any(row["receiver"] == "A" and row["kind"] == "PRECOMMIT"
               and row["value"] == 0 for row in execution["certificates"])
    assert all(execution["audit"].values())


def test_repair_after_round_advance_requires_actual_block_data():
    policy = (True,) * len(FINE_KEYS)
    received = execution_record(run_policy_schedule(policy, stage_orders={6: (1, 0, 2)}))
    suppressed = execution_record(run_policy_schedule(policy[:-1] + (False,), stage_orders={6: (1, 0, 2)}))
    assert not received["unsafe"] and not suppressed["unsafe"]
    assert received["decisions"]["P"] == 0
    assert "P" not in suppressed["decisions"]
    assert any(row["action"] == "WAIT_COMMIT_BLOCK" and row["actor"] == "P"
               for row in received["log"])
    assert any(message["kind"] == "BLOCK" and message["signer"] == "A"
               for message in received["messages"])
    assert all(received["audit"].values()) and all(suppressed["audit"].values())


def test_replay_rejects_boolean_indices_and_non_boolean_admissions(coupled_model):
    loop = CoupledTrace("MISSING_LOCK_UPDATE")
    apply_action(loop, STAGES[0][0])
    with pytest.raises(ValueError, match="strict Boolean"):
        apply_action(loop, STAGES[1][0], 1)
    for indices in ([False], [-1]):
        with pytest.raises(ValueError, match="nonnegative integers"):
            replay_protocol_witness(coupled_model, indices, (True,) * len(FINE_KEYS))
