for first in range(1, 10):
    for second in range(1, 10):
        if first == second:
            continue
        print(str(first) * 5 + "\t" + str(second) * 5 + "\t" + str(first) * 5)
