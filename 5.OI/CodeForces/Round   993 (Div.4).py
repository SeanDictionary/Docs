# Round 993 (Div.4)
# 24/12/15
# A
# AC
""" t = int(input())
for _ in range(t):
    print(int(input())-1) """

# B
# AC
""" t = int(input())
for _ in range(t):
    s = input()[::-1]
    s = s.replace("q","a").replace("p","q").replace("a","p")
    print(s)
 """

# C
# AC
""" t = int(input())
for _ in range(t):
    m,a,b,c = map(int,input())
    count = min(m,a)+min(m,b)
    count = min(count,count+c)
    print(count) """

# D
# 复现
# TLE
from typing import Counter

t = int(input())
for _ in range(t):
    n = int(input())
    lis = Counter(map(int,input().split()))
    ans = [i for i in range(1,n+1) if i not in lis]
    print(*lis,*ans)
