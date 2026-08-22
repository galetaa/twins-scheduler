from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from twinsbound.protocols.toy_locking import ToyTwoPhaseLocking


class ProtocolTests(unittest.TestCase):
    def test_event_bfs_matches_closed_form_quotient(self) -> None:
        protocol = ToyTwoPhaseLocking(3)
        for branches in (frozenset(), frozenset({0}), frozenset({0, 1}), frozenset({0, 1, 2})):
            protocol.validate_quotient(branches)

    def test_unsafe_requires_two_decision_values(self) -> None:
        protocol = ToyTwoPhaseLocking(3)
        result = protocol.explore(frozenset({0, 1}))
        self.assertTrue(any(o.unsafe() for o in result.observations))
        self.assertTrue(all(len(o.decided_values()) >= 2 for o in result.observations if o.unsafe()))


if __name__ == "__main__":
    unittest.main()
