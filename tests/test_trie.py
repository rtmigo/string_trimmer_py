# SPDX-FileCopyrightText: (c) 2022 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import unittest

from string_trimmer import PrefixTrimmer, SuffixTrimmer, TripleTrimmer


class TestPrefixRemover(unittest.TestCase):
    def test(self):
        r = PrefixTrimmer(["-suf1", "-suf2", 'junk', 'pre1-', 'pre2-'])

        self.assertEqual(list(r.trim("word")), ["word"])
        self.assertEqual(list(r.trim("pre1-abc")), ['abc'])
        self.assertEqual(list(r.trim("pre2-pre1-abc")), ['abc'])

        self.assertEqual(list(r.trim("junk")), [''])
        self.assertEqual(list(r.trim("pre2-pre1-junk-suf1-suf2")),
                         [''])
        self.assertEqual(list(r.trim("pre2-pre1-word-suf1-suf2")),
                         ['word-suf1-suf2'])


class TestSuffixRemover(unittest.TestCase):
    def test(self):
        r = SuffixTrimmer(["-suf1", "-suf2", 'junk', 'pre1-', 'pre2-',
                           'xx', 'xxx', 'hex'])

        self.assertEqual(list(r.trim("word")), ["word"])
        self.assertEqual(list(r.trim("abc-suf1")), ['abc'])
        self.assertEqual(list(r.trim("abc-suf1-suf2")), ['abc'])
        self.assertEqual(list(r.trim("pre2-pre1-abc-suf1-suf2")),
                         ['pre2-pre1-abc'])

        self.assertEqual(list(r.trim("junk")), [''])
        self.assertEqual(list(r.trim("pre2-pre1-junk-suf1-suf2")),
                         [''])

        self.assertEqual(list(r.trim("ABCxxx")), ['ABCx', 'ABC'])
        self.assertEqual(list(r.trim("ABChexxx")), ['ABC', 'ABChe'])


class TestTriple(unittest.TestCase):
    def test_old(self):
        prefixes_and_suffixes = ["-suf1", "-suf22", 'junk', 'pre1-', 'pre22-']
        r = TripleTrimmer(prefixes_and_suffixes, prefixes_and_suffixes, [])

        with self.subTest('both'):
            self.assertEqual(list(r.trim("word")), ["word"])
            self.assertEqual(list(r.trim("pre1-abc")), ['abc'])
            self.assertEqual(list(r.trim("pre22-pre1-abc")),
                             ['abc'])
            self.assertEqual(list(r.trim("abc-suf1")), ['abc'])
            self.assertEqual(list(r.trim("abc-suf1-suf22")),
                             ['abc'])
            self.assertEqual(
                list(r.trim("pre22-pre1-abc-suf1-suf22")),
                ['abc'])

            self.assertEqual(list(r.trim("junk")), [''])
            self.assertEqual(
                list(r.trim("pre22-pre1-junk-suf1-suf22")), [''])

    def test_triple(self):
        r = TripleTrimmer(
            prefixes=['aaa', 'aa'],
            suffixes=['bb', 'bbb'],
            words=["JUNK"])

        self.assertEqual(r.trim('something'), ['something'])
        self.assertEqual(r.trim('aasomething'), ['something'])
        self.assertEqual(r.trim('aaasomething'),
                         ['asomething', 'something'])

        self.assertEqual(r.trim('somethingaa'), ['somethingaa'])
        self.assertEqual(r.trim('somethingbb'), ['something'])
        self.assertEqual(r.trim('somethingbbb'),
                         ['somethingb', 'something'])

        self.assertEqual(r.trim('JUNK'), [''])
        self.assertEqual(r.trim('aaJUNKbb'), [''])
        self.assertEqual(r.trim('aaaJUNKbbb'),
                         ['aJUNKb', 'JUNKb', 'aJUNK', ''])

    def test_shortest(self):
        r = TripleTrimmer(
            prefixes=['aaa', 'aa'],
            suffixes=['bb', 'bbb'],
            words=["JUNK"])
        self.assertEqual(r.shortest('SOMETHING'), 'SOMETHING')
        self.assertEqual(r.shortest('aaaSOMETHINGbbb'), 'SOMETHING')
        self.assertEqual(r.shortest('JUNK'), '')

    def test_no_whole_words(self):
        r = TripleTrimmer(
            prefixes=['aaa', 'aa'],
            suffixes=['bb', 'bbb'])
        r.shortest('some string')

    def test_no_suffixes(self):
        r = TripleTrimmer(
            prefixes=['aaa', 'aa'],
            words=["JUNK"])
        r.shortest('some string')

    def test_no_prefixes(self):
        r = TripleTrimmer(
            suffixes=['bb', 'bbb'],
            words=["JUNK"])
        r.shortest('some string')

    def test_doc1(self):
        trimmer = TripleTrimmer(
            prefixes=["mr.", "mrs.", " "],
            suffixes=[" esq", " phd", "."])

        self.assertEqual(trimmer.shortest("Mr. John Doe Esq.".lower()),
                         "john doe")

    def test_doc2(self):
        trimmer = TripleTrimmer(
            suffixes=["'ll"],
            words=["he", "she", "they",
                   "the", "a", "an"])

        words = [trimmer.shortest(word) for word
                 in "she'll eat an ice cream".split()]
        self.assertEqual(words, ['', 'eat', '', 'ice', 'cream'])
