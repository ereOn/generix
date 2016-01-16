"""
Tokens definitions for the scope parser.
"""

import ply.lex as lex

tokens = (
    'NUMBER',
    'IDENTIFIER',
    'DOT',
)

t_IDENTIFIER = r'[\w\d_-]+'
t_DOT = r'\.'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    t.type = t[0]
    t.value = t[0]
    t.lexer.skip(1)
    return t


lexer = lex.lex()
