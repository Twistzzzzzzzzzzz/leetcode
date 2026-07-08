# 141. Linked List Cycle

## 题目

给定一个链表的头节点 `head`，判断链表中是否存在环。

如果链表中某个节点可以通过连续的 `next` 指针再次到达，说明链表有环。

## 思路

这题使用快慢指针。

```text
slow 每次走 1 步
fast 每次走 2 步
```

如果链表没有环，`fast` 最终会走到 `None`。

如果链表有环，`fast` 会在环中追上 `slow`。

循环条件写成：

```python
while fast and fast.next:
```

因为每轮要执行：

```python
fast = fast.next.next
```

所以必须保证 `fast` 和 `fast.next` 都存在。

## 代码

```python
class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        fast = head
        slow = head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            if fast == slow:
                return True

        return False
```

## 复杂度

时间复杂度：O(n)

空间复杂度：O(1)

## 心得

链表判环是快慢指针的经典应用。

判断是否相遇时，比较的是节点对象本身：

```python
if fast == slow:
```

不是比较节点的值。

因为两个不同节点的 `val` 可能相等，但它们不是同一个节点。
