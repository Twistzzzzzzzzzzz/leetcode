from __future__ import annotations


class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack: list[int] = []

        for asteroid in asteroids:
            alive = True

            while stack and stack[-1] > 0 and asteroid < 0:
                if abs(asteroid) > abs(stack[-1]):
                    stack.pop()
                elif abs(asteroid) == abs(stack[-1]):
                    stack.pop()
                    alive = False
                    break
                else:
                    alive = False
                    break

            if alive:
                stack.append(asteroid)

        return stack


if __name__ == "__main__":
    solution = Solution()

    assert solution.asteroidCollision([5, 10, -5]) == [5, 10]
    assert solution.asteroidCollision([8, -8]) == []
    assert solution.asteroidCollision([10, 2, -5]) == [10]
    assert solution.asteroidCollision([-2, -1, 1, 2]) == [-2, -1, 1, 2]
    assert solution.asteroidCollision([1, -2, -2, -2]) == [-2, -2, -2]

    print("All examples passed.")
