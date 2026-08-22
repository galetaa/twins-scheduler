# OPODIS 2026 Adaptation and Page-Budget Plan

**Primary candidate audience:** distributed systems theory/practice and formal verification.  
**Venue fit verdict:** plausible, not guaranteed.

## Why OPODIS is the primary current target

The OPODIS 2026 call explicitly spans distributed-systems theory and implementations, distributed ledgers, fault tolerance/consensus, and formal verification. It also states particular interest in work integrating theory and practice. That matches the paper’s theorem-plus-executable-validation structure.

## Current official constraints checked on 17 August 2026

- Double-blind review; the PDF must remain anonymous.
- English PDF using the current LIPIcs LaTeX style with A4 option.
- At most 15 pages excluding cover page, references, and appendices.
- Separate first cover page containing title, abstract, and best-student-paper eligibility.
- Central technical ideas and evidence needed to verify the main claims must appear in the submission; appendices are discretionary reading.
- AI assistance beyond copyediting or ordinary internet search must be disclosed, and human authors remain accountable.
- Abstract registration: **31 August 2026**; paper submission: **3 September 2026**, anywhere on earth.

Official call: `https://opodis26.software.imdea.org/cfp.html`  
Current LIPIcs style page: `https://drops.dagstuhl.de/entities/series/LIPIcs`

## Current manuscript fit

The working generic A4 PDF has:

- 1 separate cover page;
- 15 numbered manuscript pages, with references beginning on the final numbered page;
- 17 physical PDF pages total including cover and reference continuation;
- approximately 6,683 prose words before bibliography metadata.

This is **not yet proof of LIPIcs compliance**. The current PDF uses a custom A4 review template, not the official LIPIcs class. Conversion may move figures, tables, equations, and references and must be checked from the official template.

## Page budget for LIPIcs conversion

| Section | Target main pages | Non-negotiable content |
|---|---:|---|
| Introduction and contributions | 1.5 | Property-level question, contributions, nonclaims |
| Model and grammars | 2.0 | G_P/G_D/G_T/G_M/G_R, observation language, closures |
| Relational closure theorem | 1.5 | T2 statement, proof idea, non-tautology |
| Quorum-pivot separation | 2.2 | Construction, T3, both G_D branches, figure |
| Exact premise boundary | 1.0 | T6 formula, three assignments, interpretation |
| Replay boundary | 1.0 | T1 and non-idempotent counterexample |
| Executable/formal assurance | 2.2 | kernels, fuller loop, SMT controls, TCB |
| Related work and novelty | 1.5 | nearest works and narrow delta |
| Validity and responsible use | 1.2 | construct/external/proof limits and nonclaims |
| Reproducibility and conclusion | 0.9 | one-command route and final claim |
| **Total** | **15.0** | References and appendices excluded by venue policy |

## Required conversion tasks

1. Download and pin the current `lipics-v2021 v2021.1.3` template.
2. Use the A4 class option and official sectioning/macros.
3. Move bibliography to BibTeX `plainurl` and eliminate custom citation formatting.
4. Supply mandatory metadata: authors, affiliations, ORCIDs, copyright, CCS concepts, keywords, related version, funding, acknowledgments.
5. Keep the review version anonymous under the venue’s policy.
6. Place all central theorem statements, proof ideas, and decisive experimental results in the 15-page main submission.
7. Keep supplemental proof details and full logs in an appendix/artifact, without relying on them for comprehensibility.
8. Recompile with `pdflatex` as requested by LIPIcs, check 300-dpi/PDF figures, and remove overfull boxes and bibliography warnings.
9. State best-student-paper eligibility on the cover. **В брифе не указано.**
10. Retain an accurate AI-use disclosure.

## Desk-rejection controls

- No author or affiliation leakage in PDF metadata, acknowledgments, repository paths, or self-citations.
- No concurrent submission or undisclosed overlap.
- No claim that the custom Gate 8 PDF is the official LIPIcs submission.
- No central proof or decisive result located only in an optional appendix.
- No assertion of a client vulnerability.

## Venue alternatives

- A future OPODIS/DISC cycle remains plausible if proof assurance misses the 2026 deadline.
- A formal-methods venue is plausible if the mature proof-assistant route is completed and the protocol mapping remains narrow.
- A blockchain-formal-methods workshop is a lower-risk fallback but should not be chosen merely to avoid resolving the proof blocker.

## Decision

**VENUE FIT: CONDITIONAL PASS.** OPODIS 2026 is a credible audience and its deadline is still open on the evidence cut-off date, but submission is held until proof assurance, final novelty refresh, and official LIPIcs compilation are complete.
