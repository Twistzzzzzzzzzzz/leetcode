# Graphs

这个专题把 Tree 中已经学过的 DFS/BFS 推广到可能有环、不连通、存在多条路径的图结构。

## 基础笔记

- [Graph / 图基础](../notes/graph_basics.md)

## 当前状态

专题基础资料已经完成，并从网格关系热身题开始练习。

## 已完成

| 题号 | 题目 | 重点 |
| --- | --- | --- |
| 463 | [Island Perimeter](p0463_island_perimeter.md) | 网格建模、四方向、边界 |
| 953 | [Verifying an Alien Dictionary](p0953_verifying_an_alien_dictionary.md) | 字符排名、字典序、269 前置 |

## 推荐路线

| 顺序 | 题号 | 题目 | 重点 |
| --- | --- | --- | --- |
| 1 | 463 | Island Perimeter | 网格关系、四方向边界 |
| 2 | 953 | Verifying an Alien Dictionary | 字典序规则、269 前置 |
| 3 | 1971 | Find if Path Exists in Graph | 邻接表、visited、基础 DFS/BFS |
| 4 | 733 | Flood Fill | 网格 DFS |
| 5 | 200 | Number of Islands | 连通分量 |
| 6 | 695 | Max Area of Island | 区域大小 |
| 7 | 133 | Clone Graph | 旧节点到新节点的映射 |
| 8 | 994 | Rotting Oranges | 多源 BFS、层数 |
| 9 | 130 | Surrounded Regions | 从边界反向标记 |
| 10 | 417 | Pacific Atlantic Water Flow | 反向搜索、多起点 |
| 11 | 207 | Course Schedule | 有向环、拓扑排序 |
| 12 | 210 | Course Schedule II | 返回拓扑顺序 |
| 13 | 785 | Is Graph Bipartite? | BFS / DFS 染色 |
| 14 | 684 | Redundant Connection | Union-Find 判环 |
| 15 | 127 | Word Ladder | 隐式图、最短路径 BFS |
| 16 | 743 | Network Delay Time | Dijkstra + Heap |

## 核心原则

```text
节点之间存在关系或状态转移 -> Graph
访问所有可达状态 -> DFS / BFS + visited
无权最短步数或同时扩散 -> BFS
未来任务有依赖顺序 -> Topological Sort
动态合并连通分量 -> Union-Find
非负权最短路径 -> Dijkstra + Heap
```

## 入门固定步骤

```text
1. 说明节点是什么。
2. 说明边是什么。
3. 判断有向 / 无向、有权 / 无权。
4. 选择邻接表、矩阵或网格隐式图。
5. 定义 visited 的含义。
6. 选择 DFS 或 BFS。
7. 检查图是否可能不连通。
```

前 8 题完成前，不需要急着学习 Dijkstra 或最小生成树。
