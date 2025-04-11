digits = "123456789"  # 不包含 0

for fixed in digits:
    for other in digits:
        if fixed == other:
            continue
        col1 = fixed * 5
        col2 = fixed * 2 + other + fixed * 2    # 原第三列
        col3 = other * 2 + fixed + other * 2      # 原第二列
        print(col1 + "\t" + col2 + "\t" + col3)
