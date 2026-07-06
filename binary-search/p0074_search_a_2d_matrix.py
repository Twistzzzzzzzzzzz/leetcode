from __future__ import annotations


class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        row_left = 0
        row_right = len(matrix)

        while row_left < row_right:
            row_mid = (row_left + row_right) // 2

            if target > matrix[row_mid][0]:
                row_left = row_mid + 1
            elif target < matrix[row_mid][0]:
                row_right = row_mid
            else:
                return True

        row = row_left - 1
        if row < 0:
            return False

        col_left = 0
        col_right = len(matrix[0]) - 1

        while col_left <= col_right:
            col_mid = (col_left + col_right) // 2

            if target > matrix[row][col_mid]:
                col_left = col_mid + 1
            elif target < matrix[row][col_mid]:
                col_right = col_mid - 1
            else:
                return True

        return False


class FlattenedSolution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows = len(matrix)
        cols = len(matrix[0])
        left = 0
        right = rows * cols - 1

        while left <= right:
            mid = (left + right) // 2
            row = mid // cols
            col = mid % cols
            value = matrix[row][col]

            if value == target:
                return True
            if value < target:
                left = mid + 1
            else:
                right = mid - 1

        return False


if __name__ == "__main__":
    matrix_1 = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60],
    ]
    matrix_2 = [[1]]

    solution = Solution()
    flattened = FlattenedSolution()

    for solver in (solution, flattened):
        assert solver.searchMatrix(matrix_1, 3) is True
        assert solver.searchMatrix(matrix_1, 13) is False
        assert solver.searchMatrix(matrix_1, 1) is True
        assert solver.searchMatrix(matrix_1, 60) is True
        assert solver.searchMatrix(matrix_1, 0) is False
        assert solver.searchMatrix(matrix_2, 1) is True
        assert solver.searchMatrix(matrix_2, 2) is False

    print("All examples passed.")
