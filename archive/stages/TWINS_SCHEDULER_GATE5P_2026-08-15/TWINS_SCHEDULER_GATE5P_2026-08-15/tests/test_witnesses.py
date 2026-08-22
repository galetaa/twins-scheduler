from schedcheck.engine import (
    enumerate_all_grammars,
    simulate_static,
)
from schedcheck.grammars import DirectedPolicy, PartitionPolicy, TypeSpecificPolicy
from schedcheck.partitions import weak_component_partition
from schedcheck.protocols import EchoGateProtocol, InstanceOrderProtocol, TypeSplitProtocol


def _unsafe_witness(result):
    obs = min(result.unsafe, key=lambda item: item.canonical_id())
    return result.witnesses[obs]


def test_partition_closure_kills_directed_witness() -> None:
    protocol = EchoGateProtocol()
    witness = _unsafe_witness(enumerate_all_grammars(protocol)["G_D_DIRECTED_VIEW"])
    assert witness.schedule_id == "L>A,L>B"
    closure = weak_component_partition(protocol.nodes, frozenset({("L", "A"), ("L", "B")}))
    closed = simulate_static(protocol, PartitionPolicy(closure))
    assert not closed.observation.unsafe()
    assert closed.observation.canonical_id() == "A=-|B=-"


def test_type_erasure_closure_kills_type_specific_witness() -> None:
    protocol = TypeSplitProtocol()
    witness = _unsafe_witness(enumerate_all_grammars(protocol)["G_T_TYPE_SPECIFIC"])
    assert witness.observation.canonical_id() == "A=0|B=1"
    closed = simulate_static(protocol, DirectedPolicy(frozenset({("L", "A"), ("L", "B")})))
    assert closed.observation.canonical_id() == "A=0|B=0"


def test_fifo_instance_closure_kills_per_message_witness() -> None:
    protocol = InstanceOrderProtocol()
    witness = _unsafe_witness(enumerate_all_grammars(protocol)["G_M_PER_MESSAGE"])
    assert witness.observation.canonical_id() == "A=0|B=1"
    closed = simulate_static(
        protocol,
        TypeSpecificPolicy(
            frozenset({("CERT", "L", "A"), ("CERT", "L", "B")})
        ),
    )
    assert closed.observation.canonical_id() == "A=0|B=0"
