from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from schedcheck.gate6.necessity import exhaustive_premise_characterization,parameter_sensitivity
from schedcheck.gate6.proof_kernel import ProofFailure,check_induction_certificate,check_quorum_pivot_certificate
P=ROOT/'proofs_checked'
class FormalTests(unittest.TestCase):
    def test_small_certificates(self):
        self.assertEqual(check_induction_certificate(P/'t1_rules.json',P/'t1_replay_erasure_certificate.json')['status'],'PASS')
        self.assertEqual(check_induction_certificate(P/'t2_rules.json',P/'t2_closure_lifting_certificate.json')['status'],'PASS')
        self.assertEqual(check_quorum_pivot_certificate(P/'t3_quorum_pivot_certificate.json')['status'],'PASS')
    def test_tampered_t1_rejected(self):
        c=json.loads((P/'t1_replay_erasure_certificate.json').read_text()); c['premises'].remove('premise_duplicate_transition_stutters')
        with tempfile.TemporaryDirectory() as d:
            q=Path(d)/'bad.json'; q.write_text(json.dumps(c))
            with self.assertRaises(ProofFailure): check_induction_certificate(P/'t1_rules.json',q)
    def test_exact_premise_characterization(self):
        r=exhaustive_premise_characterization(); self.assertEqual(r['status'],'PASS'); self.assertEqual(r['assignments_checked'],128); self.assertEqual(r['strict_patterns_in_field_order'],['0111111','1101111','1111111']); self.assertFalse(r['mismatches'])
    def test_parameter_sensitivity(self):
        r=parameter_sensitivity(64,64,60617); self.assertEqual(r['status'],'PASS'); self.assertEqual(r['cases_checked'],128)
if __name__=='__main__': unittest.main()
