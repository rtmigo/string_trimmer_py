# [string_trimmer](https://github.com/rtmigo/string_trimmer_py)

## TripleTrimmer

`TripleTrimmer` removes unwanted parts from a string.

Unwanted parts are defined by lists.

* Parts from the `prefixes` list will only be removed at the beginning of
the string

* Parts from the `suffixes` list will only be removed at the end of
the string

* Parts from the whole_words list - will turn the string into empty if it
is equal to any of the `whole_words` elements.

Since the unwanted parts can be of different lengths, the trimmed strings
can also be different.

Therefore, the `trimmed_once` and `trimmed_recursive` methods return list
of strings, not a single string.

The `shortest` method returns a single string: the shortest possible
when all unwanted parts removed.

## PrefixTrimmer and SuffixTrimmer

These objects act exactly like the TripleTrimmer, but only remove the 
corresponding parts of the strings.

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