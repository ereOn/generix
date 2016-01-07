"""
Objects.
"""

from collections import namedtuple

Field = namedtuple('Field', ['name', 'type'])
Type = namedtuple('Type', ['name', 'fields'])
Argument = namedtuple('Argument', ['name', 'type', 'mode'])
Function = namedtuple('Function', ['name', 'arguments'])
Definition = namedtuple('Definition', ['types', 'functions'])
