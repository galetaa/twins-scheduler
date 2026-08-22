import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cometbft_bounded import Grammar, Variant, execute, verify_refinement_family


def test_canonical_f1_matrix():
    assert not execute(1, Variant.BASELINE, Grammar.PHASE_SPECIFIC).agreement_violation
    assert not execute(1, Variant.BASELINE, Grammar.DIRECTED_EDGE_OFF).agreement_violation
    assert not execute(1, Variant.BASELINE, Grammar.DIRECTED_EDGE_ON).agreement_violation
    assert execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.PHASE_SPECIFIC).agreement_violation
    assert not execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_OFF).agreement_violation
    assert not execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_ON).agreement_violation


def test_parametric_checked_range():
    rows = verify_refinement_family(range(1, 129))
    assert len(rows) == 128 * 2 * 3


def test_same_edge_and_phase_coupling():
    off = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_OFF)
    on = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_ON)
    phase = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.PHASE_SPECIFIC)
    assert (off.E_delivered, off.R_delivered) == (False, False)
    assert (on.E_delivered, on.R_delivered) == (True, True)
    assert (phase.E_delivered, phase.R_delivered) == (True, False)
