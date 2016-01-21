"""
Tests for the scope utility functions and classes.
"""

from unittest import TestCase

from pygen.scope import Scope
from pygen.exceptions import InvalidScope


class ScopeTests(TestCase):
    def test_from_string_empty(self):
        scope = Scope.from_string('')
        self.assertEqual(Scope(), scope)

    def test_from_string_single_identifier(self):
        scope = Scope.from_string('foo')
        self.assertEqual(Scope(scope=['foo']), scope)

    def test_from_string_multiple_identifiers(self):
        scope = Scope.from_string('foo.bar')
        self.assertEqual(Scope(scope=['foo', 'bar']), scope)

    def test_from_string_single_number(self):
        scope = Scope.from_string('2')
        self.assertEqual(Scope(scope=[2]), scope)

    def test_from_string_single_number_ellipsis(self):
        scope = Scope.from_string('2...')
        self.assertEqual(Scope(scope=[2], is_iterable=True), scope)

    def test_from_string_multiple_identifiers_and_numbers(self):
        scope = Scope.from_string('foo.3')
        self.assertEqual(Scope(scope=['foo', 3]), scope)

    def test_from_string_invalid(self):
        with self.assertRaises(InvalidScope) as error:
            Scope.from_string('foo.')

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
        self.assertEqual("Scope(['a', 'b'], is_iterable=False)", repr(scope))

    def test_scope_as_string(self):
        scope = Scope(['a', 'b'])
        self.assertEqual('a.b', str(scope))

    def test_scope_as_string_ellipsis(self):
        scope = Scope(['a', 'b'], is_iterable=True)
        self.assertEqual('a.b...', str(scope))

    def test_scope_resolve_empty(self):
        context = {'a': 1, 'b': 2}
        scope = Scope.from_string('')
        result = scope.resolve(context)
        self.assertEqual(context, result)

    def test_scope_resolve_single_identifier(self):
        context = {'a': 1, 'b': 2}
        scope = Scope.from_string('a')
        result = scope.resolve(context)
        self.assertEqual(context['a'], result)

    def test_scope_resolve_multiple_identifiers(self):
        context = {'a': {'c': 3}, 'b': 2}
        scope = Scope.from_string('a.c')
        result = scope.resolve(context)
        self.assertEqual(context['a']['c'], result)

    def test_scope_resolve_multiple_identifiers_and_numbers(self):
        context = {'a': [{'c': 3}], 'b': 2}
        scope = Scope.from_string('a.0.c')
        result = scope.resolve(context)
        self.assertEqual(context['a'][0]['c'], result)
