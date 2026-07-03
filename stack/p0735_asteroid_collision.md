# 735. Asteroid Collision

## 题目

给定一个数组 `asteroids`，每个数字表示一个小行星：

- 正数：向右移动
- 负数：向左移动
- 绝对值：小行星大小

当两个小行星相撞时：

- 小的会爆炸
- 一样大则两个都爆炸
- 没有相撞的小行星会保留下来

要求返回最终剩下的小行星。

## 思路

这题适合用栈保存已经处理过、还可能继续存在的小行星。

遍历当前小行星 `asteroid` 时，只需要考虑它会不会和栈顶发生碰撞。

因为栈顶是距离当前小行星最近的左侧小行星。

如果当前小行星能撞到左边的某个小行星，它一定先撞到栈顶。

## 只有一种方向会碰撞

这题最容易错的地方是：不是异号就会碰撞。

只有这一种情况会碰撞：

```python
stack[-1] > 0 and asteroid < 0
```

也就是：

```text
左边的小行星向右走，当前小行星向左走
```

它们才会面对面相撞。

其他异号情况不会相撞。

例如：

```text
[-2, 1]
```

左边 `-2` 向左走，右边 `1` 向右走，它们越走越远，不会碰撞。

再比如：

```text
[-2, -1, 1, 2]
```

所有小行星都不会相撞。

## 为什么要用 `while`

当前小行星可能连续撞碎多个栈顶小行星。

例如：

```text
[10, 2, -5]
```

处理 `-5` 时：

1. 先和 `2` 撞，`2` 爆炸。
2. `-5` 还活着，还要继续和新的栈顶 `10` 判断。
3. 最后 `-5` 被 `10` 撞碎。

所以这里不能只用 `if` 判断一次，而要用 `while`。

循环条件是：

```python
while stack and stack[-1] > 0 and asteroid < 0:
```

含义是：

```text
只要栈里还有可能和当前小行星碰撞的向右小行星，就继续处理。
```

## 三种碰撞结果

当 `stack[-1] > 0 and asteroid < 0` 时，比较大小。

### 1. 当前小行星更大

```python
if abs(asteroid) > abs(stack[-1]):
    stack.pop()
```

栈顶小行星爆炸，当前小行星还活着，所以继续 `while`。

### 2. 两个一样大

```python
elif abs(asteroid) == abs(stack[-1]):
    stack.pop()
    alive = False
    break
```

两个都爆炸。

当前小行星也没了，所以 `alive = False`，并退出循环。

### 3. 栈顶小行星更大

```python
else:
    alive = False
    break
```

当前小行星爆炸，栈顶保留。

## `alive` 的作用

`alive` 表示当前小行星最后是否还存在。

如果当前小行星在碰撞中爆炸，就不能再入栈。

如果 `while` 结束后它还活着，说明：

- 它没有发生碰撞
- 或者它撞碎了所有会和它碰撞的小行星

这时才可以入栈：

```python
if alive:
    stack.append(asteroid)
```

## 代码

```python
class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack: list[int] = []

        for asteroid in asteroids:
            alive = True

            while stack and stack[-1] > 0 and asteroid < 0:
                if abs(asteroid) > abs(stack[-1]):
                    stack.pop()
                elif abs(asteroid) == abs(stack[-1]):
                    stack.pop()
                    alive = False
                    break
                else:
                    alive = False
                    break

            if alive:
                stack.append(asteroid)

        return stack
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

虽然里面有 `while`，但每个小行星最多入栈一次、出栈一次，所以总时间复杂度仍然是 O(n)。

## 心得

1. 不是异号就会碰撞，只有左边向右、当前向左时才会碰撞。
2. 也就是只有 `stack[-1] > 0 and asteroid < 0` 这一种朝向需要处理。
3. 当前小行星可能连续撞碎多个栈顶小行星，所以这里要用 `while`。
4. `alive` 用来记录当前小行星最后还能不能入栈。
5. 看到“和最近的前一个元素反复发生关系”，可以考虑栈。
