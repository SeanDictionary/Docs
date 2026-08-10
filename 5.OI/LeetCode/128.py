from typing import *


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums.sort()
        ans = 1
        lenth = 1
        for index, num in enumerate(nums[1:]):
            if num == nums[index] + 1:
                lenth += 1
            elif num == nums[index]:
                continue
            else:
                ans = max(ans, lenth)
                lenth = 1

        return max(ans, lenth)


if __name__ == '__main__':
    s = Solution()

    inputs = [
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    ]

    print(s.longestConsecutive(*inputs))
