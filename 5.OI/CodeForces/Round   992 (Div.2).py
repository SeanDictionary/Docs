# Round 992 (Div.2)
# 24/12/8
# A
# AC
""" t = int(input())
for _ in range(t):
    n,k = map(int,input().split())
    lis = list(map(int,input().split()))
    dp = [[1]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dp[i][j] = abs(lis[i]-lis[j])%k
    for i in range(n):
        if all(dp[i]):
            print("YES")
            print(i+1)
            break
    else:
        print("NO") """

# B
# AC
""" from math import *
t = int(input())
for _ in range(t):
    n = int(input())
    if n == 1:
        print(1)
    else:
        print(ceil(log((n/2+1)/3,2))+2) """

# C
# WA
# 样例能过，奇怪
# 复现AC，n=1会有奇怪的问题
""" t = int(input())
for _ in range(t):
    r,l = [],[]
    n,k = map(int,input().split())
    if k > pow(2,n-1):
        print(-1)
    else:
        bins = bin(k-1)[2:].zfill(n-1)
        for index,i in enumerate(bins):
            if i == '1':
                r.insert(0,index+1)
            elif i == '0':
                l.append(index+1)
        print(*(l + [n] + r)) if n != 1 else print(*(l + r))
 """