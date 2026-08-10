from typing import *

# # 单调栈
# class Solution:
#     def trap(self, height: List[int]) -> int:
#         ans = 0
#         left = []
#         for right in range(len(height)):
#             if not left:
#                 left.append(right)
#             elif height[right] < height[left[-1]]:
#                 left.append(right)
#             else:
#                 floor = height[left[-1]]
#                 left.pop(-1)
#                 while left:
#                     tmp = left[-1]
#                     aa = min(height[tmp], height[right])
#                     ans += (aa - floor) * (right - tmp - 1)
#                     floor = aa
#                     if height[tmp] > height[right]:
#                         break
#                     left.pop(-1)
#                 left.append(right)

#         return ans

# 双指针


class Solution:
    def trap(self, height: List[int]) -> int:
        ans = 0
        count = 0
        left, right = 0, 0
        while right < len(height) - 1:
            right += 1
            if height[right] >= height[left]:
                ans += (right - left - 1) * height[left] - count
                count = 0
                left = right
            else:
                count += height[right]

        if left < len(height) - 2:
            height = height[:left - 1:-1] if left > 0 else height[::-1]
            count = 0
            left, right = 0, 0
            while right < len(height) - 1:
                right += 1
                if height[right] >= height[left]:
                    ans += (right - left - 1) * height[left] - count
                    count = 0
                    left = right
                else:
                    count += height[right]

        return ans


if __name__ == '__main__':
    s = Solution()

    inputs = [
        [4, 2, 3]
    ]

    print(s.trap(*inputs))
