"""Small reductions with explicit meanings for the general transition model."""

from __future__ import annotations

from typing import Iterable

from .transition_synthesis import Problem, Transition


def set_cover_problem(universe_size: int, sets: Iterable[Iterable[int]],
                      costs: Iterable[int]) -> Problem:
    """Reduce minimum-weight Set Cover to static phase-refinement synthesis.

    A forced prefix observes False at a first fine key for each set.  One
    following layer per universe element chooses a containing set by observing
    True at its second fine key.  Choosing that set therefore costs one split,
    however many elements reuse it.  The graph is acyclic and each coarse fibre
    has exactly two fine keys.  Costs are preserved exactly.
    """
    if type(universe_size) is not int or universe_size < 0:
        raise ValueError("universe size must be a nonnegative integer")
    family = []
    for members in sets:
        members = tuple(members)
        if any(type(element) is not int or element < 0 or element >= universe_size
               for element in members):
            raise ValueError("set member is outside the declared universe")
        family.append(frozenset(members))
    costs = tuple(costs)
    if len(costs) != len(family):
        raise ValueError("one cost is required for each set")
    m = len(family)
    edges = [Transition(j, j + 1, 2 * j, False, f"baseline set {j}") for j in range(m)]
    for element in range(universe_size):
        for j, members in enumerate(family):
            if element in members:
                edges.append(Transition(m + element, m + element + 1, 2 * j + 1, True,
                                        f"cover element {element} by set {j}"))
    return Problem(tuple(f"cover stage {i}" for i in range(m + universe_size + 1)),
                   0, frozenset({m + universe_size}), tuple(edges),
                   tuple(j for j in range(m) for _ in range(2)), costs)
