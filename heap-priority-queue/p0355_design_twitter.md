# 355. Design Twitter

## 题目

这道题不是只实现一个函数，而是设计一个简化版 Twitter 类。LeetCode 会按顺序调用对象的方法，检查系统状态是否一直正确。

需要实现四个功能：

| 方法 | 作用 |
| --- | --- |
| `postTweet(userId, tweetId)` | 用户发布一条推文 |
| `getNewsFeed(userId)` | 返回该用户能看到的最新 10 条推文 ID |
| `follow(followerId, followeeId)` | 前者关注后者 |
| `unfollow(followerId, followeeId)` | 前者取消关注后者 |

## 四个方法的准确含义

### 发布推文

```python
postTweet(userId, tweetId)
```

需要记录：

- 推文由哪个用户发布；
- 推文 ID；
- 推文发布的先后顺序。

题目保证每个 `tweetId` 唯一。

### 获取新闻流

```python
getNewsFeed(userId)
```

用户能看到：

```text
自己的推文
+
当前关注用户的推文
```

返回值必须满足：

- 只返回推文 ID；
- 按发布时间从新到旧；
- 最多返回 10 条。

### 关注

```python
follow(followerId, followeeId)
```

方向是：

```text
followerId 关注 followeeId
```

关注关系是单向的，不能把两个参数的含义弄反。

### 取消关注

```python
unfollow(followerId, followeeId)
```

取消关注不会删除 `followeeId` 已发布的推文，只会使 `followerId` 的新闻流不再包含这些推文。

取消一个原本没有关注的用户不应报错。

## 需要永久维护的状态

系统需要长期保存三类状态：

```python
self.time = 0
self.tweets = {}
self.following = {}
```

### 每个用户的推文列表

```text
userId -> [(timestamp, tweetId), ...]
```

例如：

```python
self.tweets[1] = [
    (0, 101),
    (3, 102),
]
```

推文按发布顺序不断 `append`，所以每个用户的列表天然按照时间从旧到新排列。

### 每个用户的关注集合

```text
followerId -> {followeeId, ...}
```

集合比列表更合适，因为：

- 重复关注不会产生重复记录；
- 添加平均 O(1)；
- `discard` 取消不存在的关注也不会报错。

### 全局逻辑时间

`self.time` 不是现实世界中的日期时间，而是全局递增的发布序号。

```python
self.tweets[userId].append((self.time, tweetId))
self.time += 1
```

它只负责表达：

```text
哪条推文更早，哪条推文更新
```

不需要使用 `time.time()`。整数计数器更稳定，也保证每条推文的时间戳唯一。

## 为什么每个用户使用列表，而不是永久维护堆

每个用户的推文是按时间依次发布的，所以列表通过 `append` 已经保持顺序。

新闻流需要合并的是：

```text
自己和多个关注用户的推文列表
```

而不是只查某一个用户的最新推文。因此更合适的设计是：

```text
永久保存：每个用户的有序推文列表
查询新闻流：临时建立一个合并候选堆
```

如果为每个用户永久维护新闻流堆，那么某个用户每次发推时，都可能需要同步更新所有关注者的堆；取消关注时还要删除历史候选，维护成本很高。

## `getNewsFeed` 的本质：K 路归并

假设用户 1 能看到用户 1、2、3 的推文：

```text
tweets[1]: 一条按时间有序的序列
tweets[2]: 一条按时间有序的序列
tweets[3]: 一条按时间有序的序列
```

现在需要从这些有序序列中找出全局最新的 10 条。

这就是 K 路归并：

```text
每个序列先提供一个当前候选
弹出全局最优候选后
只让它所属的序列提供下一个候选
```

因为每个用户的列表从旧到新排列，所以初始候选是该用户列表的最后一条推文。

## 堆元素为什么保存四个值

Python 的堆元素可以是元组：

```python
(-timestamp, tweet_id, user_id, index)
```

各字段含义：

| 字段 | 作用 |
| --- | --- |
| `-timestamp` | 让发布时间越新的推文越先弹出 |
| `tweet_id` | 弹出后加入答案 |
| `user_id` | 确定推文来自哪个用户 |
| `index` | 定位该用户列表中的上一条推文 |

元组会优先比较第一个字段。因为逻辑时间戳唯一，正常情况下不会继续依赖后续字段决定顺序；后续字段主要用于保存状态。

## 为什么时间要取负数

`heapq` 是最小堆，但 `self.time` 越大表示推文越新。

例如：

```text
旧推文：timestamp = 2  -> -2
新推文：timestamp = 8  -> -8
```

最小堆会先弹出 `-8`，因此实现最新推文优先。

## 初始化候选堆

先复制关注集合，再把用户自己加入可见范围：

```python
visible_users = set(self.following.get(userId, set()))
visible_users.add(userId)
```

这里外层 `set(...)` 会创建一个集合副本。

```python
set({2, 3})
```

完全合法，并会得到一个新的 `{2, 3}`。所以向 `visible_users` 加入自己，不会永久修改 `self.following[userId]`。

然后每个可见用户只放入最新一条推文：

```python
for visible_user in visible_users:
    user_tweets = self.tweets.get(visible_user, [])

    if user_tweets:
        index = len(user_tweets) - 1
        timestamp, tweet_id = user_tweets[index]
        heapq.heappush(
            max_heap,
            (-timestamp, tweet_id, visible_user, index),
        )
```

使用 `.get(visible_user, [])` 可以处理某个被关注用户还没有发布过推文的情况。

## 弹出一条，再补入同一用户的上一条

每次弹出全局最新候选：

```python
_, tweet_id, author_id, index = heapq.heappop(max_heap)
news_feed.append(tweet_id)
```

然后只检查这条推文所属用户是否还有更早的推文：

```python
previous_index = index - 1

if previous_index >= 0:
    timestamp, previous_tweet_id = self.tweets[author_id][previous_index]
    heapq.heappush(
        max_heap,
        (-timestamp, previous_tweet_id, author_id, previous_index),
    )
```

这样堆中始终最多只有每个可见用户的一条候选，不需要把所有历史推文都压入堆。

## 执行示例

假设：

```python
tweets[1] = [(1, 101), (8, 102)]
tweets[2] = [(3, 201), (10, 202)]
tweets[3] = [(6, 301)]
```

初始只加入每个用户的最新推文：

```text
用户 1：102，时间 8
用户 2：202，时间 10
用户 3：301，时间 6
```

第一次弹出 202，再加入用户 2 的上一条 201。

第二次弹出 102，再加入用户 1 的上一条 101。

候选始终只在三个有序推文序列的当前位置之间竞争。

## 完整代码

```python
import heapq


class Twitter(object):
    def __init__(self):
        self.time = 0
        self.tweets = {}
        self.following = {}

    def postTweet(self, userId, tweetId):
        if userId not in self.tweets:
            self.tweets[userId] = []

        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId):
        visible_users = set(self.following.get(userId, set()))
        visible_users.add(userId)

        max_heap = []

        for visible_user in visible_users:
            user_tweets = self.tweets.get(visible_user, [])

            if user_tweets:
                index = len(user_tweets) - 1
                timestamp, tweet_id = user_tweets[index]
                heapq.heappush(
                    max_heap,
                    (-timestamp, tweet_id, visible_user, index),
                )

        news_feed = []

        while max_heap and len(news_feed) < 10:
            _, tweet_id, author_id, index = heapq.heappop(max_heap)
            news_feed.append(tweet_id)

            previous_index = index - 1

            if previous_index >= 0:
                timestamp, previous_tweet_id = self.tweets[author_id][previous_index]
                heapq.heappush(
                    max_heap,
                    (-timestamp, previous_tweet_id, author_id, previous_index),
                )

        return news_feed

    def follow(self, followerId, followeeId):
        if followerId == followeeId:
            return

        if followerId not in self.following:
            self.following[followerId] = set()

        self.following[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        if followerId in self.following:
            self.following[followerId].discard(followeeId)
```

## 复杂度

设用户当前能看到 `f` 个用户的推文，包括自己。

### `postTweet`

- 时间复杂度：O(1)
- 额外空间复杂度：O(1)

所有已发布推文总共占用 O(number_of_tweets) 空间。

### `follow` / `unfollow`

- 平均时间复杂度：O(1)

集合的添加与删除平均为常数时间。

### `getNewsFeed`

- 建立候选堆：O(f log f)
- 最多弹出并补入 10 次：O(10 log f)
- 临时堆空间：O(f)

由于最终只取 10 条，查询不会遍历所有历史推文。

## 原实现中的关键问题

### 关注字典的键不一定存在

```python
self.following[userId]
```

如果用户从未关注任何人，会触发 `KeyError`。应使用：

```python
self.following.get(userId, set())
```

### 集合没有 `append`

关注关系使用的是集合，应通过 `add` 添加元素。

### 直接引用会修改原关注集合

```python
all_list = self.following[userId]
all_list.add(userId)
```

两个变量指向同一个集合，会把用户自己永久写入关注关系。应先复制集合。

### `index > 0` 会漏掉索引 0

只有一条推文时：

```text
index = 0
```

它仍然是有效候选。应直接判断 `if user_tweets`，或者检查 `index >= 0`。

### 正时间最小堆会先弹出最旧推文

要让最新推文优先，需要存入 `-timestamp`。

### 过早只取了 `tweetId`

```python
tweet = heapq.heappop(heap)[1]
```

此时 `tweet` 已经是一个整数，不能再用 `tweet[2]`、`tweet[3]` 获取用户与索引。

应该先解包整个元组：

```python
_, tweet_id, author_id, index = heapq.heappop(heap)
```

### 答案应只加入推文 ID

`getNewsFeed` 返回的是：

```text
[tweetId, tweetId, ...]
```

不是包含时间和用户信息的元组列表。

### 不要把所有历史推文都压入堆

每个用户的推文列表已经有序。只放每个用户当前最新的一条，弹出后再补该用户的上一条，能够避免无意义地处理大量历史数据。

## 心得

1. 设计题要先明确哪些数据是永久状态，哪些数据只在一次查询中临时使用。
2. 每个用户永久维护按发布时间追加的推文列表，不需要永久维护一个堆。
3. 关注关系适合使用“字典套集合”，避免重复关注并方便取消关注。
4. 逻辑时间只需表达发布先后，不需要使用真实时间库。
5. `getNewsFeed` 的本质是合并多个有序推文列表，并只取最新 10 条。
6. K 路归并时，堆中每个来源只保留一个当前候选；弹出后只补充同一来源的下一个候选。
7. 堆元组可以携带多个状态字段；第一个字段负责优先级，其余字段负责定位下一步。
8. 从字典中的集合创建副本后再添加自己，避免查询操作意外修改关注关系。
