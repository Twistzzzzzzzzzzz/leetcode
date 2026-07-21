# Heap / Priority Queue

这个专题练习使用堆维护动态候选集合中的最小值、最大值、Top K 和多路归并。

## 基础笔记

- [Heap / Priority Queue 基础](../notes/heap_priority_queue_basics.md)

## 题目顺序

| 顺序 | 题号 | 题目 | 代码 | 笔记 |
| --- | --- | --- | --- | --- |
| 1 | 703 | Kth Largest Element in a Stream | `p0703_kth_largest_element_in_a_stream.py` | `p0703_kth_largest_element_in_a_stream.md` |
| 2 | 1046 | Last Stone Weight | `p1046_last_stone_weight.py` | `p1046_last_stone_weight.md` |
| 3 | 973 | K Closest Points to Origin | `p0973_k_closest_points_to_origin.py` | `p0973_k_closest_points_to_origin.md` |
| 4 | 215 | Kth Largest Element in an Array | `p0215_kth_largest_element_in_an_array.py` | `p0215_kth_largest_element_in_an_array.md` |

## 推荐路线

1. 1046. Last Stone Weight
2. 703. Kth Largest Element in a Stream
3. 215. Kth Largest Element in an Array
4. 347. Top K Frequent Elements
5. 973. K Closest Points to Origin
6. 692. Top K Frequent Words
7. 23. Merge k Sorted Lists
8. 621. Task Scheduler
9. 767. Reorganize String
10. 295. Find Median from Data Stream

## 核心原则

```text
反复取当前最小值 / 最大值 -> Heap
保留最大的 k 个 -> 大小为 k 的最小堆
保留最小的 k 个 -> 大小为 k 的最大堆
```
