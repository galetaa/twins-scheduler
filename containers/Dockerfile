FROM docker.io/library/debian:trixie-slim@sha256:3a39a0592364683e6bab97937b72cad5a8fa6dcbbee90edb3bb48c7f8e94f258

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils ca-certificates curl gcc git golang-go libc6-dev libz3-4 make \
    pandoc poppler-utils python3 python3-pip python3-venv python-is-python3 texlive-base \
    texlive-binaries texlive-latex-base unzip zip && \
    python3 -m pip install --break-system-packages --no-cache-dir uv==0.6.14 && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends lmodern && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /artifact
COPY . /artifact
CMD ["./reproduce.sh"]
