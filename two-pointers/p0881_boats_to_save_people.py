from __future__ import annotations


class Solution:
    def numRescueBoats(self, people: list[int], limit: int) -> int:
        people.sort()

        left = 0
        right = len(people) - 1
        boats = 0

        while left <= right:
            if people[left] + people[right] <= limit:
                left += 1

            right -= 1
            boats += 1

        return boats


if __name__ == "__main__":
    solution = Solution()

    assert solution.numRescueBoats([1, 2], 3) == 1
    assert solution.numRescueBoats([3, 2, 2, 1], 3) == 3
    assert solution.numRescueBoats([3, 5, 3, 4], 5) == 4
    assert solution.numRescueBoats([1, 1, 1, 1], 3) == 2

    print("All examples passed.")
