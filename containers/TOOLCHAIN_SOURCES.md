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

