from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from twinsbound.adversaries.byzantine import accepted_message_byzantine_branch_sets
from twinsbound.adversaries.equivocation import dynamic_equivocation_branch_sets
from twinsbound.adversaries.twins_k import Lifecycle, finite_clone_branch_sets
from twinsbound.explorer import enumerate_language
from twinsbound.protocols.toy_locking import ToyTwoPhaseLocking


class AdversaryEmbeddingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol = ToyTwoPhaseLocking(3)

    def language(self, name: str, m: int, sets):
        return enumerate_language(self.protocol, name, m, sets, validate_quotient=True)

    def test_ab_equals_ae(self) -> None:
        for m in (2, 3):
            ab = self.language("AB", m, accepted_message_byzantine_branch_sets(m))
            ae = self.language("AE", m, dynamic_equivocation_branch_sets(m))
            self.assertEqual(ab.observations, ae.observations)

    def test_static_twins_embeds_and_is_monotone(self) -> None:
        for m in (2, 3):
            ae = self.language("AE", m, dynamic_equivocation_branch_sets(m))
            prev = set()
            for k in range(m + 1):
                at = self.language("AT", m, finite_clone_branch_sets(m, k, Lifecycle.GENESIS_STATIC))
                self.assertLessEqual(at.observations, ae.observations)
                self.assertLessEqual(prev, at.observations)
                prev = at.observations

    def test_binary_static_two_covers_all_unsafe(self) -> None:
        m = 2
        ae = self.language("AE", m, dynamic_equivocation_branch_sets(m))
        at1 = self.language("AT1", m, finite_clone_branch_sets(m, 1, Lifecycle.GENESIS_STATIC))
        at2 = self.language("AT2", m, finite_clone_branch_sets(m, 2, Lifecycle.GENESIS_STATIC))
        self.assertFalse(at1.unsafe)
        self.assertEqual(ae.unsafe, at2.unsafe)

    def test_reusable_snapshot_one_active_slot_equals_ae(self) -> None:
        for m in (2, 3):
            ae = self.language("AE", m, dynamic_equivocation_branch_sets(m))
            dynamic = self.language("ATD1", m, finite_clone_branch_sets(m, 1, Lifecycle.SNAPSHOT_ACTIVE_REUSE))
            self.assertEqual(ae.observations, dynamic.observations)


if __name__ == "__main__":
    unittest.main()
