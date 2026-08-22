from twins_scheduler.event_loop import evaluate_suite, order_sensitivity


def test_full_event_loop_boundary() -> None:
    result = evaluate_suite()
    assert result["status"] == "PASS"
    unsafe = [
        (case["grammar"], case["mutation"])
        for case in result["cases"]
        if case["unsafe"]
    ]
    assert unsafe == [("G_T_TYPE_SPECIFIC", "MISSING_LOCK_UPDATE")]


def test_event_order_sensitivity() -> None:
    result = order_sensitivity(random_seeds=32, first_seed=0)
    assert result["status"] == "PASS"
    assert result["case_runs_checked"] == 204

