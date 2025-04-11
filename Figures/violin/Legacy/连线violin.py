import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

# 1. 读取 Excel 文件 (替换为你实际的路径/文件名)
df = pd.read_excel("AES23.xlsx")

# 2. 函数: 根据 group 列是否以 '_Congruent' / '_Incongruent' 结尾来分组
def label_congruency(g):
    if isinstance(g, str):
        if g.endswith("_Congruent"):
            return "Congruent"
        elif g.endswith("_Incongruent"):
            return "Incongruent"
    return None

# 3. 新增列 "C_I_condition"
df["C_I_condition"] = df["group"].apply(label_congruency)
df.dropna(subset=["C_I_condition"], inplace=True)

# 4. 按 (model_name, C_I_condition) 分组，对 group_accuracy 求平均
df_agg = df.groupby(["model_name", "C_I_condition"], as_index=False)["group_accuracy"].mean()

# 5. 小提琴图：只比较 Congruent vs. Incongruent
conditions = ["Congruent", "Incongruent"]
positions = [1, 2]

plt.figure(figsize=(6, 6))
plt.title("Congruent vs. Incongruent (Averaged over 3 tasks)", 
          fontsize=14, fontweight='bold')

# --- 5A) 整理小提琴数据 ---
data_for_violin = []
for cond in conditions:
    vals = df_agg.loc[df_agg["C_I_condition"] == cond, "group_accuracy"]
    data_for_violin.append(vals)

# --- 5B) 小提琴图 ---
vplot = plt.violinplot(
    dataset=data_for_violin,
    positions=positions,
    showmeans=False,
    showextrema=False,
    widths=0.6
)

# 自定义两把小提琴的颜色、描边(黑色)、透明度
# vplot['bodies'] 是一个列表，依次对应 positions 中的每个小提琴
colors_for_violins = ["#9ecae1", "#a1d99b"]  # 左蓝右绿(柔和调)
for i, body in enumerate(vplot['bodies']):
    body.set_facecolor(colors_for_violins[i])    # 填充色
    body.set_edgecolor("black")                 # 黑色描边
    body.set_linewidth(1.2)                     # 描边线宽
    body.set_alpha(0.8)                         # 半透明度



# --- 5D) 每个模型的散点 + 连线 ---
# 为 Congruent 和 Incongruent 再各选一个颜色(比小提琴略深)
colors_for_scatter = {"Congruent": "#3182bd",  # 深蓝
                      "Incongruent": "#31a354"} # 深绿

unique_models = df_agg["model_name"].unique()

for m in unique_models:
    # 获取该模型在 Congruent / Incongruent 的均值
    row_cong = df_agg.loc[(df_agg["model_name"] == m) & 
                          (df_agg["C_I_condition"] == "Congruent"), "group_accuracy"]
    val_cong = row_cong.iloc[0] if len(row_cong) > 0 else np.nan
    
    row_incong = df_agg.loc[(df_agg["model_name"] == m) & 
                            (df_agg["C_I_condition"] == "Incongruent"), "group_accuracy"]
    val_incong = row_incong.iloc[0] if len(row_incong) > 0 else np.nan

    # 画连线(灰色半透明)
    plt.plot([1,2], [val_cong, val_incong], color="gray", alpha=0.5, linewidth=1)
    
    # 散点(用 Congruent 蓝、Incongruent 绿)
    plt.scatter(1, val_cong, color=colors_for_scatter["Congruent"], s=40, alpha=0.8)
    plt.scatter(2, val_incong, color=colors_for_scatter["Incongruent"], s=40, alpha=0.8)

# --- 5E) (可选) 做一个配对 t 检验并添加星号 ---
cong_vals = data_for_violin[0]
incong_vals = data_for_violin[1]
tstat, pval = ttest_rel(cong_vals, incong_vals)

# 在图上方画一条黑线和星号(****)示意显著
max_val = max(cong_vals.max(), incong_vals.max())
bar_y = max_val + 0.05
plt.plot([1,2], [bar_y, bar_y], color="black", linewidth=2)
plt.text(1.5, bar_y + 0.01, "****", ha='center', va='bottom', fontsize=16)

# --- 5F) 美化坐标轴 ---
plt.xticks(positions, conditions, fontsize=12)
plt.ylabel("Group accuracy", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)  # 仅画 y 轴网格

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.show()
