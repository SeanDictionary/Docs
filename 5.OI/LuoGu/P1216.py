# 递归但最后一个样例RE
"""
n = int(input())
x = [[0] for _ in range(n)]
dp = [[float("-inf")]*(i+1) for i in range(n)]
for i in range(n): 
    x[i] = [int(j) for j in input().split(" ")]
dp[0][0] = x[0][0]
def a(i,j):
    if dp[i][j] != float("-inf"):
        return dp[i][j]
    if i == j:
        dp[i][j] = a(i-1,j-1)+x[i][j]
        return dp[i][j]
    if j == 0:
        dp[i][j] = a(i-1,j)+x[i][j]
        return dp[i][j]
    else:
        dp[i][j] = max(a(i-1,j),a(i-1,j-1))+x[i][j]
        return dp[i][j]
print(max([a(n-1,i) for i in range(n)]))
"""

# 迭代AC
n = int(input())
x = [[0] for _ in range(n)]
dp = [[float("-inf")]*(i+1) for i in range(n)]
for i in range(n): 
    x[i] = [int(j) for j in input().split(" ")]
dp[0][0] = x[0][0]
for i in range(1,len(dp)):
    for j in range(len(dp[i])):
        if i == j:dp[i][j] = dp[i-1][j-1]+x[i][j]
        elif j == 0:dp[i][j] = dp[i-1][j]+x[i][j]
        else:dp[i][j] = max(dp[i-1][j-1],dp[i-1][j])+x[i][j]
print(max([dp[n-1][i] for i in range(n)]))