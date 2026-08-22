# Final package verification

Before packaging, the authoritative 21 August layer was reproduced from a clean copy with `./reproduce.sh` and exited with status 0. All available theorem, protocol, implementation, SMT, negative-control, source-hygiene, and A4-PDF checks passed. The final tree contains every earlier stage both as original ZIP artifacts and through exact expanded historical snapshots.

The final ZIP must be checked with:

```bash
sha256sum -c TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21.zip.sha256
unzip -t TWINS_SCHEDULER_FINAL_COMPLETE_2026-08-21.zip
```

After extraction, the root `SHA256SUMS` validates every regular file other than the root manifest files themselves:

```bash
sha256sum -c SHA256SUMS
```

The authoritative manuscript PDF is:

```text
manuscript/TWINS_SCHEDULER_FINAL_MANUSCRIPT_2026-08-21.pdf
```

External blockers remain explicit: no local Lean/Coq compiler and no installed official LIPIcs class.
