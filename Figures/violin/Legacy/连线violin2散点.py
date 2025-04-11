import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import friedmanchisquare

# ========== 1) 读取 Excel ==========
df = pd.read_excel("AES23.xlsx")  # 替换成你实际文件路径

# ========== 2) 根据 group 列映射到 4大条件(你的顺序) ==========

def label_four_conditions(g):
    if isinstance(g, str):
        if "Fully Incongruent" in g:
            return "Fully Incongruent"
        elif "Stimulus Congruent, Response Incongruent" in g:
            return "Stimulus Congruent, Response Incongruent"
        elif "Stimulus Incongruent, Response Congruent" in g:
            return "Stimulus Incongruent, Response Congruent"
        elif "Fully Congruent" in g:
            return "Fully Congruent"
    return None

df["FourCond"] = df["group"].apply(label_four_conditions)
df.dropna(subset=["FourCond"], inplace=True)

# ========== 3) 聚合(同一个 model_name, 四Cond) => group_accuracy 求平均 ==========
df_agg = df.groupby(["model_name", "FourCond"], as_index=False)["group_accuracy"].mean()

# ========== 4) 小提琴图：4 组, 指定顺序 ==========

conditions = [
    "Fully Incongruent",
    "Stimulus Congruent, Response Incongruent",
    "Stimulus Incongruent, Response Congruent",
    "Fully Congruent"
]
positions = [1, 2, 3, 4]

plt.figure(figsize=(8, 6))
plt.title("Four Condition Comparisons (Averaged over 3 tasks)", fontsize=14, fontweight='bold')
fig = plt.gcf()
fig.patch.set_facecolor('white')  # 设置背景

# 4A) 准备 violinplot 数据
data_for_violin = []
for cond in conditions:
    vals = df_agg.loc[df_agg["FourCond"] == cond, "group_accuracy"]
    data_for_violin.append(vals)

# 在 violinplot 中，加大 points(核密度采样数)，并改 bw_method 让分布更平滑/更宽
vplot = plt.violinplot(
    dataset=data_for_violin,
    positions=positions,
    showmeans=False,
    showextrema=False,
    widths=0.6,
    bw_method='silverman',  # or e.g. 'scott' or numeric (0.3, 0.5, etc.)
    points=200              # 默认为100, 这里设大一些, 曲线更平滑
)

# ========== 4B) 小提琴颜色 + 描边 ==========

colors_for_violins = ["#fdae6b", "#a1d99b", "#9ecae1", "#c994c7"]
for i, body in enumerate(vplot['bodies']):
    body.set_facecolor(colors_for_violins[i])
    body.set_edgecolor("black")
    body.set_linewidth(1.2)
    body.set_alpha(0.8)

# ========== (C) 水平抖动散点 + 连线 ==========

unique_models = df_agg["model_name"].unique()

# 为每个 model_name 分配一个固定 offset ∈ [-0.1, 0.1]
random_offsets = {}
for m in unique_models:
    random_offsets[m] = np.random.uniform(-0.1, 0.1)

scatter_colors = ["#e6550d", "#31a354", "#3182bd", "#7b3294"]
cond_to_color = dict(zip(conditions, scatter_colors))

for m in unique_models:
    # 获取该模型在4条件下的值
    yvals = []
    for cond in conditions:
        row = df_agg.loc[(df_agg["model_name"] == m) & (df_agg["FourCond"] == cond), "group_accuracy"]
        yval = row.iloc[0] if len(row)>0 else np.nan
        yvals.append(yval)

    offset = random_offsets[m]
    x_jitters = [pos + offset for pos in positions]

    # 连线(灰色)
    plt.plot(x_jitters, yvals, color="gray", alpha=0.4, linewidth=1)

    # 散点(颜色)
    for x_j, y_v, cond_name in zip(x_jitters, yvals, conditions):
        plt.scatter(x_j, y_v, color=cond_to_color[cond_name], s=50, alpha=0.9)

# ========== (D) Friedman 检验(四组比较) + 显著星号(若p<0.05) ==========

df_wide = df_agg.pivot(index="model_name", columns="FourCond", values="group_accuracy").dropna(axis=0)
stats, p_value = friedmanchisquare(
    df_wide["Fully Incongruent"],
    df_wide["Stimulus Congruent, Response Incongruent"],
    df_wide["Stimulus Incongruent, Response Congruent"],
    df_wide["Fully Congruent"]
)
print(f"Friedman statistic = {stats:.3f}, p = {p_value:.4e}")

if p_value < 0.05:
    max_val = max([vals.max() for vals in data_for_violin if len(vals) > 0])
    bar_y = max_val + 0.05
    plt.plot([1, 4], [bar_y, bar_y], color="black", linewidth=1.5)
    # 星号个数简单区分
    star_text = "*"
    if p_value < 0.001:
        star_text = "****"
    elif p_value < 0.01:
        star_text = "***"
    elif p_value < 0.05:
        star_text = "*"
    plt.text(2.5, bar_y+0.01, star_text, ha='center', va='bottom', fontsize=16)

# ========== (E) 美化坐标轴 ==========

plt.xticks(positions, conditions, fontsize=11)
plt.ylabel("Group accuracy", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
