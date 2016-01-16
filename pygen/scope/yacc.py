"""
Grammar definitions for the scope parser.
"""

import ply.yacc as yacc

from .lex import tokens


def p_scope_empty(p):
    'scope :'
    p[0] = []


def p_scope_path(p):
    'scope : path'
    p[0] = p[1]


def p_path(p):
    '''
    path : IDENTIFIER
         | NUMBER
    '''
    p[0] = [p[1]]


def p_dotted_path(p):
    '''
    path : path DOT IDENTIFIER
         | path DOT NUMBER
    '''
    p[0] = p[1] + [p[3]]


def p_error(p):
    return p


parser = yacc.yacc()
