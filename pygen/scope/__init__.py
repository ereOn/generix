"""
Scope manipulation.
"""

import re

from .exceptions import InvalidScope


def parse_scope(value):
    """
    Creates a `Scope` instance from a dotted path string.

    :param value: The dotted path string.
    :returns: A `Scope` instance if `value` is a valid path.
    """
    if not re.match('^[\w\d_-]+(\.[\w\d_-]+)*$', value):
        raise InvalidScope(value)

    return Scope(scope=value.split('.'))


class Scope(object):
    """
    Represents a scope.
    """
    def __init__(self, scope=None):
        """
        Creates a new scope.

        :param scope: A list of path components.
        """
        self.scope = scope or []

    def __repr__(self):
        return 'Scope(%r)' % self.scope

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
