import string

letters = string.ascii_uppercase

for first in letters:
    for second in letters:
        if first == second:
            continue
        print(first * 5 + "\t" + first * 5 + "\t" + second * 5)
