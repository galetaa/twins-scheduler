#!/usr/bin/env python3
"""Build the optional Russian revision report with the English reviewer response.

Requires Pandoc, XeLaTeX and the DejaVu font family. The scientific reproduction
entry point checks the manuscript and executable data independently of this report.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def linked_source(path: Path, branch_url: str | None) -> str:
    def rewrite(match: re.Match[str]) -> str:
        label, target = match.groups()
        if target.startswith(("http:", "https:", "#")):
            return match.group(0)
        relative = (path.parent / target).resolve().relative_to(ROOT).as_posix()
        if not branch_url:
            return label + "^[Файл артефакта: \\nolinkurl{" + relative + "}.]"
        return f"[{label}]({branch_url}/{relative})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite, path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--branch-url", help="Published branch URL; omit for local artifact-path footnotes")
    args = parser.parse_args()
    build = ROOT / ".cache/report-build"
    build.mkdir(parents=True, exist_ok=True)
    report = linked_source(ROOT / "docs/reviews/REVISION_REPORT_RU.md", args.branch_url)
    report = report.split("\n", 1)[1].lstrip()
    report = report.replace("**Дата:** 19 октября 2026 года.\n\n", "", 1)
    reply = linked_source(ROOT / "docs/reviews/RESPONSE_TO_REVIEWER.md", args.branch_url)
    source = build / "report.md"
    source.write_text(report + "\n\n\\newpage\n\n\\begingroup\n\\small\n"
                      + "\\setlength{\\parskip}{4pt}\n\n" + reply
                      + "\n\n\\endgroup\n", encoding="utf-8")
    header = build / "header.tex"
    header.write_text(r"""\usepackage{xurl}
\usepackage{fancyhdr}
\usepackage{needspace}
\setlength{\emergencystretch}{3em}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily TWINS SCHEDULER / RESEARCH REVISION}
\fancyfoot[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\headheight}{15pt}
\makeatletter
\renewcommand{\maketitle}{%
  \thispagestyle{fancy}%
  \begin{center}
  {\Large\sffamily\bfseries\@title\par}
  \vspace{5pt}{\small\@date\par}
  \end{center}\vspace{6pt}}
\makeatother
""", encoding="utf-8")
    table_filter = build / "tables.lua"
    table_filter.write_text('''local count = 0
local heights = {200, 260}
function Header(header)
  if pandoc.utils.stringify(header.content):match('^8%. ') then
    return {pandoc.RawBlock('latex', '\\\\Needspace{320pt}'), header}
  end
end
function Table(table)
  count = count + 1
  return {pandoc.RawBlock('latex', '\\\\Needspace{' .. (heights[count] or 220) .. 'pt}\\\\begingroup\\\\small'),
          table, pandoc.RawBlock('latex', '\\\\endgroup')}
end
''', encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "pandoc", str(source), "-f", "markdown+raw_tex", "--pdf-engine=xelatex",
        "--include-in-header", str(header), "--output", str(args.output.resolve()),
        "--lua-filter", str(table_filter),
        "-M", "title=Отчёт об усилении статьи", "-M", "subtitle=Результаты, проверка и ответ рецензенту",
        "-M", "date=19 октября 2026 года", "-V", "mainfont=DejaVu Serif",
        "-V", "sansfont=DejaVu Sans", "-V", "monofont=DejaVu Sans Mono",
        "-V", "fontsize=11pt", "-V", "geometry=a4paper,margin=22mm",
        "-V", "linestretch=1.03", "-V", "colorlinks=true", "-V", "urlcolor=teal",
    ], check=True)


if __name__ == "__main__":
    main()
