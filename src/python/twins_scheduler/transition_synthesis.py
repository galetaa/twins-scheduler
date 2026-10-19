"""Certifying refinement synthesis for arbitrary finite transition systems.

Protocol transitions may depend on the entire protocol state.  An observable
decision is a Boolean admission at a *fine* scheduler key; repeated uses of a
fine key must agree.  Fine keys in one coarse fibre may disagree only when
that fibre is split.  This module imposes no independent-pivot, acyclicity,
quorum-additivity, or fixed-opportunity-order assumption.

The search remembers the partial static policy in the protocol-state product.
Its certificate is a concrete unsafe path and a closed strict-cost-sublevel
set.  The checker regenerates successors from the bound input, using separate
transition and policy code, and never invokes the optimizer.  An infeasibility
certificate requires a closed set containing every reachable product state.
Resource exhaustion raises SynthesisLimit and does not establish infeasibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from heapq import heappop, heappush
import json
from math import isfinite
from time import monotonic
from typing import Any, Iterable


def _natural(value: Any, description: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{description} must be a nonnegative integer")
    return value


def _indices(values: Iterable[int], description: str) -> frozenset[int]:
    values = tuple(values)
    for value in values:
        _natural(value, description)
    if len(set(values)) != len(values):
        raise ValueError(f"{description} contains duplicate indices")
    return frozenset(values)


@dataclass(frozen=True)
class Transition:
    source: int
    target: int
    key: int | None = None
    value: bool | None = None
    label: str = ""

    def __post_init__(self) -> None:
        _natural(self.source, "transition source")
        _natural(self.target, "transition target")
        if self.key is None:
            if self.value is not None:
                raise ValueError("an internal transition has neither key nor value")
        else:
            _natural(self.key, "fine key")
            if type(self.value) is not bool:
                raise ValueError("an admission value must be a JSON Boolean")
        if type(self.label) is not str:
            raise ValueError("transition labels must be strings")

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "target": self.target, "key": self.key,
                "value": self.value, "label": self.label}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Transition:
        if type(data) is not dict or set(data) - {"source", "target", "key", "value", "label"}:
            raise ValueError("unknown transition fields")
        if not {"source", "target"} <= set(data):
            raise ValueError("a transition requires source and target")
        return cls(data["source"], data["target"], data.get("key"),
                   data.get("value"), data.get("label", ""))


@dataclass(frozen=True)
class Problem:
    states: tuple[str, ...]
    initial: int
    unsafe: frozenset[int]
    transitions: tuple[Transition, ...]
    key_fibres: tuple[int, ...]
    costs: tuple[int, ...]
    allowed_split: frozenset[int] | None = None
    required_split: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        # Copy containers: a frozen dataclass alone does not freeze a supplied list.
        for field in ("states", "transitions", "key_fibres", "costs"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if not self.states or any(type(name) is not str or not name for name in self.states):
            raise ValueError("states require nonempty string names")
        if len(set(self.states)) != len(self.states):
            raise ValueError("state names must be unique")
        _natural(self.initial, "initial state")
        if self.initial >= len(self.states):
            raise ValueError("initial state does not exist")
        object.__setattr__(self, "unsafe", _indices(self.unsafe, "unsafe state"))
        if any(state >= len(self.states) for state in self.unsafe):
            raise ValueError("unsafe state does not exist")
        for cost in self.costs:
            _natural(cost, "split cost")
        for fibre in self.key_fibres:
            _natural(fibre, "coarse fibre")
            if fibre >= len(self.costs):
                raise ValueError("coarse fibre does not exist")
        for edge in self.transitions:
            if not isinstance(edge, Transition):
                raise ValueError("transitions must contain Transition objects")
            if max(edge.source, edge.target) >= len(self.states):
                raise ValueError("transition state does not exist")
            if edge.key is not None and edge.key >= len(self.key_fibres):
                raise ValueError("transition fine key does not exist")
        available = (frozenset(range(len(self.costs))) if self.allowed_split is None
                     else _indices(self.allowed_split, "allowed split"))
        required = _indices(self.required_split, "required split")
        object.__setattr__(self, "allowed_split", available)
        object.__setattr__(self, "required_split", required)
        if not required <= available <= frozenset(range(len(self.costs))):
            raise ValueError("required splits must be allowed and all fibres must exist")

    def to_dict(self) -> dict[str, Any]:
        return {"states": list(self.states), "initial": self.initial,
                "unsafe": sorted(self.unsafe),
                "transitions": [edge.to_dict() for edge in self.transitions],
                "key_fibres": list(self.key_fibres), "costs": list(self.costs),
                "allowed_split": sorted(self.allowed_split),
                "required_split": sorted(self.required_split)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Problem:
        fields = {"states", "initial", "unsafe", "transitions", "key_fibres", "costs",
                  "allowed_split", "required_split"}
        required = fields - {"allowed_split", "required_split"}
        if type(data) is not dict or set(data) - fields or not required <= set(data):
            raise ValueError("unknown or missing transition problem fields")
        for field in required - {"initial"}:
            if type(data[field]) is not list:
                raise ValueError(f"{field} must be a JSON array")
        for field in ("allowed_split", "required_split"):
            if field in data and type(data[field]) is not list:
                raise ValueError(f"{field} must be a JSON array")
        # Validate indices before taking sets: bool is an int subclass in Python.
        unsafe = _indices(data["unsafe"], "unsafe state")
        allowed = (None if "allowed_split" not in data
                   else _indices(data["allowed_split"], "allowed split"))
        required_split = _indices(data.get("required_split", []), "required split")
        return cls(tuple(data["states"]), data["initial"], unsafe,
                   tuple(Transition.from_dict(edge) for edge in data["transitions"]),
                   tuple(data["key_fibres"]), tuple(data["costs"]), allowed, required_split)

    def digest(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("utf-8")
        return sha256(payload).hexdigest()


@dataclass(frozen=True, order=True)
class ProductState:
    state: int
    assignment: tuple[int, ...]

    def __post_init__(self) -> None:
        _natural(self.state, "product protocol state")
        object.__setattr__(self, "assignment", tuple(self.assignment))
        if any(type(value) is not int or value not in (-1, 0, 1) for value in self.assignment):
            raise ValueError("partial policy values must be integers -1, 0, or 1")

    def to_dict(self) -> dict[str, Any]:
        return {"state": self.state, "assignment": list(self.assignment)}


class SynthesisLimit(RuntimeError):
    """The requested exploration/check exceeded a resource limit; result unknown."""


def _split_set(problem: Problem, assignment: tuple[int, ...]) -> frozenset[int]:
    seen = [0] * len(problem.costs)
    for key, value in enumerate(assignment):
        if value >= 0:
            seen[problem.key_fibres[key]] |= 1 << value
    return problem.required_split | frozenset(i for i, mask in enumerate(seen) if mask == 3)


def _product_cost(problem: Problem, node: ProductState) -> int:
    return sum(problem.costs[i] for i in _split_set(problem, node.assignment))


def _optimizer_step(problem: Problem, node: ProductState, edge: Transition) -> ProductState | None:
    if edge.source != node.state:
        return None
    if edge.key is None:
        return ProductState(edge.target, node.assignment)
    value = int(edge.value)
    previous = node.assignment[edge.key]
    if previous >= 0 and previous != value:
        return None
    assignment = list(node.assignment)
    assignment[edge.key] = value
    updated = tuple(assignment)
    if not _split_set(problem, updated) <= problem.allowed_split:
        return None
    return ProductState(edge.target, updated)


def product_successors(problem: Problem, node: ProductState) -> tuple[tuple[int, ProductState, int], ...]:
    """Public product semantics, including edge index and incremental split cost.

    This helper is convenient for adapters.  The certificate checker deliberately
    uses its own transition code instead of this helper.
    """
    if node.state >= len(problem.states) or len(node.assignment) != len(problem.key_fibres):
        raise ValueError("product state is outside the problem")
    if not _split_set(problem, node.assignment) <= problem.allowed_split:
        raise ValueError("product state uses a disallowed split")
    initial_cost = _product_cost(problem, node)
    result = []
    for edge_index, edge in enumerate(problem.transitions):
        successor = _optimizer_step(problem, node, edge)
        if successor is not None:
            result.append((edge_index, successor, _product_cost(problem, successor) - initial_cost))
    return tuple(result)


def replay_trace(problem: Problem, edge_indices: Iterable[int]) -> dict[str, Any]:
    """Replay one path and return its canonical complete policy and split set."""
    node = ProductState(problem.initial, (-1,) * len(problem.key_fibres))
    path = [node.to_dict()]
    indices = list(edge_indices)
    for index in indices:
        _natural(index, "witness transition index")
        if index >= len(problem.transitions):
            raise ValueError("witness transition does not exist")
        successor = _optimizer_step(problem, node, problem.transitions[index])
        if successor is None:
            raise ValueError("trace is not a policy-consistent path")
        node = successor
        path.append(node.to_dict())
    split = _split_set(problem, node.assignment)
    policy = list(node.assignment)
    for key, value in enumerate(policy):
        if value < 0:
            fibre = problem.key_fibres[key]
            common = next((v for f, v in zip(problem.key_fibres, node.assignment)
                           if f == fibre and v >= 0), 0)
            policy[key] = 0 if fibre in split else common
    return {"transitions": indices, "product_states": path,
            "policy": [bool(value) for value in policy], "split": sorted(split),
            "cost": sum(problem.costs[i] for i in split), "terminal": node.state}


def _budget(max_states: int, time_budget_seconds: float | None):
    if type(max_states) is not int or max_states < 1:
        raise ValueError("product-state limit must be a positive integer")
    if (time_budget_seconds is not None
            and (type(time_budget_seconds) not in (int, float)
                 or not isfinite(time_budget_seconds) or time_budget_seconds <= 0)):
        raise ValueError("time budget must be positive and finite")
    deadline = None if time_budget_seconds is None else monotonic() + time_budget_seconds

    def check() -> None:
        if deadline is not None and monotonic() >= deadline:
            raise SynthesisLimit("wall-clock budget exhausted; result remains unknown")

    return check


def synthesize(problem: Problem, *, max_product_states: int = 2_000_000,
               time_budget_seconds: float | None = None) -> dict[str, Any]:
    """Find the minimum-cost existential unsafe execution in a finite model.

    The number of product states is at most |states| * 3**|fine keys|.  All
    costs are nonnegative integers; cycles, zero-cost splits, and zero-cost
    internal transitions are supported.  A bound limits resources, never the
    set of executions silently.  No liveness/fairness or universal-controller
    objective is implied by the existential unsafe-state objective.
    """
    check_time = _budget(max_product_states, time_budget_seconds)
    initial = ProductState(problem.initial, (-1,) * len(problem.key_fibres))
    initial_cost = _product_cost(problem, initial)
    outgoing: list[list[tuple[int, Transition]]] = [[] for _ in problem.states]
    for index, edge in enumerate(problem.transitions):
        outgoing[edge.source].append((index, edge))
    distance = {initial: initial_cost}
    predecessor: dict[ProductState, tuple[ProductState, int]] = {}
    frontier = [(initial_cost, initial)]
    settled: set[ProductState] = set()
    terminal: ProductState | None = None
    examined = 0
    while frontier:
        check_time()
        cost, node = heappop(frontier)
        if node in settled:
            continue
        if node.state in problem.unsafe:
            terminal = node
            break
        settled.add(node)
        for index, edge in outgoing[node.state]:
            check_time()
            examined += 1
            successor = _optimizer_step(problem, node, edge)
            if successor is None:
                continue
            new_cost = _product_cost(problem, successor)
            if new_cost < cost:
                raise AssertionError("a persistent policy cannot lose a paid split")
            if successor not in distance:
                if len(distance) >= max_product_states:
                    raise SynthesisLimit("product-state limit exhausted; result remains unknown")
                distance[successor] = new_cost
                predecessor[successor] = (node, index)
                heappush(frontier, (new_cost, successor))
            elif distance[successor] != new_cost:
                raise AssertionError("product-state split cost must be path independent")
    check_time()
    result: dict[str, Any] = {
        "schema": "transition-refinement-certificate/v1", "problem": problem.to_dict(),
        "problem_sha256": problem.digest(),
    }
    if terminal is None:
        result.update(status="infeasible", minimum_cost=None, witness=None,
                      proof={"kind": "closed-reachable-set",
                             "states": [node.to_dict() for node in sorted(settled)]})
    else:
        minimum = distance[terminal]
        indices = []
        node = terminal
        while node != initial:
            node, index = predecessor[node]
            indices.append(index)
        indices.reverse()
        result.update(status="optimal", minimum_cost=minimum,
                      witness=replay_trace(problem, indices),
                      proof={"kind": "closed-strict-sublevel", "bound": minimum,
                             "states": [node.to_dict() for node in sorted(settled)
                                        if distance[node] < minimum]})
    result["statistics"] = {"discovered_product_states": len(distance),
                            "settled_nonunsafe_states": len(settled),
                            "examined_input_transitions": examined,
                            "certificate_states": len(result["proof"]["states"]),
                            "product_state_upper_bound": len(problem.states) * 3 ** len(problem.key_fibres)}
    return result


def verify_certificate(certificate: dict[str, Any], expected_problem: Problem | None = None,
                       *, max_checked_states: int = 2_000_000,
                       time_budget_seconds: float | None = None) -> dict[str, Any]:
    """Check a bound input, closed-set lower bound, and concrete unsafe witness.

    The successor loop below is independent of _optimizer_step,
    product_successors, replay_trace, and synthesize.  Neither claimed search
    statistics nor a certificate-provided edge list is trusted.  Supplying
    expected_problem is necessary to bind the result to an externally claimed
    model; the embedded SHA-256 alone binds only the self-contained input.
    """
    check_time = _budget(max_checked_states, time_budget_seconds)
    if type(certificate) is not dict or certificate.get("schema") != "transition-refinement-certificate/v1":
        raise ValueError("unknown transition certificate schema")
    try:
        problem = Problem.from_dict(certificate["problem"])
    except (KeyError, TypeError) as error:
        raise ValueError("malformed certificate input") from error
    if certificate.get("problem_sha256") != problem.digest():
        raise ValueError("certificate input hash does not match its problem")
    if expected_problem is not None and problem.to_dict() != expected_problem.to_dict():
        raise ValueError("certificate is bound to a different problem")
    status = certificate.get("status")
    minimum = certificate.get("minimum_cost")
    proof = certificate.get("proof")
    if type(proof) is not dict or type(proof.get("states")) is not list:
        raise ValueError("a certificate requires an explicit closed state set")
    if status == "optimal":
        _natural(minimum, "certified minimum")
        if (set(proof) != {"kind", "bound", "states"}
                or proof["kind"] != "closed-strict-sublevel"
                or type(proof["bound"]) is not int or proof["bound"] != minimum):
            raise ValueError("optimality requires the matching strict-sublevel bound")
    elif status == "infeasible":
        if (minimum is not None or certificate.get("witness") is not None
                or set(proof) != {"kind", "states"} or proof["kind"] != "closed-reachable-set"):
            raise ValueError("infeasibility requires an unbounded closed reachable set")
    else:
        raise ValueError("a certificate must establish optimality or complete infeasibility")
    if len(proof["states"]) > max_checked_states:
        raise SynthesisLimit("certificate-state limit exhausted; result remains unknown")

    # Checker representation intentionally uses raw tuples, not ProductState.
    def parse_node(data: Any) -> tuple[int, tuple[int, ...]]:
        if type(data) is not dict or set(data) != {"state", "assignment"}:
            raise ValueError("malformed certificate product state")
        state, values = data["state"], data["assignment"]
        _natural(state, "certificate protocol state")
        if state >= len(problem.states) or type(values) is not list or len(values) != len(problem.key_fibres):
            raise ValueError("certificate product state is outside the problem")
        if any(type(value) is not int or value not in (-1, 0, 1) for value in values):
            raise ValueError("partial policy values must be integers -1, 0, or 1")
        return state, tuple(values)

    def checked_splits(values: tuple[int, ...]) -> frozenset[int]:
        by_fibre: list[set[int]] = [set() for _ in problem.costs]
        for key in range(len(values)):
            if values[key] != -1:
                by_fibre[problem.key_fibres[key]].add(values[key])
        splits = set(problem.required_split)
        for fibre, observed in enumerate(by_fibre):
            if len(observed) == 2:
                splits.add(fibre)
        if not splits <= problem.allowed_split:
            raise ValueError("certificate product state uses a disallowed split")
        return frozenset(splits)

    def checked_cost(values: tuple[int, ...]) -> int:
        return sum(problem.costs[fibre] for fibre in checked_splits(values))

    def checked_step(node: tuple[int, tuple[int, ...]], edge: Transition):
        state, values = node
        if edge.source != state:
            return None
        if edge.key is None:
            return edge.target, values
        chosen = 1 if edge.value is True else 0
        if values[edge.key] != -1 and values[edge.key] != chosen:
            return None
        updated = tuple(chosen if key == edge.key else value
                        for key, value in enumerate(values))
        # A newly observed opposite value requires that coarse fibre to split.
        fibre = problem.key_fibres[edge.key]
        if fibre not in problem.allowed_split:
            for key, value in enumerate(updated):
                if problem.key_fibres[key] == fibre and value != -1 and value != chosen:
                    return None
        return edge.target, updated

    closed: set[tuple[int, tuple[int, ...]]] = set()
    for data in proof["states"]:
        check_time()
        node = parse_node(data)
        if node in closed:
            raise ValueError("duplicate certificate product state")
        if node[0] in problem.unsafe:
            raise ValueError("the closed lower-bound set contains an unsafe state")
        cost = checked_cost(node[1])
        if status == "optimal" and cost >= minimum:
            raise ValueError("lower-bound states must lie in the strict cost sublevel")
        closed.add(node)
    initial = problem.initial, (-1,) * len(problem.key_fibres)
    initial_cost = checked_cost(initial[1])
    if (status == "infeasible" or initial_cost < minimum) and initial not in closed:
        raise ValueError("the required initial product state is omitted")
    # Index raw input transitions independently; no certificate edges are used.
    outgoing: dict[int, list[Transition]] = {}
    for edge in problem.transitions:
        outgoing.setdefault(edge.source, []).append(edge)
    checked_edges = 0
    for node in sorted(closed):
        check_time()
        for edge in outgoing.get(node[0], []):
            check_time()
            checked_edges += 1
            successor = checked_step(node, edge)
            if successor is None:
                continue
            cost = checked_cost(successor[1])
            if (status == "infeasible" or cost < minimum) and successor not in closed:
                raise ValueError("closed-set successor is omitted from the lower-bound proof")

    replayed = 0
    if status == "optimal":
        witness = certificate.get("witness")
        fields = {"transitions", "product_states", "policy", "split", "cost", "terminal"}
        if type(witness) is not dict or set(witness) != fields:
            raise ValueError("an optimal certificate requires a complete path witness")
        if type(witness["transitions"]) is not list or type(witness["product_states"]) is not list:
            raise ValueError("witness transitions and product states must be arrays")
        if len(witness["product_states"]) != len(witness["transitions"]) + 1:
            raise ValueError("witness must include every path product state")
        node = initial
        if parse_node(witness["product_states"][0]) != node:
            raise ValueError("witness does not start in the initial product state")
        for position, index in enumerate(witness["transitions"]):
            check_time()
            _natural(index, "witness transition index")
            if index >= len(problem.transitions):
                raise ValueError("witness transition does not exist")
            successor = checked_step(node, problem.transitions[index])
            if successor is None:
                raise ValueError("witness violates protocol adjacency or persistent fine-key consistency")
            checked_splits(successor[1])
            if parse_node(witness["product_states"][position + 1]) != successor:
                raise ValueError("witness product state disagrees with replay")
            node = successor
            replayed += 1
        if type(witness["terminal"]) is not int or witness["terminal"] != node[0] or node[0] not in problem.unsafe:
            raise ValueError("witness does not end in an unsafe protocol state")
        if type(witness["split"]) is not list:
            raise ValueError("witness split set must be an array")
        split = _indices(witness["split"], "witness split")
        if not problem.required_split <= split <= problem.allowed_split:
            raise ValueError("witness split set violates allowed/required constraints")
        if not checked_splits(node[1]) <= split:
            raise ValueError("witness omits a mixed coarse fibre")
        paid = sum(problem.costs[fibre] for fibre in split)
        if type(witness["cost"]) is not int or witness["cost"] != paid or paid != minimum:
            raise ValueError("witness cost does not match its splits and certified minimum")
        policy = witness["policy"]
        if type(policy) is not list or len(policy) != len(problem.key_fibres) or any(type(value) is not bool for value in policy):
            raise ValueError("witness requires a total Boolean fine policy")
        common: dict[int, bool] = {}
        for key, value in enumerate(policy):
            if node[1][key] != -1 and int(value) != node[1][key]:
                raise ValueError("witness policy disagrees with a used fine-key value")
            fibre = problem.key_fibres[key]
            if fibre not in split:
                if fibre in common and common[fibre] != value:
                    raise ValueError("an unsplit fibre has differing policy values")
                common[fibre] = value
    check_time()
    return {"status": "PASS", "claim": status, "minimum_cost": minimum,
            "problem_sha256": problem.digest(), "checked_product_states": len(closed),
            "checked_input_transitions": checked_edges, "replayed_transitions": replayed}
