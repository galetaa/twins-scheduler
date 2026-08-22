# Gate 8′ Artifact

This archive contains the complete manuscript and the evidence required to audit its formal and executable claims.

## One-command reproduction

```bash
./scripts/reproduce_gate8p.sh
```

The default route:

1. re-runs the Gate 7 core evidence;
2. verifies and reproduces the nested Gate 5 exact-kernel archive;
3. validates the claim ledger and Gate 8 decision;
4. regenerates the LaTeX source and PDF from Markdown;
5. checks expected manuscript text and PDF metadata;
6. verifies the Gate 8 manifest when present.

Set `GATE8_SKIP_LEGACY=1` only for a fast smoke test that omits the nested exact-kernel rerun. Such a smoke test does not reproduce every executable claim in the paper.

## Read first

- `GATE8P_EXECUTIVE_DECISION.md`
- `GATE8P_REPORT.md`
- `manuscript/FULL_MANUSCRIPT.md`
- `manuscript/CLAIM_EVIDENCE_AUDIT.md`
- `gate8p/PROOF_ASSURANCE_BLOCKER.md`
- `submission/OPODIS_2026_ADAPTATION.md`

## Submission status

**Manuscript complete; submission hold.** The Lean scaffold has not been kernel-checked, and no independent human proof review is recorded.
