from __future__ import annotations


class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        min_speed = 1
        max_speed = max(piles)

        def can_finish(speed: int) -> bool:
            hours = 0

            for pile in piles:
                hours += (pile + speed - 1) // speed

            return hours <= h

        while min_speed < max_speed:
            mid_speed = (min_speed + max_speed) // 2

            if can_finish(mid_speed):
                max_speed = mid_speed
            else:
                min_speed = mid_speed + 1

        return min_speed


if __name__ == "__main__":
    solution = Solution()

    assert solution.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert solution.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    assert solution.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23
    assert solution.minEatingSpeed([312884470], 312884469) == 2
    assert solution.minEatingSpeed([1, 1, 1, 999999999], 10) == 142857143

    print("All examples passed.")
