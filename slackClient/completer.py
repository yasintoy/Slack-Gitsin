#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import print_function

from prompt_toolkit.completion import Completer

from completions import SUBCOMMANDS, ARGS_OPTS_LOOKUP

#adapted from haxor-news project
class Completer(Completer):

    def __init__(self, fuzzy_match, text_utils):
        self.fuzzy_match = fuzzy_match
        self.text_utils = text_utils

    def completing_command(self, words, word_before_cursor):
        """
            Determine if we are currently completing the slack command.
        """
        if len(words) == 1 and word_before_cursor != '':
            return True
        else:
            return False

    def completing_subcommand(self, words, word_before_cursor):
        """
            Determine if we are currently completing a subcommand.
        """
        if (len(words) == 1 and word_before_cursor == '') \
                or (len(words) == 2 and word_before_cursor != ''):
            return True
        else:
            return False

    def completing_arg(self, words, word_before_cursor):
        """
            Determine if we are currently completing an arg.
        """
        if (len(words) == 2 and word_before_cursor == '') \
                or (len(words) == 3 and word_before_cursor != ''):
            return True
        else:
            return False



    def completing_subcommand_option_util(self, option, words):
        """
            Determine if we are currently completing an option.
        """
        # Example: Return True for: hn view 0 --comm
        if len(words) > 3:
            if option in words:
                return True
        return False


    def get_completions(self, document, _):
        """
            Get completions for the current scope.
        """
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        commands = []
        if len(words) == 0:
            return commands
        if self.completing_command(words, word_before_cursor):
            commands = ['slack']
        else:
            if 'slack' not in words:
                return commands
            if self.completing_subcommand(words, word_before_cursor):
                commands = list(SUBCOMMANDS.keys())
            else:
                if self.completing_arg(words, word_before_cursor):
                    commands = self.arg_completions(words, word_before_cursor)
                else:
                    commands = self.completing_subcommand_option(
                        words,
                        word_before_cursor)
        completions = self.text_utils.find_matches(
            word_before_cursor, commands, fuzzy=self.fuzzy_match)
        return completions
        
    def arg_completions(self, words, word_before_cursor):
        """
            Generates arguments completions based on the input.
        """
        if 'slack' not in words:
            return []
        for subcommand, args_opts in ARGS_OPTS_LOOKUP.items():
            if subcommand in words:
                return [ARGS_OPTS_LOOKUP[subcommand]['args']]
        return ['10']

    def completing_subcommand_option(self, words, word_before_cursor):
        """
            Determine if we are currently completing an option.
        """
        options = []
        for subcommand, args_opts in ARGS_OPTS_LOOKUP.items():
            if subcommand in words and \
                (words[-2] == subcommand or
                    self.completing_subcommand_option_util(subcommand, words)):
                options.extend(ARGS_OPTS_LOOKUP[subcommand]['opts'])
        return options