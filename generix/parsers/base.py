"""
The base parser.
"""

from voluptuous import (
    Any,
    Required,
    Schema,
)

from ..objects import Definition


class BaseParser(object):
    def validate(self, raw):
        return Definition.parse(raw)
