# Container reproduction

The base image is pinned by multi-platform OCI digest; the resolved amd64
manifest and acquisition date are recorded in `TOOLCHAIN_SOURCES.md`. Build and
run from the repository root:

```bash
docker build -f containers/Dockerfile -t twins-scheduler-closure .
docker run --rm twins-scheduler-closure
```

Or run `docker compose -f containers/compose.yaml up --build --abort-on-container-exit`.
The named cache avoids repeated Lean and TeX downloads. The image does not
contain release ZIPs or host caches because `.dockerignore` excludes them.
