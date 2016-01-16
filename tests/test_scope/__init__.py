"""
Tests for the scope utility functions and classes.
"""

from unittest import TestCase

from pygen.scope import (
    parse_scope,
    Scope,
)
from pygen.scope.exceptions import InvalidScope


class ScopeTests(TestCase):
    def test_parse_scope_empty(self):
        scope = parse_scope('')
        self.assertEqual(Scope(scope=[]), scope)

    def test_parse_scope_single_identifier(self):
        scope = parse_scope('foo')
        self.assertEqual(Scope(scope=['foo']), scope)

    def test_parse_scope_multiple_identifiers(self):
        scope = parse_scope('foo.bar')
        self.assertEqual(Scope(scope=['foo', 'bar']), scope)

    def test_parse_scope_single_number(self):
        scope = parse_scope('2')
        self.assertEqual(Scope(scope=[2]), scope)

    def test_parse_scope_multiple_identifiers_and_numbers(self):
        scope = parse_scope('foo.3')
        self.assertEqual(Scope(scope=['foo', 3]), scope)

    def test_parse_scope_invalid(self):
        with self.assertRaises(InvalidScope) as error:
            parse_scope('foo.')

        self.assertEqual('foo.', error.exception.scope)

    def test_scope_default_initialization(self):
        scope = Scope()
        self.assertEqual([], scope.scope)

    def test_scope_list_initialization(self):
        scope = Scope(('a', 'b'))
        self.assertEqual(['a', 'b'], scope.scope)

    def test_scope_comparison(self):
        scope_a = Scope(['a', 'b'])
        scope_b = Scope(['a', 'b'])
        scope_c = Scope(['a', 'c'])
        self.assertTrue(scope_a == scope_b)
        self.assertFalse(scope_a != scope_b)
        self.assertFalse(scope_a == scope_c)
        self.assertTrue(scope_a != scope_c)
        self.assertFalse(scope_a == 1)

    def test_scope_representation(self):
        scope = Scope(['a', 'b'])
        self.assertEqual("Scope(['a', 'b'])", repr(scope))

    def test_scope_resolve_empty(self):
        context = {'a': 1, 'b': 2}
        scope = parse_scope('')
        result = scope.resolve(context)
        self.assertEqual(context, result)

    def test_scope_resolve_single_identifier(self):
        context = {'a': 1, 'b': 2}
        scope = parse_scope('a')
        result = scope.resolve(context)
        self.assertEqual(context['a'], result)

    def test_scope_resolve_multiple_identifiers(self):
        context = {'a': {'c': 3}, 'b': 2}
        scope = parse_scope('a.c')
        result = scope.resolve(context)
        self.assertEqual(context['a']['c'], result)

    def test_scope_resolve_multiple_identifiers_and_numbers(self):
        context = {'a': [{'c': 3}], 'b': 2}
        scope = parse_scope('a.0.c')
        result = scope.resolve(context)
        self.assertEqual(context['a'][0]['c'], result)
