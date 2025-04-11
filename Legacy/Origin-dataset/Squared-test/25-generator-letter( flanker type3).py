import string

letters = string.ascii_uppercase  # "A" 到 "Z"

for fixed in letters:
    for other in letters:
        if fixed == other:
            continue
        col1 = fixed * 5                           # 例如 "AAAAA"
        col2 = other * 2 + fixed + other * 2         # 例如：对于 fixed=A, other=B 得 "BBABB"
        col3 = fixed * 2 + other + fixed * 2         # 例如：对于 fixed=A, other=B 得 "AABAA"
        print(col1 + "\t" + col2 + "\t" + col3)
