from openpyxl import Workbook
from openpyxl.styles import Font

# 定义7种颜色及其 Excel 十六进制颜色代码，颜色顺序为：红、蓝、绿、黄、橙、黑、紫
colors = ["Red", "Blue", "Green", "Yellow", "Orange", "Black", "Purple"]
color_map = {
    "Red": "FF0000",     # 红
    "Blue": "0000FF",    # 蓝
    "Green": "00FF00",   # 绿
    "Yellow": "FFFF00",  # 黄
    "Orange": "FFA500",  # 橙
    "Black": "000000",   # 黑
    "Purple": "800080"   # 紫
}

wb = Workbook()
ws = wb.active
ws.title = "Color Sequences"

row_idx = 1
# 遍历所有有序的不同颜色对，共 7*6 = 42 种组合
for A in colors:
    for B in colors:
        if A == B:
            continue
        # 三单词序列为：A, B, A
        seq = [A, B, A]
        for col_idx, word in enumerate(seq, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=word)
            # 新要求：第一列字体颜色改为与原第二列相同（即 color_map[A]），第二列保持 color_map[A]，第三列不变（color_map[B]）
            if col_idx == 1 or col_idx == 2:
                font_color = color_map[A]
            else:  # col_idx == 3
                font_color = color_map[B]
            cell.font = Font(color=font_color)
        row_idx += 1

output_file = "color_sequences_new.xlsx"
wb.save(output_file)
print(f"生成的 Excel 文件已保存为 {output_file}")
