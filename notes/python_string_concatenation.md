# Python 字符串拼接

## 核心结论

刷题里如果需要在循环中构造字符串，优先使用：

```python
parts = []
parts.append(ch)
result = "".join(parts)
```

原因是 Python 字符串是不可变对象，频繁用 `+=` 拼接字符串时，可能会反复创建新字符串。

## 1. 用 `+`

适合少量字符串拼接。

```python
a = "hello"
b = "world"

s = a + b
print(s)  # "helloworld"
```

如果需要加空格：

```python
s = a + " " + b
print(s)  # "hello world"
```

这种写法直观，但不适合在大量循环里反复使用。

## 2. 用 `+=`

适合很简单的累加。

```python
s = ""

for ch in "abc":
    s += ch

print(s)  # "abc"
```

但大量循环里不优先推荐。

因为字符串不可变，`s += ch` 看起来像是在原字符串后面追加，实际通常是创建了一个新字符串，再让 `s` 指向它。

## 3. 用 `"".join(list)`

刷题里最推荐，尤其适合循环中拼接很多字符。

```python
chars = []

for ch in "abc":
    chars.append(ch)

s = "".join(chars)
print(s)  # "abc"
```

如果想用逗号连接：

```python
words = ["a", "b", "c"]
s = ",".join(words)

print(s)  # "a,b,c"
```

如果想用空格连接：

```python
words = ["hello", "world"]
s = " ".join(words)

print(s)  # "hello world"
```

## 4. 用 f-string

适合把变量嵌入字符串。

```python
name = "Tom"
age = 18

s = f"My name is {name}, I am {age} years old."
```

f-string 更适合格式化输出，不是循环构造字符串的主要工具。

## `join` 的正确理解

`join` 的语义是：

```python
separator.join(iterable)
```

调用 `join` 的字符串是“分隔符”，不是“被追加的目标字符串”。

例如：

```python
res = "abc"
answer = res.join(["x", "y"])

print(answer)
```

结果是：

```text
xabcy
```

不是：

```text
abcxy
```

因为这里的 `res` 是分隔符，相当于把 `"abc"` 放在 `"x"` 和 `"y"` 中间。

## 为什么 `res.join(...)` 没有拼接上

这类写法容易错：

```python
res.join(word2[index:])
```

有两个问题：

1. `res` 不是被追加的目标字符串，而是分隔符。
2. 字符串不可变，`join` 会返回新字符串，不会原地修改 `res`。

如果没有把结果重新赋值，生成的新字符串会被直接丢掉。

例如：

```python
res = "abc"
res.join(["x", "y"])

print(res)  # "abc"
```

如果真要接到末尾，可以写：

```python
res = res + word2[index:]
```

或者：

```python
res += word2[index:]
```

但刷题里循环构造字符串时，更推荐：

```python
parts = []
parts.append(word1[index1])
parts.append(word2[index2])
result = "".join(parts)
```

## 常见刷题模板

### 清洗字符串

```python
s = "A man, a plan!"
chars = []

for ch in s:
    if ch.isalnum():
        chars.append(ch.lower())

cleaned = "".join(chars)
```

### 交替合并字符串

```python
parts = []

parts.append(word1[index1])
parts.append(word2[index2])

answer = "".join(parts)
```

## 总结

- 少量拼接：用 `+`。
- 简单变量嵌入：用 f-string。
- 循环构造字符串：用 `list.append(...)` 加 `"".join(...)`。
- `join` 的调用者是分隔符，不是被追加的目标字符串。
- 字符串不可变，拼接方法通常会返回新字符串，不会原地修改原字符串。
