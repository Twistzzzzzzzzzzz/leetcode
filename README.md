# LeetCode

这个仓库按题型路线整理 LeetCode 题解和学习笔记。先按目录顺序刷，不需要随机挑题。

## 刷题路线

```text
leetcode/
  README.md
  arrays-hashing/
  strings/
  two-pointers/
  sliding-window/
  stack/
  binary-search/
  linked-list/
  trees/
  heap-priority-queue/
  backtracking/
  graphs/
  dynamic-programming/
  notes/
```

推荐顺序：

1. arrays-hashing
2. strings
3. two-pointers
4. sliding-window
5. stack
6. binary-search
7. linked-list
8. trees
9. heap-priority-queue
10. backtracking
11. graphs
12. dynamic-programming

## 当前进度

| 顺序 | 题型 | 题号 | 题目 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | arrays-hashing | 217 | Contains Duplicate | 已添加 |
| 2 | arrays-hashing | 242 | Valid Anagram | 已添加 |
| 3 | arrays-hashing | 1 | Two Sum | 已添加 |
| 4 | arrays-hashing | 49 | Group Anagrams | 已添加 |
| 5 | strings | 14 | Longest Common Prefix | 已添加 |

## 文件命名

每道题建议整理成两份文件：

```text
p题号_英文题目.py   # 代码
p题号_英文题目.md   # 思路和心得
```

例如：

```text
arrays-hashing/p0001_two_sum.py
arrays-hashing/p0217_contains_duplicate.md
```

## 每题记录

每道题的思路和心得建议写在同名 `.md` 笔记里，`.py` 文件主要保留可运行代码。

笔记里建议至少写清楚：

- 题目在考什么
- 自己的解题思路
- 时间复杂度
- 空间复杂度
- 容易错的地方

## Python 运行

进入仓库后，可以直接运行某个题解文件里的示例：

```powershell
cd "C:\Users\Twistzz\Desktop\Files\学习\Graduate\leetcode"
python arrays-hashing/p0001_two_sum.py
```
