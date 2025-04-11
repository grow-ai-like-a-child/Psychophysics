import string
import os
import pandas as pd
import matplotlib.pyplot as plt

# ===== Flanker - letter 版本 =====

def generate_flanker_letter_type1():
    """
    flanker letter type1（交换第二列和第三列）：
      原始生成每一行为 [first*5, first*5, second*5]，
      交换后输出为 [first*5, second*5, first*5]。
      共生成 26*25 = 650 行数据。
    """
    rows = []
    letters = list(string.ascii_uppercase)
    for first in letters:
        for second in letters:
            if first == second:
                continue
            rows.append([first * 6, second * 5, first * 5])
    return rows

def generate_flanker_letter_type2():
    """
    flanker letter type2（保持不变）：
      每一行构造为：
         left  = fixed*2 + other + fixed*2    (例如 "AABAA")
         right = other*2 + fixed + other*2     (例如 "BBABB")
      输出为：[left, left, right]。
    """
    rows = []
    letters = list(string.ascii_uppercase)
    for fixed in letters:
        for other in letters:
            if fixed == other:
                continue
            left = fixed * 2 + other + fixed * 2
            right = other * 2 + fixed + other * 2
            rows.append([left, left, right])
    return rows

def generate_flanker_letter_type3():
    """
    flanker letter type3：
      生成：
         col1 = fixed*5                (例如 "AAAAA")
         col2 = fixed*2 + other + fixed*2  (例如 "AABAA")
         col3 = other*2 + fixed + other*2    (例如 "BBABB")
      输出顺序为 [col1, col2, col3]，
      即生成 "AAAAA    AABAA    BBABB"。
    """
    rows = []
    letters = list(string.ascii_uppercase)
    for fixed in letters:
        for other in letters:
            if fixed == other:
                continue
            col1 = fixed * 6
            col2 = fixed * 2 + other + fixed * 2
            col3 = other * 2 + fixed + other * 2
            rows.append([col1, col2, col3])
    return rows

def generate_flanker_letter_type4():
    """
    flanker letter type4：
      原始生成：
         left  = fixed*2 + other + fixed*2    (例如 "AABAA")
         mid   = fixed*5                     (例如 "AAAAA")
         right = other*5                     (例如 "BBBBB")
      交换后输出为 [left, right, mid]。
    """
    rows = []
    letters = list(string.ascii_uppercase)
    for fixed in letters:
        for other in letters:
            if fixed == other:
                continue
            left  = fixed * 2 + other + fixed * 2
            mid   = fixed * 5
            right = other * 5
            rows.append([left, right, mid])
    return rows

# ===== Flanker - number 版本 =====

def generate_flanker_number_type1():
    """
    flanker number type1（交换第二列和第三列）：
      输出为 [str(first)*5, str(second)*5, str(first)*5]。
    """
    rows = []
    for first in range(1, 10):
        for second in range(1, 10):
            if first == second:
                continue
            row = [str(first) * 5, str(second) * 5, str(first) * 5]
            rows.append(row)
    return rows

def generate_flanker_number_type2():
    """
    flanker number type2（保持不变）：
      每一行构造为：
         left  = fixed*2 + other + fixed*2    (例如 "11211")
         right = other*2 + fixed + other*2     (例如 "22322")
      输出为：[left, left, right]。
    """
    rows = []
    digits = "123456789"
    for fixed in digits:
        for other in digits:
            if fixed == other:
                continue
            left = fixed * 2 + other + fixed * 2
            right = other * 2 + fixed + other * 2
            rows.append([left, left, right])
    return rows

def generate_flanker_number_type3():
    """
    flanker number type3：
      原始生成：
         col1 = fixed*5                 (例如 "11111")
         col2 = fixed*2 + other + fixed*2   (例如 "11211")
         col3 = other*2 + fixed + other*2     (例如 "22122")
      输出顺序改为 [col1, col2, col3]，
      即生成 "11111	11211	22122"。
    """
    rows = []
    digits = "123456789"
    for fixed in digits:
        for other in digits:
            if fixed == other:
                continue
            col1 = fixed * 5
            col2 = fixed * 2 + other + fixed * 2
            col3 = other * 2 + fixed + other * 2
            rows.append([col1, col2, col3])
    return rows

def generate_flanker_number_type4():
    """
    flanker number type4：
      原始生成：
         col1 = x*2 + y + x*2    (例如 "11211")
         col2 = y*5              (例如 "22222")
         col3 = x*5              (例如 "11111")
      输出顺序改为 [col1, col2, col3]，
      即生成 "11211	22222	11111"。
    """
    rows = []
    digits = "123456789"
    for x in digits:
        for y in digits:
            if x == y:
                continue
            col1 = x * 2 + y + x * 2
            col2 = y * 5
            col3 = x * 5
            rows.append([col1, col2, col3])
    return rows

# ===== 保存Excel =====

def save_to_excel(rows, task, style, flanker_type):
    """
    将生成的数据保存到 Excel 文件中，
    Excel 文件保存到程序同目录下的 Data-set 文件夹中，
    文件夹结构：Data-set/Flanker-<Style>/，
    Excel 文件名格式：<task>_<style>_<flanker_type>_dataset.xlsx
    列标题：Title, Wrong_Option, Right_Option
    """
    base_folder = os.path.join(os.getcwd(), "Data-set")
    os.makedirs(base_folder, exist_ok=True)
    subfolder = os.path.join(base_folder, f"{task.capitalize()}-{style.capitalize()}")
    os.makedirs(subfolder, exist_ok=True)
    filename = f"{task}_{style}_{flanker_type}_dataset.xlsx"
    filepath = os.path.join(subfolder, filename)
    df = pd.DataFrame(rows, columns=["Title", "Wrong_Option", "Right_Option"])
    df.to_excel(filepath, index=False)
    print(f"数据已保存到 Excel 文件：{filepath}")
    return filepath

# ===== 生成图像 =====

def generate_images_from_excel(excel_file, task, style, flanker_type):
    """
    根据 Excel 文件生成图片，
    图片保存在程序同目录下的 Data-set-Image 文件夹中，
    文件夹结构：Data-set-Image/Flanker-<Style>-image/<flanker_type>/，
    图片生成：每行 Title 为文本1，
      Wrong_Option 为文本2（显示在右下，现放在左下），
      Right_Option 为文本3（显示在左下，现放在右下）。
    """
    df = pd.read_excel(excel_file)
    base_folder = os.path.join(os.getcwd(), "Data-set-Image")
    os.makedirs(base_folder, exist_ok=True)
    subfolder = os.path.join(base_folder, f"{task.capitalize()}-{style.capitalize()}-image")
    os.makedirs(subfolder, exist_ok=True)
    output_folder = os.path.join(subfolder, flanker_type)
    os.makedirs(output_folder, exist_ok=True)
    print("图片正在生成中...")
    
    count = 0
    for idx, row in df.iterrows():
        text_top = str(row["Title"])
        text_wrong = str(row["Wrong_Option"])
        text_right = str(row["Right_Option"])
        
        fig = plt.figure(figsize=(5, 3), dpi=100, facecolor='gray')
        ax = fig.add_subplot(111)
        ax.set_facecolor('gray')
        plt.axis('off')
        
        # 文本1：Title，显示在中上 (x=0.5, y=0.70)
        plt.text(0.5, 0.70, text_top, ha='center', va='center', fontsize=25, color='white')
        # 根据要求交换左右：
        # 将 Wrong_Option 显示在左下 (x=0.25)
        plt.text(0.25, 0.40, text_wrong, ha='center', va='center', fontsize=25, color='white')
        # 将 Right_Option 显示在右下 (x=0.75)
        plt.text(0.75, 0.40, text_right, ha='center', va='center', fontsize=25, color='white')
        
        filename = f"{text_top.strip()}_{text_wrong.strip()}_{text_right.strip()}.png"
        save_path = os.path.join(output_folder, filename)
        plt.savefig(save_path, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        count += 1
    print(f"图片已经生成完，共计 {count} 张。")

# ===== 主程序 =====

def main():
    # 首先询问任务：Flanker 或 Stroop
    task = input("请选择任务（输入 flanker 或 stroop）：").strip().lower()
    if task not in ["flanker", "stroop"]:
        print("未知任务。")
        return
    if task == "stroop":
        print("stroop 部分目前尚未实现。")
        return

    # 对于 flanker 任务，继续询问数据类型和具体类型
    style = input("请选择数据类型（输入 letter 或 number）：").strip().lower()
    if style not in ["letter", "number"]:
        print("请选择 letter 或 number。")
        return
    flanker_type = input("请选择 flanker 类型（type1/type2/type3/type4）：").strip().lower()
    if flanker_type not in ["type1", "type2", "type3", "type4"]:
        print("暂时只支持 flanker 的 type1、type2、type3 和 type4。")
        return

    # 根据选择生成数据
    if task == "flanker":
        if style == "letter":
            if flanker_type == "type1":
                rows = generate_flanker_letter_type1()
                print("生成 flanker letter type1 数据集。")
            elif flanker_type == "type2":
                rows = generate_flanker_letter_type2()
                print("生成 flanker letter type2 数据集。")
            elif flanker_type == "type3":
                rows = generate_flanker_letter_type3()
                print("生成 flanker letter type3 数据集。")
            elif flanker_type == "type4":
                rows = generate_flanker_letter_type4()
                print("生成 flanker letter type4 数据集。")
        elif style == "number":
            if flanker_type == "type1":
                rows = generate_flanker_number_type1()
                print("生成 flanker number type1 数据集。")
            elif flanker_type == "type2":
                rows = generate_flanker_number_type2()
                print("生成 flanker number type2 数据集。")
            elif flanker_type == "type3":
                rows = generate_flanker_number_type3()
                print("生成 flanker number type3 数据集。")
            elif flanker_type == "type4":
                rows = generate_flanker_number_type4()
                print("生成 flanker number type4 数据集。")

    # 保存数据到 Excel 文件到 Data-set 文件夹内
    excel_filepath = save_to_excel(rows, task, style, flanker_type)
    
    # 是否生成图像
    gen_img = input("是否要生成相关图像？(y/n)：").strip().lower()
    if gen_img == "y":
        generate_images_from_excel(excel_filepath, task, style, flanker_type)
    else:
        print("不生成图像。")

if __name__ == "__main__":
    main()
