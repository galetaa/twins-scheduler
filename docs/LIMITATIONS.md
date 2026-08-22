# Limitations

- All separation and natural-protocol evidence is bounded rule-level analysis,
  not a production CometBFT vulnerability or full event-loop conformance result.
- The results address safety observations, not liveness, timing performance,
  exploitability, prevalence, probability, or unbounded partial synchrony.
- The type-uniform directed grammar is incomplete for the explicit family; no
  universal incompleteness or universally minimal phase grammar is claimed.
- Replay erasure requires the stated finite relevant-state projection, stable
  processed keys, state/output congruence, and silent duplicate premises. The
  `X,X,Y` model demonstrates failure without them.
- Lean is primary. The retained Coq sources are secondary archival material and
  are not advertised as a second maintained mature-prover build.
- Bootstrap depends on pinned external Lean and Debian package downloads when
  the repository-local cache is empty.
