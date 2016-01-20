"""
Scope manipulation.
"""

import re

from .exceptions import InvalidScope


class Scope(object):
    """
    Represents a scope.
    """
    @classmethod
    def from_string(cls, value):
        """
        Creates a `Scope` instance from a dotted path string.

        :param value: The dotted path string.
        :returns: A `Scope` instance if `value` is a valid path.
        """
        if not re.match('^([\w\d_-]+(\.[\w\d_-]+)*(\.\.\.)?)?$', value):
            raise InvalidScope(value)

        scope = [
            int(x) if re.match('^\d+$', x) else x
            for x in value.split('.') if x
        ]

        return cls(scope=scope, is_iterable=value.endswith('...'))

    def __init__(self, scope=None, is_iterable=False):
        """
        Creates a new scope.

        :param scope: A list of path components.
        :param is_iterable: A boolean flag that indicates whether the scope
            points to an iterable.
        """
        self.scope = list(scope or [])
        self.is_iterable = is_iterable

    def __eq__(self, other):
        if not isinstance(other, Scope):
            return NotImplemented

        return (other.scope == self.scope) and \
            (other.is_iterable == self.is_iterable)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '.'.join(self.scope)

    def __repr__(self):
        return 'Scope(%r, is_iterable=%r)' % (self.scope, self.is_iterable)

    def resolve(self, context):
        """
        Resolve the scope into the specified context.

        :params context: The context to resolve the scope into.
        :returns: The resolved context.
        """
        if self.scope:
            return Scope(scope=self.scope[1:]).resolve(context[self.scope[0]])
        else:
            return context
