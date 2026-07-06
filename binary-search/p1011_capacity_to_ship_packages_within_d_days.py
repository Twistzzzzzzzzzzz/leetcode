from __future__ import annotations


class Solution:
    def shipWithinDays(self, weights: list[int], days: int) -> int:
        min_capacity = max(weights)
        max_capacity = sum(weights)

        def can_load(capacity: int) -> bool:
            used_days = 1
            loaded = 0

            for weight in weights:
                if loaded + weight > capacity:
                    loaded = 0
                    used_days += 1

                loaded += weight

                if used_days > days:
                    return False

            return True

        while min_capacity < max_capacity:
            mid_capacity = (min_capacity + max_capacity) // 2

            if can_load(mid_capacity):
                max_capacity = mid_capacity
            else:
                min_capacity = mid_capacity + 1

        return min_capacity


if __name__ == "__main__":
    solution = Solution()

    assert solution.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert solution.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6
    assert solution.shipWithinDays([1, 2, 3, 1, 1], 4) == 3
    assert solution.shipWithinDays([10], 1) == 10
    assert solution.shipWithinDays([5, 5, 5, 5], 2) == 10

    print("All examples passed.")
