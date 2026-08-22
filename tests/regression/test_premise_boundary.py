from twins_scheduler.premise_boundary import (
    exhaustive_premise_characterization,
    parameter_sensitivity,
)


def test_all_seven_flag_assignments() -> None:
    result = exhaustive_premise_characterization()
    assert result["status"] == "PASS"
    assert result["assignments_checked"] == 128
    assert result["strict_patterns_in_field_order"] == ["0111111", "1101111", "1111111"]


def test_large_f_python_arithmetic() -> None:
    result = parameter_sensitivity(max_f=128, random_cases=128, seed=60617)
    assert result["status"] == "PASS"
    assert result["cases_checked"] == 256

