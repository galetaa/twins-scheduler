"""Independent scale/guard/replay and failure-boundary regression checks."""
from dataclasses import replace
from functools import lru_cache
import pytest
from twins_scheduler.scaled_protocol import (build_model, Engine, GuardedReplay, STAGES,
    FINE_KEYS, FIBRES, OPPORTUNITY_BOUND, EnumerationLimit, replay, initial_partition)
from twins_scheduler.transition_synthesis import synthesize, verify_certificate
from twins_scheduler.transition_abstraction import quotient, verify_simulation
from scripts.run_scaled_study import policy_oracle, run_schedule

@lru_cache(maxsize=5)
def model(variant='MISSING_LOCK_UPDATE', dependency='NONE'):
    return build_model(variant, dependency=dependency)

@lru_cache
def solution():
    return synthesize(model().problem)

def test_scaled_complete_graph():
    m = model()
    assert (len(m.problem.states), len(m.problem.transitions), len(m.problem.unsafe)) == (48201,55283,36)
    assert len(FIBRES) == 6 and len(FINE_KEYS) == 12 and OPPORTUNITY_BOUND == 23

def test_exact_unit_optimum():
    assert verify_certificate(solution(), expected_problem=model().problem)['minimum_cost'] == 2
    assert solution()['witness']['split'] == [0,3]

def test_guarded_independent_replay():
    w = solution()['witness']
    result = replay(model(),w['transitions'],w['policy'])
    assert result['decisions']['A'] == 0 and result['decisions']['C'] == 1
    assert all(result['audit'].values())
    assert all(len(c['signers']) >= 5 for c in result['certificates'])

def test_total_policy_oracle_and_no_single_control():
    oracle = policy_oracle(model().problem)
    assert oracle['total_policies'] == 4096 and oracle['unsafe_policies'] == 36
    assert oracle['minimum_cost'] == 2
    for row in oracle['policies']:
        if row['unsafe']:
            assert set(row['split']) & {0,1,2} and set(row['split']) & {3,4,5}

@pytest.mark.parametrize('variant',['BASELINE','ONLY_P0_MUTATED'])
def test_guarded_baselines_no_unsafe_state(variant):
    assert not model(variant).problem.unsafe

@pytest.mark.parametrize('dependency',['NO_CROSS_PREVOTE','NO_NIL_TIMEOUT_SUPPORT','NO_ROUND1_P1_PREVOTE'])
def test_dependency_removal_prevents_disagreement(dependency):
    assert not build_model(dependency=dependency).problem.unsafe

def test_timeout_order_changes_same_policy_result():
    policy=(True,False,True,False,True,True)*2
    assert run_schedule('MISSING_LOCK_UPDATE',policy)['unsafe']
    assert not run_schedule('MISSING_LOCK_UPDATE',policy,{9:(1,0),10:(1,0)})['unsafe']

def test_forbidden_second_target_no_solution():
    p = replace(model().problem,allowed_split=frozenset({0,1,2}))
    assert policy_oracle(p)['minimum_cost'] is None

def test_weighted_optimum():
    p = replace(model().problem,costs=(2,5,9,3,7,11))
    assert policy_oracle(p)['minimum_cost'] == 5
    assert verify_certificate(synthesize(p),expected_problem=p)['minimum_cost'] == 5

def test_quotient_covers_every_edge():
    m=model();mapping=initial_partition(m)
    abstract=quotient(m.problem,mapping)
    audit=verify_simulation(m.problem,abstract,mapping)
    assert audit['checked_concrete_transitions'] == 55283
    assert len(abstract.states) < len(m.problem.states)

def test_incomplete_export_cannot_certify_safety():
    with pytest.raises(EnumerationLimit):
        build_model(max_states=5)

@pytest.mark.parametrize('costs',[(1,1,1),(1,1,1,1,1,-1)])
def test_malformed_costs_rejected(costs):
    # Avoid expensive enumeration merely to test the existing Problem boundary.
    with pytest.raises(ValueError):
        replace(model().problem,costs=costs)

def test_mutation_set_restricted_to_declared_variants():
    with pytest.raises(ValueError):
        Engine('UNDECLARED')

def test_replay_rejects_changed_policy():
    w=solution()['witness'];policy=list(w['policy']);policy[0]=not policy[0]
    with pytest.raises(ValueError):
        replay(model(),w['transitions'],policy)

def test_replay_rejects_noncontiguous_path():
    w=solution()['witness']
    with pytest.raises(ValueError):
        replay(model(),w['transitions'][1:],w['policy'])
