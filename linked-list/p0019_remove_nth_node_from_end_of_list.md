# 19. Remove Nth Node From End of List

## 题目

给定一个链表的头节点 `head` 和整数 `n`，删除链表中倒数第 `n` 个节点，并返回新的头节点。

例如：

```text
1 -> 2 -> 3 -> 4 -> 5
n = 2
```

删除倒数第 2 个节点 `4` 后：

```text
1 -> 2 -> 3 -> 5
```

## 思路

这题的核心是让 `fast` 先走 `n` 步。

然后 `slow` 和 `fast` 一起走。

当 `fast` 走到最后一个节点时，`slow.next` 正好是要删除的节点。

因为可能删除头节点，所以要用 dummy：

```python
dummy = ListNode(0)
dummy.next = head

slow = dummy
fast = dummy
```

这样即使要删除原来的 `head`，`slow` 也可以停在 dummy 上，通过：

```python
slow.next = slow.next.next
```

统一完成删除。

## 为什么需要 dummy

如果不用 dummy，删除头节点会很麻烦。

例如：

```text
1 -> 2 -> 3
n = 3
```

要删除的是 `1`。

如果 `slow` 从 `head` 开始，最后很难让 `slow` 停在 `1` 的前一个节点，因为 `head` 前面没有真实节点。

加 dummy 后：

```text
dummy -> 1 -> 2 -> 3
```

如果要删除 `1`，`slow` 可以停在 dummy：

```python
slow.next = slow.next.next
```

就变成：

```text
dummy -> 2 -> 3
```

最后返回：

```python
return dummy.next
```

也就是新的头节点 `2`。

## 代码

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0)
        dummy.next = head

        slow = dummy
        fast = dummy

        for _ in range(n):
            fast = fast.next

        while fast.next:
            fast = fast.next
            slow = slow.next

        slow.next = slow.next.next

        return dummy.next
```

## 复杂度

时间复杂度：O(n)

空间复杂度：O(1)

## 心得

这题方向是快慢指针：

- `fast` 先走 `n` 步。
- `slow` 和 `fast` 一起走。
- 当 `fast.next` 为空时，`slow.next` 是要删除的节点。

关键点是 dummy。

不用 dummy 时，删除头节点会错。例如链表长度刚好等于 `n` 时，要删除的就是 `head`。

另外最后必须返回新的头节点：

```python
return dummy.next
```

不能只修改局部变量，也不能忘记返回。
