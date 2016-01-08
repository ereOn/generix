"""
The base parser.
"""

from voluptuous import (
    Any,
    Required,
    Schema,
)

from ..objects import (
    Argument,
    Definition,
    Field,
    Function,
    Type,
)


class BaseParser(object):
    def parse_field(self, value):
        kwargs = Schema({
            'name': str,
            'type': str,
        })(value)

        return Field(**kwargs)

    def parse_type(self, value):
        kwargs = Schema({
            'name': str,
            Required('fields', default=[]): [self.parse_field],
        })(value)

        return Type(**kwargs)

    def parse_argument(self, value):
        kwargs = Schema({
            'name': str,
            'type': str,
            'mode': Any('in', 'out', 'inout'),
        })(value)

        return Argument(**kwargs)

    def parse_function(self, value):
        kwargs = Schema({
            'name': str,
            'arguments': [self.parse_argument],
        })(value)

        return Function(**kwargs)

    def parse_definition(self, value):
        kwargs = Schema({
            Required('requires', default=[]): [str],
            Required('types', default=[]): [self.parse_type],
            Required('functions', default=[]): [self.parse_function],
        })(value)

        return Definition(**kwargs)

    def validate(self, raw):
        return self.parse_definition(raw)
