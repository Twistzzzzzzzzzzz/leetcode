from __future__ import annotations

import heapq


class Solution:
    def kClosest(
        self,
        points: list[list[int]],
        k: int,
    ) -> list[list[int]]:
        max_heap: list[tuple[int, list[int]]] = []

        for point in points:
            x, y = point
            negative_distance_squared = -(x * x + y * y)

            heapq.heappush(
                max_heap,
                (negative_distance_squared, point),
            )

            if len(max_heap) > k:
                heapq.heappop(max_heap)

        return [point for _, point in max_heap]


def normalize(points: list[list[int]]) -> set[tuple[int, int]]:
    return {tuple(point) for point in points}


if __name__ == "__main__":
    solution = Solution()

    result = solution.kClosest([[1, 3], [-2, 2]], 1)
    assert result == [[-2, 2]]

    result = solution.kClosest([[3, 3], [5, -1], [-2, 4]], 2)
    assert normalize(result) == {(3, 3), (-2, 4)}

    result = solution.kClosest([[1, 1], [-1, -1], [2, 0]], 2)
    assert normalize(result) == {(1, 1), (-1, -1)}

    points = [[0, 1], [1, 0], [2, 2]]
    result = solution.kClosest(points, len(points))
    assert normalize(result) == normalize(points)

    print("All examples passed.")
