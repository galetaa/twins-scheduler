#!/usr/bin/env python3
"""Exact bounded Tendermint/CometBFT-style quorum-pivot instantiation.

This is a rule-level model pinned to the CometBFT v0.39.3 consensus
specification.  It is not production-client conformance and does not claim a
vulnerability.  The only scheduler-controlled degree of freedom is admission
of one sender->pivot edge at one height/round.  Phase-specific admission may
accept the enabling PREVOTE and reject the repair PRECOMMIT; the type-uniform
directed grammar must accept or reject both.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import json
from pathlib import Path
from typing import Iterable


class Variant(str, Enum):
    BASELINE = "BASELINE"
    MISSING_LOCK_UPDATE = "MISSING_LOCK_UPDATE"


class Grammar(str, Enum):
    PHASE_SPECIFIC = "G_T_PHASE_SPECIFIC"
    DIRECTED_EDGE_OFF = "G_D_EDGE_OFF"
    DIRECTED_EDGE_ON = "G_D_EDGE_ON"


@dataclass(frozen=True)
class Envelope:
    sender: str
    receiver: str
    height: int
    round: int
    phase: str
    value: int


@dataclass
class PivotState:
    height: int = 1
    locked_value: int | None = None
    locked_round: int | None = None
    decided_value: int | None = None
    saw_polka0: bool = False
    emitted_precommit0: bool = False
    emitted_precommit1: bool = False


@dataclass(frozen=True)
class Result:
    f: int
    n: int
    q: int
    variant: str
    grammar: str
    E_delivered: bool
    R_delivered: bool
    certificate0: bool
    certificate1: bool
    left_decision: int | None
    right_decision: int | None
    pivot_locked_value: int | None
    pivot_decided_value: int | None
    agreement_violation: bool


def admissions(grammar: Grammar) -> tuple[bool, bool]:
    """Return admission for E=PREVOTE and R=PRECOMMIT on the shared edge."""
    if grammar is Grammar.PHASE_SPECIFIC:
        return True, False
    if grammar is Grammar.DIRECTED_EDGE_OFF:
        return False, False
    if grammar is Grammar.DIRECTED_EDGE_ON:
        return True, True
    raise AssertionError(grammar)


def execute(f: int, variant: Variant, grammar: Grammar) -> Result:
    if f < 1:
        raise ValueError("f must be at least one")
    n = 3 * f + 1
    q = 2 * f + 1
    base0 = 2 * f  # B union A
    base1 = 2 * f  # B union C
    E_delivered, R_delivered = admissions(grammar)
    p = PivotState()

    # Fixed phase order at one height: E < C0 < R < C1.
    # E is the last PREVOTE on b->p at (H,0), completing a PoLC for value 0.
    if E_delivered:
        p.saw_polka0 = True
        p.emitted_precommit0 = True
        if variant is Variant.BASELINE:
            p.locked_value = 0
            p.locked_round = 0
        # The controlled mutation omits exactly this persistent lock update.

    certificate0 = base0 + int(p.emitted_precommit0) >= q
    left_decision = 0 if certificate0 else None

    # R is the last PRECOMMIT on the same b->p edge and same (H,0).
    # It completes a local +2/3 precommit set, so p enters Commit/NewHeight.
    if R_delivered and p.saw_polka0:
        p.decided_value = 0
        p.height = 2

    # At C1 (same height H=1, later round 1), p can support value 1 only if it
    # has neither committed height 1 nor retained a conflicting lock.
    pivot_available_for_value1 = (
        p.height == 1 and p.decided_value is None and p.locked_value is None
    )
    p.emitted_precommit1 = pivot_available_for_value1
    certificate1 = base1 + int(p.emitted_precommit1) >= q
    right_decision = 1 if certificate1 else None

    violation = left_decision == 0 and right_decision == 1
    return Result(
        f=f,
        n=n,
        q=q,
        variant=variant.value,
        grammar=grammar.value,
        E_delivered=E_delivered,
        R_delivered=R_delivered,
        certificate0=certificate0,
        certificate1=certificate1,
        left_decision=left_decision,
        right_decision=right_decision,
        pivot_locked_value=p.locked_value,
        pivot_decided_value=p.decided_value,
        agreement_violation=violation,
    )


def verify_refinement_family(fs: Iterable[int]) -> list[Result]:
    rows: list[Result] = []
    for f in fs:
        for variant in Variant:
            for grammar in Grammar:
                rows.append(execute(f, variant, grammar))

        by = {(r.variant, r.grammar): r for r in rows if r.f == f}
        # Correct lock update is safe in every grammar.
        assert all(
            not by[(Variant.BASELINE.value, g.value)].agreement_violation
            for g in Grammar
        )
        # Missing lock update is exposed only by phase-specific admission.
        assert by[(Variant.MISSING_LOCK_UPDATE.value, Grammar.PHASE_SPECIFIC.value)].agreement_violation
        assert not by[(Variant.MISSING_LOCK_UPDATE.value, Grammar.DIRECTED_EDGE_OFF.value)].agreement_violation
        assert not by[(Variant.MISSING_LOCK_UPDATE.value, Grammar.DIRECTED_EDGE_ON.value)].agreement_violation
    return rows


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "results" / "final"
    out.mkdir(parents=True, exist_ok=True)
    rows = verify_refinement_family(range(1, 65))
    (out / "cometbft_refinement_results.json").write_text(
        json.dumps([asdict(r) for r in rows], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {
        "source_protocol": "CometBFT v0.39.3 consensus specification",
        "scope": "bounded rule-level instantiation; not production-client conformance",
        "phase_order": ["E_PREVOTE", "C0", "R_PRECOMMIT", "C1"],
        "shared_edge": {
            "sender": "b0",
            "receiver": "pivot",
            "height": 1,
            "round": 0,
            "different_phases": ["PREVOTE", "PRECOMMIT"],
        },
        "f_checked": [1, 64],
        "cases": len(rows),
        "baseline_safe_all": True,
        "mutant_phase_specific_unsafe_all": True,
        "mutant_directed_safe_all": True,
    }
    (out / "cometbft_refinement_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("COMETBFT_BOUNDED_REFINEMENT PASS")
    print(f"cases={len(rows)} f=1..64")
    print("baseline_safe_all=true")
    print("missing_lock_update_phase_specific_unsafe_all=true")
    print("missing_lock_update_directed_safe_all=true")


if __name__ == "__main__":
    main()
