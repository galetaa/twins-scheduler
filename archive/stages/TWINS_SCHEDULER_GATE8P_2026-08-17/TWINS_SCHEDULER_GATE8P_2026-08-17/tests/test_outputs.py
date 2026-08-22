from __future__ import annotations
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OutputTests(unittest.TestCase):
    def test_decision(self):
        d=json.loads((ROOT/'results/gate7p/gate7p_decision.json').read_text())
        self.assertEqual(d['status'],'PASS_GO_TO_GATE8_MANUSCRIPT_SUBMISSION_HOLD')
        self.assertFalse(d['submission_ready'])
        self.assertEqual(d['lean_status'],'MIGRATION_SCAFFOLD_ONLY_NOT_KERNEL_CHECKED')
    def test_smt_report(self):
        r=json.loads((ROOT/'proof_outputs/smt_proof_report.json').read_text())
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(sum(x.get('observed_unsat_count',0) for x in r['checks']),8)
        self.assertEqual(sum(x.get('observed_sat_count',0) for x in r['checks']),4)
    def test_assets(self):
        r=json.loads((ROOT/'paper_assets/MANIFEST.json').read_text())
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(len(r['outputs']),24)
if __name__=='__main__': unittest.main()
