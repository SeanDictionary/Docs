n = int(input())
m = []
for _ in range(n):
    s = ""
    l,r = map(int,input().split())
    m += [[l,r]]
for k in m:
    s = 0
    j = (k[1] - k[0])%9
    for i in range(k[1]-j,k[1]+1):
        s = (s+i)%9
    print(s)