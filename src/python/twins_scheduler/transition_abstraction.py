"""Check a labelled abstraction and transfer certified refinement bounds.

This is a finite *model-to-model* simulation checker.  It checks every concrete
input edge, not just a successful execution, and preserves the complete static
scheduler interface.  A concrete internal edge may stutter; an admission may
not disappear.  Arbitrary client code requires an additional correspondence
proof to the supplied concrete transition system.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterable, Sequence

from .transition_synthesis import Problem, SynthesisLimit, Transition, synthesize, verify_certificate


def _index(value: Any, bound: int, description: str) -> int:
    if type(value) is not int or not 0 <= value < bound:
        raise ValueError(f"{description} is outside the supplied model")
    return value


def _same_interface(concrete: Problem, abstract: Problem) -> None:
    for field in ("key_fibres", "costs", "allowed_split", "required_split"):
        if getattr(concrete, field) != getattr(abstract, field):
            raise ValueError(f"abstraction changes the scheduler interface: {field}")


def verify_simulation(
    concrete: Problem, abstract: Problem, state_map: Sequence[int],
) -> dict[str, Any]:
    """Verify an all-state forward simulation with internal stuttering.

    A one-edge/stutter map is a sufficient, decidable instance of the paper's
    finite-path simulation rule.  This verifier does not construct a map or
    infer semantic correctness of a model exporter.
    """
    _same_interface(concrete, abstract)
    mapping = tuple(state_map)
    if len(mapping) != len(concrete.states):
        raise ValueError("the simulation map must cover every concrete state")
    for state in mapping:
        _index(state, len(abstract.states), "abstract state")
    if mapping[concrete.initial] != abstract.initial:
        raise ValueError("the simulation does not relate the initial states")
    if any(mapping[state] not in abstract.unsafe for state in concrete.unsafe):
        raise ValueError("the abstraction hides a concrete unsafe state")
    abstract_edges = {
        (edge.source, edge.target, edge.key, edge.value)
        for edge in abstract.transitions
    }
    stutters = 0
    for index, edge in enumerate(concrete.transitions):
        source, target = mapping[edge.source], mapping[edge.target]
        if edge.key is None and source == target:
            stutters += 1
        elif (source, target, edge.key, edge.value) not in abstract_edges:
            raise ValueError(f"concrete transition {index} has no labelled abstract match")
    return {
        "status": "PASS", "kind": "all-edge-forward-simulation",
        "concrete_sha256": concrete.digest(), "abstract_sha256": abstract.digest(),
        "concrete_states": len(concrete.states), "abstract_states": len(abstract.states),
        "checked_concrete_transitions": len(concrete.transitions),
        "internal_stutters": stutters, "unsafe_states_preserved": len(concrete.unsafe),
    }


def quotient(concrete: Problem, state_map: Sequence[int]) -> Problem:
    """Build a sound existential quotient; the quotient may have spurious paths.

    Group numbers must be contiguous and every abstract group must be used.
    Only internal self-loops are removed; all visible admission labels remain.
    Grouping unsafe and safe states makes the entire abstract group unsafe.
    """
    mapping = tuple(state_map)
    if len(mapping) != len(concrete.states) or not mapping:
        raise ValueError("a quotient requires one group per concrete state")
    if any(type(group) is not int or group < 0 for group in mapping):
        raise ValueError("quotient groups must be nonnegative integers")
    groups = max(mapping) + 1
    if set(mapping) != set(range(groups)):
        raise ValueError("quotient groups must be contiguous and all used")
    projected: set[tuple[int, int, int | None, bool | None]] = set()
    for edge in concrete.transitions:
        source, target = mapping[edge.source], mapping[edge.target]
        if edge.key is None and source == target:
            continue
        projected.add((source, target, edge.key, edge.value))
    ordered = sorted(projected, key=lambda edge: (
        edge[0], edge[1], -1 if edge[2] is None else edge[2],
        -1 if edge[3] is None else int(edge[3])))
    abstract = Problem(
        tuple(f"group-{i}" for i in range(groups)), mapping[concrete.initial],
        frozenset(mapping[state] for state in concrete.unsafe),
        tuple(Transition(*edge, label=f"projected-{i}") for i, edge in enumerate(ordered)),
        concrete.key_fibres, concrete.costs, concrete.allowed_split, concrete.required_split,
    )
    verify_simulation(concrete, abstract, mapping)
    return abstract


def _verify_quotient_shape(concrete: Problem, abstract: Problem, mapping: Sequence[int]) -> None:
    """Check the existential quotient used by the policy-elimination argument.

    A general overapproximation suffices for the final optimum sandwich, but
    spurious-policy elimination additionally needs no invented quotient edge
    and no invented bad group.  This check reconstructs sets without calling
    the quotient generator.
    """
    if set(mapping) != set(range(len(abstract.states))):
        raise ValueError("the quotient map must cover every abstract state")
    if abstract.unsafe != frozenset(mapping[state] for state in concrete.unsafe):
        raise ValueError("quotient unsafe groups differ from projected concrete unsafety")
    projected = set()
    for edge in concrete.transitions:
        source, target = mapping[edge.source], mapping[edge.target]
        if source != target or edge.key is not None:
            projected.add((source, target, edge.key, edge.value))
    actual = {(edge.source, edge.target, edge.key, edge.value) for edge in abstract.transitions}
    if projected != actual:
        raise ValueError("quotient edges differ from projected concrete transitions")


def replay_unsafe_witness(concrete: Problem, transitions: Iterable[int]) -> dict[str, Any]:
    """Independently replay a concrete path and compute its least split cost.

    This code does not use the optimizer's product-state or replay helpers.
    Input edges encode protocol legality; protocol adapters can additionally
    replay their native/model guards before supplying the path.
    """
    state = concrete.initial
    assignment: dict[int, bool] = {}
    values_by_fibre: dict[int, set[bool]] = {}
    indices = tuple(transitions)
    for raw_index in indices:
        index = _index(raw_index, len(concrete.transitions), "witness edge")
        edge = concrete.transitions[index]
        if edge.source != state:
            raise ValueError("concrete witness violates protocol adjacency")
        if edge.key is not None:
            if edge.key in assignment and assignment[edge.key] != edge.value:
                raise ValueError("concrete witness changes a persistent fine-key decision")
            assignment[edge.key] = edge.value
            values_by_fibre.setdefault(concrete.key_fibres[edge.key], set()).add(edge.value)
        state = edge.target
    if state not in concrete.unsafe:
        raise ValueError("concrete witness does not end in an unsafe state")
    split = set(concrete.required_split)
    split.update(fibre for fibre, values in values_by_fibre.items() if len(values) > 1)
    if not split <= concrete.allowed_split:
        raise ValueError("concrete witness needs a disallowed split")
    # Complete each unsplit fibre uniformly.  Unseen split phases may be false.
    policy = []
    for key, fibre in enumerate(concrete.key_fibres):
        if key in assignment:
            policy.append(assignment[key])
        elif fibre not in split and values_by_fibre.get(fibre):
            policy.append(next(iter(values_by_fibre[fibre])))
        else:
            policy.append(False)
    return {
        "transitions": list(indices), "terminal": state, "policy": policy,
        "split": sorted(split), "cost": sum(concrete.costs[fibre] for fibre in split),
    }


def _policy_reachability(
    concrete: Problem, policy: Sequence[bool],
) -> tuple[list[int] | None, frozenset[int]]:
    values = tuple(policy)
    if len(values) != len(concrete.key_fibres) or any(type(value) is not bool for value in values):
        raise ValueError("a replay policy must give one Boolean per fine key")
    mixed = set(concrete.required_split)
    fibre_values: dict[int, set[bool]] = {}
    for key, value in enumerate(values):
        fibre_values.setdefault(concrete.key_fibres[key], set()).add(value)
    mixed.update(fibre for fibre, observations in fibre_values.items() if len(observations) > 1)
    if not mixed <= concrete.allowed_split:
        raise ValueError("the replay policy needs a disallowed split")
    outgoing: dict[int, list[tuple[int, Transition]]] = {}
    for index, edge in enumerate(concrete.transitions):
        outgoing.setdefault(edge.source, []).append((index, edge))
    previous: dict[int, tuple[int, int] | None] = {concrete.initial: None}
    queue = deque([concrete.initial])
    while queue:
        state = queue.popleft()
        if state in concrete.unsafe:
            path = []
            while previous[state] is not None:
                source, index = previous[state]
                path.append(index)
                state = source
            return list(reversed(path)), frozenset(previous)
        for index, edge in outgoing.get(state, []):
            if edge.key is not None and values[edge.key] != edge.value:
                continue
            if edge.target not in previous:
                previous[edge.target] = state, index
                queue.append(edge.target)
    return None, frozenset(previous)


def witness_under_policy(concrete: Problem, policy: Sequence[bool]) -> list[int] | None:
    """Find a concrete unsafe execution of one fixed total policy, if it exists.

    Plain model-state BFS suffices once the complete policy is fixed.  A None
    result rejects only this policy in the finite model, not all policies.
    """
    return _policy_reachability(concrete, policy)[0]


def _refine_by_reachable(mapping: Sequence[int], reachable: frozenset[int]) -> list[int]:
    groups: dict[tuple[int, bool], int] = {}
    result = []
    for state, group in enumerate(mapping):
        signature = group, state in reachable
        if signature not in groups:
            groups[signature] = len(groups)
        result.append(groups[signature])
    return result


def verify_optimality_bridge(
    concrete: Problem,
    abstract: Problem,
    state_map: Sequence[int],
    abstract_certificate: dict[str, Any],
    concrete_transitions: Sequence[int] | None = None,
) -> dict[str, Any]:
    """Check lower ≤ concrete optimum ≤ upper, or complete infeasibility.

    Equal bounds certify the concrete model's optimum without optimizing that
    model.  An unmatched abstract witness yields only a lower bound.  A caller
    cannot promote it to a concrete counterexample by giving a simulation map.
    """
    simulation = verify_simulation(concrete, abstract, state_map)
    certificate = verify_certificate(abstract_certificate, expected_problem=abstract)
    if certificate["claim"] == "infeasible":
        if concrete_transitions is not None:
            raise ValueError("an abstract infeasibility certificate cannot accompany a concrete unsafe witness")
        return {
            "status": "PASS", "claim": "concrete-infeasible",
            "lower_bound": None, "upper_bound": None,
            "simulation": simulation, "abstract_certificate": certificate,
            "concrete_witness": None,
        }
    lower = certificate["minimum_cost"]
    witness = (None if concrete_transitions is None
               else replay_unsafe_witness(concrete, concrete_transitions))
    upper = None if witness is None else witness["cost"]
    if upper is not None and upper < lower:
        raise ValueError("a concrete witness contradicts the abstract lower bound")
    claim = ("concrete-optimal" if lower == upper else
             "concrete-bounds" if upper is not None else "concrete-lower-bound-only")
    return {
        "status": "PASS", "claim": claim,
        "lower_bound": lower, "upper_bound": upper,
        "simulation": simulation, "abstract_certificate": certificate,
        "concrete_witness": witness,
    }


def synthesize_via_abstraction(
    concrete: Problem, initial_map: Sequence[int] | None = None, *,
    max_refinements: int | None = None, max_product_states: int = 2_000_000,
) -> dict[str, Any]:
    """Certifying refinement of state abstraction using entire false policies.

    Optimize a sound quotient, then execute its fixed policy on the concrete
    model.  If that policy is spurious, partition every current group by its
    membership in the concrete reachable set.  The new quotient eliminates
    the whole false policy: the image of that set is closed and has no unsafe
    states.  Each failed iteration strictly increases the number of groups,
    so at most |concrete.states|-|initial groups| refinements are possible.

    This is existential safety-counterexample synthesis, not a universal
    winning-controller game.  The algorithm never deletes a concrete edge.
    """
    if max_refinements is not None and (type(max_refinements) is not int or max_refinements < 0):
        raise ValueError("refinement limit must be a nonnegative integer")
    mapping = list(initial_map) if initial_map is not None else [0] * len(concrete.states)
    # Validate the initial partition before beginning the iteration history.
    quotient(concrete, mapping)
    iterations: list[dict[str, Any]] = []
    while True:
        abstract = quotient(concrete, mapping)
        certificate = synthesize(abstract, max_product_states=max_product_states)
        verify_certificate(certificate, expected_problem=abstract)
        item: dict[str, Any] = {
            "state_map": mapping, "abstract": abstract.to_dict(),
            "abstract_certificate": certificate,
        }
        iterations.append(item)
        if certificate["status"] == "infeasible":
            item["action"] = "certified-infeasible"
            bridge = verify_optimality_bridge(concrete, abstract, mapping, certificate)
            break
        path, reachable = _policy_reachability(concrete, certificate["witness"]["policy"])
        if path is not None:
            item["action"] = "matched-concrete-witness"
            item["concrete_transitions"] = path
            bridge = verify_optimality_bridge(concrete, abstract, mapping, certificate, path)
            if bridge["claim"] != "concrete-optimal":
                raise AssertionError("a concrete path under the optimal abstract policy must attain its bound")
            break
        item["action"] = "refine-false-policy"
        item["policy_reachable_states"] = sorted(reachable)
        refined = _refine_by_reachable(mapping, reachable)
        if len(set(refined)) <= len(set(mapping)):
            raise AssertionError("a false quotient policy must split a mixed reachable group")
        if max_refinements is not None and len(iterations) > max_refinements:
            raise SynthesisLimit("abstraction-refinement limit exhausted; result remains unknown")
        mapping = refined
    return {
        "schema": "transition-abstraction-run/v1", "concrete": concrete.to_dict(),
        "concrete_sha256": concrete.digest(), "iterations": iterations, "bridge": bridge,
    }


def verify_abstraction_run(
    result: dict[str, Any], expected_concrete: Problem | None = None,
) -> dict[str, Any]:
    """Independently check every saved bound and every policy-elimination step.

    Only the last all-edge simulation and matching bound/witness are needed
    for final optimality.  Checking the saved history additionally prevents
    unsupported claims about eliminated policies, progress and intermediate
    lower bounds.  No optimizer or abstraction-generation function is called.
    """
    if type(result) is not dict or result.get("schema") != "transition-abstraction-run/v1":
        raise ValueError("unknown abstraction-run schema")
    concrete = Problem.from_dict(result["concrete"])
    if concrete.digest() != result.get("concrete_sha256"):
        raise ValueError("concrete model hash does not match")
    if expected_concrete is not None and concrete.to_dict() != expected_concrete.to_dict():
        raise ValueError("abstraction run is bound to a different concrete model")
    iterations = result.get("iterations")
    if type(iterations) is not list or not iterations:
        raise ValueError("an abstraction run requires at least one iteration")
    previous_map = None
    previous_reachable = None
    previous_lower = None
    rejected = 0
    bridge = None
    for position, item in enumerate(iterations):
        abstract = Problem.from_dict(item["abstract"])
        mapping = item["state_map"]
        simulation = verify_simulation(concrete, abstract, mapping)
        _verify_quotient_shape(concrete, abstract, mapping)
        if previous_map is not None:
            # Every new group lies entirely within one old group and entirely
            # within or outside the previously rejected policy's reachable set.
            origins: dict[int, tuple[int, bool]] = {}
            for state, group in enumerate(mapping):
                signature = previous_map[state], state in previous_reachable
                if group in origins and origins[group] != signature:
                    raise ValueError("refinement mixes old groups or reachable-set classes")
                origins[group] = signature
            if len(set(mapping)) <= len(set(previous_map)):
                raise ValueError("a rejected policy must cause a strict partition refinement")
        certificate = item["abstract_certificate"]
        audit = verify_certificate(certificate, expected_problem=abstract)
        lower = audit["minimum_cost"]
        if lower is not None and previous_lower is not None and lower < previous_lower:
            raise ValueError("a recorded lower bound decreased during state refinement")
        last = position == len(iterations) - 1
        action = item.get("action")
        if action == "refine-false-policy":
            if last or audit["claim"] != "optimal":
                raise ValueError("a false-policy iteration requires a following refinement")
            policy = certificate["witness"]["policy"]
            claimed = item.get("policy_reachable_states")
            if type(claimed) is not list or len(set(claimed)) != len(claimed):
                raise ValueError("false policy requires distinct reachable-state indices")
            reachable = frozenset(_index(state, len(concrete.states), "policy reachable state") for state in claimed)
            if concrete.initial not in reachable or concrete.unsafe & reachable:
                raise ValueError("false-policy reachable set omits initial state or contains unsafety")
            # Closure is enough: a safe inductive overapproximation also proves
            # the policy false.  Exact BFS reachability is not trusted/required.
            for edge in concrete.transitions:
                if edge.source in reachable and (edge.key is None or policy[edge.key] == edge.value):
                    if edge.target not in reachable:
                        raise ValueError("false-policy reachable set omits a compatible successor")
            previous_map, previous_reachable, previous_lower = tuple(mapping), reachable, lower
            rejected += 1
        elif action == "matched-concrete-witness":
            if not last or audit["claim"] != "optimal":
                raise ValueError("a matching witness must finish the abstraction run")
            bridge = verify_optimality_bridge(concrete, abstract, mapping, certificate, item["concrete_transitions"])
            if bridge["claim"] != "concrete-optimal":
                raise ValueError("the final concrete witness does not attain the certified bound")
        elif action == "certified-infeasible":
            if not last or audit["claim"] != "infeasible":
                raise ValueError("infeasibility must finish the abstraction run")
            bridge = verify_optimality_bridge(concrete, abstract, mapping, certificate)
        else:
            raise ValueError("unknown abstraction iteration action")
    if result.get("bridge") != bridge:
        raise ValueError("claimed final bridge disagrees with independent verification")
    return {"status": "PASS", "claim": bridge["claim"],
            "minimum_cost": bridge["lower_bound"], "iterations": len(iterations),
            "eliminated_policies": rejected, "final_abstract_states": simulation["abstract_states"],
            "concrete_sha256": concrete.digest()}
