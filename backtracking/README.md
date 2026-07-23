# Backtracking

这个专题练习把问题表示成决策树，通过“选择、递归、撤销”枚举所有合法方案。

## 基础笔记

- [Backtracking / 回溯基础](../notes/backtracking_basics.md)

## 当前状态

专题基础资料已经完成，题目将从 78. Subsets 开始依次添加。

## 推荐路线

| 顺序 | 题号 | 题目 | 重点 |
| --- | --- | --- | --- |
| 1 | 78 | Subsets | `start`、每个决策树节点都是答案 |
| 2 | 77 | Combinations | 固定长度与数量剪枝 |
| 3 | 46 | Permutations | `used` 数组 |
| 4 | 17 | Letter Combinations of a Phone Number | 每层候选来自字符映射 |
| 5 | 39 | Combination Sum | `remaining` 与元素复用 |
| 6 | 22 | Generate Parentheses | 构造过程保持合法 |
| 7 | 131 | Palindrome Partitioning | 字符串切割 |
| 8 | 79 | Word Search | 棋盘标记与恢复 |
| 9 | 90 | Subsets II | 排序与同层去重 |
| 10 | 40 | Combination Sum II | 不复用与同层去重 |
| 11 | 47 | Permutations II | `used` 与排列去重 |
| 12 | 51 | N-Queens | 多约束集合与棋盘恢复 |

## 核心原则

```text
回溯 = 枚举选择 + 约束剪枝 + 递归深入 + 恢复现场

组合 / 子集：通常使用 start
排列：通常使用 used
目标和：通常增加 remaining
棋盘：标记当前位置，递归结束后恢复
```

## 通用模板

```python
def backtrack(state):
    if 满足结束条件:
        保存当前结果
        return

    for choice in 当前候选:
        if choice 不合法:
            continue

        做选择
        backtrack(下一层状态)
        撤销选择
```

开始每道题前，先回答：

```text
path 表示什么？
当前有哪些候选？
什么选择不合法？
什么时候收集答案？
递归返回时恢复什么？
```
