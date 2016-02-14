"""
Filters for templates.
"""

import re

_filters = {}


def filter(func):
    """
    Mark and registers a function as a filter.

    :param func: The function to mark and register.
    :returns: `func`, unchanged.
    """
    _filters[func.__name__] = func
    return func


def get_filters():
    """
    Get all the registered filters.

    :returns: A dict of the registered filters.
    """
    return _filters


@filter
def snake_case(value):
    """
    Convert the passed-in value to snake case.

    :param value: The value to transform.
    :returns: The transformed value.

    >>> snake_case('getName')
    'get_name'
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@filter
def camel_case(value):
    """
    Convert the passed-in value to camel case.

    :param value: The value to transform.
    :returns: The transformed value.

    >>> camel_case('get_name')
    'getName'
    """
    words = value.split('_')
    first = words[0][:1].lower() + words[0][1:]
    return ''.join([first] + [word.capitalize() for word in words[1:]])


@filter
def pascal_case(value):
    """
    Convert the passed-in value to pascal case.

    :param value: The value to transform.
    :returns: The transformed value.

    >>> pascal_case('get_name')
    'GetName'
    """
    s1 = camel_case(value)
    return s1[:1].upper() + s1[1:]
