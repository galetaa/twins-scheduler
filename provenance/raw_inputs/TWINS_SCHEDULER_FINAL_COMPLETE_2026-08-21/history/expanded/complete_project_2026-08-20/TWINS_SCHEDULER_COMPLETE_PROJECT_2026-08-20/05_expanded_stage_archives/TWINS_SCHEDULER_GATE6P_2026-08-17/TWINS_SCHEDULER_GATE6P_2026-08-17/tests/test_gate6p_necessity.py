from __future__ import annotations

from schedcheck.gate6.necessity import (
    exhaustive_premise_characterization,
    parameter_sensitivity,
    premise_ablation_matrix,
)


def test_complete_boolean_characterization() -> None:
    result = exhaustive_premise_characterization()
    assert result["status"] == "PASS"
    assert result["assignments_checked"] == 128
    assert result["strict_patterns_in_field_order"] == [
        "0111111",
        "1101111",
        "1111111",
    ]
    assert result["globally_necessary_in_boolean_model"] == [
        "second_base_short_by_one",
        "repair_disables_pivot",
        "repair_precedes_second_quorum_opportunity",
        "enabling_and_repair_share_endpoint_edge",
        "phase_specific_grammar_can_split_E_and_R",
    ]
    assert not result["mismatches"]


def test_one_at_a_time_ablation_has_expected_boundaries() -> None:
    result = premise_ablation_matrix()
    assert result["status"] == "PASS"
    assert set(result["necessary_premises"]) == {
        "second_base_short_by_one",
        "repair_disables_pivot",
        "repair_precedes_second_quorum_opportunity",
        "enabling_and_repair_share_endpoint_edge",
        "phase_specific_grammar_can_split_E_and_R",
    }
    assert set(result["redundant_premises"]) == {
        "first_base_short_by_one",
        "second_pivot_requires_enabling_evidence",
    }


def test_large_parameter_sensitivity() -> None:
    result = parameter_sensitivity(max_f=64, random_cases=64, seed=60617)
    assert result["status"] == "PASS"
    assert result["cases_checked"] == 128
    assert not result["failures"]
