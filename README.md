# LeetCode

这个仓库按题型路线整理 LeetCode 题解和学习笔记。先按目录顺序刷，不需要随机挑题。

## 刷题路线

```text
leetcode/
  README.md
  arrays-hashing/
  strings/
  two-pointers/
  sorting/
  prefix-sum/
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
4. sorting
5. prefix-sum
6. sliding-window
7. stack
8. binary-search
9. linked-list
10. trees
11. heap-priority-queue
12. backtracking
13. graphs
14. dynamic-programming

## 当前进度

| 顺序 | 题型 | 题号 | 题目 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | arrays-hashing | 217 | Contains Duplicate | 已添加 |
| 2 | arrays-hashing | 242 | Valid Anagram | 已添加 |
| 3 | arrays-hashing | 1 | Two Sum | 已添加 |
| 4 | arrays-hashing | 49 | Group Anagrams | 已添加 |
| 5 | arrays-hashing | 169 | Majority Element | 已添加 |
| 6 | arrays-hashing | 705 | Design HashSet | 已添加 |
| 7 | arrays-hashing | 706 | Design HashMap | 已添加 |
| 8 | strings | 14 | Longest Common Prefix | 已添加 |
| 9 | two-pointers | 27 | Remove Element | 已添加 |
| 10 | two-pointers | 75 | Sort Colors | 已添加 |
| 11 | sorting | 912 | Sort an Array | 已添加 |
| 12 | strings | 271 | Encode and Decode Strings | 已添加 |
| 13 | prefix-sum | 304 | Range Sum Query 2D - Immutable | 已添加 |
| 14 | prefix-sum | 238 | Product of Array Except Self | 已添加 |
| 15 | arrays-hashing | 36 | Valid Sudoku | 已添加 |
| 16 | arrays-hashing | 128 | Longest Consecutive Sequence | 已添加 |
| 17 | arrays-hashing | 121 | Best Time to Buy and Sell Stock | 已添加 |
| 18 | arrays-hashing | 122 | Best Time to Buy and Sell Stock II | 已添加 |
| 19 | prefix-sum | 560 | Subarray Sum Equals K | 已添加 |
| 20 | arrays-hashing | 41 | First Missing Positive | 已添加 |
| 21 | two-pointers | 344 | Reverse String | 已添加 |
| 22 | two-pointers | 125 | Valid Palindrome | 已添加 |
| 23 | two-pointers | 680 | Valid Palindrome II | 已添加 |
| 24 | two-pointers | 1768 | Merge Strings Alternately | 已添加 |
| 25 | two-pointers | 88 | Merge Sorted Array | 已添加 |
| 26 | two-pointers | 26 | Remove Duplicates from Sorted Array | 已添加 |
| 27 | two-pointers | 167 | Two Sum II - Input Array Is Sorted | 已添加 |
| 28 | two-pointers | 15 | 3Sum | 已添加 |
| 29 | two-pointers | 18 | 4Sum | 已添加 |
| 30 | two-pointers | 881 | Boats to Save People | 已添加 |
| 31 | two-pointers | 11 | Container With Most Water | 已添加 |
| 32 | two-pointers | 42 | Trapping Rain Water | 已添加 |
| 33 | stack | 682 | Baseball Game | 已添加 |

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
