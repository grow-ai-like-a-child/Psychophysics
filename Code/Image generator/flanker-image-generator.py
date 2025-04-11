import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk
from tkinter import filedialog

def generate_images_from_excel():
    """ 让用户选择 Excel 文件，并从 'index' 列生成图片 """
    
    # 打开文件选择对话框
    root = tk.Tk()
    root.withdraw()  # 隐藏 Tkinter 窗口
    file_path = filedialog.askopenfilename(title="选择 Excel 文件", filetypes=[("Excel 文件", "*.xlsx;*.xls")])
    
    if not file_path:  # 用户取消选择
        print("未选择文件，程序退出。")
        return
    
    print(f"已选择文件: {file_path}")
    
    # 读取 Excel 文件
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"读取 Excel 失败: {e}")
        return
    
    # 确保 index 存在
    if 'index' not in df.columns:
        print("Excel 文件中没有找到 'index' 列")
        return

    # 创建输出文件夹
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)

    # 图片参数
    img_width, img_height = 500, 300  # 设定图片大小
    bg_color = (128, 128, 128)  # 灰色背景
    text_color = (255, 255, 255)  # 白色文字
    font_path = "arial.ttf"  # 确保系统有 Arial 字体或替换为可用字体
    font_size = 70

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("找不到字体文件，尝试使用默认字体")
        font = ImageFont.load_default()

    # 生成图片
    for i, text in enumerate(df['index'].astype(str)):  # 处理 NaN 和数值型 index
        img = Image.new("RGB", (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # 计算文本居中位置
        text_size = draw.textbbox((0, 0), text, font=font)
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        x = (img_width - text_width) / 2
        y = (img_height - text_height) / 2
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=text_color)

        # 保存图片
        img_path = os.path.join(output_folder, f"{text}.png")
        img.save(img_path)

        print(f"已生成图片: {img_path}")

# 运行程序
generate_images_from_excel()
