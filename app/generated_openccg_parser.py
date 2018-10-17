#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class OpenCCGBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(OpenCCGBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class OpenCCGParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=OpenCCGBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(OpenCCGParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa
        self._semspec_()
        self._check_eof()

    @tatsumasu()
    def _semspec_(self):  # noqa
        with self._choice():
            with self._option():
                self._nominal_()
            with self._option():
                self._term_()
            with self._option():
                self._conjunction_()
            with self._option():
                self._expression_()
            self._error('no available options')

    @tatsumasu()
    def _conjunction_(self):  # noqa
        with self._choice():
            with self._option():
                self._expression_()
                self.name_last_node('@')
                self._token('^')
                self._cut()
                self._conjunction_()
                self.name_last_node('@')
            with self._option():
                self._expression_()
                self.name_last_node('@')
            self._error('no available options')

    @tatsumasu()
    def _expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._role_expression_()
            with self._option():
                self._nominal_expression_()
            with self._option():
                self._variable_expression_()
            with self._option():
                self._atom_expression_()
            self._error('no available options')

    @tatsumasu()
    def _role_expression_(self):  # noqa
        self._role_()

    @tatsumasu()
    def _variable_expression_(self):  # noqa
        with self._choice():
            with self._option():
                self._variable_()
                self.name_last_node('variable')
                self._token('^')
                self._cut()
                self._conjunction_()
                self.name_last_node('roles')
            with self._option():
                self._variable_()
                self.name_last_node('variable')
            self._error('no available options')
        self.ast._define(
            ['roles', 'variable'],
            []
        )

    @tatsumasu()
    def _nominal_expression_(self):  # noqa
        self._nominal_()
        self.name_last_node('nominal')
        self.ast._define(
            ['nominal'],
            []
        )

    @tatsumasu()
    def _atom_expression_(self):  # noqa
        self._atom_()
        self.name_last_node('entity')
        self.ast._define(
            ['entity'],
            []
        )

    @tatsumasu()
    def _term_(self):  # noqa
        self._token('(')
        self._cut()
        self._conjunction_()
        self.name_last_node('@')
        self._token(')')

    @tatsumasu()
    def _nominal_(self):  # noqa
        self._token('@')
        self._cut()
        self._variable_()
        self.name_last_node('nominal')
        self._term_()
        self.name_last_node('roles')
        self.ast._define(
            ['nominal', 'roles'],
            []
        )

    @tatsumasu()
    def _role_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('<')
                self._atom_()
                self.name_last_node('type')
                self._token('>')
                self._variable_()
                self.name_last_node('target')
            with self._option():
                self._token('<')
                self._atom_()
                self.name_last_node('type')
                self._token('>')
                self._term_()
                self.name_last_node('target')
            with self._option():
                self._token('<')
                self._atom_()
                self.name_last_node('type')
                self._token('>')
                self._atom_()
                self.name_last_node('target')
            self._error('no available options')
        self.ast._define(
            ['target', 'type'],
            []
        )

    @tatsumasu()
    def _variable_(self):  # noqa
        self._pattern(r'[a-z]\d+(:[a-zA-Z\-]+)?')

    @tatsumasu()
    def _atom_(self):  # noqa
        self._pattern(r'[a-zA-Z\-\.]+')


class OpenCCGSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def semspec(self, ast):  # noqa
        return ast

    def conjunction(self, ast):  # noqa
        return ast

    def expression(self, ast):  # noqa
        return ast

    def role_expression(self, ast):  # noqa
        return ast

    def variable_expression(self, ast):  # noqa
        return ast

    def nominal_expression(self, ast):  # noqa
        return ast

    def atom_expression(self, ast):  # noqa
        return ast

    def term(self, ast):  # noqa
        return ast

    def nominal(self, ast):  # noqa
        return ast

    def role(self, ast):  # noqa
        return ast

    def variable(self, ast):  # noqa
        return ast

    def atom(self, ast):  # noqa
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'start'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = OpenCCGParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, OpenCCGParser, name='OpenCCG')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
