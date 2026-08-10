from typing import *


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        i = 0
        l, r = 0, n - 1
        while l < r:
            mid = (l + r) // 2
            if matrix[i][mid] == target:
                return True
            elif matrix[i][mid] < target:
                l = mid + 1
            elif matrix[i][mid] > target:
                r = mid - 1

        j = l
        while 0 <= i < m and 0 <= j < n:
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                i += 1
            elif matrix[i][j] > target:
                j -= 1
        else:
            return False


if __name__ == '__main__':
    param = [
        [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]],
        5
    ]
    print(Solution().searchMatrix(*param))
