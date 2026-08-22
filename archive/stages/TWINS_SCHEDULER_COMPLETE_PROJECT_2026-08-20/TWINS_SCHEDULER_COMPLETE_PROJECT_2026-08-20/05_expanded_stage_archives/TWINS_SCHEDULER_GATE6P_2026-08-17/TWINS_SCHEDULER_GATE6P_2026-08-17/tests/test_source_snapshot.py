from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "inputs" / "hotstuff_snapshot"


def test_snapshot_contains_partition_semantics() -> None:
    network = (SNAPSHOT / "network.go").read_text(encoding="utf-8")
    assert "partition.Contains(sender) && partition.Contains(receiver)" in network
    assert "return ok" in network


def test_snapshot_records_controlled_message_types() -> None:
    scenario = (SNAPSHOT / "scenario.go").read_text(encoding="utf-8")
    for token in (
        "hotstuff.ProposeMsg{}",
        "hotstuff.VoteMsg{}",
        "hotstuff.NewViewMsg{}",
        "hotstuff.TimeoutMsg{}",
    ):
        assert token in scenario
