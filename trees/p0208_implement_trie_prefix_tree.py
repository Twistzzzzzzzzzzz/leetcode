from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True


if __name__ == "__main__":
    trie = Trie()

    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True

    trie.insert("app")
    assert trie.search("app") is True

    trie.insert("apply")
    trie.insert("bat")
    assert trie.search("apply") is True
    assert trie.search("bat") is True
    assert trie.search("bad") is False
    assert trie.startsWith("appl") is True
    assert trie.startsWith("cat") is False
    assert trie.startsWith("") is True

    print("All examples passed.")
