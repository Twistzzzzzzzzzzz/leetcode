# 138. Copy List with Random Pointer

## 题目

给定一个特殊链表，每个节点除了 `next` 指针，还有一个 `random` 指针。

`random` 可以指向链表中的任意节点，也可以是 `None`。

要求深拷贝整个链表，返回新链表的头节点。

深拷贝的意思是：

- 新链表节点的值和原链表一样。
- 新链表的 `next` 和 `random` 关系和原链表一样。
- 新链表的节点必须是新创建的节点，不能复用原节点。

## 思路

这题的难点是 `random` 指针。

普通链表只有 `next`，可以边遍历边复制。

但这里的 `random` 可能指向后面的节点，也可能指向前面的节点。如果复制当前节点时立刻处理 `random`，目标节点可能还没有创建。

所以更稳的做法是两遍遍历。

第一遍：

```text
复制每个节点本身，建立 原节点 -> 新节点 的映射。
```

也就是：

```python
old_to_new[curr] = Node(curr.val)
```

第二遍：

```text
根据映射补上新节点的 next 和 random。
```

也就是：

```python
old_to_new[curr].next = old_to_new[curr.next]
old_to_new[curr].random = old_to_new[curr.random]
```

## `old_to_new = {None: None}`

这个初始化很关键：

```python
old_to_new = {None: None}
```

它的作用是统一处理空指针。

如果 `curr.next` 是 `None`：

```python
old_to_new[curr.next]
```

就等于：

```python
old_to_new[None]
```

结果是 `None`。

同理，如果 `curr.random` 是 `None`，也可以直接得到 `None`。

这样就不用额外写很多判断：

```python
if curr.next:
if curr.random:
```

## 代码

```python
class Solution:
    def copyRandomList(self, head: Node | None) -> Node | None:
        old_to_new: dict[Node | None, Node | None] = {None: None}

        curr = head
        while curr:
            old_to_new[curr] = Node(curr.val)
            curr = curr.next

        curr = head
        while curr:
            old_to_new[curr].next = old_to_new[curr.next]
            old_to_new[curr].random = old_to_new[curr.random]
            curr = curr.next

        return old_to_new[head]
```

## 复杂度

时间复杂度：O(n)

空间复杂度：O(n)

空间来自 HashMap，需要保存每个原节点到新节点的映射。

## 心得

这题属于复杂指针 + HashMap。

核心不是直接复制 `random` 指针，而是先建立映射：

```text
原节点 -> 新节点
```

之后所有指针关系都通过这个映射转换。

两遍遍历的含义：

1. 第一遍只创建节点，不连指针。
2. 第二遍再补 `next` 和 `random`。

`old_to_new = {None: None}` 可以让空指针也走同一套逻辑，代码更简洁。
