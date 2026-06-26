# 88. Merge Sorted Array

## 题目

给定两个已经升序排列的数组 `nums1` 和 `nums2`。

`nums1` 的长度是 `m + n`，前 `m` 个位置是有效数字，后 `n` 个位置是空位，用来放合并后的结果。

要求把 `nums2` 合并进 `nums1`，并且直接修改 `nums1`。

## 思路

使用三个指针：

- `index1` 指向 `nums1` 有效部分的最后一个元素
- `index2` 指向 `nums2` 的最后一个元素
- `write_index` 指向当前应该写入的位置

因为两个数组本身已经排好序，所以每次只需要比较 `nums1[index1]` 和 `nums2[index2]`。

较大的数字应该放到最终数组的最后面。

所以从后往前写：

```text
谁大，谁放到 write_index
```

然后对应指针左移。

## 为什么从后插入更好

因为 `nums1` 的空位在后面。

如果从前往后写，很容易覆盖 `nums1` 里还没有比较过的有效数字。

例如：

```text
nums1 = [1, 2, 3, 0, 0, 0]
nums2 = [2, 5, 6]
```

如果从前面开始写，写入 `2` 时可能会破坏原来的 `1`、`2`、`3`，还需要额外移动元素。

但从后往前写时，后面本来就是空位：

```text
[1, 2, 3, 0, 0, 6]
[1, 2, 3, 0, 5, 6]
[1, 2, 3, 3, 5, 6]
...
```

这样不会覆盖还没处理的有效元素。

## 为什么只需要额外处理 `nums2`

主循环结束后，可能有两种情况：

1. `nums2` 还有剩余元素。
2. `nums1` 还有剩余元素。

如果 `nums2` 还有剩余，就必须复制到 `nums1` 前面。

如果 `nums1` 还有剩余，不需要处理。

因为这些元素本来就在 `nums1` 里，而且已经在正确位置上。

## 代码

```python
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        index1 = m - 1
        index2 = n - 1
        write_index = m + n - 1

        while index1 >= 0 and index2 >= 0:
            if nums1[index1] <= nums2[index2]:
                nums1[write_index] = nums2[index2]
                index2 -= 1
            else:
                nums1[write_index] = nums1[index1]
                index1 -= 1

            write_index -= 1

        while index2 >= 0:
            nums1[write_index] = nums2[index2]
            index2 -= 1
            write_index -= 1
```

## 复杂度

- 时间复杂度：O(m + n)
- 空间复杂度：O(1)

只在 `nums1` 原地写入，没有创建额外数组。

## 心得

1. 这题适合从后往前合并，因为 `nums1` 的空位就在后面。
2. 从前往后写可能覆盖 `nums1` 里还没处理的有效元素。
3. 合并结束后别忘记处理剩余元素。
4. 如果剩下的是 `nums2`，需要继续复制；如果剩下的是 `nums1`，它本来就在正确位置，不用额外处理。
