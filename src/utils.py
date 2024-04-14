def open_file(filepath) -> str:
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


def words_length(text: str) -> int:
    words = text.split(" ")
    return len(words)
