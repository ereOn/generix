"""
Objects.
"""

from itertools import chain
from six import add_metaclass
from voluptuous import (
    Any,
    Extra,
    Required,
    Schema,
    UNDEFINED,
)

from .exceptions import DuplicateTypeError


class ParsableTypeMeta(type):
    def __new__(cls, name, bases, attrs):
        schema = attrs.pop('schema', {})
        attrs['_fields'] = tuple(
            str(field)
            for field in schema
            if field is not Extra
        )
        attrs['_defaults'] = {
            str(key): key.default()
            for key in schema
            if hasattr(key, 'default') and key.default is not UNDEFINED
        }
        attrs['__slots__'] = attrs.get('__slots__', ()) + attrs['_fields'] + \
            ('_extra',)
        attrs['_schema'] = Schema(schema)
        return super(ParsableTypeMeta, cls).__new__(cls, name, bases, attrs)


@add_metaclass(ParsableTypeMeta)
class ParsableType(object):
    id = None

    def __init__(self, **kwargs):
        for key in self._fields:
            if key in self._defaults:
                setattr(self, key, kwargs.pop(key, self._defaults[key]))
            else:
                setattr(self, key, kwargs.pop(key))

        self._extra = kwargs

    @classmethod
    def parse(cls, data):
        kwargs = cls._schema(data)
        return cls(**kwargs)

    def __getattr__(self, key):
        if key in self._extra:
            return self._extra[key]
        else:
            raise AttributeError(
                "%r object has no attribute %r" % (self.__class__, key),
            )

    def __iter__(self):
        pairs = []

        if self.id is not None:
            pairs.append([(self.id, getattr(self, self.id))])

        pairs.extend([
            (
                (key, getattr(self, key))
                for key in self._fields
                if key != self.id
            ),
            self._extra.items(),
        ])
        return chain(*pairs)

    def __str__(self):
        if self.id is not None:
            return getattr(self, self.id)
        else:
            return self.__class__.__name__

    def __repr__(self):
        return "{class_}({kwargs})".format(
            class_=self.__class__.__name__,
            kwargs=', '.join('%s=%r' % pair for pair in self),
        )


class Field(ParsableType):
    id = 'name'
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for fields",
        ): str,
        Required(
            'type',
            msg="The type attribute is mandatory for fields",
        ): str,
        Extra: object,
    }


class Type(ParsableType):
    id = 'name'
    schema = {
        Required('name', msg="The name attribute is mandatory for types"): str,
        Required('fields', default=[]): [Field.parse],
        Extra: object,
    }


class Argument(ParsableType):
    id = 'name'
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for arguments",
        ): str,
        Required('type'): str,
        Required('mode'): Any('in', 'out', 'inout'),
        Extra: object,
    }


class Function(ParsableType):
    id = 'name'
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for functions",
        ): str,
        Required('arguments', default=[]): [Argument.parse],
        Extra: object,
    }


class Definition(ParsableType):
    __slots__ = (
        '_types_map',
    )
    schema = {
        Required('types', default=[]): [Type.parse],
        Required('functions', default=[]): [Function.parse],
    }

    @classmethod
    def merge(cls, *definitions):
        definitions = iter(definitions)
        result = next(definitions)

        for definition in definitions:
            result = Definition(
                types=result.types + definition.types,
                functions=result.functions + definition.functions,
            )

        return result

    def __init__(self, **kwargs):
        super(Definition, self).__init__(**kwargs)

        self._types_map = {}

        for type in self.types:
            if type.name in self._types_map:
                raise DuplicateTypeError(
                    type=type,
                    current_type=self._types_map[type.name],
                )

            self._types_map[type.name] = type

    def get_type(self, type_name):
        return self._types_map.get(type_name)
