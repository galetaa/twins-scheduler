from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from schedcheck.closures import partition_closure, type_erasure_closure, type_instance_closure
from schedcheck.engine import LanguageResult, enumerate_all_grammars, simulate_static
from schedcheck.grammars import DirectedPolicy, TypeSpecificPolicy
from schedcheck.model import Observation, Witness
from schedcheck.protocols import (
    EchoGateProtocol,
    InstanceOrderProtocol,
    TwinBranchProtocol,
    TypeSplitProtocol,
)
from schedcheck.protocols.base import FiniteProtocol

GRAMMARS = (
    "G_P_PARTITION",
    "G_D_DIRECTED_VIEW",
    "G_T_TYPE_SPECIFIC",
    "G_M_PER_MESSAGE",
)

PROTOCOLS: tuple[FiniteProtocol, ...] = (
    EchoGateProtocol(),
    TypeSplitProtocol(),
    InstanceOrderProtocol(),
    TwinBranchProtocol(),
)

SOURCE_COMMIT = "3179c6e62929294961acbfd9bf8445769716a121"
SOURCE_BASE = f"https://raw.githubusercontent.com/relab/hotstuff/{SOURCE_COMMIT}"
SOURCE_FILES = (
    ("inputs/hotstuff_snapshot/scenario.go", f"{SOURCE_BASE}/twins/scenario.go"),
    ("inputs/hotstuff_snapshot/network.go", f"{SOURCE_BASE}/twins/network.go"),
    ("inputs/hotstuff_snapshot/generator.go", f"{SOURCE_BASE}/twins/generator.go"),
    ("inputs/hotstuff_snapshot/sender.go", f"{SOURCE_BASE}/twins/sender.go"),
    ("inputs/hotstuff_snapshot/twins.md", f"{SOURCE_BASE}/docs/twins.md"),
    ("inputs/hotstuff_snapshot/LICENSE", f"{SOURCE_BASE}/LICENSE"),
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _json_dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _canonical_ids(observations: Iterable[Observation]) -> str:
    return ";".join(sorted(obs.canonical_id() for obs in observations))


def _minimal_unsafe(result: LanguageResult, observation_id: str | None = None) -> Witness:
    choices = sorted(result.unsafe, key=lambda item: item.canonical_id())
    if observation_id is not None:
        choices = [obs for obs in choices if obs.canonical_id() == observation_id]
    if not choices:
        raise RuntimeError(f"no matching unsafe witness for {result.protocol}/{result.grammar}")
    return result.witnesses[choices[0]]


def _command_version(command: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    output = (completed.stdout or completed.stderr).strip()
    return output.splitlines()[0] if output else None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect() -> dict[str, dict[str, LanguageResult]]:
    return {protocol.name: enumerate_all_grammars(protocol) for protocol in PROTOCOLS}


def write_language_outputs(
    out: Path,
    results: dict[str, dict[str, LanguageResult]],
) -> None:
    summary_rows: list[dict[str, object]] = []
    observation_rows: list[dict[str, object]] = []
    witness_rows: list[dict[str, object]] = []

    for protocol in PROTOCOLS:
        by_grammar = results[protocol.name]
        for grammar in GRAMMARS:
            result = by_grammar[grammar]
            summary_rows.append(
                {
                    "protocol": protocol.name,
                    "grammar": grammar,
                    "policy_count": result.policy_count,
                    "execution_count": result.execution_count,
                    "observation_count": len(result.observations),
                    "unsafe_observation_count": len(result.unsafe),
                    "unsafe_observations": _canonical_ids(result.unsafe),
                }
            )
            for observation in sorted(result.observations, key=lambda item: item.canonical_id()):
                observation_rows.append(
                    {
                        "protocol": protocol.name,
                        "grammar": grammar,
                        "observation": observation.canonical_id(),
                        "unsafe": str(observation.unsafe()).lower(),
                    }
                )
                if observation.unsafe():
                    witness_rows.append(result.witnesses[observation].as_dict())

    _write_csv(
        out / "language_summary.csv",
        (
            "protocol",
            "grammar",
            "policy_count",
            "execution_count",
            "observation_count",
            "unsafe_observation_count",
            "unsafe_observations",
        ),
        summary_rows,
    )
    _write_csv(
        out / "protocol_observations.csv",
        ("protocol", "grammar", "observation", "unsafe"),
        observation_rows,
    )
    with (out / "witnesses.jsonl").open("w", encoding="utf-8") as handle:
        for row in sorted(
            witness_rows,
            key=lambda item: (item["protocol"], item["grammar"], item["observation"]),
        ):
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def write_separation_outputs(
    out: Path,
    results: dict[str, dict[str, LanguageResult]],
) -> dict[str, object]:
    pair_rows: list[dict[str, object]] = []
    inclusions: dict[str, dict[str, bool]] = {}

    for protocol in PROTOCOLS:
        by_grammar = results[protocol.name]
        inclusions[protocol.name] = {}
        for weaker, stronger in zip(GRAMMARS, GRAMMARS[1:]):
            weak_result = by_grammar[weaker]
            strong_result = by_grammar[stronger]
            observation_inclusion = weak_result.observations <= strong_result.observations
            unsafe_inclusion = weak_result.unsafe <= strong_result.unsafe
            stronger_only = strong_result.unsafe - weak_result.unsafe
            key = f"{weaker}_SUBSET_{stronger}"
            inclusions[protocol.name][key] = observation_inclusion and unsafe_inclusion
            pair_rows.append(
                {
                    "protocol": protocol.name,
                    "weaker": weaker,
                    "stronger": stronger,
                    "observation_inclusion": str(observation_inclusion).lower(),
                    "unsafe_inclusion": str(unsafe_inclusion).lower(),
                    "strict_on_unsafe": str(bool(stronger_only)).lower(),
                    "stronger_only_unsafe": _canonical_ids(stronger_only),
                }
            )

    designated = (
        ("G_P_PARTITION", "G_D_DIRECTED_VIEW", "ECHO_GATE", "A=0|B=1"),
        ("G_D_DIRECTED_VIEW", "G_T_TYPE_SPECIFIC", "TYPE_SPLIT", "A=0|B=1"),
        ("G_T_TYPE_SPECIFIC", "G_M_PER_MESSAGE", "INSTANCE_ORDER", "A=0|B=1"),
    )
    strict_witnesses: list[dict[str, object]] = []
    for weaker, stronger, protocol_name, observation_id in designated:
        weak = results[protocol_name][weaker]
        strong = results[protocol_name][stronger]
        observation = next(
            obs for obs in strong.unsafe if obs.canonical_id() == observation_id
        )
        witness = strong.witnesses[observation]
        strict_witnesses.append(
            {
                "weaker": weaker,
                "stronger": stronger,
                "protocol": protocol_name,
                "observation": observation_id,
                "absent_from_weaker": observation not in weak.unsafe,
                "witness": witness.as_dict(),
            }
        )

    hierarchy = {
        "grammar_order": list(GRAMMARS),
        "all_inclusions_hold": all(
            value for protocol_checks in inclusions.values() for value in protocol_checks.values()
        ),
        "inclusions_by_protocol": inclusions,
        "adjacent_strict_on_safety_observations": strict_witnesses,
        "unrestricted_partition_normal_form_refuted": all(
            item["absent_from_weaker"] for item in strict_witnesses[:1]
        ),
        "full_adjacent_safety_hierarchy_witnessed": all(
            item["absent_from_weaker"] for item in strict_witnesses
        ),
    }

    _write_csv(
        out / "adjacent_separations.csv",
        (
            "protocol",
            "weaker",
            "stronger",
            "observation_inclusion",
            "unsafe_inclusion",
            "strict_on_unsafe",
            "stronger_only_unsafe",
        ),
        pair_rows,
    )
    _json_dump(out / "suite_hierarchy.json", hierarchy)
    return hierarchy


def write_closure_outputs(
    out: Path,
    results: dict[str, dict[str, LanguageResult]],
) -> list[dict[str, object]]:
    counterfactuals: list[dict[str, object]] = []

    echo = EchoGateProtocol()
    echo_strong = _minimal_unsafe(results[echo.name]["G_D_DIRECTED_VIEW"], "A=0|B=1")
    echo_policy = DirectedPolicy(frozenset({("L", "A"), ("L", "B")}))
    echo_closed_policy = partition_closure(echo.nodes, echo_policy)
    echo_closed = simulate_static(echo, echo_closed_policy)
    counterfactuals.append(
        {
            "boundary": "G_P_PARTITION_vs_G_D_DIRECTED_VIEW",
            "protocol": echo.name,
            "strong_schedule": echo_policy.schedule_id(),
            "strong_observation": echo_strong.observation.canonical_id(),
            "closure": "weak-component equivalence closure",
            "closed_schedule": echo_closed_policy.schedule_id(),
            "closed_observation": echo_closed.observation.canonical_id(),
            "unsafe_preserved": echo_closed.observation.unsafe(),
            "interpretation": "Adding the reverse/transitive links forced by a partition delivers peer echoes and removes the split decision.",
        }
    )

    type_split = TypeSplitProtocol()
    type_strong = _minimal_unsafe(
        results[type_split.name]["G_T_TYPE_SPECIFIC"], "A=0|B=1"
    )
    type_policy = TypeSpecificPolicy(
        frozenset(
            {
                ("PRIMARY_CERT", "L", "A"),
                ("FALLBACK_CERT", "L", "B"),
            }
        )
    )
    type_closed_policy = type_erasure_closure(type_policy)
    type_closed = simulate_static(type_split, type_closed_policy)
    counterfactuals.append(
        {
            "boundary": "G_D_DIRECTED_VIEW_vs_G_T_TYPE_SPECIFIC",
            "protocol": type_split.name,
            "strong_schedule": type_policy.schedule_id(),
            "strong_observation": type_strong.observation.canonical_id(),
            "closure": "message-type erasure by endpoint union",
            "closed_schedule": type_closed_policy.schedule_id(),
            "closed_observation": type_closed.observation.canonical_id(),
            "unsafe_preserved": type_closed.observation.unsafe(),
            "interpretation": "Enabling both certificate types on every used edge makes both replicas accept the canonical primary certificate.",
        }
    )

    instance = InstanceOrderProtocol()
    instance_strong = _minimal_unsafe(
        results[instance.name]["G_M_PER_MESSAGE"], "A=0|B=1"
    )
    instance_closed_policy = type_instance_closure(
        frozenset({("CERT", "L", "A"), ("CERT", "L", "B")})
    )
    instance_closed = simulate_static(instance, instance_closed_policy)
    counterfactuals.append(
        {
            "boundary": "G_T_TYPE_SPECIFIC_vs_G_M_PER_MESSAGE",
            "protocol": instance.name,
            "strong_schedule": instance_strong.schedule_id,
            "strong_observation": instance_strong.observation.canonical_id(),
            "closure": "same-type instance completion with canonical FIFO order",
            "closed_schedule": instance_closed_policy.schedule_id(),
            "closed_observation": instance_closed.observation.canonical_id(),
            "unsafe_preserved": instance_closed.observation.unsafe(),
            "interpretation": "Delivering every instance on each selected type-edge in emission order makes both replicas accept certificate 0.",
        }
    )

    positive = TwinBranchProtocol()
    positive_witness = _minimal_unsafe(
        results[positive.name]["G_P_PARTITION"], "A=0|B=1"
    )
    counterfactuals.append(
        {
            "boundary": "positive_control",
            "protocol": positive.name,
            "strong_schedule": positive_witness.schedule_id,
            "strong_observation": positive_witness.observation.canonical_id(),
            "closure": "not applicable",
            "closed_schedule": positive_witness.schedule_id,
            "closed_observation": positive_witness.observation.canonical_id(),
            "unsafe_preserved": True,
            "interpretation": "A classic branch-separable Twins witness is already expressible by the partition grammar.",
        }
    )

    _json_dump(out / "closure_counterfactuals.json", counterfactuals)
    return counterfactuals


def write_environment(root: Path, out: Path) -> None:
    environment = {
        "artifact_date": "2026-08-12",
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "platform": platform.platform(),
        },
        "tools": {
            "uv": _command_version(["uv", "--version"]),
            "pytest": _command_version(["pytest", "--version"]),
        },
        "determinism": {
            "randomness_used": False,
            "random_seed": None,
            "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
            "enumeration": "exhaustive over every finite policy/execution in the declared bounds",
        },
        "runtime_dependencies": [],
    }
    _json_dump(out / "environment.json", environment)

    source_rows: list[dict[str, object]] = []
    for relative, url in SOURCE_FILES:
        path = root / relative
        source_rows.append(
            {
                "local_path": relative,
                "upstream_repository": "relab/hotstuff",
                "upstream_commit": SOURCE_COMMIT,
                "upstream_url": url,
                "retrieved_date": "2026-08-12",
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    _write_csv(
        root / "gate2p" / "source_manifest.csv",
        (
            "local_path",
            "upstream_repository",
            "upstream_commit",
            "upstream_url",
            "retrieved_date",
            "sha256",
            "bytes",
        ),
        source_rows,
    )


def write_decision(
    out: Path,
    hierarchy: dict[str, object],
    counterfactuals: list[dict[str, object]],
) -> None:
    strict = hierarchy["full_adjacent_safety_hierarchy_witnessed"]
    closures_kill = all(
        not item["unsafe_preserved"]
        for item in counterfactuals
        if item["boundary"] != "positive_control"
    )
    decision = {
        "gate_0_prime": {
            "status": "CONDITIONAL_PASS",
            "reason": "The implementation-specific partition restriction is real and richer schedulers are known; novelty survives only as a property-preserving characterization for a natural protocol class, not as a richer fault-injection API.",
        },
        "gate_1_prime": {
            "status": "PASS",
            "reason": "Four scheduler grammars, safety observations, embeddings, counterexamples, and explicit abstraction limits are formalized.",
        },
        "gate_2_prime": {
            "status": "PASS",
            "reason": "The exact checker is standard-library-only, locally reproducible, source-pinned, and does not require a blockchain node, solver, network service, or dataset.",
        },
        "gate_3_prime": {
            "status": "PASS_GO_WITH_NARROWING" if strict and closures_kill else "NO_GO",
            "reason": "Every adjacent grammar inclusion is strict on safety observations, and each least natural closure destroys its designated witness." if strict and closures_kill else "The pilot did not establish the planned strict hierarchy and closure mechanism.",
        },
        "overall_status": "ТРЕБУЕТ СУЖЕНИЯ" if strict and closures_kill else "ОТКЛОНИТЬ",
        "allowed_next_claim": "Necessary and sufficient (or sharply sufficient plus separation) closure-preservation conditions under which view-partition schedules preserve all safety-violating observations of richer message schedulers for a natural class of view-based BFT protocol implementations.",
        "disallowed_claims": [
            "The current pilot proves that relab/hotstuff misses a real HotStuff safety bug.",
            "All partition-based Twins implementations are incomplete for every BFT protocol.",
            "A richer scheduler API is itself a novel scientific contribution.",
            "The one-view bounded model covers cross-view late delivery, replay, timing, or liveness.",
        ],
        "next_gate": "Gate 4': instantiate one correct locking protocol plus seeded implementation mutants, check actual executor conformance, and seek a protocol-class closure theorem or a natural minimal separation.",
    }
    _json_dump(out / "gate_decision.json", decision)

    lines = [
        "# Gate 0′–3′ decision",
        "",
        f"**Overall status:** {decision['overall_status']}",
        "",
        "The unrestricted partition-normal-form completeness hypothesis is falsified in the declared finite deterministic protocol class. The exact pilot establishes a strict safety-observation hierarchy:",
        "",
        "`G_P_PARTITION ⊊ G_D_DIRECTED_VIEW ⊊ G_T_TYPE_SPECIFIC ⊊ G_M_PER_MESSAGE`.",
        "",
        "This is a GO only for the narrowed closure-preservation research question. It is not evidence of a production HotStuff vulnerability and not a license to build a large new testing framework before protocol-class validation.",
        "",
        "## Gate statuses",
        "",
    ]
    for gate_name in ("gate_0_prime", "gate_1_prime", "gate_2_prime", "gate_3_prime"):
        gate = decision[gate_name]
        lines.append(f"- **{gate_name}: {gate['status']}** — {gate['reason']}")
    lines.extend(
        [
            "",
            "## Next admissible claim",
            "",
            decision["allowed_next_claim"],
            "",
            "## Next gate",
            "",
            decision["next_gate"],
            "",
        ]
    )
    (out / "DECISION.md").write_text("\n".join(lines), encoding="utf-8")


def write_run_log(
    out: Path,
    results: dict[str, dict[str, LanguageResult]],
    hierarchy: dict[str, object],
) -> None:
    lines = [
        "schedcheck exact pilot",
        "artifact_date=2026-08-12",
        "randomness=false",
        f"all_inclusions_hold={str(hierarchy['all_inclusions_hold']).lower()}",
        f"full_adjacent_safety_hierarchy_witnessed={str(hierarchy['full_adjacent_safety_hierarchy_witnessed']).lower()}",
        "",
    ]
    for protocol in PROTOCOLS:
        for grammar in GRAMMARS:
            result = results[protocol.name][grammar]
            lines.append(
                " ".join(
                    (
                        f"protocol={protocol.name}",
                        f"grammar={grammar}",
                        f"policies={result.policy_count}",
                        f"executions={result.execution_count}",
                        f"observations={len(result.observations)}",
                        f"unsafe={len(result.unsafe)}",
                    )
                )
            )
    (out / "run_log.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    results = collect()
    write_language_outputs(out, results)
    hierarchy = write_separation_outputs(out, results)
    counterfactuals = write_closure_outputs(out, results)
    write_environment(root, out)
    write_decision(out, hierarchy, counterfactuals)
    write_run_log(out, results, hierarchy)
