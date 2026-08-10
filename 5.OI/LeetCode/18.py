from typing import *


class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ans = []
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            a = nums[i]
            for h in range(i + 1, n - 2):
                if h > i + 1 and nums[h] == nums[h - 1]:
                    continue
                b = nums[h]
                j, k = h + 1, n - 1
                while j < k:
                    c, d = nums[j], nums[k]
                    s = a + b + c + d
                    if s == target:
                        ans.append([a, b, c, d])
                        j += 1
                        k -= 1
                        while j < k and nums[j] == nums[j - 1]:
                            j += 1
                        while j < k and nums[k] == nums[k + 1]:
                            k -= 1
                    elif s < target:
                        j += 1
                    else:
                        k -= 1
        return ans


if __name__ == '__main__':
    s = Solution()
