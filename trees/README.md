# Trees

这个专题练习树结构，以二叉树为主，包括深度优先搜索、层序遍历、路径回溯、二叉搜索树和分治构造树。

## 基础笔记

- [树基础](../notes/tree_basics.md)
- [Trie 前缀树基础](../notes/trie_basics.md)

## 题目顺序

| 顺序 | 题号 | 题目 | 代码 | 笔记 |
| --- | --- | --- | --- | --- |
| 1 | 94 | Binary Tree Inorder Traversal | `p0094_binary_tree_inorder_traversal.py` | `p0094_binary_tree_inorder_traversal.md` |
| 2 | 144 | Binary Tree Preorder Traversal | `p0144_binary_tree_preorder_traversal.py` | `p0144_binary_tree_preorder_traversal.md` |
| 3 | 145 | Binary Tree Postorder Traversal | `p0145_binary_tree_postorder_traversal.py` | `p0145_binary_tree_postorder_traversal.md` |
| 4 | 226 | Invert Binary Tree | `p0226_invert_binary_tree.py` | `p0226_invert_binary_tree.md` |
| 5 | 104 | Maximum Depth of Binary Tree | `p0104_maximum_depth_of_binary_tree.py` | `p0104_maximum_depth_of_binary_tree.md` |
| 6 | 543 | Diameter of Binary Tree | `p0543_diameter_of_binary_tree.py` | `p0543_diameter_of_binary_tree.md` |
| 7 | 110 | Balanced Binary Tree | `p0110_balanced_binary_tree.py` | `p0110_balanced_binary_tree.md` |
| 8 | 100 | Same Tree | `p0100_same_tree.py` | `p0100_same_tree.md` |
| 9 | 572 | Subtree of Another Tree | `p0572_subtree_of_another_tree.py` | `p0572_subtree_of_another_tree.md` |
| 10 | 235 | Lowest Common Ancestor of a Binary Search Tree | `p0235_lowest_common_ancestor_of_a_binary_search_tree.py` | `p0235_lowest_common_ancestor_of_a_binary_search_tree.md` |
| 11 | 701 | Insert into a Binary Search Tree | `p0701_insert_into_a_binary_search_tree.py` | `p0701_insert_into_a_binary_search_tree.md` |
| 12 | 450 | Delete Node in a BST | `p0450_delete_node_in_a_bst.py` | `p0450_delete_node_in_a_bst.md` |
| 13 | 102 | Binary Tree Level Order Traversal | `p0102_binary_tree_level_order_traversal.py` | `p0102_binary_tree_level_order_traversal.md` |
| 14 | 199 | Binary Tree Right Side View | `p0199_binary_tree_right_side_view.py` | `p0199_binary_tree_right_side_view.md` |
| 15 | 1448 | Count Good Nodes in Binary Tree | `p1448_count_good_nodes_in_binary_tree.py` | `p1448_count_good_nodes_in_binary_tree.md` |
| 16 | 427 | Construct Quad Tree | `p0427_construct_quad_tree.py` | `p0427_construct_quad_tree.md` |
| 17 | 98 | Validate Binary Search Tree | `p0098_validate_binary_search_tree.py` | `p0098_validate_binary_search_tree.md` |
| 18 | 337 | House Robber III | `p0337_house_robber_iii.py` | `p0337_house_robber_iii.md` |
| 19 | 1325 | Delete Leaves With a Given Value | `p1325_delete_leaves_with_a_given_value.py` | `p1325_delete_leaves_with_a_given_value.md` |
| 20 | 208 | Implement Trie (Prefix Tree) | `p0208_implement_trie_prefix_tree.py` | `p0208_implement_trie_prefix_tree.md` |
| 21 | 211 | Design Add and Search Words Data Structure | `p0211_design_add_and_search_words_data_structure.py` | `p0211_design_add_and_search_words_data_structure.md` |

## 三种遍历

| 遍历 | 顺序 | 处理当前节点的位置 | 常见用途 |
| --- | --- | --- | --- |
| 前序 | 根、左、右 | 两次递归之前 | 自顶向下传递状态 |
| 中序 | 左、根、右 | 两次递归之间 | BST 有序遍历 |
| 后序 | 左、右、根 | 两次递归之后 | 汇总左右子树结果 |

## 推荐路线

1. 94. Binary Tree Inorder Traversal
2. 144. Binary Tree Preorder Traversal
3. 145. Binary Tree Postorder Traversal
4. 226. Invert Binary Tree
5. 104. Maximum Depth of Binary Tree
6. 543. Diameter of Binary Tree
7. 110. Balanced Binary Tree
8. 100. Same Tree
9. 572. Subtree of Another Tree
10. 235. Lowest Common Ancestor of a Binary Search Tree
11. 701. Insert into a Binary Search Tree
12. 450. Delete Node in a BST
13. 102. Binary Tree Level Order Traversal
14. 101. Symmetric Tree
15. 112. Path Sum
16. 199. Binary Tree Right Side View
17. 1448. Count Good Nodes in Binary Tree
18. 98. Validate Binary Search Tree
19. 230. Kth Smallest Element in a BST
20. 236. Lowest Common Ancestor of a Binary Tree
21. 105. Construct Binary Tree from Preorder and Inorder Traversal
22. 427. Construct Quad Tree
23. 208. Implement Trie (Prefix Tree)
24. 211. Design Add and Search Words Data Structure
25. 1325. Delete Leaves With a Given Value
26. 337. House Robber III
27. 124. Binary Tree Maximum Path Sum
