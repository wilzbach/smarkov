#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from smarkov import Markov

# This is just a toy example without nltk

SENTENCE_STOPS = [".", "?", ",", ":", ";", "'"]
REPLACE_WORDS = {'n\'t': 'not', '\'ll': 'will',
                 '\'re': 'are', '\'ve': 'have', '\'s': 'is', 'ca': 'can', 'wo': 'will'}


def join_tokens_to_sentences(tokens):
    """ Correctly joins tokens to multiple sentences

    Instead of always placing white-space between the tokens, it will distinguish
    between the next symbol and *not* insert whitespace if it is a sentence
    symbol (e.g. '.', or '?')

    Args:
        tokens: array of string tokens
    Returns:
        Joint sentences as one string
    """
    text = ""
    for (entry, next_entry) in zip(tokens, tokens[1:]):
        text += entry
        if next_entry not in SENTENCE_STOPS:
            text += " "

    text += tokens[-1]
    return text


def expanding_words(words):
    """ Transforms words into a their expanded form - replaces all
    abbreviations like "'ll" or "n't"

    There are some special case like can't (in tokens ("ca", "n't")) or won't
    where we want to replace both forms

    Args:
        words: words iterator to search and replace
    Returns:
        words iterator with replaced abbreviations
    """
    for word in words:
        if word in REPLACE_WORDS:
            yield REPLACE_WORDS[word]
        else:
            yield word


def tokenize(s):
    return expanding_words(re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", s))

scriptDir = os.path.dirname(os.path.realpath(__file__))
inputFile = os.path.join(scriptDir, "./pg1342.txt")
with open(inputFile, "r") as inFile:
    corpus = re.split(
        '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', inFile.read())
    chain = Markov(corpus, tokenize=tokenize)
    print(join_tokens_to_sentences(chain.generate_text()))
