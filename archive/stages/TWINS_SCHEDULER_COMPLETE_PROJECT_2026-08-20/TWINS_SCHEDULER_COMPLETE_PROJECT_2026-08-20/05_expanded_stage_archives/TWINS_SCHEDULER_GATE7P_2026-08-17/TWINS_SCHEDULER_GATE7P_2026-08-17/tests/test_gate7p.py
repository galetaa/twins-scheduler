from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from schedcheck.formal.source_mapping import verify_source_mapping
from schedcheck.gate6.event_loop import evaluate_suite, order_sensitivity
from schedcheck.gate6.necessity import exhaustive_premise_characterization
from schedcheck.gate6.proof_kernel import (
    check_induction_certificate,
    check_quorum_pivot_certificate,
)


class Gate7CoreTests(unittest.TestCase):
    def test_t1_certificate(self) -> None:
        result = check_induction_certificate(
            ROOT / "proofs_checked/t1_rules.json",
            ROOT / "proofs_checked/t1_replay_erasure_certificate.json",
        )
        self.assertEqual(result["status"], "PASS")

    def test_t2_certificate(self) -> None:
        result = check_induction_certificate(
            ROOT / "proofs_checked/t2_rules.json",
            ROOT / "proofs_checked/t2_closure_lifting_certificate.json",
        )
        self.assertEqual(result["status"], "PASS")

    def test_t3_certificate(self) -> None:
        result = check_quorum_pivot_certificate(
            ROOT / "proofs_checked/t3_quorum_pivot_certificate.json"
        )
        self.assertEqual(result["status"], "PASS")

    def test_exact_premise_characterization(self) -> None:
        result = exhaustive_premise_characterization()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["assignments_checked"], 128)
        self.assertEqual(result["mismatches"], [])
        self.assertEqual(
            result["strict_patterns_in_field_order"],
            ["0111111", "1101111", "1111111"],
        )

    def test_event_loop_classification(self) -> None:
        suite = evaluate_suite(strategy="fifo", seed=0)
        self.assertEqual(suite["status"], "PASS")
        by_case = {
            (case["grammar"], case["mutation"]): case["unsafe"]
            for case in suite["cases"]
        }
        self.assertFalse(by_case[("G_T_TYPE_SPECIFIC", "BASELINE")])
        self.assertTrue(by_case[("G_T_TYPE_SPECIFIC", "MISSING_LOCK_UPDATE")])
        self.assertFalse(by_case[("G_D_ROUND0_EDGE_OFF", "MISSING_LOCK_UPDATE")])
        self.assertFalse(by_case[("G_D_ROUND0_EDGE_ON", "MISSING_LOCK_UPDATE")])

    def test_small_order_sensitivity(self) -> None:
        result = order_sensitivity(random_seeds=4, first_seed=0)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["classification_failures"], [])

    def test_pinned_source_mapping(self) -> None:
        result = verify_source_mapping(ROOT)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
