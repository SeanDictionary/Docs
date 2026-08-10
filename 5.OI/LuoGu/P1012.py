n = int(input())
m = input().split()
# 冒泡排序
# 使得int(a + b) > int(b + a)
for i in range(n - 1):
    for j in range(n - i - 1):
        if int(m[j] + m[j + 1]) < int(m[j + 1] + m[j]):
            m[j], m[j + 1] = m[j + 1], m[j]
print("".join(m))