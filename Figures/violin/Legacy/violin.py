import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取 Excel 数据
df = pd.read_excel("AES.xlsx")

# 2. 构建映射关系
task_map = {
    "Stroop": ("stroop_Congruent", "stroop_Incongruent"),
    "Flanker_letter": ("flanker_letter_Congruent", "flanker_letter_Incongruent"),
    "Flanker_number": ("flanker_number_Congruent", "flanker_number_Incongruent")
}

# 3. 创建画布：1行3列，3个子图
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 5), sharey=True)

# 让整体背景为白色（有些环境默认是灰色）
fig.patch.set_facecolor('white')

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
    # 返回值是一个字典，比如 {'bodies': [...], 'cbars': ...} 等
    vplot = ax.violinplot(
        dataset=data_for_violin,
        positions=positions,
        showmeans=False,
        showextrema=False,
        widths=0.7
    )
    # 给小提琴加一个淡颜色 + 半透明
    for body in vplot['bodies']:
        body.set_facecolor("#87CEFA")  # 浅蓝
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
    # 如果想让中位数线、须线等也变成黑色，可加:
    # medianprops=dict(color='black'), whiskerprops=dict(color='black'), capprops=dict(color='black')

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
    ax.set_xticklabels(["Congruent", "Incongruent"], fontsize=11)
    ax.set_title(task_name, fontsize=13, fontweight='bold')

    # 只在第一个子图显示y轴标签
    if i == 0:
        ax.set_ylabel("Group accuracy", fontsize=12)

    # 去掉顶部和右侧边框，让图更简洁
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    
    # 打开水平网格线(只在 y 轴)
    ax.set_axisbelow(True)  # 让网格在最底层
    ax.grid(axis='y', linestyle='--', alpha=0.6)

# 4. 调整布局并显示
plt.tight_layout()
plt.show()
