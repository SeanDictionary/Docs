# ABC 389
# 25/01/18
# A
""" a,b = map(int,input().split("x"))
print(a*b) """

# B
""" n = int(input())
i = 1
while n != 1:
    i += 1
    n = n // i
print(i) """

# C
""" n = int(input())
leave = 0
lis = [0,0]
for _ in range(n):
    k = input().split()
    if k[0] == '1':
        lis += [lis[-1] + int(k[1])]
    if k[0] == '2':
        leave += 1
    if k[0] == '3':
        print(lis[int(k[1])+leave] - lis[leave+1]) """

# D
""" r = int(input())
ans = 0
i,j = 0.5,r-0.5
while j > 0.5 and i < r + 0.5:
    if i**2+j**2 <= r**2:
        ans += j-0.5
        i += 1
    else:
        while i**2+j**2 > r**2:
            j -= 1
        ans += j-0.5
        i += 1
print(int(ans*4+1)) """

# E
# TLE
""" n,m = map(int,input().split())
price = list(map(int,input().split()))
for i in range(n):
    price[i] = [price[i],0,price[i]]
sum,ans = 0,0
while sum < m:
    price.sort(key = lambda x: x[0])
    if price[0][0] > m-sum:
        break
    sum += price[0][0]
    price[0][1] += 1
    price[0][0] = (price[0][1]*2+1)*price[0][2]
    ans += 1
print(ans) """
