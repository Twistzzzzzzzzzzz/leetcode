from __future__ import annotations


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for index, num in enumerate(nums):
            need = target - num
            if need in seen:
                return [seen[need], index]
            seen[num] = index
        return []

