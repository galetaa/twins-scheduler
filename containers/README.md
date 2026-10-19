# Container reproduction

Build and run the revised reproduction from the repository root:

```bash
docker build -f containers/Dockerfile -t twins-scheduler-closure .
docker run --rm -v twins-cache:/artifact/.cache twins-scheduler-closure ./reproduce_revision.sh
```

`./reproduce_revision.sh` is an alias for the expanded `./reproduce.sh` pipeline.
The image's default command and the existing Compose service use that same
pipeline, including the new concrete-trace and repair-frontier runners:

```bash
docker compose -f containers/compose.yaml up --build --abort-on-container-exit
```

The run prints its isolated output location and writes a reproduction summary
there. The named cache retains those outputs and avoids repeated Lean and TeX
downloads. The image does not copy release ZIPs or host caches because
`.dockerignore` excludes them. Any mandatory check failure produces a failing
reproduction command.

## Dependencies and version scope

The base image is pinned by multi-platform OCI digest; the resolved amd64
manifest and acquisition date are recorded in
[toolchain sources](TOOLCHAIN_SOURCES.md). Debian package installation still
uses the package repositories configured in that image. The OCI pin alone does
not make every later package resolution immutable.

The Dockerfile installs Python, Go, a C compiler, Git, Pandoc, base TeX and
BibTeX, Poppler, fonts, and the acquisition tools used by bootstrap. It pins
uv to 0.6.14. The project lock supplies `z3-solver==4.13.3.0`, whose Z3 runtime
is used for SMT checks. Lean 4.33.0 and the checksum-pinned TeX overlay are
installed by the same repository-local bootstrap used on the host.

Pandoc is required to generate the synchronized LaTeX source from Markdown.
The PDF build records the executed engine and Pandoc versions, verifies the
official LIPIcs class, checks source synchronization, enforces the 15-page
main-text limit, rejects the specified layout/reference/bibliography errors,
and checks font embedding. The current verified document has 17 physical pages
and 13 main-text pages. PDF byte identity across different TeX engines is not a
required gate; deterministic data results are compared byte-for-byte.

## Expected revision results

The active Python suite has 35 tests, including 8 frontier and 14 concrete-trace
tests. The Lean build has 12 jobs, audits 20 declarations, and rechecks its
kernel objects with `leanchecker`. SMT expects 8 UNSAT and 4 SAT controls.
The new finite enumerations report zero mismatches, and all 12 concrete trace
legality audits pass. Counts, filenames, and finite sweep scopes are specified
in [expected outputs](../docs/reproduction/EXPECTED_OUTPUTS.md).

The container runs the declared models and checks. Its successful execution
does not establish production CometBFT conformance. In particular, the Lean
module proves behavioral-contract and arithmetic components; the full graph
correspondence and concrete protocol transitions retain the distinct evidence
boundaries described in [limitations](../docs/LIMITATIONS.md).
