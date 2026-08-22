from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from schedcheck.closures import partition_closure, type_erasure_closure, type_instance_closure
from schedcheck.engine import enumerate_all_grammars, simulate_static
from schedcheck.grammars import DirectedPolicy, TypeSpecificPolicy
from schedcheck.protocols import EchoGateProtocol, InstanceOrderProtocol, TwinBranchProtocol, TypeSplitProtocol

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "results" / "pilot"
GRAMMARS = (
    "G_P_PARTITION",
    "G_D_DIRECTED_VIEW",
    "G_T_TYPE_SPECIFIC",
    "G_M_PER_MESSAGE",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = args.output.resolve()
    protocols = (EchoGateProtocol(), TypeSplitProtocol(), InstanceOrderProtocol(), TwinBranchProtocol())
    all_results = {}
    for protocol in protocols:
        results = enumerate_all_grammars(protocol)
        all_results[protocol.name] = results
        for weaker, stronger in zip(GRAMMARS, GRAMMARS[1:]):
            require(
                results[weaker].observations <= results[stronger].observations,
                f"observation inclusion failed: {protocol.name} {weaker} <= {stronger}",
            )

    require(not all_results["ECHO_GATE"]["G_P_PARTITION"].unsafe, "partition unexpectedly finds EchoGate split")
    require(bool(all_results["ECHO_GATE"]["G_D_DIRECTED_VIEW"].unsafe), "directed witness missing")
    require(not all_results["TYPE_SPLIT"]["G_D_DIRECTED_VIEW"].unsafe, "directed unexpectedly finds type split")
    require(bool(all_results["TYPE_SPLIT"]["G_T_TYPE_SPECIFIC"].unsafe), "type-specific witness missing")
    require(not all_results["INSTANCE_ORDER"]["G_T_TYPE_SPECIFIC"].unsafe, "type grammar unexpectedly finds instance split")
    require(bool(all_results["INSTANCE_ORDER"]["G_M_PER_MESSAGE"].unsafe), "per-message witness missing")
    require(bool(all_results["TWIN_BRANCH_CONTROL"]["G_P_PARTITION"].unsafe), "partition positive control missing")

    echo = EchoGateProtocol()
    closed_echo = simulate_static(
        echo,
        partition_closure(echo.nodes, DirectedPolicy(frozenset({("L", "A"), ("L", "B")}))),
    )
    require(not closed_echo.observation.unsafe(), "partition closure should destroy EchoGate witness")

    type_split = TypeSplitProtocol()
    closed_type = simulate_static(
        type_split,
        type_erasure_closure(
            TypeSpecificPolicy(
                frozenset({("PRIMARY_CERT", "L", "A"), ("FALLBACK_CERT", "L", "B")})
            )
        ),
    )
    require(not closed_type.observation.unsafe(), "type erasure should destroy TypeSplit witness")

    instance = InstanceOrderProtocol()
    closed_instance = simulate_static(
        instance,
        type_instance_closure(frozenset({("CERT", "L", "A"), ("CERT", "L", "B")})),
    )
    require(not closed_instance.observation.unsafe(), "instance closure should destroy ordering witness")

    hierarchy = json.loads((out / "suite_hierarchy.json").read_text(encoding="utf-8"))
    require(hierarchy["all_inclusions_hold"], "serialized inclusion check failed")
    require(hierarchy["full_adjacent_safety_hierarchy_witnessed"], "serialized strict hierarchy failed")

    with (out / "language_summary.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 16, "language summary must contain 4 protocols x 4 grammars")

    print("SELF-CHECK PASS")
    print("claims=language_inclusions,adjacent_strictness,closure_counterfactuals,positive_control")


if __name__ == "__main__":
    main()
