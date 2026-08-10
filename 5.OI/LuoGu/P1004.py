l,_ = map(int,input().split())
inputs = [[0] * (l+1) for _ in range(l+1)]
for i in range(l):
    inputs[i+1] = [0] + list(map(int,input().split()))

dp = [[[[0] * (l + 1) for _ in range(l + 1)] for _ in range(l + 1)] for _ in range(l + 1)]
for i in range(1,l+1):
    for j in range(1,l+1):
        for m in range(1,l+1):
            for n in range(1,l+1):
                dp[i][j][m][n] = max(dp[i-1][j][m-1][n],dp[i][j-1][m-1][n],dp[i-1][j][m][n-1],dp[i][j-1][m][n-1])+inputs[i][j]+inputs[m][n]
                if i == m and j == n:
                    dp[i][j][m][n] -= inputs[i][j]
print(dp[m][n-1][m-1][n])