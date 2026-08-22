from twins_scheduler.bounded import Grammar, Variant, execute, verify_refinement_family


def test_canonical_f1_matrix() -> None:
    for grammar in Grammar:
        assert not execute(1, Variant.BASELINE, grammar).agreement_violation
    assert execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.PHASE_SPECIFIC).agreement_violation
    assert not execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_OFF).agreement_violation
    assert not execute(1, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_ON).agreement_violation


def test_shared_edge_and_distinct_phase_admission() -> None:
    phase = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.PHASE_SPECIFIC)
    off = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_OFF)
    on = execute(2, Variant.MISSING_LOCK_UPDATE, Grammar.DIRECTED_EDGE_ON)
    assert (phase.E_delivered, phase.R_delivered) == (True, False)
    assert (off.E_delivered, off.R_delivered) == (False, False)
    assert (on.E_delivered, on.R_delivered) == (True, True)


def test_parametric_family() -> None:
    assert len(verify_refinement_family(range(1, 129))) == 128 * 2 * 3

