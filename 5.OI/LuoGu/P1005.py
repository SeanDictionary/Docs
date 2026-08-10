n,m = map(int,input().split())
x = [[0] for _ in range(n)]
for i in range(n):
    x[i] = [0]+list(map(int,input().split()))+[0]
ans = 0
for k in range(n):
    dp = [[0]*(m+2) for _ in range(m+2)]
    for i in range(1,m+1):
        for j in range(i,m+1)[::-1]:
            dp[i][j] = max(dp[i-1][j]+x[k][i-1]*2**(m-j+i-1), dp[i][j+1]+x[k][j+1]*2**(m-j+i-1))
    ans += max([dp[i][i]+x[k][i]*2**m for i in range(1,m+1)])
print(ans)