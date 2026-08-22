from __future__ import annotations
import json,subprocess,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from schedcheck.gate6.event_loop import compare_suites,evaluate_suite,order_sensitivity
class EventLoopTests(unittest.TestCase):
    def test_python_boundary(self):
        r=evaluate_suite(); self.assertEqual(r['status'],'PASS')
        u=[(x['grammar'],x['mutation']) for x in r['cases'] if x['unsafe']]
        self.assertEqual(u,[('G_T_TYPE_SPECIFIC','MISSING_LOCK_UPDATE')])
    def test_order_sensitivity(self):
        r=order_sensitivity(random_seeds=32,first_seed=0); self.assertEqual(r['status'],'PASS'); self.assertEqual(r['case_runs_checked'],204)
    def test_go_python_conformance(self):
        d=ROOT/'implementation_fixture/full_event_loop'; subprocess.run(['go','test','./...'],cwd=d,check=True,capture_output=True)
        p=subprocess.run(['go','run','.'],cwd=d,check=True,text=True,capture_output=True); g=json.loads(p.stdout); self.assertEqual(compare_suites(evaluate_suite(),g)['status'],'PASS')
if __name__=='__main__': unittest.main()
