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

# 读取Excel数据，确保 Target 和 Image 列均以字符串格式读取
df = pd.read_excel(file_path, dtype={'Target': str, 'Image': str})

# 输入行号范围（Excel 行号从1开始）
start_row = int(input("请输入起始行号（从1开始）："))
end_row = int(input("请输入结束行号："))

# 固定使用的列名称
target_col = 'Target'
image_col = 'Image'

for idx, row in df.iloc[start_row-1:end_row].iterrows():
    # 读取 Target 文本，去除空白
    text_target = str(row[target_col]).strip()
    # 读取 Image 列作为文件名
    raw_filename = str(row[image_col]).strip()
    
    # 若 Target 或 Image 为纯数字，则补零（假设应为5位）
    if text_target.isdigit():
        text_target = text_target.zfill(5)
    if raw_filename.isdigit():
        raw_filename = raw_filename.zfill(5)
    filename = raw_filename + ".png"
    
    # 创建图像：尺寸500x300像素，背景色设为 'gray'
    fig = plt.figure(figsize=(5, 3), dpi=100, facecolor='gray')
    ax = fig.add_subplot(111)
    ax.set_facecolor('gray')
    plt.axis('off')
    # 调整子图边距，确保整个画布都被保存
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # 在图像正中绘制 Target 文本（坐标：0.5, 0.5），字号45，颜色白色
    plt.text(0.5, 0.5, text_target, ha='center', va='center', fontsize=45, color='white')
    
    # 拼接图片保存路径
    save_path = output_folder + "/" + filename
    # 保存图片，不使用 bbox_inches 参数，确保图片尺寸严格为 500×300 像素
    plt.savefig(save_path, facecolor=fig.get_facecolor())
    plt.close()
    print(f"生成图片：{save_path}")
