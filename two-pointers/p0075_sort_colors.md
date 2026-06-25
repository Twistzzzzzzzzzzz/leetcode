# 75. Sort Colors

## 题目

给定一个只包含 `0`、`1`、`2` 的数组 `nums`。

要求原地排序，使所有 `0` 在前，所有 `1` 在中间，所有 `2` 在后。

这题也叫荷兰国旗问题。

## 思路

使用三个指针：

- `low`：下一个 `0` 应该放的位置
- `mid`：当前正在检查的位置
- `high`：下一个 `2` 应该放的位置

数组会被分成几个区域：

```text
[0 区间] [1 区间] [未知区间] [2 区间]
```

遍历时看 `nums[mid]`：

1. 如果是 `0`，和 `low` 交换，然后 `low += 1`，`mid += 1`。
2. 如果是 `1`，它本来就该在中间，直接 `mid += 1`。
3. 如果是 `2`，和 `high` 交换，然后 `high -= 1`，但 `mid` 不动。

## 为什么交换 high 后 mid 不动

这是这道题最容易忘的地方。

当 `nums[mid] == 2` 时，需要把它换到右边。

但是 `high` 指向的元素还没有被检查过，它可能是：

- `0`
- `1`
- `2`

所以交换后，新的 `nums[mid]` 仍然是不确定的。

这时 `mid` 不能前进，必须继续检查当前位置。

相反，当 `nums[mid] == 0` 时，和 `low` 交换后可以 `mid += 1`。

因为 `low` 左边已经是确定的 `0` 区间，`low` 和 `mid` 中间最多是已经处理过的 `1`，换过来的元素不会破坏后续判断。

## 代码

```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        low = 0
        mid = 0
        high = len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(1)

只遍历一遍数组，并且在原数组上交换。

## 心得

1. 第一次用三指针，核心是维护三个区域：`0` 区间、未知区间、`2` 区间。
2. `mid` 负责检查未知区间里的当前元素。
3. 和 `low` 交换后，`mid` 可以前进。
4. 和 `high` 交换后，`mid` 不能前进，因为换回来的元素还不确定，必须重新判断。
