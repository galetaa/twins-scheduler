# Partial recovery of the interrupted revision

**Status: recovery snapshot, not a complete reproducible revision. Do not treat this directory or its PDFs as a new validated release.**

On 21 October 2026 the interrupted publication was retried. The repository's main branch was still at `452b6497de40de0f56b16905088896dc94bbeeb5` (tree `a3faf969675714849d61e4ba6e1c591e3f477a4e`). Creating the complete prepared revision failed because not all referenced Git blob objects exist in the remote repository.

This directory preserves the binary artifacts that were already uploaded before the interruption, byte-for-byte by their recorded Git blob identifiers. It does not replace the active manuscript, code, results, or workflows. The current main branch is left unchanged.

## Recovered materials

- [Author PDF](manuscript/pdf/final_lipics_manuscript.pdf), original blob `1a91db4c045746a6a5219085b07b533405849050`.
- [Anonymous review PDF](manuscript/pdf/review_lipics_manuscript.pdf), original blob `dafa55936a27fff9f8827c78aa31248fac64f5a3`.
- Serialized seven-validator experiment models, certificates, policy-oracle outputs, guard controls, and four replay files under `results/scaled/`.

The original build records reported PDF SHA-256 values `4b54c2de56f22c2da324c02c24b12a38e9dcc3dd80fb4b1727f26b8810dde6d6` (author) and `6bcc17fcda5b9bde738648570ad7ffc864889f529068720eb755d4ce4034914b` (review). The recovery preserves the corresponding remote blobs; it is not a fresh PDF compilation or a new reproduction run.

## Publication blockers

The prepared revision manifest refers to files that could not be resolved on the remote, including:

| Path in intended revision | Expected Git blob |
|---|---|
| `src/python/twins_scheduler/scaled_protocol.py` | `49ae4be939effe9f6089a0bf519874a4e1847cb5` |
| `docs/reviews/AUTHOR_METADATA.md` | `856092a823436987d8bccb99805b65188ced3da2` |
| `docs/CLAIM_EVIDENCE_LEDGER.csv` | `9095c957cdca4147846166ec5d23e9df3afc2e9f` |
| `manuscript/lipics/main.tex` | `a23340086ff2fd4a072172a4c0b6c694511a0c03` |
| `build_logs/manuscript_consistency.log` | `f0c97e916ad594be2d753237b23a57faba7474bd` |

This is a confirmed list of missing objects, not an exhaustive inventory. The full prepared manifest also includes study scripts, tests, summary outputs, source documents and synchronization checks. They must be recovered or reconstructed and revalidated before the revision can replace the active tree. Recorded source SHA-256 identities were `25fd3dc97e885fdb03c722dcd33b5893c9597151aa42a679ae4968bf0bad0e3b` for `scaled_protocol.py` and `16b75391afe11b3c18c897958f3de7d5a75d185868ec4cad6e4c8b16c108dfa7` for `run_scaled_study.py`.

The previous work reported successful tests and reproduction, but this recovery does **not** claim that those checks were rerun or that the present incomplete snapshot satisfies the reproduction contract. A green existing workflow would test the unchanged base, not certify the recovered experiment.

## Before promotion

Restore the complete source, test and result set; compare all recovered files with the prepared manifest; run the complete reproduction contract and both manuscript builds; verify the author/student statement, cross-references, claim ledger and reviewer matrix together. Only then update the active manuscript/results and main branch.
