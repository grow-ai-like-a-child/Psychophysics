import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 读取 Excel 数据
df = pd.read_excel("AES23.xlsx")

# 2. 为每个 Task 列出它在 group 列下可能出现的 4 种取值
task_map = {
    "Stroop Squared": [
        "stroop_squared_Fully Congruent",
        "stroop_squared_Fully Incongruent",
        "stroop_squared_Stimulus Congruent, Response Incongruent",
        "stroop_squared_Stimulus Incongruent, Response Congruent"
    ],
    "Flanker Letter Squared": [
        "flanker_letter_squared_Fully Congruent",
        "flanker_letter_squared_Fully Incongruent",
        "flanker_letter_squared_Stimulus Congruent, Response Incongruent",
        "flanker_letter_squared_Stimulus Incongruent, Response Congruent"
    ],
    "Flanker Number Squared": [
        "flanker_number_squared_Fully Congruent",
        "flanker_number_squared_Fully Incongruent",
        "flanker_number_squared_Stimulus Congruent, Response Incongruent",
        "flanker_number_squared_Stimulus Incongruent, Response Congruent"
    ]
}

# 3. 定义更简洁的 x 轴标签
short_label_map = {
    "stroop_squared_Fully Congruent": "Fully Congruent",
    "stroop_squared_Fully Incongruent": "Fully Incongruent",
    "stroop_squared_Stimulus Congruent, Response Incongruent": "Stimulus-\ncongruent/\nResponse-\nincongruent",
    "stroop_squared_Stimulus Incongruent, Response Congruent": "Stimulus-\nincongruent/\nResponse-\ncongruent",

    "flanker_letter_squared_Fully Congruent": "Fully Congruent",
    "flanker_letter_squared_Fully Incongruent": "Fully Incongruent",
    "flanker_letter_squared_Stimulus Congruent, Response Incongruent": "Stimulus-\ncongruent/\nResponse-\nincongruent",
    "flanker_letter_squared_Stimulus Incongruent, Response Congruent": "Stimulus-\nincongruent/\nResponse-\ncongruent",

    "flanker_number_squared_Fully Congruent": "Fully Congruent",
    "flanker_number_squared_Fully Incongruent": "Fully Incongruent",
    "flanker_number_squared_Stimulus Congruent, Response Incongruent": "Stimulus-\ncongruent/\nResponse-\nincongruent",
    "flanker_number_squared_Stimulus Incongruent, Response Congruent": "Stimulus-\nincongruent/\nResponse-\ncongruent"
}

# 4. 创建画布：1 行 3 列(3个子图)，共同共享 y 轴
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5), sharey=True)
fig.patch.set_facecolor('white')  # 若需要白色背景

# 小提琴颜色
colors_for_violins = ["#9ecae1", "#a1d99b", "#fdae6b", "#c994c7"]

# 逐个 Task 画子图
for i, (task_name, group_list) in enumerate(task_map.items()):
    ax = axes[i]
    
    # 构造 violinplot 数据，x 轴上4个位置
    data_for_violin = []
    x_positions = [1, 2, 3, 4]

    # 依次把每个 group（condition）的数值取出来
    for grp in group_list:
        series_data = df.loc[df["group"] == grp, "group_accuracy"]
        data_for_violin.append(series_data)

    # 小提琴图
    vplot = ax.violinplot(
        dataset=data_for_violin,
        positions=x_positions,
        showmeans=False,
        showextrema=False,
        widths=0.7
    )
    # 调整每个小提琴颜色
    for j, body in enumerate(vplot['bodies']):
        body.set_facecolor(colors_for_violins[j])
        body.set_alpha(0.6)

    # 箱线图
    bp = ax.boxplot(
        data_for_violin,
        positions=x_positions,
        widths=0.15,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor='white', edgecolor='black')
    )

    # 均值散点
    mean_vals = [np.mean(g) for g in data_for_violin]
    ax.scatter(x_positions, mean_vals, color='red', zorder=3, s=60)

    # 设置 x 轴标签
    x_ticklabels = [short_label_map[g] for g in group_list]
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_ticklabels, fontsize=9)

    # 设置子图标题等
    ax.set_title(task_name, fontsize=18, fontweight='bold')
    if i == 0:
        ax.set_ylabel("Group Accuracy", fontsize=16)
    
    # 去掉顶部、右侧边框 + 增加水平网格(可选)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

# 调整布局
plt.tight_layout()

# 保存为 PDF 文件，放在show前面
plt.savefig("my_figure.pdf", bbox_inches='tight')  # 你可自定义文件名，比如 result.pdf

# 如果还需要在屏幕上展示，可以再调用 plt.show()
plt.show()
