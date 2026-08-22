#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from schedcheck.formal.source_mapping import verify_source_mapping
from schedcheck.gate6.event_loop import compare_suites,evaluate_suite,order_sensitivity
from schedcheck.gate6.necessity import exhaustive_premise_characterization,parameter_sensitivity,premise_ablation_matrix
from schedcheck.gate6.proof_kernel import check_induction_certificate,check_quorum_pivot_certificate,write_json
OUT=ROOT/'results/gate7p'; PROOFS=ROOT/'proofs_checked'

def run_json(cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,check=False)
    if p.returncode: raise RuntimeError(f"command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return json.loads(p.stdout)

def go_fixture(path):
    subprocess.run(['go','test','./...'],cwd=path,text=True,capture_output=True,check=True)
    return run_json(['go','run','.'],path)

def csv_write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as h:
        if not rows: return
        w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n'); w.writeheader(); w.writerows(rows)

def case_rows(suite):
    out=[]
    for c in suite['cases']:
        out.append({'grammar':c['grammar'],'mutation':c['mutation'],'unsafe':c['unsafe'],'decisions':json.dumps(c['decisions'],sort_keys=True),'locks':json.dumps(c['locks'],sort_keys=True),'polka_rounds':json.dumps(c['polka_rounds']),'commit_rounds':json.dumps(c['commit_rounds'])})
    return out

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for p in OUT.iterdir():
        if p.is_file(): p.unlink()
    t1=check_induction_certificate(PROOFS/'t1_rules.json',PROOFS/'t1_replay_erasure_certificate.json')
    t2=check_induction_certificate(PROOFS/'t2_rules.json',PROOFS/'t2_closure_lifting_certificate.json')
    t3=check_quorum_pivot_certificate(PROOFS/'t3_quorum_pivot_certificate.json')
    write_json(OUT/'t1_replay_erasure_proof_check.json',t1); write_json(OUT/'t2_closure_lifting_proof_check.json',t2); write_json(OUT/'t3_quorum_pivot_proof_check.json',t3)
    ab= premise_ablation_matrix(); ch=exhaustive_premise_characterization(); sens=parameter_sensitivity(256,256,60617)
    write_json(OUT/'premise_ablation.json',ab); write_json(OUT/'premise_characterization.json',ch); write_json(OUT/'parameter_sensitivity.json',sens)
    csv_write(OUT/'premise_ablation.csv',ab['ablations']); csv_write(OUT/'premise_truth_table.csv',ch['truth_table'])
    py=evaluate_suite(strategy='fifo',seed=0); order=order_sensitivity(random_seeds=256,first_seed=0)
    write_json(OUT/'full_event_loop_python.json',py); write_json(OUT/'event_order_sensitivity.json',order)
    if shutil.which('go') is None: raise RuntimeError('Go toolchain required')
    go=go_fixture(ROOT/'implementation_fixture/full_event_loop'); big=go_fixture(ROOT/'implementation_fixture/proof_crosscheck')
    conf=compare_suites(py,go)
    write_json(OUT/'full_event_loop_go.json',go); write_json(OUT/'full_event_loop_conformance.json',conf); write_json(OUT/'t3_bigint_crosscheck.json',big)
    csv_write(OUT/'full_event_loop_matrix.csv',case_rows(go))
    mapping=verify_source_mapping(ROOT); write_json(OUT/'pinned_source_recheck.json',mapping)
    checks={
      'small_kernel_t1':t1['status']=='PASS','small_kernel_t2':t2['status']=='PASS','small_kernel_t3':t3['status']=='PASS',
      'premise_characterization':ch['status']=='PASS' and ch['assignments_checked']==128 and not ch['mismatches'],
      'parameter_sensitivity':sens['status']=='PASS' and sens['cases_checked']==512,
      'python_event_loop':py['status']=='PASS','go_event_loop':go['status']=='PASS','go_python_conformance':conf['status']=='PASS' and conf['cases_checked']==6,
      'bigint_crosscheck':big['status']=='PASS' and big['cases_checked']==1028,'event_order_sensitivity':order['status']=='PASS' and order['case_runs_checked']==1548,
      'source_mapping':mapping['status']=='PASS'
    }
    summary={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'counts':{'premise_assignments':128,'parameter_cases':512,'bigint_cases':1028,'event_loop_cases':6,'event_order_case_runs':1548},'frozen_scope':'finite agreement observations in explicit certificate-driven locking schemas'}
    write_json(OUT/'core_evidence_summary.json',summary)
    print(json.dumps(summary,indent=2,sort_keys=True)); return 0 if summary['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
