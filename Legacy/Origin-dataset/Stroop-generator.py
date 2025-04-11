from colorama import Fore, Style, init

# 初始化 colorama 以支持 Windows 终端颜色
init(autoreset=True)

# 定义颜色映射
colors = {
    "Red": Fore.RED,
    "Blue": Fore.BLUE,
    "Green": Fore.GREEN,
    "Yellow": Fore.YELLOW,
    "Orange": Fore.LIGHTRED_EX,  # 近似橙色
    "Black": Fore.LIGHTBLACK_EX,
    "Purple": Fore.MAGENTA
}

# 生成并打印颜色文本
for text_color in colors:  # 文字内容
    for display_color, color_code in colors.items():  # 显示的颜色
        print(color_code + text_color + Style.RESET_ALL)  # 文字颜色+重置格式
