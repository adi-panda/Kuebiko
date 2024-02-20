import profanity_filter
from trie import Trie
import time
from better_profanity import profanity


def text_check():
    filter = profanity_filter.ProfanityFilter()
    clean_text = filter.censor("D*mn you shit77923244")
    print(clean_text)

    filter.add_profane_words(["you", "maria"])
    print(filter.censor("are you maria"))

    filter.load_profane_words(custom_profane_wordlist={'abc'}, whitelist={'shit'})
    print(filter.censor("you Shit abc"))


def get_image_analysis(url):
    return profanity_filter.get_image_analysis(url)


def censor_image(url):
    profanity_filter.censor_image(url)


def trie_test():
    test = Trie()
    test.insert('helloworld')
    test.insert('ilikeapple')
    test.insert('helloz')

    print(test.search('hello'))
    print(test.startsWith('hello'))
    print(test.search('ilikeapple'))


def compare():
    startTime1 = time.time()
    filter = profanity_filter.ProfanityFilter()
    print(filter.censor("Damnnn you"))
    endTime1 = time.time()
    print("Time for 1st filter: "+str(endTime1-startTime1))

    startTime2 = time.time()
    profanity.load_censor_words()
    print(profanity.censor("D*mn you"))
    endTime2 = time.time()
    print("Time for 2nd filter: " + str(endTime2 - startTime2))


if __name__ == "__main__":
    text_check()
    compare()



