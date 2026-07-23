# Graph / 图基础

## 1. 为什么现在可以先学 Graph

可以先学 Graph，不必先完成 Backtracking。

你已经具备 Graph 入门最重要的前置知识：

- 树的递归 DFS；
- 树的队列 BFS；
- `set` 判断是否访问过；
- `deque` 的 `append` 和 `popleft`；
- 栈和递归调用栈；
- HashMap / 字典保存关系。

树本身就是一种特殊的图：

```text
树 = 连通 + 无环的图
```

从 Tree 进入 Graph，主要增加三个问题：

```text
图可能有环
图可能不连通
同一节点可能由多条路径到达
```

所以 Graph 入门最核心的新工具只有：

```text
邻接表 adjacency list
+
visited 访问集合
```

Backtracking 更强调枚举选择和恢复状态；基础 Graph 更强调防止重复访问。因此先学 Graph 完全合理。

## 2. 什么是图

图由两部分组成：

```text
节点 Vertex / Node
边 Edge
```

例如：

```text
0 -- 1
|    |
2 -- 3
```

节点集合：

```text
{0, 1, 2, 3}
```

边表示节点之间的关系：

```text
(0, 1)
(0, 2)
(1, 3)
(2, 3)
```

图可以表示：

- 城市与道路；
- 用户与关注关系；
- 课程与先修关系；
- 网页与链接；
- 单词之间的转换；
- 棋盘格之间的移动；
- 服务器与网络连接；
- 任务之间的依赖。

## 3. 图的基础术语

### Vertex / Node

图中的节点。

### Edge

两个节点之间的连接。

### Neighbor

与当前节点通过一条边直接相连的节点。

### Path

从一个节点沿边走到另一个节点经过的序列。

### Cycle

从某个节点出发，沿边最终又回到该节点形成的环。

### Degree

无向图中，与节点相连的边数。

### Indegree

有向图中，指向当前节点的边数。

### Outdegree

有向图中，从当前节点指出去的边数。

### Connected Component

无向图中的连通分量。

同一个连通分量中的任意两个节点都可以通过某条路径互相到达。

## 4. 无向图与有向图

### 无向图

边没有方向：

```text
0 -- 1
```

表示：

```text
0 可以到 1
1 也可以到 0
```

建立邻接表时必须添加两次：

```python
graph[0].append(1)
graph[1].append(0)
```

### 有向图

边有方向：

```text
0 -> 1
```

只表示：

```text
0 可以沿这条边到 1
```

不能自动推出 1 可以到 0。

建立邻接表时只添加题目给出的方向：

```python
graph[0].append(1)
```

课程先修关系、关注关系通常是有向图。

道路、朋友关系、网络连接通常可能是无向图，但必须以题意为准。

## 5. 加权图与无权图

### 无权图

每条边的代价相同，可以理解为每走一条边成本都是 1。

例如：

```text
0 -> 1
0 -> 2
```

### 加权图

每条边带有距离、时间、价格等权重：

```text
0 --5--> 1
0 --2--> 2
```

邻接表可以保存：

```python
graph[node].append((neighbor, weight))
```

无权图最短路通常使用 BFS。

非负权图最短路通常使用 Dijkstra + 最小堆。

## 6. 稀疏图与稠密图

设：

```text
V = 节点数量
E = 边数量
```

### 稀疏图

边数量远小于 `V^2`。

通常使用邻接表，空间 O(V + E)。

### 稠密图

大量节点之间都有边，边数量接近 `V^2`。

邻接矩阵有时更方便。

LeetCode 大多数普通图题优先使用邻接表。

## 7. 图的三种常见表示方式

### Edge List / 边列表

题目输入常直接给：

```python
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
]
```

它适合输入和排序，但从某个节点寻找全部邻居不方便。

通常先转换为邻接表。

### Adjacency List / 邻接表

```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2],
}
```

含义：

```text
node -> 所有邻居
```

这是 LeetCode 图题最常用的表示方式。

### Adjacency Matrix / 邻接矩阵

```python
matrix[i][j] == 1
```

表示节点 `i` 和 `j` 之间存在边。

优点：

- 查询两个节点是否直接相连为 O(1)；

缺点：

- 空间 O(V^2)；
- 遍历某节点邻居需要扫描整行 O(V)。

节点数量较小或输入本身就是矩阵时可以直接使用。

## 8. 如何建立邻接表

### 节点编号是 `0..n-1`

无向图：

```python
graph = [[] for _ in range(n)]

for node_a, node_b in edges:
    graph[node_a].append(node_b)
    graph[node_b].append(node_a)
```

有向图：

```python
graph = [[] for _ in range(n)]

for source, destination in edges:
    graph[source].append(destination)
```

### 节点编号不连续

可以使用：

```python
from collections import defaultdict

graph = defaultdict(list)
```

然后：

```python
graph[source].append(destination)
```

### 是否使用列表还是集合

邻居没有重复边时，列表更轻量。

如果需要自动去重或高效删除，可以使用集合：

```python
graph[node] = set()
```

## 9. 图和树遍历最大的区别

树中从根向孩子遍历时，通常不会重新回到父节点。

图中可能存在：

```text
0 -> 1 -> 2 -> 0
```

如果没有 `visited`，DFS 会无限递归：

```text
0, 1, 2, 0, 1, 2, ...
```

因此基础图遍历必须维护：

```python
visited = set()
```

进入节点时立即标记：

```python
visited.add(node)
```

再访问邻居。

## 10. 看到图题时的固定八问

### 1. 节点是什么

可能是：

- 数字；
- 城市；
- 课程；
- 用户；
- 单词；
- 矩阵格子；
- 某种状态。

### 2. 边是什么

什么条件表示两个状态可以互相转移？

### 3. 有方向吗

无向边要添加两次，有向边只添加一次。

### 4. 有权重吗

无权最短路与加权最短路使用的算法不同。

### 5. 输入已经是图吗

输入可能是：

- 边列表；
- 邻接表；
- 邻接矩阵；
- 网格；
- 需要自己根据规则建图。

### 6. 题目问什么

- 是否可达；
- 连通分量数量；
- 最短距离；
- 是否有环；
- 拓扑顺序；
- 复制整张图；
- 最小生成树；
- 所有路径。

### 7. `visited` 表示什么

- 全局已经处理过；
- 当前 DFS 路径正在访问；
- 已经确定安全；
- 当前最短距离已经确定。

### 8. 图可能不连通吗

如果题目要求处理全部节点，通常要：

```python
for node in range(n):
    if node not in visited:
        dfs(node)
```

不能只从节点 0 开始。

## 11. DFS：递归版本

```python
def dfs(node):
    if node in visited:
        return

    visited.add(node)

    for neighbor in graph[node]:
        dfs(neighbor)
```

调用：

```python
visited = set()
dfs(start)
```

更常见的写法是在进入递归前检查邻居：

```python
def dfs(node):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)
```

两种都正确。

核心不变量是：

```text
一个节点进入 DFS 后，就立刻加入 visited
```

## 12. DFS：显式栈版本

```python
def dfs_iterative(start):
    stack = [start]
    visited = {start}

    while stack:
        node = stack.pop()

        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            stack.append(neighbor)
```

递归 DFS 使用系统调用栈。

显式版本自己维护：

```python
stack = []
```

当图很深、可能超过 Python 递归深度时，显式栈更稳妥。

## 13. BFS：队列版本

```python
from collections import deque


def bfs(start):
    queue = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)
```

BFS 按距离起点的层数遍历：

```text
距离 0
距离 1
距离 2
...
```

因此无权图中寻找最短边数时优先考虑 BFS。

## 14. BFS 为什么入队时就要标记

推荐：

```python
visited.add(neighbor)
queue.append(neighbor)
```

不要等到出队时才标记。

假设节点 3 同时是节点 1 和节点 2 的邻居。

如果标记太晚：

```text
1 把 3 加入队列
2 又把 3 加入队列
```

节点 3 会重复入队，造成无意义的工作，某些计数题还可能出错。

固定记忆：

```text
DFS：决定进入递归时标记
BFS：决定入队时标记
```

## 15. DFS 与 BFS 怎么选

### 两者都可以

- 判断两个节点是否连通；
- 访问整个连通分量；
- 统计岛屿数量；
- 图的普通遍历。

### 优先 DFS

- 递归表达自然；
- 需要完整探索一条路径；
- 连通分量；
- 染色；
- 后序状态；
- 代码简洁。

### 优先 BFS

- 无权图最短路径；
- 最少步数；
- 按层处理；
- 同时扩散；
- 离所有起点最近的距离；
- 腐烂、感染、传播时间。

可以记成：

```text
可达 / 连通 -> DFS 或 BFS
无权最短 / 层数 / 扩散时间 -> BFS
```

## 16. BFS 如何记录层数

```python
queue = deque([start])
visited = {start}
distance = 0

while queue:
    level_size = len(queue)

    for _ in range(level_size):
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    distance += 1
```

每轮外层 `while` 处理一整层。

也可以直接把距离一起入队：

```python
queue = deque([(start, 0)])
```

选择哪一种取决于题目是否需要每个节点的独立距离。

## 17. 连通分量

如果图不连通，从一个起点只能访问一个连通分量。

统计全部连通分量：

```python
components = 0
visited = set()

for node in range(n):
    if node in visited:
        continue

    components += 1
    dfs(node)
```

每次从一个尚未访问的节点启动 DFS，就发现一个新连通分量。

这个模式对应：

- 岛屿数量；
- 朋友圈 / 省份数量；
- 网络分组；
- 无向图中的独立区域。

## 18. 网格也是图

二维矩阵中的每个格子可以看作一个节点。

上下左右相邻格子之间存在边：

```python
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]
```

从当前格子：

```python
next_row = row + row_change
next_col = col + col_change
```

这叫隐式图：

```text
不需要真的创建邻接表
根据坐标规则动态得到邻居
```

## 19. 网格 DFS 模板

```python
rows = len(grid)
cols = len(grid[0])


def dfs(row, col):
    if (
        row < 0
        or row >= rows
        or col < 0
        or col >= cols
        or grid[row][col] != "1"
    ):
        return

    grid[row][col] = "0"

    dfs(row + 1, col)
    dfs(row - 1, col)
    dfs(row, col + 1)
    dfs(row, col - 1)
```

这里直接修改网格：

```python
grid[row][col] = "0"
```

相当于把该节点加入 `visited`。

如果题目要求保留输入，可以单独使用：

```python
visited = set()
```

## 20. Number of Islands 模式

```python
islands = 0

for row in range(rows):
    for col in range(cols):
        if grid[row][col] == "1":
            islands += 1
            dfs(row, col)
```

每遇到一个尚未访问的陆地，就发现一个新岛屿。

DFS 会把整个岛屿标记完成。

它本质上就是：

```text
二维隐式图中的连通分量计数
```

## 21. 网格 BFS 模板

```python
from collections import deque

queue = deque([(start_row, start_col)])
visited = {(start_row, start_col)}

while queue:
    row, col = queue.popleft()

    for row_change, col_change in directions:
        next_row = row + row_change
        next_col = col + col_change

        if (
            0 <= next_row < rows
            and 0 <= next_col < cols
            and (next_row, next_col) not in visited
        ):
            visited.add((next_row, next_col))
            queue.append((next_row, next_col))
```

网格最短路径、传播时间、最近距离通常使用 BFS。

## 22. Multi-source BFS / 多源 BFS

普通 BFS 从一个起点开始。

多源 BFS 把所有起点同时放入队列：

```python
queue = deque(all_starting_positions)
visited = set(all_starting_positions)
```

然后统一向外扩散。

这相当于添加一个虚拟超级起点，它到所有真实起点的距离都是 0。

典型题：

- 994. Rotting Oranges；
- 542. 01 Matrix；
- 离最近出口、最近陆地或最近零的距离。

如果分别从每个起点执行一次 BFS，会大量重复计算。

## 23. Rotting Oranges 的时间层

```python
minutes = 0

while queue and fresh_count > 0:
    for _ in range(len(queue)):
        row, col = queue.popleft()

        for next_position in neighbors:
            if 是新鲜橘子:
                标记为腐烂
                fresh_count -= 1
                queue.append(next_position)

    minutes += 1
```

每一层表示一分钟内同时发生的传播。

这里必须在入队时立即标记，否则同一个新鲜橘子可能被多个方向重复加入。

## 24. Clone Graph 为什么需要 HashMap

复制图时，每个旧节点都要对应唯一的新节点：

```text
old_node -> new_node
```

使用：

```python
old_to_new = {}
```

DFS 模板：

```python
def clone(node):
    if node in old_to_new:
        return old_to_new[node]

    copy = Node(node.val)
    old_to_new[node] = copy

    for neighbor in node.neighbors:
        copy.neighbors.append(clone(neighbor))

    return copy
```

必须先把新节点加入字典，再递归复制邻居。

否则遇到环时，会在当前节点的副本尚未登记前再次递归回来，造成无限递归。

这与 138. Copy List with Random Pointer 的：

```text
旧对象 -> 新对象
```

映射思想相同。

## 25. 无向图判环

无向图中：

```text
当前节点看到已经访问过的父节点
```

是正常现象，因为边会双向保存。

真正的环是遇到：

```text
已经访问过，并且不是当前父节点的邻居
```

模板：

```python
def has_cycle(node, parent):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor == parent:
            continue

        if neighbor in visited:
            return True

        if has_cycle(neighbor, node):
            return True

    return False
```

如果图可能不连通，需要从所有未访问节点启动检查。

## 26. 有向图判环：三种状态

有向图不能只看 `visited`。

需要区分：

```text
0：从未访问
1：正在当前递归路径中
2：已经完整处理完成
```

模板：

```python
state = [0] * n


def has_cycle(node):
    if state[node] == 1:
        return True

    if state[node] == 2:
        return False

    state[node] = 1

    for neighbor in graph[node]:
        if has_cycle(neighbor):
            return True

    state[node] = 2
    return False
```

遇到状态 1 表示：

```text
沿当前路径回到了一个尚未退出的祖先节点
```

这就是有向环。

## 27. 为什么有向图需要“当前路径”

假设两个不同分支都指向同一个已完成节点：

```text
0 -> 1 -> 3
 \-> 2 -> 3
```

第二次到达 3 不代表有环。

所以需要区分：

```text
节点 3 正在当前路径中
节点 3 已经由另一条分支处理完成
```

这就是状态 1 和状态 2 的区别。

## 28. Topological Sort / 拓扑排序

拓扑排序适用于有向无环图 DAG。

它给出一个顺序，使每条边：

```text
source -> destination
```

中的 `source` 都出现在 `destination` 前面。

典型场景：

- 课程先修关系；
- 构建依赖；
- 任务执行顺序；
- 软件包安装顺序。

如果图中存在有向环，就不存在合法拓扑顺序。

## 29. Kahn 算法：入度 BFS

步骤：

```text
1. 统计每个节点入度。
2. 把所有入度为 0 的节点加入队列。
3. 弹出节点，相当于完成它。
4. 删除它指出去的边，让邻居入度减一。
5. 邻居入度变成 0 时加入队列。
```

模板：

```python
from collections import deque

graph = [[] for _ in range(n)]
indegree = [0] * n

for source, destination in edges:
    graph[source].append(destination)
    indegree[destination] += 1

queue = deque(
    node
    for node in range(n)
    if indegree[node] == 0
)

order = []

while queue:
    node = queue.popleft()
    order.append(node)

    for neighbor in graph[node]:
        indegree[neighbor] -= 1

        if indegree[neighbor] == 0:
            queue.append(neighbor)

if len(order) != n:
    return []  # 存在环

return order
```

## 30. Course Schedule 中边的方向

如果课程 `course` 依赖 `prerequisite`：

```text
[course, prerequisite]
```

执行顺序是：

```text
prerequisite -> course
```

所以邻接表通常写：

```python
graph[prerequisite].append(course)
indegree[course] += 1
```

题目输入元组的字段顺序，不一定等于图边方向。

必须先用自然语言说清：

```text
谁完成后，谁才能开始？
```

## 31. 拓扑排序与有向环

Kahn 算法结束后：

```python
len(order) == n
```

表示所有节点都被处理，没有环。

如果：

```python
len(order) < n
```

剩余节点都处于相互依赖中，无法出现入度为 0 的节点，因此存在环。

207. Course Schedule 只问能否完成：

```python
return processed_count == num_courses
```

210. Course Schedule II 还需要返回具体顺序。

## 32. Bipartite Graph / 二分图

二分图可以把节点分成两组，使每条边的两个端点属于不同组。

可以用两种颜色进行染色：

```python
color = {}
```

DFS / BFS 时：

```text
当前节点颜色为 0
邻居必须为 1
```

如果某条边连接了同色节点，就不是二分图。

模板：

```python
from collections import deque

color = {}

for start in range(n):
    if start in color:
        continue

    color[start] = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in color:
                color[neighbor] = 1 - color[node]
                queue.append(neighbor)
            elif color[neighbor] == color[node]:
                return False

return True
```

需要遍历所有起点，因为图可能不连通。

## 33. Union-Find / 并查集

并查集适合动态维护：

```text
哪些节点属于同一个连通分量
```

主要操作：

```text
find(x)：查找 x 所属集合的代表节点
union(a, b)：合并 a 和 b 所在集合
```

典型题：

- 判断加入一条边后是否形成环；
- 统计连通分量；
- 合并账户；
- 判断两个节点是否连通；
- Kruskal 最小生成树。

## 34. 并查集基础模板

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])

        return self.parent[node]

    def union(self, node_a, node_b):
        root_a = self.find(node_a)
        root_b = self.find(node_b)

        if root_a == root_b:
            return False

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        return True
```

两个优化：

```text
路径压缩
按大小 / 按秩合并
```

使单次操作的均摊复杂度接近 O(1)。

## 35. 并查集如何检测无向环

逐条处理边：

```python
for node_a, node_b in edges:
    if not union_find.union(node_a, node_b):
        # 两个节点原本已经连通
        # 再加入这条边就形成环
        return [node_a, node_b]
```

对应经典题：

```text
684. Redundant Connection
```

DFS 也能判断连通，但并查集更适合“边不断加入”的动态过程。

## 36. 无权图最短路径

每条边代价相同，使用 BFS。

为什么？

BFS 按层扩展：

```text
第 0 层：起点
第 1 层：走 1 条边能到达
第 2 层：走 2 条边能到达
```

第一次到达目标时，经过的边数一定最少。

模板：

```python
queue = deque([(start, 0)])
visited = {start}

while queue:
    node, distance = queue.popleft()

    if node == target:
        return distance

    for neighbor in graph[node]:
        if neighbor in visited:
            continue

        visited.add(neighbor)
        queue.append((neighbor, distance + 1))
```

## 37. Dijkstra：非负权最短路径

如果边权不同，但全部非负，普通 BFS 不再保证最短。

使用：

```text
最小堆 + 当前已知最短距离
```

堆元素：

```python
(distance_from_start, node)
```

模板：

```python
import heapq

distances = {start: 0}
min_heap = [(0, start)]

while min_heap:
    distance, node = heapq.heappop(min_heap)

    if distance != distances[node]:
        continue

    for neighbor, weight in graph[node]:
        new_distance = distance + weight

        if (
            neighbor not in distances
            or new_distance < distances[neighbor]
        ):
            distances[neighbor] = new_distance
            heapq.heappush(
                min_heap,
                (new_distance, neighbor),
            )
```

这一部分是 Heap 与 Graph 的结合。

先知道结构即可，等基础 DFS/BFS、拓扑排序完成后再深入。

## 38. 为什么 Dijkstra 要跳过过期堆元素

`heapq` 不支持直接修改堆中旧距离。

发现更短路径时，会把新记录再次放入堆：

```text
(10, node)
(6, node)
```

当旧的 `(10, node)` 后来弹出时，字典中已经记录：

```text
distances[node] = 6
```

所以：

```python
if distance != distances[node]:
    continue
```

跳过过期状态。

这叫 lazy deletion / 懒删除思想。

## 39. 有负权边怎么办

Dijkstra 依赖：

```text
已经取出的最短距离不会再被负权边降低
```

所以它不能直接处理负权边。

存在负权边时，可能需要：

- Bellman-Ford；
- SPFA；
- Floyd-Warshall；
- DAG 最短路。

这些属于后续 Advanced Graph 内容，入门阶段先不展开。

## 40. Minimum Spanning Tree / 最小生成树

最小生成树要求：

```text
连接全部节点
不形成环
总边权最小
```

经典算法：

- Kruskal：排序边 + Union-Find；
- Prim：最小堆逐步扩展节点。

它与最短路径不同：

```text
最短路径：从一个起点到其他节点距离最小
最小生成树：连接整张图的总成本最小
```

这部分也可以等基础 Graph 完成后再学。

## 41. 图遍历的复杂度

使用邻接表时：

```text
DFS：O(V + E)
BFS：O(V + E)
```

原因：

- 每个节点最多进入一次；
- 每条边最多检查常数次。

空间：

```text
邻接表：O(V + E)
visited：O(V)
递归栈或队列：O(V)
```

网格图中：

```text
V = rows * cols
```

每个格子最多访问一次，所以常见复杂度为：

```text
O(rows * cols)
```

## 42. 邻接矩阵的复杂度

邻接矩阵扫描某节点所有潜在邻居需要 O(V)。

访问所有节点时总成本可能是：

```text
O(V^2)
```

即使实际边很少，也必须扫描矩阵中的 0。

所以稀疏图优先使用邻接表。

## 43. Graph 中 `visited` 的不同含义

不要把所有题的 `visited` 当成同一件事。

### 普通可达性

```text
visited = 已经处理过，不再重复访问
```

### 有向环

需要：

```text
visiting = 当前递归路径中
visited = 已经完整处理
```

### Dijkstra

距离字典保存当前最短候选，可能有过期堆记录。

### Backtracking 路径

```text
visited = 当前路径正在使用
```

递归返回后可能需要撤销。

做题前必须用一句话定义：

```text
visited 中的节点为什么以后不需要再次处理？
```

## 44. Graph DFS 与 Backtracking 的区别

这是你当前最需要分清的地方。

### 基础 Graph DFS

目标通常是：

```text
访问所有可达节点
```

节点一旦访问过，永久加入：

```python
visited.add(node)
```

通常不撤销。

### Backtracking

目标通常是：

```text
枚举所有可能路径或方案
```

节点或选择可能在其他路径中再次使用，所以：

```python
visited.add(node)
backtrack(...)
visited.remove(node)
```

是否恢复不由“DFS”决定，而由状态语义决定。

可以先学 Graph，因为前几类题的 `visited` 大多是永久标记，比 Backtracking 的路径状态更直观。

## 45. 常见错误

### 无向边只添加一个方向

导致从反方向无法到达。

### 有向边错误添加成双向

改变了原图含义，可能凭空制造环。

### 忘记 `visited`

遇到环时无限循环或递归。

### BFS 出队时才标记

同一节点可能被重复入队。

### 只从节点 0 开始

无法处理不连通图中的其他分量。

### 网格越界条件不完整

必须同时检查行、列上下界。

### 修改网格后忘记题目是否允许

如果后续仍需要原网格，应使用独立 `visited` 或恢复状态。

### 把 BFS 层数多加或少加一

先明确：

```text
distance 表示当前层，还是下一层？
```

### Course Schedule 建反边

先修课程应该指向后续课程。

### 无向图看到父节点就认为有环

双向边必然会返回父节点，需要单独跳过。

### 有向图只使用一个 visited 集合判环

无法区分当前路径节点和已经完成节点。

### Dijkstra 用于负权图

算法前提不成立。

### 递归深度过大

长链图可能触发 Python `RecursionError`，可改用显式栈或 BFS。

## 46. 调试图题的方法

### 先打印邻接表

```python
for node, neighbors in enumerate(graph):
    print(node, "->", neighbors)
```

确认：

- 方向是否正确；
- 无向边是否添加两次；
- 孤立节点是否存在。

### 打印访问过程

```python
print("visit", node)
```

### BFS 打印层

```python
print("distance", distance, "queue", list(queue))
```

### Topological Sort 打印入度

```python
print(indegree)
```

### 网格题画坐标

固定使用：

```text
row 向下增加
col 向右增加
```

不要混淆 `grid[row][col]`。

## 47. 必背模板一：邻接表

```python
graph = [[] for _ in range(n)]

for node_a, node_b in edges:
    graph[node_a].append(node_b)
    graph[node_b].append(node_a)
```

## 48. 必背模板二：DFS

```python
visited = set()


def dfs(node):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor)
```

## 49. 必背模板三：BFS

```python
from collections import deque

queue = deque([start])
visited = {start}

while queue:
    node = queue.popleft()

    for neighbor in graph[node]:
        if neighbor in visited:
            continue

        visited.add(neighbor)
        queue.append(neighbor)
```

## 50. 必背模板四：网格方向

```python
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

for row_change, col_change in directions:
    next_row = row + row_change
    next_col = col + col_change

    if (
        0 <= next_row < rows
        and 0 <= next_col < cols
    ):
        ...
```

## 51. 必背模板五：多源 BFS

```python
queue = deque()

for row in range(rows):
    for col in range(cols):
        if 是起点:
            queue.append((row, col))
            标记已访问

distance = 0

while queue:
    for _ in range(len(queue)):
        row, col = queue.popleft()
        扩展邻居

    distance += 1
```

## 52. 必背模板六：Kahn 拓扑排序

```python
queue = deque(
    node
    for node in range(n)
    if indegree[node] == 0
)

processed = 0

while queue:
    node = queue.popleft()
    processed += 1

    for neighbor in graph[node]:
        indegree[neighbor] -= 1

        if indegree[neighbor] == 0:
            queue.append(neighbor)

return processed == n
```

## 53. 推荐刷题顺序

| 顺序 | 题号 | 题目 | 重点 |
| --- | --- | --- | --- |
| 1 | 463 | Island Perimeter | 网格关系、四方向边界 |
| 2 | 953 | Verifying an Alien Dictionary | 字典序规则、269 前置 |
| 3 | 1971 | Find if Path Exists in Graph | 邻接表、visited、基础 DFS/BFS |
| 4 | 733 | Flood Fill | 网格 DFS |
| 5 | 200 | Number of Islands | 连通分量 |
| 6 | 695 | Max Area of Island | DFS 返回或累计区域大小 |
| 7 | 133 | Clone Graph | 旧节点到新节点的 HashMap |
| 8 | 994 | Rotting Oranges | 多源 BFS、层数 |
| 9 | 130 | Surrounded Regions | 从边界反向标记 |
| 10 | 417 | Pacific Atlantic Water Flow | 反向搜索、多起点 |
| 11 | 207 | Course Schedule | 有向环、拓扑排序 |
| 12 | 210 | Course Schedule II | 返回拓扑顺序 |
| 13 | 785 | Is Graph Bipartite? | BFS / DFS 染色 |
| 14 | 684 | Redundant Connection | Union-Find 判环 |
| 15 | 127 | Word Ladder | 隐式图、最短路径 BFS |
| 16 | 743 | Network Delay Time | Dijkstra + Heap |

建议先完成前 8 题，再进入有向图和并查集。

743 属于加权图，可以放在最后。

## 54. 分阶段学习目标

### 第一阶段：图的表示和遍历

完成：

- 463；
- 953；
- 1971；
- 733；
- 200；
- 695。

需要掌握：

```text
邻接表
visited
DFS
BFS
网格隐式图
连通分量
```

### 第二阶段：图的复制与扩散

完成：

- 133；
- 994；
- 130；
- 417。

需要掌握：

```text
old -> new 映射
多源 BFS
边界反向搜索
从目标反向出发
```

### 第三阶段：有向图

完成：

- 207；
- 210；
- 785。

需要掌握：

```text
入度
拓扑排序
有向环
染色
```

### 第四阶段：高级连接结构

完成：

- 684；
- 127；
- 743。

需要掌握：

```text
Union-Find
隐式状态图
最短路径
Dijkstra
```

## 55. 当前阶段最重要的结论

刚进入 Graph 时，不要急着学习全部高级算法。

先固定掌握：

```text
1. 根据 edges 建 adjacency list。
2. 进入节点时标记 visited。
3. 可达性和连通分量使用 DFS / BFS。
4. 无权最短距离和扩散时间使用 BFS。
5. 网格可以直接视为隐式图。
6. 图不一定连通，需要检查所有起点。
```

最核心的条件反射：

```text
节点之间存在关系或状态转移
-> 抽象成 Graph

访问所有可达状态
-> DFS / BFS + visited

无权最短步数或同时扩散
-> BFS
```

## 56. 最后总结

Graph 入门不是从陌生算法重新开始，而是把 Tree 的 DFS/BFS 推广到更一般的连接关系。

树中默认成立的条件，在图中必须显式处理：

```text
树通常有根       -> 图可能没有固定起点
树通常连通       -> 图可能有多个连通分量
树通常无环       -> 图必须使用 visited
树到节点路径唯一 -> 图可能有多条路径
```

看到图题先回答：

```text
节点是什么？
边是什么？
有向还是无向？
有权还是无权？
题目问可达、连通、最短、环还是顺序？
visited 应该表示什么？
```

基础图题的核心模板是：

```text
建图
选择 DFS 或 BFS
维护 visited
处理所有必要起点
```
