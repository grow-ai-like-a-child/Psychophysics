digits = "123456789"  # 不包含 0

for fixed in digits:
    for other in digits:
        if fixed == other:
            continue
        left = fixed * 2 + other + fixed * 2
        right = other * 2 + fixed + other * 2
        print(left + "\t" + left + "\t" + right)
