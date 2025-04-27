import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from textwrap import fill

# ── 1. 读取数据表 ─────────────────────────────────────────────
default_file = r"E:\Grow-AI\psychophysic\parrot\model_parameters_with_accuracy_and_tasks - model_parameters_with_accuracy_and_tasks.csv.csv"
file_path = input(f"CSV file path [{default_file}]: ").strip() or default_file

df = pd.read_csv(file_path)

# —— 显示列名方便选择 ——
print("\nAvailable columns:")
for col in df.columns:
    print("  •", col)
print()

def ask_col(msg):
    while True:
        name = input(msg).strip()
        if name in df.columns:
            return name
        print("  !! Column not found, please re-enter exactly as shown above.")

x_col = ask_col("Column for X axis: ")
y_col = ask_col("Column for Y axis: ")

def ask(msg, default=""):
    s = input(f"{msg}{f' [{default}]' if default else ''}: ").strip()
    return s or default

x_label = ask("X-axis label", x_col.replace("_", " ").title())
y_label = ask("Y-axis label", y_col.replace("_", " ").title())
title    = ask("Plot title",  f"{x_label} vs {y_label}")

default_out = os.path.join(os.path.dirname(file_path),
                           f"{title.replace(' ', '_')}.pdf")
out_path = ask("Output PDF path", default_out)

# ── 2. 计算数据 ───────────────────────────────────────────────
x = df[x_col]
y = df[y_col]
scale = 30
sizes = np.sqrt(df["params_B"]) * scale
overall_acc = (x + y) / 2

# ★ 统一颜色范围 0–1
norm = plt.Normalize(vmin=0, vmax=1)

# ── 3. 绘图 ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))
sc = ax.scatter(
    x, y,
    s=sizes,
    c=overall_acc,
    cmap="viridis",
    norm=norm,               # ★ 固定颜色归一化
    alpha=0.85,
    edgecolor="k",
    linewidth=0.4,
)

# 参考对角线
ax.set_xlim(0, 1.03)
ax.set_ylim(0, 1.03)
max_lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
ax.plot([0, max_lim], [0, max_lim], ls="--", lw=1, color="grey", zorder=0)

ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel(y_label, fontsize=12)
ax.set_title(fill(title, 60), fontsize=16)
ax.set_aspect("equal")

# 颜色条
cbar = plt.colorbar(
    sc, ax=ax,
    label="Overall Accuracy",
    shrink=0.77,
    pad=0.02
)
# ★ 设定固定刻度（0.0, 0.2, … 1.0）
ticks = np.linspace(0, 1, 6)          # 0,0.2,…,1.0
cbar.set_ticks(ticks)
cbar.set_ticklabels([f"{t:.1f}" for t in ticks])

# 图例（模型大小）
legend_vals = [1, 10, 100]            # 单位 B
handles = [
    Line2D([], [], marker="o", linestyle="",
           markeredgecolor="k", markerfacecolor="lightgray",
           markersize=np.sqrt(np.sqrt(v) * scale),
           label=f"{v} B Params")
    for v in legend_vals
]
ax.legend(handles=handles, title="Model Size",
          loc="upper left", frameon=True)

plt.tight_layout()

# ── 4. 保存 & 显示 ───────────────────────────────────────────
fig.savefig(out_path, format="pdf", bbox_inches="tight")
print(f"\nSaved PDF to: {out_path}")

plt.show()
