from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search(self, word: str) -> bool:
        def dfs(index: int, node: TrieNode) -> bool:
            if index == len(word):
                return node.is_end

            char = word[index]

            if char == ".":
                for child_node in node.children.values():
                    if dfs(index + 1, child_node):
                        return True

                return False

            if char not in node.children:
                return False

            return dfs(index + 1, node.children[char])

        return dfs(0, self.root)


if __name__ == "__main__":
    dictionary = WordDictionary()

    dictionary.addWord("bad")
    dictionary.addWord("dad")
    dictionary.addWord("mad")

    assert dictionary.search("pad") is False
    assert dictionary.search("bad") is True
    assert dictionary.search(".ad") is True
    assert dictionary.search("b..") is True
    assert dictionary.search("...") is True
    assert dictionary.search("..") is False
    assert dictionary.search("....") is False

    dictionary.addWord("a")
    dictionary.addWord("bake")
    assert dictionary.search(".") is True
    assert dictionary.search("ba.e") is True
    assert dictionary.search("b...") is True
    assert dictionary.search("c...") is False
    assert dictionary.search("") is False

    print("All examples passed.")
