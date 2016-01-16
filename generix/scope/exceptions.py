"""
Scope exceptions.
"""


class InvalidScope(ValueError):
    """
    An invalid scope was specified.
    """
    def __init__(self, scope):
        super(InvalidScope, self).__init__("Not a valid scope: %r" % scope)
        self.scope = scope
