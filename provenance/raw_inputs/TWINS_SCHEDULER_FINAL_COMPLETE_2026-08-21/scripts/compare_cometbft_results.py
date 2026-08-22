#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'results'/'final'
p=json.loads((out/'cometbft_refinement_results.json').read_text())
g=json.loads((out/'cometbft_refinement_results_go.json').read_text())
keys=['f','n','q','variant','grammar','E_delivered','R_delivered','certificate0','certificate1','left_decision','right_decision','pivot_locked_value','pivot_decided_value','agreement_violation']
def canonical(rows):
    return sorted(({k:r.get(k) for k in keys} for r in rows), key=lambda r:(r['f'],r['variant'],r['grammar']))
if canonical(p)!=canonical(g):
    raise SystemExit('COMETBFT_CROSS_LANGUAGE FAIL')
msg=f'COMETBFT_CROSS_LANGUAGE PASS rows={len(p)}\n'
(out/'cometbft_cross_language_check.txt').write_text(msg)
print(msg,end='')
