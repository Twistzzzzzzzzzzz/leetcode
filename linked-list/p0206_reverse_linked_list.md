# 206. Reverse Linked List

## 题目

给定一个单链表的头节点 `head`，反转整个链表，并返回反转后的新头节点。

例如：

```text
1 -> 2 -> 3 -> 4 -> 5
```

反转后：

```text
5 -> 4 -> 3 -> 2 -> 1
```

## 思路

这题是链表专题最核心的基础题。

反转链表的关键是维护三个指针：

```text
prev  已经反转好的前一个节点
curr  当前正在处理的节点
nxt   原链表中 curr 后面的节点
```

每次循环做四步：

```python
nxt = curr.next
curr.next = prev
prev = curr
curr = nxt
```

最重要的是第一步：

```python
nxt = curr.next
```

因为一旦执行：

```python
curr.next = prev
```

原来 `curr` 后面的链表就会断开。如果没有提前保存 `nxt`，后面的节点就找不到了。

## 代码

```python
class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        curr = head

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        return prev
```

## 复杂度

时间复杂度：O(n)

空间复杂度：O(1)

## 心得

链表反转的口诀：

```text
先存 next
再改 curr.next
再移动 prev 和 curr
```

最后返回的是 `prev`，不是原来的 `head`。

因为循环结束时，`curr` 已经走到 `None`，`prev` 才是反转后链表的新头节点。
