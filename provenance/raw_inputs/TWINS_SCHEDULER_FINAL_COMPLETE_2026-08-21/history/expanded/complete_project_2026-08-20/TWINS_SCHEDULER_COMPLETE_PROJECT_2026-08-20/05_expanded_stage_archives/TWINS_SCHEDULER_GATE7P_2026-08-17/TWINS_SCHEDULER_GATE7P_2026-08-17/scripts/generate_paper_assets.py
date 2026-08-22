#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'paper_data'; RES=ROOT/'results/gate7p'; PROOF=ROOT/'proof_outputs/smt_proof_report.json'; FIG=ROOT/'paper_assets/figures'; TAB=ROOT/'paper_assets/tables'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s.rstrip()+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tex(v):
    r={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(r.get(c,c) for c in str(v))
def table(stem,headers,rows,caption):
    with (TAB/f'{stem}.csv').open('w',encoding='utf-8',newline='') as h:
        w=csv.writer(h,lineterminator='\n'); w.writerow(headers); w.writerows(rows)
    md=[f'<!-- {caption} -->','', '| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']
    md += ['| '+' | '.join(str(x).replace('|','\\|') for x in row)+' |' for row in rows]
    write(TAB/f'{stem}.md','\n'.join(md))
    spec=''.join(['p{'+f'{0.94/len(headers):.3f}\\linewidth'+'}' for _ in headers])
    lines=[r'\begin{table*}[t]',r'\centering',r'\small',f'\\begin{{tabular}}{{{spec}}}',r'\toprule',' & '.join(tex(h) for h in headers)+r' \\',r'\midrule']
    lines += [' & '.join(tex(x) for x in row)+r' \\' for row in rows]
    lines += [r'\bottomrule',r'\end{tabular}',f'\\caption{{{tex(caption)}}}',f'\\label{{tab:{stem}}}',r'\end{table*}']
    write(TAB/f'{stem}.tex','\n'.join(lines))
def head(w,h,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<title>{html.escape(title)}</title>','<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>','<rect width="100%" height="100%" fill="white"/>','<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#111}.b{fill:#f5f5f5;stroke:#222;stroke-width:1.5}.ar{stroke:#222;stroke-width:1.6;fill:none;marker-end:url(#a)}.d{stroke:#555;stroke-width:1.3;stroke-dasharray:6 5;fill:none}.h{font-size:19px;font-weight:700}.s{font-size:13px}.m{font-size:15px}.k{font-size:14px;font-weight:700}</style>']
def fig_grammar():
    d=load(DATA/'scheduler_grammars.json')
    labels={x['id']:x for x in d['grammars']}
    pos={'G_P':(20,75),'G_D':(220,75),'G_T':(420,75),'G_M':(620,75),'G_R':(820,75),'G_D1':(420,235)}
    w=180; h=78
    o=head(1020,380,'Scheduler grammar embeddings')
    o += ['<text x="510" y="30" text-anchor="middle" class="h">Scheduler grammar embeddings</text>']
    wrapped={
      'G_P':('partition','per view'),
      'G_D':('directed graph','per view; type-uniform'),
      'G_T':('phase/type-specific','directed graph'),
      'G_M':('per-message','instance control'),
      'G_R':('per-message','plus replay'),
      'G_D1':('directed graph plus','one-view terminal delay'),
    }
    for gid,(x,y) in pos.items():
        line1,line2=wrapped[gid]
        o += [
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="b"/>',
          f'<text x="{x+w/2}" y="{y+25}" text-anchor="middle" class="k">{gid}</text>',
          f'<text x="{x+w/2}" y="{y+49}" text-anchor="middle" class="s">{html.escape(line1)}</text>',
          f'<text x="{x+w/2}" y="{y+66}" text-anchor="middle" class="s">{html.escape(line2)}</text>',
        ]
    for left,right,_ in d['relations']:
        x1,y1=pos[left]; x2,y2=pos[right]
        if right=='G_D1':
            o.append(f'<path d="M{x1+w/2},{y1+h} C{x1+w/2},190 {x2+w/2},190 {x2+w/2},{y2}" class="ar"/>')
        else:
            o.append(f'<line x1="{x1+w}" y1="{y1+h/2}" x2="{x2}" y2="{y2+h/2}" class="ar"/>')
    o += [
      '<path d="M510,235 C560,205 560,180 510,153" class="d"/>',
      '<text x="585" y="205" class="s">incomparable dimensions</text>',
      f'<text x="510" y="350" text-anchor="middle" class="m">{html.escape(d["note"])}</text>',
      '</svg>'
    ]
    write(FIG/'figure1_scheduler_grammar.svg','\n'.join(o))
def fig_pivot():
    o=head(1000,560,'Parametric quorum pivot separation'); o+=['<text x="500" y="32" text-anchor="middle" class="h">Quorum-pivot separation: n=3f+1, q=2f+1</text>']
    for x,g,l in [(45,'B','f Byzantine'),(235,'A','f honest'),(425,'p','one honest pivot'),(615,'C','f honest')]: o += [f'<rect x="{x}" y="65" width="160" height="65" rx="9" class="b"/>',f'<text x="{x+80}" y="92" text-anchor="middle" class="k">{g}</text>',f'<text x="{x+80}" y="115" text-anchor="middle" class="s">{l}</text>']
    o += ['<rect x="45" y="150" width="540" height="40" rx="6" class="b"/><text x="315" y="176" text-anchor="middle" class="m">Q₀ = B ∪ A ∪ {p}, size 2f+1</text>','<rect x="425" y="205" width="350" height="40" rx="6" class="b"/><text x="600" y="231" text-anchor="middle" class="m">Q₁ = B ∪ C ∪ {p}, size 2f+1</text>','<text x="810" y="95" class="s">Q₀ ∩ Q₁ = B ∪ {p}</text>','<text x="810" y="117" class="s">unique honest overlap: p</text>','<text x="500" y="285" text-anchor="middle" class="h">One sender→p edge carries enabling E, then repair R</text>']
    cases=[(30,'G_T: E yes, R no','p serves both branches','Q₀=q and Q₁=q → unsafe'),(355,'G_D: edge off','neither E nor R','first support=2f=q−1 → safe'),(680,'G_D: edge on','both E and R','repair removes p; Q₁=2f → safe')]
    for x,t,m,r in cases: o += [f'<rect x="{x}" y="315" width="290" height="175" rx="10" class="b"/>',f'<text x="{x+145}" y="345" text-anchor="middle" class="k">{html.escape(t)}</text>',f'<text x="{x+145}" y="385" text-anchor="middle" class="m">{html.escape(m)}</text>',f'<text x="{x+145}" y="450" text-anchor="middle" class="s">{html.escape(r)}</text>']
    o += ['<text x="500" y="535" text-anchor="middle" class="m">Existential result for the explicit schema; no universal incompleteness claim.</text>','</svg>']; write(FIG/'figure2_quorum_pivot.svg','\n'.join(o))
def fig_premises():
    d=load(RES/'premise_characterization.json'); o=head(980,420,'Exact premise characterization'); o+=['<text x="490" y="32" text-anchor="middle" class="h">Exact seven-flag characterization</text>',f'<text x="160" y="105" text-anchor="middle" style="font-size:42px;font-weight:700">{d["assignments_checked"]}</text>','<text x="160" y="135" text-anchor="middle" class="m">assignments</text>',f'<text x="490" y="105" text-anchor="middle" style="font-size:42px;font-weight:700">{len(d["strict_patterns_in_field_order"])}</text>','<text x="490" y="135" text-anchor="middle" class="m">strict assignments</text>','<text x="820" y="105" text-anchor="middle" style="font-size:42px;font-weight:700">0</text>','<text x="820" y="135" text-anchor="middle" class="m">mismatches</text>','<rect x="70" y="170" width="840" height="65" rx="9" class="b"/>','<text x="490" y="200" text-anchor="middle" class="k">Strict = S₂ ∧ D ∧ T ∧ E ∧ X ∧ (S₁ ∨ Rq)</text>','<text x="490" y="222" text-anchor="middle" class="s">patterns: 0111111, 1101111, 1111111</text>']
    labs=['S₂: second base short by one','D: repair disables pivot','T: repair precedes second chance','E: messages share endpoint edge','X: grammar can split E and R']
    for i,l in enumerate(labs):
        x=55+(i%3)*305; y=270+(i//3)*54; o += [f'<rect x="{x}" y="{y}" width="270" height="38" rx="6" class="b"/>',f'<text x="{x+135}" y="{y+24}" text-anchor="middle" class="s">{html.escape(l)}</text>']
    o += ['<text x="490" y="398" text-anchor="middle" class="m">S₁ and Rq are individually optional, but at least one is required.</text>','</svg>']; write(FIG/'figure3_premise_characterization.svg','\n'.join(o))
def tables():
    d=load(DATA/'scheduler_grammars.json'); rel={x['id']:[] for x in d['grammars']}
    for a,b,r in d['relations']: rel[a].append(f'{b}: {r}')
    table('table1_scheduler_grammars',['Grammar','Control authority','Direct extension'],[[x['id'],x['controls'],'; '.join(rel[x['id']]) or '—'] for x in d['grammars']],'Scheduler grammar ladder and the separate bounded-delay branch.')
    rows=[]
    with (RES/'full_event_loop_matrix.csv').open(encoding='utf-8',newline='') as h:
        for r in csv.DictReader(h):
            ds=json.loads(r['decisions']); rows.append([r['grammar'],r['mutation'],'YES' if r['unsafe']=='True' else 'no',', '.join(f'{x["replica"]}={x["value"]}' for x in ds),r['polka_rounds'],r['commit_rounds']])
    table('table2_full_event_loop',['Grammar','Variant','Violation','Decisions','POLKA','COMMIT'],rows,'Fuller two-round event-loop outcomes.')
    p=load(RES/'premise_characterization.json'); table('table3_premise_characterization',['Item','Result'],[['Assignments',p['assignments_checked']],['Strict assignments',len(p['strict_patterns_in_field_order'])],['Patterns',', '.join(p['strict_patterns_in_field_order'])],['Exact formula','S2 ∧ D ∧ T ∧ E ∧ X ∧ (S1 ∨ Rq)'],['Necessary flags','; '.join(p['globally_necessary_in_boolean_model'])],['Mismatches',len(p['mismatches'])]],'Exact result for the supplied seven-flag model.')
    z=load(PROOF); table('table4_smt_migration',['Kind','Obligation','Expected','Observed','Status','Digest'],[[x['kind'],x['name'],x['expected'],str(x.get('observed_unsat_count',x.get('observed_sat_count'))),x['status'],x['source_sha256'][:12]] for x in z['checks']],'Z3 proof obligations and negative controls.')
    c=load(DATA/'claim_evidence.json'); table('table5_claim_to_evidence',['Claim','Scope','Formal evidence','Executable evidence','Status'],[[x['claim'],x['scope'],x['formal_evidence'],x['executable_evidence'],x['status']] for x in c],'Frozen claim-to-evidence ledger.')
    v=load(DATA/'validity.json'); table('table6_validity',['Class','Risk','Control','Residual'],[[x['category'],x['risk'],x['control'],x['residual']] for x in v],'Validity controls and remaining limitations.')
    n=load(DATA/'nonclaims.json'); table('table7_nonclaims',['No.','Prohibited claim'],[[i+1,x] for i,x in enumerate(n)],'Claims explicitly excluded from the paper.')
def main():
    FIG.mkdir(parents=True,exist_ok=True); TAB.mkdir(parents=True,exist_ok=True)
    for d in [FIG,TAB]:
        for p in d.iterdir():
            if p.is_file(): p.unlink()
    fig_grammar(); fig_pivot(); fig_premises(); tables()
    outs=[]
    for p in sorted([*FIG.iterdir(),*TAB.iterdir()]):
        if p.is_file(): outs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})
    m={'status':'PASS','generator':'scripts/generate_paper_assets.py','outputs':outs,'source_files':['paper_data/*.json','results/gate7p/*.json','results/gate7p/*.csv','proof_outputs/smt_proof_report.json']}
    write(ROOT/'paper_assets/MANIFEST.json',json.dumps(m,indent=2,sort_keys=True)); print(json.dumps({'status':'PASS','outputs':len(outs)},sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
