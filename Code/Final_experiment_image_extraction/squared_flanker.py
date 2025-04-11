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

# 读取Excel数据，确保相关列以字符串格式读取
df = pd.read_excel(file_path, dtype={'Image': str, 'Target': str, 'Option_Left': str, 'Option_Right': str})

# 输入行号范围（注意Excel行号从1开始）
start_row = int(input("请输入起始行号（从1开始）："))
end_row = int(input("请输入结束行号："))

# 固定使用的列名称
target_col = 'Target'
option_left_col = 'Option_Left'
option_right_col = 'Option_Right'
image_col = 'Image'

# 针对指定行生成图片
for idx, row in df.iloc[start_row-1:end_row].iterrows():
    # 读取各列文本，并转换为字符串，去除空白
    text_target = str(row[target_col]).strip()
    text_option_left = str(row[option_left_col]).strip()
    text_option_right = str(row[option_right_col]).strip()
    
    # 针对 Target 列进行补零处理（假设应为5位）
    if text_target.isdigit():
        text_target = text_target.zfill(5)
    
    # 生成图片文件名，针对 Image 列同样补零处理（假设应为5位）
    raw_filename = str(row[image_col]).strip()
    if raw_filename.isdigit():
        raw_filename = raw_filename.zfill(5)
    filename = raw_filename + ".png"
    
    # 创建图像，尺寸500x300像素（figsize=(5,3) 与 dpi=100），背景色为灰色
    fig = plt.figure(figsize=(5, 3), dpi=100, facecolor='gray')
    ax = fig.add_subplot(111)
    ax.set_facecolor('gray')
    plt.axis('off')  # 不显示坐标轴
    
    # 调整子图边距，确保整个画布都被保存
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # 绘制文本：
    # 中上位置显示 Target 文本（坐标：0.5, 0.70）
    plt.text(0.5, 0.70, text_target, ha='center', va='center', fontsize=36, color='white')
    # 左下位置显示 Option_Left 文本（坐标：0.25, 0.40）
    plt.text(0.25, 0.40, text_option_left, ha='center', va='center', fontsize=32, color='white')
    # 右下位置显示 Option_Right 文本（坐标：0.75, 0.40）
    plt.text(0.75, 0.40, text_option_right, ha='center', va='center', fontsize=32, color='white')
    
    # 拼接生成的图片文件完整保存路径
    save_path = output_folder + "/" + filename
    
    # 保存图片时不使用 bbox_inches 参数，确保图片尺寸严格为 500x300 像素
    plt.savefig(save_path, facecolor=fig.get_facecolor())
    plt.close()
    print(f"生成图片：{save_path}")
