from typing import *


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        closest = nums[0] + nums[1] + nums[2]
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            a = nums[i]
            j, k = i + 1, n - 1
            while j < k:
                b, c = nums[j], nums[k]
                s = a + b + c
                if abs(s - target) < abs(closest - target):
                    closest = s
                if s == target:
                    return closest
                elif s < target:
                    j += 1
                else:
                    k -= 1
        return closest


if __name__ == '__main__':
    s = Solution()
    print(s.threeSumClosest([1, 1, 1, 0], 100))
