# 代码应该没问题不知道为什么RE
# 6/6 RE
n = int(input())
words = []
for _ in range(n):
    words += [input()]
start = input()

def cal(i,j):
    a,b = words[i],words[j]
    for i in range(1,min(len(a),len(b))+1):
        if a[-i:] == b[:i]:
            return i
    return 0    

dp = [[cal(i,j) for j in range(n)] for i in range(n)]

def choose(i,count):
    count[i] += 1
    ans = 0
    for j in range(n):
        if dp[i][j] != 0 and count[j] != 2:
            ans = max(choose(j,count.copy())-dp[i][j],ans)
    return ans + len(words[i])
print(str(max(choose(i, [0]*n) for i in range(n) if words[i][0] == start)))