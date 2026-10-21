from pathlib import Path
import csv
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]

def test_reviewer_matrix_is_generated_from_current_ledger():
    subprocess.run([sys.executable, str(ROOT/'scripts/sync_review_matrix.py'), '--check'], check=True)

def test_current_six_theorems_are_not_old_review_numbers():
    text=(ROOT/'manuscript/markdown/manuscript.md').read_text()
    assert re.findall(r'\*\*Theorem ([0-9]+)',text)==list('123456')
    matrix=(ROOT/'docs/reviews/REVIEWER_COMPLETION_MATRIX.md').read_text()
    assert 'C36' in matrix and 'Only Theorems 1--3' not in matrix

def test_markdown_references_preserve_raw_latex_tildes():
    for name in ('body','appendices'):
        text=(ROOT/f'manuscript/lipics/{name}.tex').read_text()
        assert not re.search(r'(Appendix|Table|Section|Figure|Theorem)\\textasciitilde',text)
    assert r'Appendix~\ref{app:scaled}' in (ROOT/'manuscript/lipics/body.tex').read_text()

def test_author_and_definite_award_statement():
    text=(ROOT/'manuscript/lipics/main.tex').read_text()
    assert 'Mikhail Alexandrovich Galeta' in text and 'SUAI' in text
    assert 'not nominated (eligibility not claimed)' in text
    assert 'to be confirmed' not in text and 'anonymous@example.invalid' not in text
    assert '\\def\\TwinsAnonymous' in (ROOT/'manuscript/lipics/review.tex').read_text()

def test_scaled_claim_keeps_scope_and_cost_boundary():
    with (ROOT/'docs/CLAIM_EVIDENCE_LEDGER.csv').open(newline='') as f:
        rows={r['id']:r for r in csv.DictReader(f)}
    assert len(rows)==36 and 'C36' in rows
    claim=rows['C36']
    assert '48,201' in claim['exact_claim'] and '121,615' in claim['scope_boundary']
    assert 'speedup' in claim['prohibited_extension']
