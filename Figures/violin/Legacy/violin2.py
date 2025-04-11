import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取 Excel 数据
df = pd.read_excel("AES.xlsx")

# 2. 为每个 Task 列出它在 group 列下可能出现的 4 种取值（改顺序）
task_map = {
    "stroop squared": [
        "stroop_squared_Fully Incongruent",
        "stroop_squared_Stimulus Congruent, Response Incongruent",
        "stroop_squared_Stimulus Incongruent, Response Congruent",
        "stroop_squared_Fully Congruent"
    ],
    "flanker letter squared": [
        "flanker_letter_squared_Fully Incongruent",
        "flanker_letter_squared_Stimulus Congruent, Response Incongruent",
        "flanker_letter_squared_Stimulus Incongruent, Response Congruent",
        "flanker_letter_squared_Fully Congruent"
    ],
    "flanker number squared": [
        "flanker_number_squared_Fully Incongruent",
        "flanker_number_squared_Stimulus Congruent, Response Incongruent",
        "flanker_number_squared_Stimulus Incongruent, Response Congruent",
        "flanker_number_squared_Fully Congruent"
    ]
}

# 3. 定义用于在图表上显示更简洁 x 轴标签的映射
short_label_map = {
    "stroop_squared_Fully Congruent": "Fully Cong",
    "stroop_squared_Fully Incongruent": "Fully Incong",
    "stroop_squared_Stimulus Congruent, Response Incongruent": "Stim.Cong,\nResp.Incong",
    "stroop_squared_Stimulus Incongruent, Response Congruent": "Stim.Incong,\nResp.Cong",

    "flanker_letter_squared_Fully Congruent": "Fully Cong",
    "flanker_letter_squared_Fully Incongruent": "Fully Incong",
    "flanker_letter_squared_Stimulus Congruent, Response Incongruent": "Stim.Cong,\nResp.Incong",
    "flanker_letter_squared_Stimulus Incongruent, Response Congruent": "Stim.Incong,\nResp.Cong",

    "flanker_number_squared_Fully Congruent": "Fully Cong",
    "flanker_number_squared_Fully Incongruent": "Fully Incong",
    "flanker_number_squared_Stimulus Congruent, Response Incongruent": "Stim.Cong,\nResp.Incong",
    "flanker_number_squared_Stimulus Incongruent, Response Congruent": "Stim.Incong,\nResp.Cong"
}

# 4. 创建画布：1 行 3 列(3 个子图)，共同共享 y 轴
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), sharey=True)
fig.patch.set_facecolor('white')  # 若需要白色背景

# 逐个 Task 画子图
for i, (task_name, group_list) in enumerate(task_map.items()):
    ax = axes[i]
    
    # 构造 violinplot 数据，x 轴上4个位置
    data_for_violin = []
    x_positions = [1, 2, 3, 4]

    # 依次把每个 group（condition）的数值取出来
    for grp in group_list:
        # 这里假设你的表里，指标列叫 "group_accuracy"（若不同请改）
        series_data = df.loc[df["group"] == grp, "group_accuracy"]
        data_for_violin.append(series_data)

    # ---- 小提琴图 ----
    vplot = ax.violinplot(
        dataset=data_for_violin,
        positions=x_positions,
        showmeans=False,
        showextrema=False,
        widths=0.7
    )
    # 给小提琴加淡颜色+半透明
    for body in vplot['bodies']:
        body.set_facecolor("#87CEFA")
        body.set_alpha(0.6)

    # ---- 箱线图 ----
    bp = ax.boxplot(
        data_for_violin,
        positions=x_positions,
        widths=0.15,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor='white', edgecolor='black')
    )

    # ---- 均值散点 ----
    # 计算每一组的均值，然后在 x=1,2,3,4 画出来
    mean_vals = [np.mean(g) for g in data_for_violin]
    ax.scatter(x_positions, mean_vals, color='red', zorder=3, s=60)

    # ---- 设置 x 轴标签 ----
    x_ticklabels = [short_label_map[g] for g in group_list]
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_ticklabels, fontsize=10)

    # ---- 设置子图标题等 ----
    ax.set_title(task_name, fontsize=13, fontweight='bold')
    if i == 0:
        ax.set_ylabel("Group accuracy", fontsize=12)
    
    # 去掉顶部、右侧边框 + 增加水平网格(可选)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

# 5. 调整布局并显示
plt.tight_layout()
plt.show()
