# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from itertools import chain
from typing import Iterable, List

from marisa_trie import Trie  # pylint: disable=no-name-in-module


def _add_if_absent(lst, item):
    if item not in lst:
        lst.append(item)


class BaseTrimmer:
    def trimmed_once(self, word: str) -> Iterable[str]:
        raise NotImplementedError

    def trimmed_recursive(self, word: str) -> List[str]:
        result: List[str] = []
        for smaller in self.trimmed_once(word):
            if smaller == word:
                _add_if_absent(result, word)
            else:
                for sub in self.trimmed_recursive(smaller):
                    _add_if_absent(result, sub)
        return result

    def shortest(self, word: str) -> str:
        return sorted(self.trimmed_recursive(word), key=len)[0]


class PrefixTrimmer(BaseTrimmer):
    def __init__(self, prefixes_or_suffixes: Iterable[str]):
        self._prefix_finder = Trie(prefixes_or_suffixes)

    def trimmed_once(self, word: str) -> Iterable[str]:
        found = False
        for pre in self._prefix_finder.prefixes(word):
            found = True
            assert word.startswith(pre)
            yield word[len(pre):]
        if not found:
            yield word


class SuffixTrimmer(BaseTrimmer):
    def __init__(self, prefixes_or_suffixes: Iterable[str]):
        self._suffix_finder = Trie(w[::-1] for w in prefixes_or_suffixes)

    def trimmed_once(self, word: str) -> Iterable[str]:
        found = False
        for pre in self._suffix_finder.prefixes(word[::-1]):
            found = True
            assert word.endswith(pre[::-1])
            yield word[:-len(pre)]
        if not found:
            yield word


class TripleTrimmer(BaseTrimmer):
    """Removes unwanted parts from a string.

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
    """

    def __init__(self, prefixes: Iterable[str], suffixes: Iterable[str],
                 whole_words: Iterable[str]):
        self._prefix_finder = PrefixTrimmer(prefixes)
        self._suffix_finder = SuffixTrimmer(suffixes)
        self._whole_words = set(whole_words)

    def trimmed_once(self, word: str) -> List[str]:
        result: List[str] = []
        if word in self._whole_words:
            _add_if_absent(result, '')

        for trimmed in chain(self._suffix_finder.trimmed_once(word),
                             self._prefix_finder.trimmed_once(word)):
            if trimmed != word:
                assert len(trimmed) < len(word) and trimmed in word
                _add_if_absent(result, trimmed)
                if trimmed in self._whole_words:
                    _add_if_absent(result, '')

        if not result:
            result.append(word)
        return result
