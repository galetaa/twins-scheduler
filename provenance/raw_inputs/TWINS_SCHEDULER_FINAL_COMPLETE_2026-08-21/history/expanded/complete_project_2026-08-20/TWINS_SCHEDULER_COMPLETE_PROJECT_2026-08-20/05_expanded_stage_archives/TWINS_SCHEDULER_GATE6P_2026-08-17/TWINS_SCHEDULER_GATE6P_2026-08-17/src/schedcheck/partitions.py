from __future__ import annotations


def canonical_partition(blocks: tuple[tuple[str, ...], ...]) -> tuple[tuple[str, ...], ...]:
    normalized = [tuple(sorted(block)) for block in blocks if block]
    return tuple(sorted(normalized, key=lambda block: (block[0], len(block), block)))


def set_partitions(items: tuple[str, ...]) -> tuple[tuple[tuple[str, ...], ...], ...]:
    """Enumerate each set partition exactly once in canonical form."""

    if not items:
        return ((),)

    first, rest = items[0], items[1:]
    generated: set[tuple[tuple[str, ...], ...]] = set()
    for partition in set_partitions(rest):
        generated.add(canonical_partition(((first,),) + partition))
        for index in range(len(partition)):
            blocks = list(partition)
            blocks[index] = tuple(blocks[index]) + (first,)
            generated.add(canonical_partition(tuple(blocks)))
    return tuple(sorted(generated))


def weak_component_partition(
    nodes: tuple[str, ...],
    edges: frozenset[tuple[str, str]],
) -> tuple[tuple[str, ...], ...]:
    adjacency = {node: set() for node in nodes}
    for sender, receiver in edges:
        adjacency[sender].add(receiver)
        adjacency[receiver].add(sender)

    remaining = set(nodes)
    blocks: list[tuple[str, ...]] = []
    while remaining:
        root = min(remaining)
        stack = [root]
        component: set[str] = set()
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(adjacency[node] - component)
        remaining -= component
        blocks.append(tuple(sorted(component)))
    return canonical_partition(tuple(blocks))
