from schedcheck.partitions import set_partitions, weak_component_partition


def test_three_node_bell_number() -> None:
    partitions = set_partitions(("L", "A", "B"))
    assert len(partitions) == 5
    assert (("A", "B", "L"),) in partitions
    assert (("A",), ("B",), ("L",)) in partitions


def test_weak_component_partition_closes_star() -> None:
    result = weak_component_partition(
        ("L", "A", "B"),
        frozenset({("L", "A"), ("L", "B")}),
    )
    assert result == (("A", "B", "L"),)
