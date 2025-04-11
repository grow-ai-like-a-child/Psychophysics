import string

letters = string.ascii_uppercase  # 大写字母表 "A" 到 "Z"

for fixed in letters:
    for other in letters:
        if fixed == other:
            continue
        left = fixed * 2 + other + fixed * 2   # 例如 "AABAA"
        right = other * 2 + fixed + other * 2    # 例如 "BBABB"
        # 第一列和第二列都是 left，第三列为 right
        print(left + "\t" + left + "\t" + right)
