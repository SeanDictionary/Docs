# A
# AC
""" a = set(map(int,input().split()))
if 4 in a or 7 in a:
    print("NO")
else:
    print("YES") """

# B
# AC
""" from math import *

n = int(input())
lis = sorted(list(map(int,input().split())))
print(lis[-ceil(n/2)]) """

# C
# WA
""" alpha = "abcdefghijklmnopqrstuvwxyz"
t = int(input())
for _ in range(t):
    n,m = map(int,input().split())
    if m+26 >= n > m and m <= 26:
        print("YES")
        print(alpha[:min(n-1,26)]+alpha[m-1]*(n-min(n-1,26)))
    else:
        print("NO")
 """

# F
# AC
""" t = int(input())
for _ in range(t):
    l,r = map(int,input().split())
    print(r-l+1) """

# G
# AC
""" from math import *
t = int(input())
for _ in range(t):
    n, m = map(int,input().split())
    if m == 1:
        print(1)
    else:
        x = log(n,m)
        a,b = ceil(x),floor(x)
        if m**a+m**b >= n*2:
            print(max(b,1))
        else:
            print(a)
 """

# J
# AC
""" from time import *

n,y,m = map(int,input().split())
a,b,c = set(),set(),set()
a1 = strptime("07:00:00", "%H:%M:%S")
a2 = strptime("09:00:00", "%H:%M:%S")
a3 = strptime("18:00:00", "%H:%M:%S")
a4 = strptime("20:00:00", "%H:%M:%S")
b1 = strptime("11:00:00", "%H:%M:%S")
b2 = strptime("13:00:00", "%H:%M:%S")
c1 = strptime("22:00:00", "%H:%M:%S")
c2 = strptime("23:59:59", "%H:%M:%S")
c3 = strptime("00:00:00", "%H:%M:%S")
c4 = strptime("01:00:00", "%H:%M:%S")
for _ in range(n):
    ids,day,times = input().split()
    d = strptime(day, "%Y-%m-%d")
    t = strptime(times, "%H:%M:%S")
    if d.tm_year == y and d.tm_mon == m:
        if ids not in a and (a1 <= t <= a2 or a3 <= t <= a4):
            a.add(ids)
            continue
        if ids not in b and b1 <= t <= b2:
            b.add(ids)
            continue
        if ids not in c and (c1 <= t <= c2 or c3 <= t <= c4):
            c.add(ids)
            continue

print(len(a),len(b),len(c)) """

# K
# TLE
import sys

sys.setrecursionlimit(1000000)
def dfs(x,y):
    count1[x][y] = 0
    ans = 0
    if x != 0:
        if lis[x-1][y] and count1[x-1][y]:
            ans += dfs(x-1,y)
            if ans > ans1:
                return float("inf")
        elif lis[x-1][y] == 0 and count0[x-1][y]:
            count0[x-1][y] = 0
            ans += 1
    if x != n-1:
        if lis[x+1][y] and count1[x+1][y]:
            ans += dfs(x+1,y)
            if ans > ans1:
                return float("inf")
        elif lis[x+1][y] == 0 and count0[x+1][y]:
            count0[x+1][y] = 0
            ans += 1
    if y != 0:
        if lis[x][y-1] and count1[x][y-1]:
            ans += dfs(x,y-1)
            if ans > ans1:
                return float("inf")
        elif lis[x][y-1] == 0 and count0[x][y-1]:
            count0[x][y-1] = 0
            ans += 1
    if y != m-1:
        if lis[x][y+1] and count1[x][y+1]:
            ans += dfs(x,y+1)
            if ans > ans1:
                return float("inf")
        elif lis[x][y+1] == 0 and count0[x][y+1]:
            count0[x][y+1] = 0
            ans += 1
    return ans

n,m = map(int,input().split())
lis = []
count1 = [[1]*m for _ in range(n)]
for _ in range(n):
    lis += [list(map(int,list(input())))]
ans1 = float("inf")
for i in range(n):
    if ans1 == 1 or ans1 == 0:
        break
    for j in range(m):
        if count1[i][j] and lis[i][j]:
            count0 = [[1]*m for _ in range(n)]
            ans1 = min(dfs(i,j),ans1)

print(ans1)