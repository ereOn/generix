"""
Scope unit tests.
"""

import pytest

from pygen.scope import Scope
from pygen.exceptions import InvalidScope


def test_from_string_invalid():
    with pytest.raises(InvalidScope) as error:
        Scope.from_string('&$#@')

    assert error.value.scope == '&$#@'


def test_from_string_empty():
    scope = Scope.from_string('')
    assert scope == Scope()


def test_from_string_empty_iterable():
    scope = Scope.from_string('...')
    assert scope == Scope(is_iterable=True)


def test_from_string_single():
    scope = Scope.from_string('a')
    assert scope == Scope(['a'])


def test_from_string_path():
    scope = Scope.from_string('a.b.c')
    assert scope == Scope(['a', 'b', 'c'])


def test_from_string_indexes():
    scope = Scope.from_string('a.2.c')
    assert scope == Scope(['a', 2, 'c'])


def test_from_string_iterable():
    scope = Scope.from_string('a.2.c...')
    assert scope == Scope(['a', 2, 'c'], is_iterable=True)


def test_compare_to_different_type():
    assert Scope() != 2


def test_str():
    assert str(Scope()) == ''
    assert str(Scope(['a', 'b'])) == 'a.b'
    assert str(Scope(is_iterable=True)) == '...'
    assert str(Scope(['a', 'b'], is_iterable=True)) == 'a.b...'


def test_repr():
    assert repr(Scope()) == 'Scope()'
    assert repr(Scope(['a', 'b'])) == "Scope(['a', 'b'])"
    assert repr(Scope(is_iterable=True)) == "Scope(is_iterable=True)"
    assert repr(Scope(['a', 'b'], is_iterable=True)) == \
        "Scope(['a', 'b'], is_iterable=True)"


def test_resolve():
    context = {
        'a': {
            'b': 'c',
        },
    }
    scope = Scope(['a', 'b'])
    assert scope.resolve(context) == 'c'
