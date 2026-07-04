from __future__ import annotations


class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        slowest_time = 0.0

        for car_position, car_speed in cars:
            time = (target - car_position) / car_speed

            if time > slowest_time:
                fleets += 1
                slowest_time = time

        return fleets


if __name__ == "__main__":
    solution = Solution()

    assert solution.carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert solution.carFleet(10, [3], [3]) == 1
    assert solution.carFleet(100, [0, 2, 4], [4, 2, 1]) == 1
    assert solution.carFleet(10, [6, 8], [3, 2]) == 2

    print("All examples passed.")
