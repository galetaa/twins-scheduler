#!/usr/bin/env python3
from pathlib import Path
import csv, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]
required=[
 'manuscript/FULL_MANUSCRIPT.md',
 'manuscript/TWINS_SCHEDULER_FULL_MANUSCRIPT_2026-08-17.pdf',
 'manuscript/CLAIM_EVIDENCE_AUDIT.csv',
 'gate8p/PRIOR_ART_AND_NOVELTY_REFRESH_2026-08-17.md',
 'gate8p/NATURAL_PROTOCOL_ASSUMPTION_MAP.md',
 'gate8p/PROOF_ASSURANCE_BLOCKER.md',
 'submission/OPODIS_2026_ADAPTATION.md',
 'results/gate8p/gate8p_decision.json',
 'legacy_evidence/TWINS_SCHEDULER_GATE5P_2026-08-15.zip',
]
for rel in required:
 p=ROOT/rel
 if not p.exists() or p.stat().st_size==0: errors.append(f'missing_or_empty:{rel}')

text=(ROOT/'manuscript/FULL_MANUSCRIPT.md').read_text(encoding='utf-8')
phrases=[
 'Phase Erasure Can Hide Agreement-Violation Witnesses',
 'Relational closure lifting',
 'Parametric quorum-pivot separation',
 'Exact seven-premise boundary',
 'Replay erasure',
 'does not claim',
 'AI-use disclosure draft',
]
for ph in phrases:
 if ph not in text: errors.append(f'manuscript_missing_phrase:{ph}')

with (ROOT/'manuscript/CLAIM_EVIDENCE_AUDIT.csv').open(encoding='utf-8') as f:
 rows=list(csv.DictReader(f))
if len(rows)<25: errors.append(f'claim_count:{len(rows)}')
ids=[r['id'] for r in rows]
if len(ids)!=len(set(ids)): errors.append('duplicate_claim_ids')
for r in rows:
 if not r['evidence'].strip(): errors.append(f'claim_without_evidence:{r["id"]}')
 if r['status'].strip() in {'FAIL','UNKNOWN'}: errors.append(f'unresolved_unlabelled_claim:{r["id"]}')

d=json.loads((ROOT/'results/gate8p/gate8p_decision.json').read_text())
if d.get('submission_ready') is not False: errors.append('submission_ready_must_be_false')
if 'SUBMISSION_HOLD' not in d.get('status',''): errors.append('missing_submission_hold')
if d.get('proof_assurance',{}).get('lean_kernel_check')!='NOT_COMPLETED_TOOLCHAIN_UNAVAILABLE': errors.append('lean_status_mismatch')

lean_attempt=(ROOT/'formal/lean/BUILD_ATTEMPT_2026-08-17.md').read_text()
if 'exit_status=127' not in lean_attempt: errors.append('lean_attempt_not_recorded')

if errors:
 print('GATE 8 VALIDATION FAIL')
 for e in errors: print(e)
 sys.exit(1)
print('GATE 8 VALIDATION PASS')
print(f'claims={len(rows)}')
print('submission_ready=false')
