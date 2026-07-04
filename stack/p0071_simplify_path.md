# 71. Simplify Path

## 题目

给定一个 Unix 风格的绝对路径 `path`，把它简化成规范路径。

规则：

- `.` 表示当前目录，可以忽略。
- `..` 表示返回上一级目录。
- 多个连续 `/` 等价于一个 `/`。
- 最终路径必须以 `/` 开头。

## 思路

这题适合用栈模拟路径变化。

先用 `/` 切分路径：

```python
parts = path.split("/")
```

然后逐段处理：

1. 如果是普通目录名，入栈。
2. 如果是 `..`，表示回到上一级目录，栈非空时出栈。
3. 如果是 `.` 或空字符串，直接跳过。

最后用 `/` 把栈里的目录重新拼起来。

## 为什么用栈

路径里的 `..` 表示撤销最近进入的目录。

例如：

```text
/home/user/Documents/../Pictures
```

进入顺序是：

```text
home -> user -> Documents
```

遇到 `..` 时，要删除最近进入的 `Documents`。

这正好符合栈的后进先出：

```python
stack.pop()
```

## `split("/")` 会产生空字符串

例如：

```python
"/home//foo/".split("/")
```

会得到类似：

```python
["", "home", "", "foo", ""]
```

这些空字符串来自：

- 开头的 `/`
- 连续的 `//`
- 结尾的 `/`

所以遇到空字符串时要跳过。

## 代码

```python
class Solution:
    def simplifyPath(self, path: str) -> str:
        stack: list[str] = []

        for part in path.split("/"):
            if part == "..":
                if stack:
                    stack.pop()
            elif part == "." or part == "":
                continue
            else:
                stack.append(part)

        return "/" + "/".join(stack)
```

## 复杂度

- 时间复杂度：O(n)
- 空间复杂度：O(n)

其中 `n` 是路径字符串长度。

## 心得

1. 路径里的 `..` 本质是撤销最近进入的目录，所以可以想到栈。
2. `path.split("/")` 会产生空字符串，遇到空字符串要跳过。
3. `.` 表示当前目录，也可以跳过。
4. 最后用 `"/".join(stack)` 拼回路径，再在前面补一个 `/`。
