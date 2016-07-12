#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.Meta.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Meta: 'bg:#00aaaa #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
        Token.Scrollbar.Button: 'bg:#003333',
        Token.Scrollbar: 'bg:#00aaaa',
        Token.Toolbar : 'bg:#222222 #ffffff',
        Token.Toolbar.Arg: 'noinherit bold',
        Token.Toolbar.Arg.Text: 'nobold'
    }
    styles.update(DefaultStyle.styles)