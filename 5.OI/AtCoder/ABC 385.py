# ABC 383
# 24/12/21
# A
# AC
""" lis = list(map(int,input().split()))
if lis[0] == lis[1] ==lis[2]:
    print("Yes")
else:
    for i in range(3):
        if lis[i]*2 == sum(lis):
            print("Yes")
            break
    else:
        print("No") """

# B
# AC
""" h,w,x,y = map(int,input().split())
lis = []
count = 0
x,y = x-1,y-1
for _ in range(h):
    lis += [input()]
strs = input()
for action in strs:
    if action == "L":
        if lis[x][y-1] != "#":
            if lis[x][y-1] == "@":
                count += 1
                lis[x] = lis[x][:y-1]+"."+lis[x][y:]
            y -= 1
    elif action == "R":
        if lis[x][y+1] != "#":
            if lis[x][y+1] == "@":
                count += 1
                lis[x] = lis[x][:y+1]+"."+lis[x][y+2:]
            y += 1
    elif action == "U":
        if lis[x-1][y] != "#":
            if lis[x-1][y] == "@":
                count += 1
                lis[x-1] = lis[x-1][:y]+"."+lis[x-1][y+1:]
            x -= 1
    elif action == "D":
        if lis[x+1][y] != "#":
            if lis[x+1][y] == "@":
                count += 1
                lis[x+1] = lis[x+1][:y]+"."+lis[x+1][y+1:]
            x += 1
print(x+1,y+1,count) """

# C
# AC
# 感动woc，第一次在这种情况下写出动规
""" n = int(input())
lis = list(map(int,input().split()))
count = [0]*3001
dp = [[1]*n for _ in range(n)]
for index in range(n):
    if count[lis[index]] == 0:
        count[lis[index]] += 1
    else:
        for d in range(1,index+1):
            if lis[index-d] == lis[index]:
                dp[index][d] = dp[index-d][d] + 1
print(max(max(i) for i in dp)) """

# D
# TLE
""" n,m,x,y = map(int,input().split())
lis = {}
for _ in range(n):
    x1,y1 = map(int,input().split())
    if x1 in lis:
        lis[x1] += [y1]
    else:
        lis[x1] = [y1]
count = 0
for _ in range(m):
    direction,lenth = input().split()
    lenth = int(lenth)
    if direction == "R":
        for i in range(x+1,x+lenth+1):
            if i in lis and y in lis[i]:
                lis[i].remove(y)
                count += 1
        x += lenth
    elif direction == "L":
        for i in range(x-1,x-lenth-1,-1):
            if i in lis and y in lis[i]:
                lis[i].remove(y)
                count += 1
        x -= lenth
    elif direction == "U":
        for i in range(y+1,y+lenth+1):
            if x in lis and i in lis[x]:
                lis[x].remove(i)
                count += 1
        y += lenth
    elif direction == "D":
        for i in range(y-1,y-lenth-1,-1):
            if x in lis and i in lis[x]:
                lis[x].remove(i)
                count += 1
        y -= lenth
        
print(x,y,count) """