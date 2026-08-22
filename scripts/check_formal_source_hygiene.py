#!/usr/bin/env python3
from __future__ import annotations
import json,os,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
patterns={
 'sorry': re.compile(r'\bsorry\b'),
 'admit': re.compile(r'\badmit\b|\bAdmitted\b'),
 'axiom_declaration': re.compile(r'^\s*(axiom|Axiom)\s+',re.M),
 'unsafe_declaration': re.compile(r'^\s*unsafe\s+(def|theorem)\s+',re.M),
}
hits=[]
for base in [root/'formal'/'lean',root/'formal'/'coq']:
    for p in sorted(base.rglob('*')):
        if p.suffix not in {'.lean','.v'}: continue
        text=p.read_text(encoding='utf-8')
        for name,rx in patterns.items():
            for m in rx.finditer(text):
                hits.append({'file':str(p.relative_to(root)),'kind':name,'line':text.count('\n',0,m.start())+1,'match':m.group(0)})
# AxiomAudit files mention the command "#print axioms" but do not declare axioms.
result={'status':'PASS' if not hits else 'FAIL','files_checked':sum(1 for b in [root/'formal'/'lean',root/'formal'/'coq'] for p in b.rglob('*') if p.suffix in {'.lean','.v'}),'hits':hits}
output_root=Path(os.environ.get('TWINS_OUTPUT_ROOT',root))
out=output_root/'results'/'generated'; out.mkdir(parents=True,exist_ok=True)
(out/'formal_source_hygiene.json').write_text(json.dumps(result,indent=2)+'\n')
log_dir=Path(os.environ.get('TWINS_LOG_DIR',output_root/'build_logs'))
log_dir.mkdir(parents=True,exist_ok=True)
(log_dir/'formal_source_hygiene.log').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if hits: raise SystemExit(1)
