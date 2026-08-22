from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True, slots=True)
class QuorumConstruction:
    f: int
    n: int
    quorum: int
    byzantine: tuple[str, ...]
    pivot: str
    left_only: tuple[str, ...]
    right_only: tuple[str, ...]
    q0: tuple[str, ...]
    q1: tuple[str, ...]


def construct_quorums(f: int) -> QuorumConstruction:
    if f < 1:
        raise ValueError("f must be positive")
    byzantine = tuple(f"B{i}" for i in range(f))
    pivot = "P"
    left = tuple(f"A{i}" for i in range(f))
    right = tuple(f"C{i}" for i in range(f))
    q0 = byzantine + (pivot,) + left
    q1 = byzantine + (pivot,) + right
    return QuorumConstruction(
        f=f,
        n=3 * f + 1,
        quorum=2 * f + 1,
        byzantine=byzantine,
        pivot=pivot,
        left_only=left,
        right_only=right,
        q0=q0,
        q1=q1,
    )


def _simulate(construction: QuorumConstruction, *, mode: str) -> dict[str, object]:
    """Evaluate the symbolic two-round phase-coupled template.

    E is enabling evidence that makes the pivot emit the first-round vote but,
    under the defect, does not retain the intended lock. R is a later message on
    the same sender-to-pivot edge that disables the pivot's conflicting action
    by deciding or repairing its constraint.
    """
    f = construction.f
    q = construction.quorum
    base_q0 = f + f  # Byzantine set plus A-only honest set
    base_q1 = f + f  # Byzantine set plus C-only honest set

    outcomes: list[dict[str, object]] = []
    if mode == "TYPE_SPECIFIC":
        policies = ((True, False),)  # deliver E, omit R at pivot
    elif mode == "DIRECTED":
        policies = ((False, False), (True, True))  # endpoint edge couples E and R
    elif mode == "DELAY1":
        policies = ((True, "late"),)
    else:
        raise ValueError(mode)

    for e_delivered, r_delivery in policies:
        first_support = base_q0 + int(bool(e_delivered))
        first_certificate = first_support >= q
        pivot_disabled_before_round1 = r_delivery is True and first_certificate
        second_support = base_q1 + int(bool(e_delivered) and not pivot_disabled_before_round1)
        second_certificate = second_support >= q
        unsafe = first_certificate and second_certificate
        outcomes.append(
            {
                "E_to_pivot": bool(e_delivered),
                "R_to_pivot": r_delivery,
                "first_support": first_support,
                "second_support": second_support,
                "first_certificate": first_certificate,
                "second_certificate": second_certificate,
                "unsafe": unsafe,
            }
        )
    return {
        "mode": mode,
        "unsafe_reachable": any(item["unsafe"] for item in outcomes),
        "policies": outcomes,
    }


def phase_coupled_separation_check(max_f: int = 8) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    passed = True
    for f in range(1, max_f + 1):
        construction = construct_quorums(f)
        type_specific = _simulate(construction, mode="TYPE_SPECIFIC")
        directed = _simulate(construction, mode="DIRECTED")
        delay1 = _simulate(construction, mode="DELAY1")
        row = {
            **asdict(construction),
            "q0_size": len(construction.q0),
            "q1_size": len(construction.q1),
            "intersection": sorted(set(construction.q0) & set(construction.q1)),
            "type_specific_unsafe": type_specific["unsafe_reachable"],
            "directed_unsafe": directed["unsafe_reachable"],
            "delay1_unsafe": delay1["unsafe_reachable"],
            "directed_policies": directed["policies"],
        }
        row_pass = (
            len(construction.q0) == construction.quorum
            and len(construction.q1) == construction.quorum
            and len(set(construction.q0) & set(construction.q1)) == f + 1
            and type_specific["unsafe_reachable"]
            and not directed["unsafe_reachable"]
            and delay1["unsafe_reachable"]
        )
        row["status"] = "PASS" if row_pass else "FAIL"
        passed &= row_pass
        rows.append(row)
    return {
        "status": "PASS" if passed else "FAIL",
        "checked_fault_bounds": list(range(1, max_f + 1)),
        "theorem_shape": (
            "For n=3f+1 and q=2f+1, if the unique honest quorum-intersection "
            "pivot must receive enabling evidence E and a later repair/terminal "
            "message R shares the same directed edge, then a type-uniform view "
            "graph cannot both form the first quorum and keep the pivot available "
            "for a conflicting quorum. A phase-specific schedule can deliver E "
            "while omitting R; bounded late delivery can defer R past round two."
        ),
        "rows": rows,
    }
