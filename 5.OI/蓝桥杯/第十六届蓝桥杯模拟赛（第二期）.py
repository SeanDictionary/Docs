# 24/11/30
# 蓝桥模拟赛2 T2
""" from math import lcm
print(lcm(2024,1024)) """

# 蓝桥模拟赛2 T4
""" dp = [float("inf")]*4047
dp[1] = 0
for i in range(1,2024):
    dp[i+1] = min(dp[i+1],dp[i]+1)
    dp[i+int(max(str(i)))] = min(dp[i+int(max(str(i)))],dp[i]+3)
    dp[2*i] = min(dp[2*i],dp[i]+10)
print(dp[2024]) """

# 蓝桥模拟赛2 T5
""" nums = [
    534, 386, 319, 692, 169, 338, 521, 713, 640, 692, 969, 362, 311, 349, 308, 357, 515, 140, 591, 216,
    57, 252, 575, 630, 95, 274, 328, 614, 18, 605, 17, 980, 166, 112, 997, 37, 584, 64, 442, 495,
    821, 459, 453, 597, 187, 734, 827, 950, 679, 78, 769, 661, 452, 983, 356, 217, 394, 342, 697, 878,
    475, 250, 468, 33, 966, 742, 436, 343, 255, 944, 588, 734, 540, 508, 779, 881, 153, 928, 764, 703,
    459, 840, 949, 500, 648, 163, 547, 780, 749, 132, 546, 199, 701, 448, 265, 263, 87, 45, 828, 634
]
dp =[0]+[float("-inf")]*23

for i in nums:
    tmp = dp.copy()
    for j in range(24):
        if dp[j] != float("-inf"):
            k = (i+j)%24
            tmp[k] = max(tmp[k],dp[j]+i)
    dp = tmp.copy()

print(dp[0]) """

# 蓝桥模拟赛2 T6
""" n = int(input())
print(2024//n + int(2024%n != 0)) """

# 蓝桥模拟赛2 T7
""" n=int(input())
a=list(map(int,input().split()))
ans = float("inf")
for i in a:
    if i%2 == 0:
        ans = min(ans,i)
print(ans) """

# 蓝桥模拟赛2 T8
""" n = input()
target = list("LANQIAO")
index = 0
for i in n:
    if i == target[index]:
        index += 1
print("YES" if index == 7 else "NO") """

# 蓝桥模拟赛2 T9
""" n,m = map(int, input().split())
arr = []
for _ in range(n):
    arr += [list(map(int, input().split()))]

sums_r = [[0]*m for _ in range(n)] # 行前缀和
sums_c = [[0]*m for _ in range(n)] # 列前缀和

# 行前缀和
for i in range(n):
    total = 0
    for j in range(m):
        total += arr[i][j]
        sums_r[i][j] = total
# 列前缀和
for i in range(m):
    total = 0
    for j in range(n):
        total += arr[j][i]
        sums_c[j][i] = total

total = 0
print()
for x in range(n):
    for y in range(m):
        for l in range(2,min(m-y+1,n-x+1)):
            up = sums_r[x][y+l-1] - sums_r[x][y]
            down = sums_r[x+l-1][y+l-1] - sums_r[x+l-1][y]
            left = sums_c[x+l-1][y] - sums_c[x][y]
            right = sums_c[x+l-1][y+l-1] - sums_c[x][y+l-1]
            total = max(arr[x][y] + up + left + down + right - arr[x+l-1][y+l-1], total)
print(total) """

# 蓝桥模拟赛2 T10