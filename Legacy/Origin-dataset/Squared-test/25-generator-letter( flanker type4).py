import string

letters = string.ascii_uppercase  # 大写字母 A-Z

for x in letters:
    for y in letters:
        if x == y:
            continue
        col1 = x * 2 + y + x * 2
        col2 = y * 5
        col3 = x * 5
        # 使用制表符分隔三列
        print(col1 + "\t" + col2 + "\t" + col3)
