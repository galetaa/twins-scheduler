#!/usr/bin/env python3
"""Render the exact budget in Eq. (4); requires matplotlib for regeneration."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
k = 4
palette = ListedColormap(["#eef2f6", "#c9dce6", "#90b9ce", "#5088a9", "#205270"])
norm = BoundaryNorm(np.arange(-.5, 5.5, 1), palette.N)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
fig, axes = plt.subplots(1, 3, figsize=(7.35, 2.75), constrained_layout=True)
for ax, capacity in zip(axes, [0, 2, 4]):
    data = np.full((6, 6), np.nan)
    for d0 in range(5):
        for d1 in range(5):
            data[d1, d0] = max(0, d0 + d1 - k - capacity)
    ax.imshow(data, origin="lower", cmap=palette, norm=norm)
    for d0 in range(5):
        for d1 in range(5):
            value = int(data[d1, d0])
            ax.text(d0, d1, str(value), ha="center", va="center",
                    color="white" if value >= 3 else "#172d3b", fontsize=10)
    ax.set_xticks(range(6)); ax.set_yticks(range(6))
    ax.set_xticks(np.arange(-.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 6, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_xlabel(r"First deficit $d_0$")
    ax.set_title(rf"$k=4,\quad \alpha(H)={capacity}$", pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
axes[0].set_ylabel(r"Second deficit $d_1$")
target = ROOT / "manuscript" / "figures" / "repair_frontier_boundary.pdf"
fig.savefig(target, metadata={"Title": "Minimum phase-control budget",
                             "Author": "Anonymous", "CreationDate": None})
fig.savefig(target.with_suffix(".png"), dpi=190)
print(target)
