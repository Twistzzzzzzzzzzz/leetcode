# 167. Two Sum II - Input Array Is Sorted

## 题目

给定一个从小到大排列的数组 `numbers`，从中找出两个数，使它们的和等于 `target`。

返回两个数的下标，注意题目要求返回的是从 `1` 开始的下标。

## 关键信息

题目给了一个非常重要的信息：

```text
numbers is sorted in non-decreasing order
```

也就是数组已经按非递减顺序排好序。

所以这题不要优先想 HashMap 或双层循环，而应该先想到左右双指针。

## 双指针的应用场景

这题是非常典型的左右双指针应用场景。

可以从三个条件判断：

1. 数组已经排序。
2. 题目要找两个数满足某种关系，这里是两数之和等于 `target`。
3. 移动左指针或右指针，会让当前结果发生可预测的变化。

其中最关键的是第一点：数组已经排好序。

正是因为排好序，指针移动才有方向感。

在这题里：

- `left` 向右移动，数字会变大，所以两数之和可能变大。
- `right` 向左移动，数字会变小，所以两数之和可能变小。

因此可以根据当前和与 `target` 的大小关系，决定移动哪一个指针。

这就是双指针比 HashMap 更适合这题的原因。

如果数组没有排序，就不能通过大小关系判断该移动哪边，这时才更适合回到 HashMap 思路。

## 思路

定义两个指针：

- `left` 指向数组最左边
- `right` 指向数组最右边

每次计算：

```python
current_sum = numbers[left] + numbers[right]
```

然后根据 `current_sum` 和 `target` 的关系移动指针：

1. 如果 `current_sum < target`，说明当前和太小，需要更大的数，所以 `left += 1`。
2. 如果 `current_sum > target`，说明当前和太大，需要更小的数，所以 `right -= 1`。
3. 如果相等，就返回 `[left + 1, right + 1]`。

## 为什么可以这样移动

因为数组已经排序。

当 `numbers[left] + numbers[right]` 太小时，右边已经是当前能选到的较大值了。

如果还想让和变大，只能让左边指针向右移动，换一个更大的左边数字。

当和太大时，同理，需要让右边指针向左移动，换一个更小的右边数字。

这就是排序数组里左右双指针能成立的原因。

## 和第 1 题 Two Sum 的区别

第 1 题的数组没有排序。

未排序时，不能通过大小关系判断应该移动哪边，所以常用 HashMap。

这一题数组已经排序，大小关系可以指导指针移动，所以用左右双指针更直接。

## 代码

```python
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum < target:
                left += 1
            elif current_sum > target:
                right -= 1
            else:
                return [left + 1, right + 1]

        return []
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

每个指针最多移动 `n` 次，并且没有使用额外数据结构。

## 心得

1. 这题最重要的信息是：数组已经排序。
2. 已排序数组中找两个数满足某个和，可以优先想到左右双指针。
3. 未排序版 Two Sum 常用 HashMap；排序版 Two Sum 可以用双指针。
4. 返回结果要记得加一，因为题目要求的是 `1-indexed` 下标。
