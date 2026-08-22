# Gate 2 — Environment report

**Decision:** PASS for the blocking pilot; CONDITIONAL for optional external-client validation.

## Pinned mandatory environment

| Component | Pinned value | Role |
|---|---|---|
| Python | `3.13.5` | Pilot runtime; actual interpreter available in the execution environment. |
| uv | `0.10.0` | Environment and lockfile runner. |
| Project dependencies | none | The decisive explorer uses only the Python standard library. |
| Hash seed | `PYTHONHASHSEED=0` | Stable iteration-independent reproduction contract. |
| OS used for reference run | Linux `6.18.35`, x86-64, glibc 2.41 | Recorded in `results/pilot/environment.json`. |
| Git | `2.47.3` | Manifest/repository utility; not required by the scientific computation. |

The earlier specification named Python 3.14.7, pytest 9.1.1, Hypothesis and optional Z3. The actual isolated environment provides Python 3.13.5 and uv 0.10.0. Rather than pretend those versions were installed, the pilot was reduced to a standard-library-only implementation and pinned to the available interpreter.

## Optional tools observed

- pytest `9.0.2` is installed globally but is not required; tests use `unittest`.
- Go `1.23.2` is installed, but no external HotStuff build is on the blocking path.
- Coq and Z3 are not installed. Neither is required for Gates 0–3.

## Offline contract

After obtaining this package, the decisive run needs no network access and no third-party Python package:

```bash
uv run python -m unittest discover -s tests -v
PYTHONHASHSEED=0 uv run python scripts/run_pilot.py --config configs/pilot.toml
```

`uv.lock` contains only the virtual local project.
