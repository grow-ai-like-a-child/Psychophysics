from itertools import product

def generate_sequences(start, end):
    """ 生成符合规则的排列组合，确保变动发生在第三个字符 """
    chars = [chr(i) for i in range(ord(start), ord(end) + 1)]
    
    results = []
    for first_last in chars:  # 控制首尾字符
        for middle in chars:  # 只改变中间的第三个字符
            sequence = first_last + first_last + middle + first_last + first_last
            results.append(sequence)
    
    return results

# 示例：生成 A 到 Z 的排列
sequences = generate_sequences('0', '9')

# 输出前 20 个结果
for seq in sequences[:]:
    print(seq)

# 也可以用于数字：
# sequences = generate_sequences('0', '9')
