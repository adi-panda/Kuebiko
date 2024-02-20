# profanity-filter

Most of the words which are in the `profane_wordlist.txt` are taken from Bad Words list for Facebook. <br/>
Supports modified spellings like `D@mn`, `$h1t` etc. <br/>
This library is significantly faster than other profanity filters which use **regex or string methods**. <br/>

Reason to use trie: <https://link.medium.com/tMuykUJZJ9> <br/>
Reason to not use regex: <https://github.com/snguyenthanh/better_profanity/issues/14> <br/>

The filter also censors words if their prefixes match with any profane word. 

## Working

```python
import profanity_filter
filter = profanity_filter.ProfanityFilter()
clean_text = filter.censor("D*mnn you!")
print(clean_text) 
# ***** you!
```

All modified spellings of profane words will be detected
Example: `D*mn, D@mn, $h17, 4r53` etc

## Add your custom profane wordlist and custom whitelist
```python
filter.load_profane_words(custom_profane_wordlist = {'damn', 'douche'}, whitelist = {'shit'})
```

## Check if your text has any profane word
```python
filter.isProfane('You piece of $h*t')
# returns true
```

## How this profanity filter works for text words
```python
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7")
        }
```
This map maps characters with set of similar looking alphabets. Using commonly used profane wordlist and this map, Distorted profane words (Leetspeak words) are generated and the generated words are inserted into a trie. 

The wordlist generated contains a total of approximately 40000 words, including 130 words from the default profanity_wordlist.txt and their variants by modified spellings.

Time Complexity to check whether a word is profane is `O(length of the word)`.

## Add more profane words
```python
filter.add_profane_words(['damn', 'shit'])
```

## Add more whitelist words
```python
filter.add_whitelist_words(['damn', 'shit'])
```

## Censor profane urls
```python
filter.censor_url(url)
```

## Check whether your image is profane or not
```python
r = filter.get_image_analysis(IMAGE_URL)
print(r.json())
# json output which contains profanity_score of the image and other details
```
This is done with the help of `DeepAI` Api <br/>
<https://deepai.org/machine-learning-model/nsfw-detector>

## Censor your profane image
```python
filter.censor_image(image_url)
```
This is done with the help of pillow library which is a Photo imaging library <br/>
<https://pypi.org/project/Pillow/> <br/>
The censored images are stored in the images folder.

## TO-DO
1) Implement Compressed trie instead of normal trie for space optimization.
2) Censor words whose inner substrings match with profane words while avoiding false positives.
3) Add support for adding wordlist as a file.

