# 287. Find the Duplicate Number

## 题目

给定一个长度为 `n + 1` 的数组 `nums`，其中每个数字都在 `1..n` 范围内。

数组中只有一个重复数字，要求找出这个重复数字。

要求：

- 不能修改数组
- 只能使用 O(1) 额外空间

## 思路

这题表面上是数组题，但可以把它看成链表判环题。

题目给了一个关键信息：

```text
nums[i] 的范围在 1..len(nums) - 1
```

所以 `nums[i]` 可以继续当作下一个下标。

也就是：

```python
next_index = nums[index]
```

这就形成了一个隐式链表：

```text
index -> nums[index] -> nums[nums[index]] -> ...
```

因为数组长度是 `n + 1`，但值只在 `1..n`，一定会有重复值。

重复值会让两个位置指向同一个下标，形成环。

换成链表语言理解就是：

```text
如果有两个元素指向同一个元素，在这题的数组模拟链表结构里，路径最终就会汇入同一个环。
```

所以重复数字对应的就是环入口。

所以这题可以用 Floyd 快慢指针。

## 第一阶段：找到相遇点

```python
slow = 0
fast = 0

while True:
    slow = nums[slow]
    fast = nums[nums[fast]]

    if slow == fast:
        break
```

这里的移动方式是：

```text
slow 每次走一步
fast 每次走两步
```

注意这里不是链表节点的 `next`，而是数组里的：

```python
nums[index]
```

可以理解为从当前下标跳到下一个下标。

## 第二阶段：找到环入口

第一阶段相遇后，让一个指针回到起点 `0`：

```python
finder = 0
```

然后两个指针每次都走一步：

```python
while finder != slow:
    finder = nums[finder]
    slow = nums[slow]
```

最终相遇的位置就是环入口，也就是重复数字。

## 为什么返回 `finder`，不是 `nums[finder]`

在这题里，环入口的位置本身就是重复数字。

第二阶段结束时：

```python
finder == slow
```

这个相遇位置就是重复数字。

所以直接返回：

```python
return finder
```

如果你的变量叫 `count`，那也是同理：

```python
while count != fast:
    fast = nums[fast]
    count = nums[count]

return count
```

循环结束时，`count == fast`，这个位置就是环入口，也就是重复数字。

## 代码

```python
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow = 0
        fast = 0

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]

            if slow == fast:
                break

        finder = 0

        while finder != slow:
            finder = nums[finder]
            slow = nums[slow]

        return finder
```

## 复杂度

时间复杂度：O(n)

空间复杂度：O(1)

## 心得

看到这题可以想到解法可能和下标有关。

关键提示是：

```text
nums 中的元素范围是 1 到 len(nums) - 1
```

所以数组值可以当作下一个下标，从而把数组看成链表。

这题本质是：

```text
数组下标模拟链表指针 + Floyd 判环找入口
```

重复数字就是环入口。
