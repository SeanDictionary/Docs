# 6/10 AC 
# 4/10 TLE
# 四维动规
"""
m,n = map(int,input().split())
inputs = [[0] * (n+1) for _ in range(m+1)]
for i in range(m):
    inputs[i+1] = [0] + list(map(int,input().split()))

dp = [[[[0] * (n + 1) for _ in range(m + 1)] for _ in range(n + 1)] for _ in range(m + 1)]
for i in range(1,m+1):
    for j in range(1,n+1):
        for x in range(1,m+1):
            for y in range(1,n+1):
                if x == i and y == j:
                    continue
                dp[i][j][x][y] = max(
                    dp[i-1][j][x-1][y],
                    dp[i-1][j][x][y-1],
                    dp[i][j-1][x-1][y],
                    dp[i][j-1][x][y-1]
                    ) + inputs[i][j] + inputs[x][y]
print(dp[m-1][n][m][n-1])
"""

# 10/10 AC 
# 三维动规
m,n = map(int,input().split())
inputs = [[0] * (n+1) for _ in range(m+1)]
for i in range(m):
    inputs[i+1] = [0] + list(map(int,input().split()))

dp = [[[0] * (m + 1) for _ in range(m + 1)] for _ in range(n + m)] 
for steps in range(2,n + m + 1):
    for i in range(max(1,steps-n),min(steps,m+1)):
        for j in range(max(1,steps-n),min(steps,m+1)):
            if i == j:
                continue
            dp[steps][i][j] = max(
                dp[steps-1][i][j],
                dp[steps-1][i-1][j],
                dp[steps-1][i][j-1],
                dp[steps-1][i-1][j-1]
                )+inputs[i][steps-i]+inputs[j][steps-j]
print(dp[-1][-1][-2])
