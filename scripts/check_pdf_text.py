#!/usr/bin/env python3
"""Semantic PDF checks complement rendering; never substitute for it."""
from pathlib import Path
import re
import subprocess
import sys

pdf, variant = Path(sys.argv[1]), sys.argv[2]
text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
metadata = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
first = text.split('\f')[0]
assert 'Best student paper award: not nominated' in first
assert not re.search(r'(Appendix|Table|Section|Figure|Theorem)\s*[~\u02dc]', text)
assert 'to be confirmed' not in text and 'not specified in the research brief' not in text
assert '\ufffd' not in text and not re.search(r'(?<!\?)\?\?(?!\?)', text)
if variant == 'review':
    assert 'Anonymous author(s)' in metadata
    for identity in ('Galeta', 'galetaa', 'SUAI', 'Aerospace Instrumentation'):
        assert identity not in text + metadata, identity
else:
    assert 'Mikhail Alexandrovich Galeta' in text + metadata
    assert 'Aerospace Instrumentation' in text
print(f'PDF TEXT PASS {variant}: named/anonymous metadata, award statement, references')
