# Q1 动规 O(n^2)
# Q2 贪心 O(n^2)
# 7/10 AC  3/10 TLE
# 0/10 AC 10/10 TLE
# 0/10 AC  0/10 TLE
"""
heights = list(map(int,input().split()))
# 前i个数的最大长度
def cal_max_nums(heights):
    dp = [1]*len(heights)
    for i in range(1,len(heights)):
        try:
            dp[i] = max(dp[j]+1 for j in range(i) if heights[j] >= heights[i])
        except Exception:
            None
    return max(dp)
# 贪心计算最长的非递增子序列
def cal_least_nums(heights):
    choose = []
    counts = 0
    while len(choose) != len(heights):
        tmp = float("inf")
        for i in range(len(heights)):
            if i not in choose and heights[i] <= tmp:
                tmp = heights[i]
                choose += [i]
        counts += 1
    return counts

print(cal_max_nums(heights))
print(cal_least_nums(heights))
"""

# https://www.luogu.com.cn/article/0qsxfefy
# Q1 二分+贪心 O(n*log n)
# Q2 二分+贪心 O(n*log n)
# 21/21 AC
heights = list(map(int,input().split()))
# 二分法定义
def erfen(lis,i):
    a,b = 0,len(lis)-1
    while b-a > 1:
        c = (a+b)//2
        if lis[c] >= i:
            a = c
        else:
            b = c
    return a,b
# 压栈贪心计算最长，详解看洛谷题解
def cal_max_nums(heights):
    ans = [heights[0]]
    for i in heights[1:]:
        if i <= ans[-1]:
            ans += [i]
        elif i > ans[0]:
            ans[0] = i
        else:
            _,index = erfen(ans,i)
            ans[index] = i
    return len(ans)


# 依据Dilworth定理
# 对于一个偏序集，最少链划分等于最长反链长度。
# 即最长上升子序列的长度就是能构成的不上升序列的个数。
def cal_least_nums(heights):
    ans = [heights[0]]
    for i in heights[1:]:
        if i > ans[0]:
            ans.insert(0,i)
        elif i < ans[-1]:
            ans[-1] = i
        else:
            index,_ = erfen(ans,i)
            ans[index] = i
    return len(ans)

print(cal_max_nums(heights))
print(cal_least_nums(heights))