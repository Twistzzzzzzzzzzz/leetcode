from __future__ import annotations


class Codec:
    def encode(self, strs: list[str]) -> str:
        encoded = []

        for word in strs:
            encoded.append(f"{len(word)}#{word}")

        return "".join(encoded)

    def decode(self, s: str) -> list[str]:
        decoded: list[str] = []
        i = 0

        while i < len(s):
            j = i

            while s[j] != "#":
                j += 1

            length = int(s[i:j])
            start = j + 1
            decoded.append(s[start : start + length])
            i = start + length

        return decoded


if __name__ == "__main__":
    codec = Codec()

    examples = [
        ["lint", "code", "love", "you"],
        ["we", "say", ":", "yes"],
        ["", "a", "", "bc"],
        ["10chars###", "#", "hello#world"],
        [],
    ]

    for strs in examples:
        assert codec.decode(codec.encode(strs)) == strs

    print("All examples passed.")
