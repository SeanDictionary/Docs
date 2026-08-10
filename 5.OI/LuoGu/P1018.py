N,K = map(int,input().split())
n = input()
# 动规，i表示前i个数，j表示分成j个部分，即有j-1个乘号
dp = [[1]*(K+2) for _ in range(len(n)+1)]
for j in range(1,K+2):
    for i in range(j,len(n)+1):
        dp[i][j] = max(dp[k][j-1]*int(n[k:i]) for k in range(j-1,i))
print(dp[-1][-1])