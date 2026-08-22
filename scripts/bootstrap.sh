#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CACHE_ROOT=${TWINS_CACHE_ROOT:-"$ROOT/.cache"}
ELAN_HOME=${ELAN_HOME:-"$CACHE_ROOT/elan"}
export ELAN_HOME
export PATH="$ELAN_HOME/bin:$PATH"

required=(python uv go git curl cc pdflatex bibtex pdfinfo pdffonts pdftotext dpkg-deb)
for command_name in "${required[@]}"; do
  command -v "$command_name" >/dev/null || {
    echo "BOOTSTRAP FAIL missing command: $command_name" >&2
    exit 1
  }
done

cd "$ROOT"
uv sync --frozen

mkdir -p "$CACHE_ROOT/downloads"
ELAN_INSTALLER="$CACHE_ROOT/downloads/elan-init-464c9d28395000a2a0128e07081e4956d50eced2.sh"
if [[ ! -x "$ELAN_HOME/bin/elan" ]]; then
  curl -fL --retry 3 -o "$ELAN_INSTALLER" \
    https://raw.githubusercontent.com/leanprover/elan/464c9d28395000a2a0128e07081e4956d50eced2/elan-init.sh
  echo "a620ff1641616222c8d37c54845492004bb84d6877cdbc944dd65c1aa685bf53  $ELAN_INSTALLER" | sha256sum -c -
  sh "$ELAN_INSTALLER" -y --default-toolchain none --no-modify-path
fi
LEAN_TOOLCHAIN=$(<lean-toolchain)
if ! elan toolchain list | grep -Fxq "$LEAN_TOOLCHAIN"; then
  elan toolchain install "$LEAN_TOOLCHAIN"
fi

TEX_DEBS="$CACHE_ROOT/tex-debs"
TEX_OVERLAY="$CACHE_ROOT/texlive-overlay"
TEX_MARKER="$TEX_OVERLAY/.complete-v2024.20250309"
if [[ ! -f "$TEX_MARKER" ]]; then
  mkdir -p "$TEX_DEBS" "$TEX_OVERLAY"
  files=(
    "texlive-fonts-recommended_2024.20250309-1_all.deb"
    "texlive-latex-recommended_2024.20250309-1_all.deb"
    "texlive-pictures_2024.20250309-1_all.deb"
    "texlive-latex-extra_2024.20250309-2_all.deb"
    "texlive-plain-generic_2024.20250309-2_all.deb"
    "texlive-bibtex-extra_2024.20250309-2_all.deb"
  )
  urls=(
    "https://snapshot.debian.org/archive/debian/20250314T145501Z/pool/main/t/texlive-base/${files[0]}"
    "https://snapshot.debian.org/archive/debian/20250314T145501Z/pool/main/t/texlive-base/${files[1]}"
    "https://snapshot.debian.org/archive/debian/20250314T145501Z/pool/main/t/texlive-base/${files[2]}"
    "https://snapshot.debian.org/archive/debian/20250315T025205Z/pool/main/t/texlive-extra/${files[3]}"
    "https://snapshot.debian.org/archive/debian/20250315T025205Z/pool/main/t/texlive-extra/${files[4]}"
    "https://snapshot.debian.org/archive/debian/20250315T025205Z/pool/main/t/texlive-extra/${files[5]}"
  )
  sums=(
    "f96805afa6f936b18c24fcaaf9de63b4b02f43de71b9195647ba01c11336b601"
    "6eb7e1f3cfbe4993817757bc68132a4d7171bdd500084eea9b4d0040c7477d96"
    "e687c9456cf9c7e5133f4599d570409143bcf7b01f8a7a4f4f464bee4acacebb"
    "179c1edecb716ee11420b512bf5e4ba13c30a51eb131fffb6993053511cfa40b"
    "920cb9a3173e178c1d42f9d22378e816adcd34ca0351dfd8dc0f7eb93b5258fb"
    "dd61392705f2c0db4fce398c9d3f936b1baacee94f270c6e5f7fdbabac0fc56e"
  )
  for index in "${!files[@]}"; do
    package_path="$TEX_DEBS/${files[$index]}"
    if [[ ! -f "$package_path" ]]; then
      curl -fL --retry 3 -o "$package_path" "${urls[$index]}"
    fi
    echo "${sums[$index]}  $package_path" | sha256sum -c -
    dpkg-deb -x "$package_path" "$TEX_OVERLAY"
  done
  touch "$TEX_MARKER"
fi

echo "BOOTSTRAP PASS"
python --version
uv --version
go version
elan --version
lake --version
pdflatex --version | head -1
bibtex --version | head -1
