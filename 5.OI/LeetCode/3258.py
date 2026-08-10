class Solution:
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        def counts(a,b): return s.count("1",a,b) <= k or s.count("0",a,b) <= k
        left = 0
        ans = 0
        while left < len(s):
            right = left + 1
            while right <= len(s) and counts(left,right):
                right += 1
            ans += right-left-1
            left += 1
        return ans