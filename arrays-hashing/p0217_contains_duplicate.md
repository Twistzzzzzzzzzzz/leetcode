# 217. Contains Duplicate

## 题目

判断数组 `nums` 中是否存在重复元素。

如果某个值至少出现两次，返回 `True`；如果所有元素都不重复，返回 `False`。

## 思路

这道题的关键词是“是否出现过”“是否重复”。

看到这类问题，可以优先想到集合 `set`：

- 集合可以记录已经见过的元素
- 集合自带去重效果
- 判断一个元素是否在集合里很快

遍历 `nums` 时，用 `seen` 记录已经出现过的数字。

如果当前数字已经在 `seen` 里，说明它重复出现了，直接返回 `True`。

如果遍历结束都没有发现重复，返回 `False`。

## 代码

```python
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False
```

## 一行写法

```python
class Solution:
    def containsDuplicate(self, nums):
        return len(nums) != len(set(nums))
```

`set(nums)` 会去掉重复元素。

如果原数组没有重复元素：

```text
len(nums) == len(set(nums))
```

如果原数组有重复元素，转成集合后长度会变小：

```text
len(nums) != len(set(nums))
```

这里是用 `len` 间接判断列表规模是否发生变化，而不是直接比较 `set(nums)` 和 `nums`。

不要直接比较 `set(nums)` 和 `nums`，因为一个是集合，一个是列表，类型不同，比较结果不直观。

## 复杂度

手动遍历写法：

- 时间复杂度：O(n)
- 空间复杂度：O(n)

一行写法：

- 时间复杂度：O(n)
- 空间复杂度：O(n)

## 心得

1. 看到“判断某个元素之前是否出现过”“是否有重复”这类描述，可以尝试使用集合 `set`，因为集合自带去重效果。
2. 一行写法可以用 `len(nums) != len(set(nums))`，通过长度变化来判断是否有重复，而不是将 `set` 和 `array` 直接进行对比。
