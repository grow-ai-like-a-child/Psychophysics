import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# ========== 1) 读取 Excel + 筛选仅 flanker_letter ==========
df = pd.read_excel("AES23.xlsx")
df_flanker_letter = df[df["group"].str.contains("flanker_letter", case=False, na=False)]

# ========== 2) 根据 group 列内容，映射到 4 个条件 ==========

def label_four_conditions(g):
    if isinstance(g, str):
        if "Fully Congruent" in g:
            return "Fully Congruent"
        elif "Fully Incongruent" in g:
            return "Fully Incongruent"
        elif "Stimulus Congruent, Response Incongruent" in g:
            return "Stimulus Congruent, Response Incongruent"
        elif "Stimulus Incongruent, Response Congruent" in g:
            return "Stimulus Incongruent, Response Congruent"
    return None

df_flanker_letter["FourCond"] = df_flanker_letter["group"].apply(label_four_conditions)
df_flanker_letter.dropna(subset=["FourCond"], inplace=True)

# ========== 3) 按 (model_name, FourCond) 分组，对 group_accuracy 求平均 (仅在 flanker_letter 内) ==========
df_agg_fl = df_flanker_letter.groupby(["model_name", "FourCond"], as_index=False)["group_accuracy"].mean()

# ========== 4) 准备画四种条件的小提琴图 + 散点连线 ==========

conditions = [
    "Fully Congruent",
    "Fully Incongruent",
    "Stimulus Congruent, Response Incongruent",
    "Stimulus Incongruent, Response Congruent"
]
positions = [1, 2, 3, 4]

plt.figure(figsize=(12.5, 7.5), dpi=300)
plt.title("Flanker Letter: 4 Condition Comparisons", 
          fontsize=18, fontweight='bold')

fig = plt.gcf()
fig.patch.set_facecolor('white')  # 保证背景白色

# 4A) 小提琴图数据
data_for_violin = []
for cond in conditions:
    vals = df_agg_fl.loc[df_agg_fl["FourCond"] == cond, "group_accuracy"]
    data_for_violin.append(vals)

vplot = plt.violinplot(
    dataset=data_for_violin,
    positions=positions,
    showmeans=False,
    showextrema=False,
    widths=0.6
)

# 给每个小提琴上色 + 描边
colors_for_violins = ["#9ecae1", "#a1d99b", "#fdae6b", "#c994c7"]
for i, body in enumerate(vplot['bodies']):
    body.set_facecolor(colors_for_violins[i])
    body.set_edgecolor("black")
    body.set_linewidth(1.2)
    body.set_alpha(0.8)

# 4B) 画每个 model_name 在 4 个条件上的连线 + 散点
unique_models = df_agg_fl["model_name"].unique()
scatter_colors = ["#3182bd", "#31a354", "#e6550d", "#7b3294"]
condition_to_color = dict(zip(conditions, scatter_colors))

for m in unique_models:
    # 收集该模型在4个条件下的值(若无则 np.nan)
    yvals = []
    for cond in conditions:
        row = df_agg_fl.loc[(df_agg_fl["model_name"] == m) & (df_agg_fl["FourCond"] == cond), "group_accuracy"]
        if len(row) > 0:
            yvals.append(row.iloc[0])
        else:
            yvals.append(np.nan)
    
    # 连线(灰色、半透明)
    plt.plot(positions, yvals, color="gray", alpha=0.4, linewidth=1)
    
    # 散点(每个x位置用对应颜色，点大小 s=20)
    for x_pos, y_val, c_label in zip(positions, yvals, conditions):
        plt.scatter(x_pos, y_val, color=condition_to_color[c_label], s=20, alpha=0.9)

# ========== 5) 做配对 t 检验 + 添加星标 ==========

# pivot 成“宽格式”：行= model_name, 列= FourCond
df_wide_fl = df_agg_fl.pivot(index="model_name", columns="FourCond", values="group_accuracy")

pairs = [
    ("Fully Congruent", "Fully Incongruent"),
    ("Fully Incongruent", "Stimulus Congruent, Response Incongruent"),
    ("Stimulus Congruent, Response Incongruent", "Stimulus Incongruent, Response Congruent")
]

def get_star(p_value):
    if p_value < 1e-4:
        return "****"
    elif p_value < 0.001:
        return "***"
    elif p_value < 0.01:
        return "**"
    elif p_value < 0.05:
        return "*"
    else:
        return "n.s."

ax = plt.gca()
y_max = df_agg_fl["group_accuracy"].max()
line_height = y_max + 0.05
height_step = 0.05

for i, (condA, condB) in enumerate(pairs):
    x1 = conditions.index(condA) + 1
    x2 = conditions.index(condB) + 1
    
    a_vals = df_wide_fl[condA].dropna()
    b_vals = df_wide_fl[condB].dropna()
    
    if len(a_vals) > 1 and len(b_vals) > 1:
        t_stat, p_val = ttest_rel(a_vals, b_vals, nan_policy='omit')
        star_label = get_star(p_val)
        print(f"[Flanker Letter] {condA} vs. {condB} -> t={t_stat:.3f}, p={p_val:.3e}, star={star_label}")
    else:
        star_label = "n.s."
        print(f"[Flanker Letter] {condA} vs. {condB} -> 数据不足，n.s.")

    h = line_height + i * height_step
    ax.plot([x1, x1, x2, x2], [h, h+0.01, h+0.01, h], lw=1.2, c='black')
    ax.text((x1 + x2)*0.5, h+0.012, star_label, ha='center', va='bottom',
            fontsize=14, fontweight='bold')

# ========== 6) 美化 ==========

plt.xticks(
    positions,
    [
        "Fully Congruent",
        "Fully Incongruent",
        "Stimulus-congruent/\nResponse-incongruent",
        "Stimulus-incongruent/\nResponse-congruent"
    ],
    fontsize=16
)

plt.ylabel("Group Accuracy", fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
# ==== 同时输出为 PNG 和 PDF，让两者大小一致 ====
# 若只需 PDF，可把保存 PNG 的行注释掉
plt.savefig("Flanker_Letter_Comparison.png", dpi=300, bbox_inches='tight')
plt.savefig("Flanker_Letter_Comparison.pdf", dpi=300, bbox_inches='tight')
plt.show()
