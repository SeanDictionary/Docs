# Round 994 (Div.2)
# 24/12/20
# A
# AC
""" t = int(input())
for _ in range(t):
    n = int(input())
    lis = list(map(int,input().split()))
    if not any(lis):
        print(0)
    else:
        while lis and lis[0] == 0:
            lis.pop(0)
        while lis and lis[-1] == 0:
            lis.pop()
        if 0 in lis:
            print(2)
        else:
            print(1) """

# B
# WA
t = int(input())
for _ in range(t):
    n = int(input())
    strs = input()
    for i in range(n-1):
        if strs[i] == "p":
            sign = 1
            break
    else:
        sign = 0
    for i in range(n-1):
        if strs[n-i-1] == "s":
            sign &= 1
            break
    else:
        sign &= 0
    if sign:
        print("NO")
    else:
        print("YES")