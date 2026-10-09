"""Redraw the SoupFold structure prediction results using only the numbers
printed on the original figure (totals, +Soup gains, GPCR and glue values)."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

SP = sys.argv[1]
for w in (400, 600):
    fm.fontManager.addfont(f"{SP}/fonts/PublicSans-{w}.ttf")
plt.rcParams.update({
    "font.family": "Public Sans", "font.size": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#c9c6bf", "axes.linewidth": .8,
    "xtick.color": "#4a4a52", "ytick.color": "#91919b",
    "xtick.major.size": 0, "ytick.major.size": 0,
})

BASE, AF3 = "#a4aec4", "#c4cad8"   # baselines, quiet
SOUP = "#c64b4b"                   # SoupFold, same red as the homepage tile
TEXT, FAINT = "#16161a", "#6a6a73"

foldbench = {
    "Antibody-antigen": dict(af3=52.4, base=[47.6, 52.4, 59.4], gain=[14.1, 10.6, 8.8], ylim=(30, 75)),
    "Protein-ligand":   dict(af3=61.2, base=[62.7, 64.3, 55.3], gain=[3.2, 3.4, 8.4],   ylim=(50, 72)),
    "Protein-protein":  dict(af3=74.1, base=[74.5, 75.9, 74.1], gain=[3.3, 2.2, 4.4],   ylim=(60, 82)),
}
anchors = ["Protenix", "ESMFold2", "OpenDDE"]
hard = {
    "GPCR":           dict(vals=[49.3, 49.3, 43.5, 46.4], soup=56.5, ylim=(35, 60)),
    "Molecular glue": dict(vals=[31.8, 28.4, 30.7, 31.8], soup=39.8, ylim=(20, 43)),
}
models = ["AF3", "Protenix", "ESMFold2", "OpenDDE"]

fig = plt.figure(figsize=(11.6, 7.0), dpi=200)
gs = fig.add_gridspec(2, 6, height_ratios=[1, 1], hspace=.55, wspace=.9)

def style(ax, title, ylim):
    ax.set_title(title, fontsize=12, fontweight=600, color=TEXT, pad=12)
    ax.set_ylim(*ylim)
    ax.grid(axis="y", color="#eceae5", linewidth=.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", labelsize=9)

for i, (name, d) in enumerate(foldbench.items()):
    ax = fig.add_subplot(gs[0, 2 * i:2 * i + 2])
    w, step, x0 = .42, 1.3, 1.35
    ax.bar(0, d["af3"], .5, color=BASE)
    ax.text(0, d["af3"] + .6, f"{d['af3']:.1f}", ha="center", va="bottom", fontsize=8.5, color=FAINT)
    for j, (b, g) in enumerate(zip(d["base"], d["gain"])):
        x = x0 + j * step
        ax.bar(x - w / 2, b, w, color=BASE)
        ax.bar(x + w / 2, b + g, w, color=SOUP)
        ax.text(x - w / 2 - .06, b + .6, f"{b:.1f}", ha="center", va="bottom", fontsize=8, color=FAINT)
        ax.text(x + w / 2, b + g + .6, f"+{g:.1f}", ha="center", va="bottom", fontsize=8, color=SOUP, fontweight=600)
    ax.set_xticks([0] + [x0 + j * step for j in range(3)], ["AF3"] + anchors, fontsize=8.5)
    style(ax, name, d["ylim"])
    if i == 0:
        ax.set_ylabel("Success rate (%)", fontsize=9.5, color=FAINT)

for i, (name, d) in enumerate(hard.items()):
    ax = fig.add_subplot(gs[1, 3 * i:3 * i + 3])
    xs = range(5)
    vals = d["vals"] + [d["soup"]]
    cols = [BASE, BASE, BASE, BASE, SOUP]
    ax.bar(xs, vals, .62, color=cols)
    for x, v, c in zip(xs, vals, cols):
        ax.text(x, v + .5, f"{v:.1f}", ha="center", va="bottom", fontsize=8.5,
                color=SOUP if c == SOUP else FAINT, fontweight=600 if c == SOUP else 400)
    ax.set_xticks(list(xs), models + ["SoupFold"], fontsize=8.5)
    ax.get_xticklabels()[-1].set_color(SOUP); ax.get_xticklabels()[-1].set_fontweight(600)
    style(ax, name, d["ylim"])
    if i == 0:
        ax.set_ylabel("Success rate (%)", fontsize=9.5, color=FAINT)

from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=BASE, label="Base model"), Patch(color=SOUP, label="With SoupFold")],
           loc="lower center", ncol=2, frameon=False, fontsize=9.5, bbox_to_anchor=(.5, -.01))
fig.savefig(f"{SP}/soupfold_results_v2.png", bbox_inches="tight", facecolor="white", pad_inches=.2)
print("saved")
