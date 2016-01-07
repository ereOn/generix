"""
The base parser.
"""

from contextlib import contextmanager
from voluptuous import (
    Any,
    Required,
    Schema,
)

from ..exceptions import (
    DuplicateTypeError,
    UnknownTypeError,
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
            'type': self.get_type_or_fail,
        })(value)

        return Field(**kwargs)

    def parse_type(self, value):
        kwargs = Schema({
            'name': str,
            Required('fields', default=[]): [self.parse_field],
        })(value)

        type = Type(**kwargs)

        if type.name in self.types:
            current_type = self.types[type.name]

            raise DuplicateTypeError(type=type, current_type=current_type)

        self.types[type.name] = type
        return type

    def parse_argument(self, value):
        kwargs = Schema({
            'name': str,
            'type': self.get_type_or_fail,
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
            Required('types', default=[]): list,
            Required('functions', default=[]): list,
        })(value)

        types = Schema([self.parse_type])(kwargs['types'])
        functions = Schema([self.parse_function])(kwargs['functions'])

        return Definition(types=types, functions=functions)

    def get_type_or_fail(self, type_name):
        type = self.types.get(type_name)

        if type is None:
            raise UnknownTypeError(type_name=type_name, types=self.types)

        return type

    @contextmanager
    def context(self):
        self.types = {}

        try:
            yield
        finally:
            self.types = None

    def validate(self, raw):
        with self.context():
            return self.parse_definition(raw)
