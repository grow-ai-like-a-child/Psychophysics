digits = "123456789"  # 不包含 0

for x in digits:
    for y in digits:
        if x == y:
            continue
        col1 = x * 2 + y + x * 2
        col2 = y * 5
        col3 = x * 5
        # 使用制表符分隔三列，复制到 Excel 时会自动分列
        print(col1 + "\t" + col2 + "\t" + col3)
