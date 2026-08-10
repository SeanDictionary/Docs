# 牛客周赛 Round 73
# 24/12/22
# A
# AC
""" import math
a,b,c = map(int,input().split())
print(-1 if math.ceil(a/c)*c > b else math.ceil(a/c)*c) """

# B
# AC
""" n,k,x = map(int,input().split())
if (n+1)*x > k > (n-1)*x:
    tmp = k-(n-1)*x-1
    print((-tmp//2)%x,k-1+((-tmp//2)%x))
else:
    print(-1) """

# C
# AC
""" n = int(input())
s = input()
ans = []
if s[-1] == "0":
    print("-1")
else:
    count = [0]*n
    index = 0
    for i in range(len(s)):
        if s[i] == "0":
            ans += [i+2]
            count[i+1] = 1
        else:
            ans += [index+1]
            for j in range(index+1,len(s)):
                if count[j] == 0:
                    index = j
                    break
    print(*ans) """

# D
# TLE
""" n,k = map(int,input().split())
s = input()
lis = [int(s[0])] + [0]*(n-1)
for i in range(1,n):
    if s[i] == "1":
        lis[i] = lis[i-1] + 1
    else:
        lis[i] = lis[i-1]
print(lis)
for right in range(n)[::-1]:
    sums = 0
    for left in range(right)[::-1]:
        if s[left] == "0":
            sums += lis[right]-lis[left]
            if sums == k:
                print(left+1,right+1)
                break
    else:
        continue
    break
else:
    print(-1) """