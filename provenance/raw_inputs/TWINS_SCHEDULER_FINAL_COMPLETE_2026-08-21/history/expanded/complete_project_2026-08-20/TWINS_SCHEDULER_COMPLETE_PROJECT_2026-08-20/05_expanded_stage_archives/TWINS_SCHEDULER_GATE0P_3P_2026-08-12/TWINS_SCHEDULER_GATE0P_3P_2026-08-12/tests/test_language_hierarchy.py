from schedcheck.engine import enumerate_all_grammars
from schedcheck.protocols import EchoGateProtocol, InstanceOrderProtocol, TwinBranchProtocol, TypeSplitProtocol

GRAMMARS = (
    "G_P_PARTITION",
    "G_D_DIRECTED_VIEW",
    "G_T_TYPE_SPECIFIC",
    "G_M_PER_MESSAGE",
)


def test_language_inclusions_hold_for_each_protocol() -> None:
    for protocol in (EchoGateProtocol(), TypeSplitProtocol(), InstanceOrderProtocol(), TwinBranchProtocol()):
        results = enumerate_all_grammars(protocol)
        for weaker, stronger in zip(GRAMMARS, GRAMMARS[1:]):
            assert results[weaker].observations <= results[stronger].observations


def test_partition_vs_directed_separation() -> None:
    results = enumerate_all_grammars(EchoGateProtocol())
    assert not results["G_P_PARTITION"].unsafe
    assert {obs.canonical_id() for obs in results["G_D_DIRECTED_VIEW"].unsafe} == {"A=0|B=1"}


def test_directed_vs_type_specific_separation() -> None:
    results = enumerate_all_grammars(TypeSplitProtocol())
    assert not results["G_D_DIRECTED_VIEW"].unsafe
    assert {obs.canonical_id() for obs in results["G_T_TYPE_SPECIFIC"].unsafe} == {
        "A=0|B=1",
        "A=1|B=0",
    }


def test_type_specific_vs_per_message_separation() -> None:
    results = enumerate_all_grammars(InstanceOrderProtocol())
    assert not results["G_T_TYPE_SPECIFIC"].unsafe
    assert {obs.canonical_id() for obs in results["G_M_PER_MESSAGE"].unsafe} == {
        "A=0|B=1",
        "A=1|B=0",
    }


def test_partition_positive_control_finds_twins_branch_split() -> None:
    results = enumerate_all_grammars(TwinBranchProtocol())
    assert {obs.canonical_id() for obs in results["G_P_PARTITION"].unsafe} == {
        "A=0|B=1",
        "A=1|B=0",
    }
