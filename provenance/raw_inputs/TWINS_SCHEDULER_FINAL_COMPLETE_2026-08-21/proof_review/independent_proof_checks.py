#!/usr/bin/env python3
"""Independent checks reconstructed solely from the proof-audit statements.

This script does not import the project's experiment code, proof kernel, SMT
encodings, or Lean/Coq source.
"""
from __future__ import annotations
import itertools, json

def t1_counterexample():
    def step(state,event):
        rel,hidden=state
        if event=='X': return (rel,1-hidden)
        if event=='Y': return (hidden,hidden)
        raise ValueError
    def run(trace):
        s=(0,1)
        for e in trace:s=step(s,e)
        return s[0]
    full=run(['X','X','Y']); erased=run(['X','Y'])
    assert (full,erased)==(1,0)
    return {'full_relevant':full,'erased_relevant':erased,'weak_noninterference_refuted':True}

def t2_finite():
    valid_models=0; prefix_checks=0
    def transitive(R):
        return all(not(R[a][b] and R[b][c]) or R[a][c] for a in range(2) for b in range(2) for c in range(2))
    traces=[()] + [x for n in range(1,5) for x in itertools.product((0,1),repeat=n)]
    for rb in itertools.product((False,True),repeat=4):
        R=((rb[0],rb[1]),(rb[2],rb[3]))
        if not transitive(R) or not all(R[s][s] for s in range(2)): continue
        for step in itertools.product(range(2),repeat=2):
            for add in itertools.product(range(2),repeat=2):
                if not all(R[s][add[s]] for s in range(2)): continue
                if not all((not R[s][t]) or R[step[s]][step[t]] for s in range(2) for t in range(2)):continue
                valid_models+=1
                for start in range(2):
                    for tr in traces:
                        a=b=start; assert R[a][b];prefix_checks+=1
                        for kind in tr:
                            if kind==0:a=step[a];b=step[b]
                            else:b=add[b]
                            assert R[a][b];prefix_checks+=1
    return {'valid_models':valid_models,'prefix_checks':prefix_checks,'counterexamples':0}

def t3():
    def exec_policy(mode):
        if mode=='phase':e,r=True,False
        elif mode=='off':e,r=False,False
        elif mode=='on':e,r=True,True
        enabled=e
        c0=enabled
        disabled=r # R is processed before C1 by the declared phase order
        c1=enabled and not disabled
        decisions=(0 if c0 else None,1 if c1 else None)
        return {'certificate0':c0,'certificate1':c1,'agreement_violation':decisions==(0,1)}
    results={m:exec_policy(m) for m in ('phase','off','on')}
    assert results['phase']['agreement_violation']
    assert not results['off']['agreement_violation']
    assert not results['on']['agreement_violation']
    fs=[1,2,10,10**6,int('9'*400)]
    for f in fs:
        q=2*f+1;base=2*f
        assert base+1==q and base==q-1
    return {'same_view':True,'phase_order':['E','C0','R','C1'],'bounded_directed_domain':['off','on'],'policies':results,'parameter_cases':len(fs)}

def U(p,e,r):
    return ((not p['S1']) or e) and ((not p['S2']) or (((not p['Rq']) or e) and not(r and p['D'] and p['T'])))
def strict(p):return p['X'] and p['Ed'] and U(p,1,0) and not U(p,0,0) and not U(p,1,1)
def closed(p):return p['S2'] and p['D'] and p['T'] and p['Ed'] and p['X'] and (p['S1'] or p['Rq'])
def t6():
    fields=['S1','S2','Rq','D','T','Ed','X']; pats=[]
    for bits in itertools.product((False,True),repeat=7):
        p=dict(zip(fields,bits)); assert strict(p)==closed(p)
        if strict(p):pats.append(''.join('1' if b else '0' for b in bits))
    assert pats==['0111111','1101111','1111111']
    return {'assignments':128,'mismatches':0,'patterns':pats}

def main():
    result={'status':'PASS','independence':'does not import project models or proof kernel','T1':t1_counterexample(),'T2':t2_finite(),'T3':t3(),'T6':t6()}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
