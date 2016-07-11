#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import re

import six
import shlex
from prompt_toolkit.completion import Completion

from completions import META_LOOKUP


class TextUtils(object):
    """Utilities for parsing and matching text."""

    def find_matches(self, word, collection, fuzzy):
        """
            Find all matches in collection for word.
        """
        word = self._last_token(word).lower()
        for suggestion in self._find_collection_matches(
                word, collection, fuzzy):
            yield suggestion

    def get_tokens(self, text):
        """
            Parse out all tokens.
        """
        if text is not None:
            text = text.strip()
            words = self._safe_split(text)
            return words
        return []

    def _last_token(self, text):
        """
            Find the last word in text.
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = self._safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    def _fuzzy_finder(self, text, collection, case_sensitive=True):
        """
            Customized fuzzy finder with optional case-insensitive matching.
        """
        suggestions = []
        if case_sensitive:
            pat = '.*?'.join(map(re.escape, text))
        else:
            pat = '.*?'.join(map(re.escape, text.lower()))
        regex = re.compile(pat)
        for item in collection:
            if case_sensitive:
                r = regex.search(item)
            else:
                r = regex.search(item.lower())
            if r:
                suggestions.append((len(r.group()), r.start(), item))
        return (z for _, _, z in sorted(suggestions))

    def _find_collection_matches(self, word, collection, fuzzy):
        """
            Yield all matching names in list.
        """
        word = word.lower()
        if fuzzy:
            for suggestion in self._fuzzy_finder(word,
                                                 collection,
                                                 case_sensitive=False):
                yield Completion(suggestion,
                                 -len(word),
                                 display_meta='display_meta')
        else:
            for name in sorted(collection):
                if name.lower().startswith(word) or not word:
                    display = None
                    display_meta = None
                    if name in META_LOOKUP:
                        display_meta = META_LOOKUP[name]
                    yield Completion(name,
                                     -len(word),
                                     display=display,
                                     display_meta=display_meta)

    def _shlex_split(self, text):
        """
            Wrapper for shlex, because it does not seem to handle unicode in 2.6.
        """
        if six.PY2:
            text = text.encode('utf-8')
        return shlex.split(text)

    def _safe_split(self, text):
        """
            Safely splits the input text.
        """
        try:
            words = self._shlex_split(text)
            return words
        except:
            return text