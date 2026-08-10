class Solution:
    def minCost(n: int, cuts: list[int]) -> int:
        # 记忆化搜索
        """
        from functools import cache

        cuts += [0,n]
        cuts.sort()
        @cache
        def dfs(i,j):
            ans = float("inf")
            if i + 1 == j:
                return 0
            for k in range(i+1,j):
                ans = min(dfs(i,k)+dfs(k,j),ans)
            return ans + cuts[j] - cuts[i]
        return dfs(0,len(cuts)-1)
        """

        # 动规
        cuts += [0,n]
        cuts.sort()
        dp = [[float("inf")]* len(cuts) for _ in range(len(cuts))]
        for i in range(len(cuts))[::-1]:
            for j in range(i+1,len(cuts)):
                if j == i+1:
                    dp[i][j] = 0
                else:
                    dp[i][j] = min(dp[i][k]+dp[k][j] for k in range(i+1,j))+cuts[j]-cuts[i]
        return dp[0][-1]