from __future__ import annotations

from schedcheck.grammars import DirectedPolicy, PartitionPolicy, TypeSpecificPolicy
from schedcheck.partitions import weak_component_partition


def partition_closure(
    nodes: tuple[str, ...],
    policy: DirectedPolicy,
) -> PartitionPolicy:
    """Least partition policy containing every directed edge as an undirected relation.

    The closure is the partition into weakly connected components.  It is the
    smallest equivalence relation that contains all endpoints connected by the
    directed schedule.
    """

    return PartitionPolicy(weak_component_partition(nodes, policy.edges))


def type_erasure_closure(policy: TypeSpecificPolicy) -> DirectedPolicy:
    """Forget message types and enable each endpoint pair used by any type."""

    return DirectedPolicy(
        frozenset((sender, receiver) for _, sender, receiver in policy.type_edges)
    )


def type_instance_closure(
    delivered_type_edges: frozenset[tuple[str, str, str]],
) -> TypeSpecificPolicy:
    """Enable every instance on each type-edge used by a per-message witness.

    Static execution then delivers all emitted instances for the enabled
    type-edge in canonical emission order.  This is a counterfactual closure,
    not a claim that every implementation has FIFO channels.
    """

    return TypeSpecificPolicy(delivered_type_edges)
