"""
Objects.
"""

from functools import partial
from itertools import chain
from six import add_metaclass
from voluptuous import (
    Any,
    Required,
    Schema,
    UNDEFINED,
)


class ParsableTypeMeta(type):
    def __new__(cls, name, bases, attrs):
        schema = attrs.pop('schema', {})
        attrs['_fields'] = list(map(str, schema))
        attrs['_defaults'] = {
            str(key): key.default()
            for key in schema
            if hasattr(key, 'default') and key.default is not UNDEFINED
        }
        attrs['__slots__'] = attrs['_fields'] + ['_extra']
        attrs['_schema'] = Schema(schema)
        return super(ParsableTypeMeta, cls).__new__(cls, name, bases, attrs)


@add_metaclass(ParsableTypeMeta)
class ParsableType(object):
    id = 'name'

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
            return super(ParsableType, self).__getattr__(key)

    def __iter__(self):
        return chain(
            [(self.id, getattr(self, self.id))],
            (
                (key, getattr(self, key))
                for key in self._fields
                if key != self.id
            ),
            self._extra.items(),
        )

    def __str__(self):
        return getattr(self, self.id)

    def __repr__(self):
        return "{class_}({kwargs})".format(
            class_=self.__class__.__name__,
            kwargs=', '.join('%r=%r' % pair for pair in self),
        )


class Indirection(object):
    def __init__(self, method, key):
        self.method = method
        self.key = str(key)

    def __str__(self):
        return self.key

    def __repr__(self):
        return "{class_}({kwargs})".format(
            class_=self.__class__.__name__,
            kwargs=', '.join('%r=%r' % pair for pair in self.__dict__.items()),
        )

    @classmethod
    def linked_to(cls, method):
        def validator(value):
            return Indirection(method=method, key=value)

        return validator


class Field(ParsableType):
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for fields",
        ): str,
        Required(
            'type',
            msg="The type attribute is mandatory for fields",
        ): Indirection.linked_to('get_type'),
    }


class Type(ParsableType):
    schema = {
        Required('name', msg="The name attribute is mandatory for types"): str,
        Required('fields', default=[]): [Field.parse],
    }


class Argument(ParsableType):
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for arguments",
        ): str,
        Required('type'): Indirection.linked_to('get_type'),
        Required('mode'): Any('in', 'out', 'inout'),
    }


class Function(ParsableType):
    schema = {
        Required(
            'name',
            msg="The name attribute is mandatory for functions",
        ): str,
        Required('arguments', default=[]): [Argument.parse],
    }


class Definition(ParsableType):
    schema = {
        Required('requires', default=[]): [str],
        Required('types', default=[]): [Type.parse],
        Required('functions', default=[]): [Function.parse],
    }
