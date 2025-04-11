import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# ========== 1) 读取 Excel ==========
#  请将 "AES23.xlsx" 改成你的真实文件路径/名字
df = pd.read_excel("AES23.xlsx")

# ========== 2) 根据 group 列内容，映射到 4 个条件 ==========
def label_four_conditions(g):
    """
    根据字符串 g 来识别是哪种(4类)大条件：
    - 'Fully Congruent'
    - 'Fully Incongruent'
    - 'Stimulus Congruent, Response Incongruent'
    - 'Stimulus Incongruent, Response Congruent'
    如果不符合四大类，返回 None
    """
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

df["FourCond"] = df["group"].apply(label_four_conditions)
df.dropna(subset=["FourCond"], inplace=True)

# ========== 3) 按 (model_name, FourCond) 分组，对 group_accuracy 求平均 ==========
df_agg = df.groupby(["model_name", "FourCond"], as_index=False)["group_accuracy"].mean()

# ========== 4) 准备画四种条件的连线小提琴图 ==========
conditions = [
    "Fully Congruent",
    "Fully Incongruent",
    "Stimulus Congruent, Response Incongruent",
    "Stimulus Incongruent, Response Congruent"
]
positions = [1, 2, 3, 4]

plt.figure(figsize=(15, 9), dpi=300)
plt.title("Four Condition Comparisons: Averaged over 3 tasks", 
          fontsize=20.5, fontweight='bold')  # 字体加大

fig = plt.gcf()
fig.patch.set_facecolor('white')  # 保证背景是白色

# 4A) 小提琴图数据
data_for_violin = []
for cond in conditions:
    vals = df_agg.loc[df_agg["FourCond"] == cond, "group_accuracy"]
    data_for_violin.append(vals)

vplot = plt.violinplot(
    dataset=data_for_violin,
    positions=positions,
    showmeans=False,
    showextrema=False,
    widths=0.6
)

# 给每个小提琴上色 + 黑色描边
colors_for_violins = ["#9ecae1", "#a1d99b", "#fdae6b", "#c994c7"]
for i, body in enumerate(vplot['bodies']):
    body.set_facecolor(colors_for_violins[i])
    body.set_edgecolor("black")
    body.set_linewidth(1.2)
    body.set_alpha(0.8)

# 4B) 画每个 model_name 在 4 个条件上的连线 + 散点
unique_models = df_agg["model_name"].unique()
scatter_colors = ["#3182bd", "#31a354", "#e6550d", "#7b3294"]
condition_to_color = dict(zip(conditions, scatter_colors))

for m in unique_models:
    # 收集该模型在4个条件下的值(若无则 np.nan)
    yvals = []
    for cond in conditions:
        row = df_agg.loc[(df_agg["model_name"] == m) & (df_agg["FourCond"] == cond), "group_accuracy"]
        if len(row) > 0:
            yvals.append(row.iloc[0])
        else:
            yvals.append(np.nan)
    
    # 连线(灰色、半透明)
    plt.plot(positions, yvals, color="gray", alpha=0.4, linewidth=1)
    
    # 散点(每个x位置用对应颜色，点大小改为s=20)
    for x_pos, y_val, c_label in zip(positions, yvals, conditions):
        plt.scatter(x_pos, y_val, color=condition_to_color[c_label], s=20, alpha=0.9)

# ========== 5) 做配对统计检验(示例:配对 t 检验) + 添加星标 ==========

# （1）先将 df_agg pivot 成“宽格式”：行=每个 model_name, 列=每个FourCond
df_wide = df_agg.pivot(index="model_name", columns="FourCond", values="group_accuracy")

# 我们要比较的三对条件(对应positions: 1-2, 2-3, 3-4)
pairs = [
    ("Fully Congruent", "Fully Incongruent"),
    ("Fully Incongruent", "Stimulus Congruent, Response Incongruent"),
    ("Stimulus Congruent, Response Incongruent", "Stimulus Incongruent, Response Congruent")
]

# 定义一个根据p值返回星号的函数
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

# 用来记录每个 pair 上方标注线的 y 值大概位置
y_max = df_agg["group_accuracy"].max()
line_height = y_max + 0.05  # 起始标注高度
height_step = 0.05         # 每加一条线，往上错一些，避免重叠

for i, (condA, condB) in enumerate(pairs):
    # 两个条件在 x 轴上的位置
    x1 = conditions.index(condA) + 1
    x2 = conditions.index(condB) + 1
    
    # 从 pivot 表里取出这两个条件列，做配对 t 检验(忽略 NaN)
    a_vals = df_wide[condA].dropna()
    b_vals = df_wide[condB].dropna()
    
    # 如果两列都有数据，则执行 t 检验
    if len(a_vals) > 1 and len(b_vals) > 1:
        t_stat, p_val = ttest_rel(a_vals, b_vals, nan_policy='omit')
        star_label = get_star(p_val)

        # ========== 在 IDLE 里打印配对检验结果 ==========
        print(f"{condA} vs. {condB} -> t={t_stat:.3f}, p={p_val:.3e}, star={star_label}")

    else:
        # 若数据不足，标记为 n.s.
        star_label = "n.s."
        print(f"{condA} vs. {condB} -> 数据不足，n.s.")
    
    # 画连线(连 x1, x2) + 中间放星号
    h = line_height + i * height_step
    ax.plot([x1, x1, x2, x2], [h, h+0.01, h+0.01, h], lw=1.2, c='black')
    ax.text((x1 + x2)*0.5, h+0.012, star_label, ha='center', va='bottom',
            fontsize=14, fontweight='bold')

# ========== 6) 美化坐标轴、网格、边框等 ==========

plt.xticks(
    positions,
    [
        "Fully Congruent",
        "Fully Incongruent",
        "Stimulus-congruent/\nResponse-incongruent",
        "Stimulus-incongruent/\nResponse-congruent"
    ],
    fontsize=19
)

plt.ylabel("Group Accuracy", fontsize=20)
plt.grid(axis='y', linestyle='--', alpha=0.5)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
# ==== 同时输出为 PNG 和 PDF，让两者大小一致 ====
# 若只需 PDF，可把保存 PNG 的行注释掉
plt.savefig("Flanker_Letter_Comparison.png", dpi=300, bbox_inches='tight')
plt.savefig("Flanker_Letter_Comparison.pdf", dpi=300, bbox_inches='tight')
plt.show()
