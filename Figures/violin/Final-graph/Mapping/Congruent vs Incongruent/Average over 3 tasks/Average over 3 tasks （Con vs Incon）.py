import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# ========== 1) 读取 Excel ==========
df = pd.read_excel("AES23.xlsx")  # 请替换为你实际的路径或文件名

# ========== 2) 函数: 根据 group 列是否以 '_Congruent' / '_Incongruent' 结尾来分组 ==========
def label_congruency(g):
    if isinstance(g, str):
        if g.endswith("_Congruent"):
            return "Congruent"
        elif g.endswith("_Incongruent"):
            return "Incongruent"
    return None

df["C_I_condition"] = df["group"].apply(label_congruency)
df.dropna(subset=["C_I_condition"], inplace=True)

# ========== 3) 按 (model_name, C_I_condition) 分组，对 group_accuracy 求平均 ==========
df_agg = df.groupby(["model_name", "C_I_condition"], as_index=False)["group_accuracy"].mean()

# ========== 4) 只比较 Congruent vs. Incongruent ==========
conditions = ["Congruent", "Incongruent"]
positions = [1, 2]

plt.figure(figsize=(10, 6), dpi=300)
plt.title("Congruent vs. Incongruent: Averaged over 3 tasks", 
          fontsize=18, fontweight='bold')

# ========== 4A) 整理小提琴图数据 ==========
data_for_violin = []
for cond in conditions:
    vals = df_agg.loc[df_agg["C_I_condition"] == cond, "group_accuracy"]
    data_for_violin.append(vals)

vplot = plt.violinplot(
    dataset=data_for_violin,
    positions=positions,
    showmeans=False,
    showextrema=False,
    widths=0.6
)

colors_for_violins = ["#9ecae1", "#a1d99b"]  # 左蓝右绿(柔和调)
for i, body in enumerate(vplot['bodies']):
    body.set_facecolor(colors_for_violins[i])
    body.set_edgecolor("black")
    body.set_linewidth(1.2)
    body.set_alpha(0.8)

# ========== 4B) 每个模型的散点 + 连线 ==========
colors_for_scatter = {
    "Congruent": "#3182bd",   # 深蓝
    "Incongruent": "#31a354"  # 深绿
}
unique_models = df_agg["model_name"].unique()

for m in unique_models:
    # 获取该模型在 Congruent / Incongruent 条件的均值
    row_cong = df_agg.loc[
        (df_agg["model_name"] == m) &
        (df_agg["C_I_condition"] == "Congruent"),
        "group_accuracy"
    ]
    val_cong = row_cong.iloc[0] if len(row_cong) > 0 else np.nan

    row_incong = df_agg.loc[
        (df_agg["model_name"] == m) &
        (df_agg["C_I_condition"] == "Incongruent"),
        "group_accuracy"
    ]
    val_incong = row_incong.iloc[0] if len(row_incong) > 0 else np.nan

    # 连线(灰色半透明)
    plt.plot([1, 2], [val_cong, val_incong], color="gray", alpha=0.5, linewidth=1)
    
    # 散点
    plt.scatter(1, val_cong, color=colors_for_scatter["Congruent"], s=40, alpha=0.8)
    plt.scatter(2, val_incong, color=colors_for_scatter["Incongruent"], s=40, alpha=0.8)

# ========== 5) 配对 t 检验 + 添加星号 & 打印结果 ==========
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

cong_vals = data_for_violin[0]  # Congruent 数据
incong_vals = data_for_violin[1]  # Incongruent 数据

tstat, pval = ttest_rel(cong_vals, incong_vals)
star_label = get_star(pval)

print(f"Paired t-test (Congruent vs. Incongruent): t={tstat:.3f}, p={pval:.3g}, star={star_label}")

# 在图上方标注
max_val = max(cong_vals.max(), incong_vals.max())

# 将星标横线位置略向下：由 +0.05 改为 +0.04
bar_y = max_val + 0.04
plt.plot([1, 2], [bar_y, bar_y], color="black", linewidth=2)

# 将星标与横线的距离略减：由 +0.01 改为 +0.005
plt.text(1.5, bar_y + 0.005, star_label, ha='center', va='bottom', fontsize=16)

# ========== 6) 美化坐标轴 ==========
plt.xticks(positions, conditions, fontsize=16)
plt.ylabel("Group Accuracy", fontsize=16)
plt.grid(axis='y', linestyle='--', alpha=0.5)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# ==== 同时输出为 PNG 和 PDF，让两者大小一致 ====
# 若只需 PDF，可把保存 PNG 的行注释掉
plt.savefig("Flanker_Letter_Comparison.png", dpi=300, bbox_inches='tight')
plt.savefig("Flanker_Letter_Comparison.pdf", dpi=300, bbox_inches='tight')

# 如需要显示图窗口，可保留此行
plt.show()
