"""
Filters for templates.
"""

import re


def snake_case(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case(value):
    words = value.split('_')
    first = words[0][:1].lower() + words[0][1:]
    return ''.join([first] + [word.capitalize() for word in words[1:]])


def pascal_case(value):
    s1 = camel_case(value)
    return s1[:1].upper() + s1[1:]
