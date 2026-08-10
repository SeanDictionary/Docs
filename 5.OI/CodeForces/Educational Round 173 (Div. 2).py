# Educational Round 173 (Div. 2)
# 24/12/24
# A
# AC
""" t = int(input())
for _ in range(t):
    n = int(input())
    ans = 1
    while n > 3:
        n //= 4
        ans *= 2
    print(ans) """

# B
# AC
""" from math import factorial

t = int(input())
for _ in range(t):
    a,b = map(int,input().split())
    ans = {1}
    if a >= 3 or b%3 == 0:
        ans.update({3})
    if b == 5:
        ans.update({5})
    if a == 1 and b%7 == 0:
        ans.update({7})
    if a == 2 and (10*b+b)%7 == 0:
        ans.update({7})
    if a >= 3:
        ans.update({7})
    if a >= 6:
        ans.update({9})
    if a >= 3 and b%3 == 0:
        ans.update({9})
    if b%9 == 0:
        ans.update({9})
    print(*(sorted(list(ans)))) """

# C
t = int(input())
for _ in range(t):
    n = int(input())
    lis = list(map(int,input().split()))
    sums = [lis[0]]+[0]*(n-1)
    for i in range(1,n):
        sums[i] = sums[i-1]+lis[i]
    sums = [0] + sums
    ans = {0}
    for i in range(n):
        for j in range(i+1,n+1):
            ans.update({sums[j]-sums[i]})
    print(len(ans))
    print(*(sorted(list(ans))))