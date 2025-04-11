import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

# 隐藏Tkinter主窗口
root = Tk()
root.withdraw()

# 弹出文件对话框选择Excel文件
file_path = askopenfilename(title="请选择Excel文件", filetypes=[("Excel files", "*.xlsx;*.xls")])
if not file_path:
    print("未选择Excel文件，程序退出。")
    exit()

# 弹出文件夹选择对话框，选择保存图片的文件夹
output_folder = askdirectory(title="请选择保存图片的文件夹")
if not output_folder:
    print("未选择保存路径，程序退出。")
    exit()

# 读取Excel数据
df = pd.read_excel(file_path)

# 输入行号范围（注意Excel行号从1开始）
start_row = int(input("请输入起始行号（从1开始）："))
end_row = int(input("请输入结束行号："))

# 输入生成图片的三列名称（用逗号分隔）
columns_input = input("请输入生成图片的三列名称（用逗号分隔，例如 col1, col2, col3）：")
cols = [col.strip() for col in columns_input.split(",")]

if len(cols) != 3:
    print("错误：请输入恰好三个列名称。")
    exit()

# 针对指定行生成图片
for idx, row in df.iloc[start_row-1:end_row].iterrows():
    # 获取每一列的文本（转换为字符串）
    text_top = str(row[cols[0]])
    text_bottom_left = str(row[cols[1]])
    text_bottom_right = str(row[cols[2]])
    
    # 创建图像，指定背景色为灰色，尺寸500x300像素（figsize单位为英寸，dpi=100）
    fig = plt.figure(figsize=(5, 3), dpi=100, facecolor='gray')
    ax = fig.add_subplot(111)
    ax.set_facecolor('gray')
    plt.axis('off')  # 不显示坐标轴

    # 调整文本位置（采用归一化坐标）
    # 文本1：放在中上位置（x=0.5, y=0.65）
    plt.text(0.5, 0.70, text_top, ha='center', va='center', fontsize=25, color='white')
    # 文本2：放在中下偏左（x=0.25, y=0.45）
    plt.text(0.75, 0.40, text_bottom_left, ha='center', va='center', fontsize=25, color='white')
    # 文本3：放在中下偏右（x=0.75, y=0.45）
    plt.text(0.25, 0.40, text_bottom_right, ha='center', va='center', fontsize=25, color='white')

    # 构造输出文件名，去除可能的空白字符
    filename = f"{text_top.strip()}_{text_bottom_left.strip()}_{text_bottom_right.strip()}.png"
    # 拼接保存路径
    save_path = output_folder + "/" + filename
    
    # 保存图片，不保留多余空白
    plt.savefig(save_path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"生成图片：{save_path}")
