"""Redraw the ADMET win/draw/loss figure; every value is printed on the original."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Patch

SP = sys.argv[1]
for w in (400, 600):
    fm.fontManager.addfont(f"{SP}/fonts/PublicSans-{w}.ttf")
plt.rcParams.update({"font.family": "Public Sans", "font.size": 10.5})

WIN, DRAW, LOSS = "#2f877e", "#e4e2dd", "#d9a597"   # win uses the homepage ADMET teal
TEXT, FAINT = "#16161a", "#6a6a73"
rows = ["MolE", "KPGT", "Mini.", "QIP", "UniMol"]
data = {   # (win, draw, loss) per baseline, top to bottom
    "Absorption":   [(100, 0, 0), (33, 33, 33), (67, 17, 17), (33, 33, 33), (100, 0, 0)],
    "Distribution": [(100, 0, 0), (100, 0, 0), (100, 0, 0), (67, 0, 33), (100, 0, 0)],
    "Metabolism":   [(33, 0, 67), (17, 0, 83), (17, 0, 83), (33, 17, 50), (100, 0, 0)],
    "Excretion":    [(67, 33, 0), (67, 33, 0), (67, 33, 0), (67, 33, 0), (67, 33, 0)],
    "Toxicity":     [(100, 0, 0), (75, 25, 0), (75, 25, 0), (75, 25, 0), (100, 0, 0)],
}

fig, axes = plt.subplots(1, 5, figsize=(13, 3.6), dpi=200, sharey=True)
fig.subplots_adjust(wspace=.08)
for ax, (name, vals) in zip(axes, data.items()):
    for i, (w, d, l) in enumerate(vals):
        y = len(rows) - 1 - i
        left = 0
        for v, c, tc in ((w, WIN, "#fff"), (d, DRAW, FAINT), (l, LOSS, TEXT)):
            if v:
                ax.barh(y, v, .72, left=left, color=c, edgecolor="white", linewidth=1.2)
                ax.text(left + v / 2, y, f"{v}", ha="center", va="center", fontsize=8.5, color=tc)
                left += v
    ax.set_xlim(0, 100)
    ax.set_title(name, fontsize=12, fontweight=600, color=TEXT, pad=10)
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=9.5, colors="#4a4a52")
axes[0].set_yticks(range(len(rows)), rows[::-1])
fig.legend(handles=[Patch(color=WIN, label="Win"), Patch(color=DRAW, label="Draw"), Patch(color=LOSS, label="Loss")],
           loc="lower center", ncol=3, frameon=False, fontsize=9.5, bbox_to_anchor=(.5, -.06))
fig.savefig(f"{SP}/admet_results_v2.png", bbox_inches="tight", facecolor="white", pad_inches=.2)
print("saved")
