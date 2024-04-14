import nltk  # type: ignore
from twitchio import Message  # type: ignore


def check_and_filter_user_message(message: Message) -> bool:
    # Messages with echo set to True are messages sent by the bot...
    # For now we just want to ignore them...
    if message.echo:
        return True

    # download the words corpus
    nltk.download("words")  # English words
    nltk.download("cess_esp")  # Spanish words

    user_message = message.content

    # Check if the message contains english words
    english_words = nltk.corpus.words.words()
    if not any(word in user_message for word in english_words):
        return True

    # Check if the message contains spanish words
    spanish_words = nltk.corpus.cess_esp.words()
    if not any(word in user_message for word in spanish_words):
        return True

    # Check if the message is too long or short
    if len(user_message) > 70 or len(user_message) < 3:
        return True

    return False
