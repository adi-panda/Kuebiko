from collections import defaultdict


class Trie:
    def __init__(self):
        self.root = defaultdict()

    # @param {string} word
    # @return {void}
    # Inserts a word into the trie.
    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    # @param {string} word
    # @return {boolean}
    # Returns if the word is in the trie.
    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False

    def hasPrefix(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                if "_end" in current:
                    return True
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False


    # @param {string} prefix
    # @return {boolean}
    # Returns if there is any word in the trie
    # that starts with the given prefix.
    def startsWith(self, prefix):
        prefix = prefix.lower()
        current = self.root
        for letter in prefix:
            if letter not in current:
                return False
            current = current[letter]
        return True



