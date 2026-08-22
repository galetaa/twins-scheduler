from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from twinsbound.model import Observation
from twinsbound.oracles import dynamic_active_k_min, static_k_min


class CanonicalizationTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        obs = Observation.from_tokens(["D0", "P1", "N"])
        self.assertEqual(obs.canonical_id(), "D0|P1|N")
        self.assertEqual(Observation.from_tokens(obs.canonical_id().split("|")), obs)

    def test_width_and_snapshot_collapse(self) -> None:
        obs = Observation.from_tokens(["D0", "D1", "P2"])
        self.assertEqual(static_k_min(obs), 3)
        self.assertEqual(dynamic_active_k_min(obs), 1)

    def test_every_unsafe_profile_has_two_branch_core(self) -> None:
        obs = Observation.from_tokens(["D0", "D1", "D2"])
        core = obs.minimal_pair_core()
        self.assertIsNotNone(core)
        assert core is not None
        self.assertTrue(core.unsafe())
        self.assertEqual(core.width(), 2)


if __name__ == "__main__":
    unittest.main()
