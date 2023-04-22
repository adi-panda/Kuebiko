import nltk
from twitchio import Message


def check_and_filter_user_message(message: Message) -> bool:
    # Messages with echo set to True are messages sent by the bot...
    # For now we just want to ignore them...
    if message.echo:
        return True

    # download the words corpus
    nltk.download("words")

    # Check if the message contains english words
    words = nltk.corpus.words.words()
    user_message = message.content
    if not any(word in user_message for word in words):
        return True

    # Check if the message is too long or short
    if len(user_message) > 70 or len(user_message) < 3:
        return True

    return False


def open_file(filepath) -> str:
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


def words_length(text: str) -> int:
    words = text.split(" ")
    return len(words)
