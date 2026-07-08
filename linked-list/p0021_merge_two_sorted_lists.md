# 21. Merge Two Sorted Lists

## 题目

给定两个升序链表 `list1` 和 `list2`，把它们合并成一个新的升序链表，并返回合并后链表的头节点。

## 思路

这题是 dummy 构造链表的典型题。

用一个虚拟头节点：

```python
dummy = ListNode(0)
curr = dummy
```

其中：

```text
dummy  用来固定新链表的起点
curr   永远指向新链表的尾巴
```

每次比较 `list1.val` 和 `list2.val`，把更小的节点接到 `curr.next`，然后移动对应链表的指针。

接完一个节点后，`curr` 也要往后移动：

```python
curr = curr.next
```

当其中一个链表为空时，另一个链表剩下的部分本身已经有序，直接接到 `curr.next` 后面即可。

最后返回：

```python
return dummy.next
```

## 代码

```python
class Solution:
    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode(0)
        curr = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next

            curr = curr.next

        if list1:
            curr.next = list1
        else:
            curr.next = list2

        return dummy.next
```

## 复杂度

设两个链表长度分别为 `m` 和 `n`。

时间复杂度：O(m + n)

空间复杂度：O(1)

## 心得

这题的核心是 dummy + curr。

`curr` 永远指向新链表尾部，每次把较小节点接到 `curr.next`。

dummy 不是真正答案的一部分，它只是为了方便构造链表；最后要返回 `dummy.next`。
