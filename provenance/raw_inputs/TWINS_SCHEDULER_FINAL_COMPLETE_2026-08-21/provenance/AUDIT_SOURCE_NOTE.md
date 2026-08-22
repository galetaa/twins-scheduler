# Provenance note for the independent audit

The independent audit text supplied in the conversation is preserved in `proof_review/INDEPENDENT_PROOF_AUDIT_RU_2026-08-19.md`. The original four sandbox attachments named in that text were not physically present in the active runtime when this post-audit package was rebuilt. Therefore:

- the audit text is a reconstruction from the conversation and is explicitly marked as such in its heading;
- `proof_review/independent_proof_checks.py` is a newly created independent checker implementing the published audit obligations; it is not represented as byte-identical to the missing original checker;
- its output, JSON result, and SHA-256 file were generated in the current run and are reproducible;
- no missing historical file is silently replaced or assigned an invented checksum.

The complete all-stage archive also retains the earlier missing-artifact register for provenance.
