# [string_trimmer](https://github.com/rtmigo/string_trimmer_py)

`TripleTrimmer` removes unwanted parts from a string.

Deletion occurs recursively in order to find the shortest possible string
without prefixes, suffixes, etc.

## Examples

```python3
from string_trimmer import TripleTrimmer

trimmer = TripleTrimmer(
    prefixes=["mr.", "mrs.", " "],
    suffixes=[" esq", " phd", "."])

print(trimmer.shortest("Mr. John Doe Esq.".lower()))
# john doe
```

```python3
from string_trimmer import TripleTrimmer

trimmer = TripleTrimmer(
    suffixes=["'ll"],
    words=["he", "she", "they"])

words = [trimmer.shortest(word) for word 
         in "she'll eat an ice cream".split()]
print(words)
# ['', 'eat', '', 'ice', 'cream']
```


## Install

### pip

```bash
pip3 install git+https://github.com/rtmigo/string_trimmer_py#egg=string_trimmer
```

### setup.py

```python3
install_requires = [
    "string_trimmer@ git+https://github.com/rtmigo/string_trimmer_py"
]
```

## TripleTrimmer

`TripleTrimmer` removes unwanted parts from a string.

Unwanted parts are defined by lists.

* Parts from the `prefixes` list will only be removed at the beginning of the
  string

* Parts from the `suffixes` list will only be removed at the end of the string

* Parts from the whole_words list - will turn the string into empty if it is
  equal to any of the `words` elements.

Since the unwanted parts can be of different lengths, the trimmed strings can
also be different.

The `trim` method will try to trim the word in every possible way, repeating
attempts recursively. The result will be a list of strings.

The `shortest` method returns a single string: the first of the shortest strings
returned by `trim`.

## PrefixTrimmer and SuffixTrimmer

These objects act exactly like the TripleTrimmer, but only remove the
corresponding parts of the strings.