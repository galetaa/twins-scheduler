# Expected outputs

| Check | Required result | Canonical evidence |
| --- | --- | --- |
| Python | 13 tests pass | `build_logs/python_tests.log` |
| Go | all active packages pass | `build_logs/go_tests.log` |
| Python/Go bridge | equal canonical observations | `results/generated/cometbft_cross_language_check.txt` |
| Independent checks | PASS | `results/generated/independent_proof_checks.json` |
| Certificate kernels | originals accepted; tampered controls rejected | `results/generated/certificate_verification.json` |
| SMT | 8 positive UNSAT; 4 damaged SAT | `results/generated/smt_summary.json` |
| Lean | 11 build jobs; exit 0 | `build_logs/lean_build.log` |
| Axiom audit | only documented standard axioms | `formal/lean/AXIOM_REPORT.md` |
| LIPIcs | 16 physical, 14 main-text pages | `build_logs/lipics_page_budget.log` |
| Manifests | hashes and byte comparisons pass | `results/manifests/REFERENCE_SHA256SUMS` |

The run summary is `build_logs/reproduction_summary.log` inside its isolated
output root. The committed final PDF must have the same SHA-256 as a fresh
build.
