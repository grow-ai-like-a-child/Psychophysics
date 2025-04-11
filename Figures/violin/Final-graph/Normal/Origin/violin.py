import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取 Excel 数据
df = pd.read_excel("AES23.xlsx")

# 2. 构建映射关系
task_map = {
    "Stroop": ("stroop_Congruent", "stroop_Incongruent"),
    "Flanker Letter": ("flanker_letter_Congruent", "flanker_letter_Incongruent"),
    "Flanker Number": ("flanker_number_Congruent", "flanker_number_Incongruent")
}

# 3. 创建画布：1行3列，3个子图
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 5), sharey=True)
fig.patch.set_facecolor('white')  # 整体背景白色

# 逐个 Task 画图
for i, (task_name, (cong_label, incong_label)) in enumerate(task_map.items()):
    ax = axes[i]
    
    # 取出 Congruent / Incongruent 的 Accuracy
    cong_data = df.loc[df["group"] == cong_label, "group_accuracy"]
    incong_data = df.loc[df["group"] == incong_label, "group_accuracy"]
    data_for_violin = [cong_data, incong_data]

    # x 轴上两个位置
    positions = [1, 2]

    # ---- 小提琴图 (violinplot) ----
    vplot = ax.violinplot(
        dataset=data_for_violin,
        positions=positions,
        showmeans=False,
        showextrema=False,
        widths=0.7
    )
    
    # 两个小提琴分别指定不同颜色
    violin_colors = ["#9ecae1", "#a1d99b"]  # 浅蓝、浅绿
    for j, body in enumerate(vplot['bodies']):
        body.set_facecolor(violin_colors[j])
        body.set_alpha(0.6)

    # ---- 箱线图 (boxplot) ----
    bp = ax.boxplot(
        data_for_violin,
        positions=positions,
        widths=0.1,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor='white', edgecolor='black')
    )

    # ---- 均值散点 ----
    ax.scatter(
        [1, 2],
        [cong_data.mean(), incong_data.mean()],
        color='red',
        zorder=3,
        s=60
    )

    # ---- 设置子图坐标轴和标题 ----
    ax.set_xticks(positions)
    ax.set_xticklabels(["Congruent", "Incongruent"], fontsize=16)
    ax.set_title(task_name, fontsize=18, fontweight='bold')

    # 只在第一个子图显示 y 轴标签
    if i == 0:
        ax.set_ylabel("Group Accuracy", fontsize=16)

    # 去掉顶部和右侧边框
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    
    # 打开水平网格线(只在 y 轴)
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

# 4. 调整布局
plt.tight_layout()

# 5. 保存为 PDF 文件（示例文件名：my_plot.pdf）
plt.savefig("my_plot.pdf", bbox_inches='tight')  

# 如需在脚本运行后显示窗口，可以保留下面这行
plt.show()
