from dataclasses import replace
from copy import deepcopy

import pytest

from twins_scheduler.transition_abstraction import (
    quotient, replay_unsafe_witness, verify_optimality_bridge,
    verify_simulation, witness_under_policy, synthesize_via_abstraction,
    verify_abstraction_run,
)
from twins_scheduler.transition_synthesis import Problem, SynthesisLimit, Transition, synthesize


def example():
    return Problem(
        ("start", "internal", "enabled", "unsafe"), 0, frozenset({3}),
        (Transition(0, 1), Transition(1, 2, 0, True), Transition(2, 3, 1, False)),
        (0, 0), (4,),
    )


def test_matching_abstract_bound_and_concrete_witness_certifies_optimum():
    concrete = example()
    mapping = [0, 0, 1, 2]
    abstract = quotient(concrete, mapping)
    certificate = synthesize(abstract)
    concrete_path = witness_under_policy(concrete, certificate["witness"]["policy"])
    assert concrete_path == [0, 1, 2]
    audit = verify_optimality_bridge(concrete, abstract, mapping, certificate, concrete_path)
    assert audit["claim"] == "concrete-optimal"
    assert audit["lower_bound"] == audit["upper_bound"] == 4
    assert audit["simulation"]["internal_stutters"] == 1
    assert audit["simulation"]["checked_concrete_transitions"] == 3


def test_spurious_abstract_witness_gives_only_lower_bound_then_refines():
    concrete = example()
    mapping = [0, 0, 0, 1]
    abstract = quotient(concrete, mapping)
    certificate = synthesize(abstract)
    assert certificate["minimum_cost"] == 0
    assert witness_under_policy(concrete, certificate["witness"]["policy"]) is None
    lower_only = verify_optimality_bridge(concrete, abstract, mapping, certificate)
    assert lower_only["claim"] == "concrete-lower-bound-only"
    bounded = verify_optimality_bridge(concrete, abstract, mapping, certificate, [0, 1, 2])
    assert bounded["claim"] == "concrete-bounds"
    assert (bounded["lower_bound"], bounded["upper_bound"]) == (0, 4)
    refined_map = [0, 0, 1, 2]
    refined = quotient(concrete, refined_map)
    exact = verify_optimality_bridge(concrete, refined, refined_map, synthesize(refined), [0, 1, 2])
    assert exact["claim"] == "concrete-optimal"


def test_infeasibility_transfers_without_concrete_search():
    concrete = replace(example(), allowed_split=frozenset())
    mapping = [0, 0, 1, 2]
    abstract = quotient(concrete, mapping)
    audit = verify_optimality_bridge(concrete, abstract, mapping, synthesize(abstract))
    assert audit["claim"] == "concrete-infeasible"


def test_checker_rejects_missing_edge_and_hidden_unsafe_state():
    concrete = example()
    mapping = [0, 0, 1, 2]
    abstract = quotient(concrete, mapping)
    with pytest.raises(ValueError, match="labelled abstract match"):
        verify_simulation(concrete, replace(abstract, transitions=abstract.transitions[:-1]), mapping)
    with pytest.raises(ValueError, match="hides a concrete unsafe"):
        verify_simulation(concrete, replace(abstract, unsafe=frozenset()), mapping)


def test_visible_admission_cannot_be_erased_as_stutter():
    concrete = Problem(("start", "later"), 0, frozenset(),
                       (Transition(0, 1, 0, True),), (0,), (1,))
    abstract = Problem(("one",), 0, frozenset(), (), (0,), (1,))
    with pytest.raises(ValueError, match="labelled abstract match"):
        verify_simulation(concrete, abstract, [0, 0])


def test_mapping_and_interface_must_preserve_full_problem():
    concrete = example()
    abstract = quotient(concrete, [0, 0, 1, 2])
    with pytest.raises(ValueError, match="cover every"):
        verify_simulation(concrete, abstract, [0, 0])
    with pytest.raises(ValueError, match="outside"):
        verify_simulation(concrete, abstract, [False, 0, 1, 2])
    with pytest.raises(ValueError, match="initial states"):
        verify_simulation(concrete, abstract, [1, 0, 1, 2])
    with pytest.raises(ValueError, match="scheduler interface: costs"):
        verify_simulation(concrete, replace(abstract, costs=(3,)), [0, 0, 1, 2])
    with pytest.raises(ValueError, match="scheduler interface: key_fibres"):
        verify_simulation(concrete, replace(abstract, key_fibres=(0, 0, 0)), [0, 0, 1, 2])


def test_expected_abstract_input_is_bound_to_checked_certificate():
    concrete = example()
    mapping = [0, 0, 1, 2]
    abstract = quotient(concrete, mapping)
    different = replace(abstract, states=("other-0", "other-1", "other-2"))
    with pytest.raises(ValueError, match="different problem"):
        verify_optimality_bridge(concrete, abstract, mapping, synthesize(different), [0, 1, 2])


def test_concrete_replay_rejects_adaptive_policy_and_nonunsafe_terminal():
    conflicting = Problem(("start", "mid", "bad"), 0, frozenset({2}),
                          (Transition(0, 1, 0, True), Transition(1, 2, 0, False)),
                          (0,), (4,))
    with pytest.raises(ValueError, match="persistent fine-key"):
        replay_unsafe_witness(conflicting, [0, 1])
    with pytest.raises(ValueError, match="unsafe state"):
        replay_unsafe_witness(example(), [0, 1])
    with pytest.raises(ValueError, match="adjacency"):
        replay_unsafe_witness(example(), [1, 2])
    assert witness_under_policy(conflicting, [True]) is None


def test_required_zero_costs_and_unused_keys_are_counted_once():
    concrete = Problem(("start", "mid", "bad"), 0, frozenset({2}),
                       (Transition(0, 1, 0, True), Transition(1, 2, 1, False)),
                       (0, 0, 1, 2), (0, 7, 9), required_split=frozenset({1}))
    witness = replay_unsafe_witness(concrete, [0, 1])
    assert witness["cost"] == 7
    assert witness["split"] == [0, 1]
    assert witness["policy"] == [True, False, False, False]


def test_iterative_abstraction_eliminates_false_policies_and_certifies_minimum(monkeypatch):
    concrete = example()
    run = synthesize_via_abstraction(concrete)
    assert len(run["iterations"]) > 1
    audit = verify_abstraction_run(run, expected_concrete=concrete)
    assert audit["claim"] == "concrete-optimal"
    assert audit["minimum_cost"] == 4
    assert audit["iterations"] <= len(concrete.states)
    # Verification is independent of both search and quotient construction.
    def forbidden(*args, **kwargs):
        raise AssertionError("checker must not invoke optimization or model construction")
    monkeypatch.setattr("twins_scheduler.transition_abstraction.synthesize", forbidden)
    monkeypatch.setattr("twins_scheduler.transition_abstraction.quotient", forbidden)
    monkeypatch.setattr("twins_scheduler.transition_abstraction._policy_reachability", forbidden)
    assert verify_abstraction_run(run, expected_concrete=concrete) == audit


def test_abstraction_refinement_safe_model_and_resource_cutoff():
    concrete = replace(example(), allowed_split=frozenset())
    run = synthesize_via_abstraction(concrete)
    assert verify_abstraction_run(run)["claim"] == "concrete-infeasible"
    with pytest.raises(SynthesisLimit, match="remains unknown"):
        synthesize_via_abstraction(example(), max_refinements=0)


def test_false_policy_certificate_cannot_omit_reachable_successor():
    concrete = example()
    run = synthesize_via_abstraction(concrete)
    forged = deepcopy(run)
    first = forged["iterations"][0]
    assert first["action"] == "refine-false-policy"
    first["policy_reachable_states"] = [0]
    with pytest.raises(ValueError, match="compatible successor"):
        verify_abstraction_run(forged, expected_concrete=concrete)


def test_abstraction_run_rejects_invented_quotient_edges_even_if_simulation_passes():
    concrete = example()
    run = synthesize_via_abstraction(concrete)
    forged = deepcopy(run)
    final = forged["iterations"][-1]
    abstract = Problem.from_dict(final["abstract"])
    # An extra internal loop preserves forward simulation and the optimum,
    # but is not in this algorithm's canonical existential quotient.
    abstract = replace(abstract, transitions=abstract.transitions + (Transition(0, 0),))
    final["abstract"] = abstract.to_dict()
    final["abstract_certificate"] = synthesize(abstract)
    with pytest.raises(ValueError, match="quotient edges differ"):
        verify_abstraction_run(forged)
