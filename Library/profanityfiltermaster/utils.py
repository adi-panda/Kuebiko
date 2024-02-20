import os


def get_complete_path(file):
    return os.path.abspath(file)


def read_wordList(file):
    wordList = []
    with open(file, encoding='utf-8') as wordlist:
        for word in wordlist:
            word = word.strip()
            if word != "":
                wordList.append(word)
    return wordList