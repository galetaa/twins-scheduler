# Toolchain sources

## Lean and elan

- Lean toolchain: `leanprover/lean4:v4.33.0`
- Lean release commit: `d8b18978322de05a8f3dba51ef03cf5461676c17`
- Linux release asset:
  `https://github.com/leanprover/lean4/releases/download/v4.33.0/lean-4.33.0-linux.tar.zst`
- Asset size: 574,882,764 bytes
- Official GitHub release digest:
  `sha256:4b3fb03c29a1e0a253fb1d11f9bae3725f19a0dc6fc09b3ea16d2c9df3349e2c`
- elan source commit:
  `464c9d28395000a2a0128e07081e4956d50eced2`
- installer URL:
  `https://raw.githubusercontent.com/leanprover/elan/464c9d28395000a2a0128e07081e4956d50eced2/elan-init.sh`
- downloaded installer SHA-256:
  `a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53`
- installed elan: 4.2.3; Lake: 5.0.0.

The installer ran with repository-local `ELAN_HOME=.cache/elan`,
`--no-modify-path`, and no default toolchain.  Full acquisition output is in
`build_logs/lean_toolchain_install.log`.

## LIPIcs and TeX Live

- Official LIPIcs author package: v2021.1.3
- Official URL:
  `https://submission.dagstuhl.de/styles/download-tag/lipics/v2021.1.3/authors/zip`
- Package SHA-256:
  `b9a4a6d6b44444cc4b9463c8d402e8f41b87e411a344b4af2508cd5bed6c19ef`
- `lipics-v2021.cls` SHA-256:
  `ecae53dfd29c7b22d02a9065327c104760fb726a028b146d556732021a5977f0`
- License: LPPL 1.3c, preserved at `vendor/lipics/LICENSE.md`.
- TeX package overlay: Debian trixie TeX Live 2024 package revisions
  `2024.20250309-1`/`-2`, fetched from official snapshot timestamps
  `20250314T145501Z` and `20250315T025205Z`; exact URLs and SHA-256 values are
  enforced by `scripts/bootstrap.sh`.

The overlay is extracted beneath `.cache/` and does not modify the host TeX
installation. The executed engine identifies itself as pdfTeX 1.40.26; the
official-class declaration is recorded in `build_logs/lipics_build.log`.

## Reproduction container

- Docker Official Image: `debian:trixie-slim`
- OCI index digest resolved 2026-08-22:
  `sha256:3a39a0592364683e6bab97937b72cad5a8fa6dcbbee90edb3bb48c7f8e94f258`
- amd64 manifest:
  `sha256:38a76d01668772e381ad2826d876627c89e7133e2f8a0f5d567306798b0f2a16`
- source revision: `b09f23ad7aab0cafa864c696dfbf130128e5e452`
- official image record: `https://hub.docker.com/_/debian`

The Dockerfile pins uv 0.6.14 and delegates Lean and TeX acquisition to the
same checksum-enforcing `scripts/bootstrap.sh` used on the host.
