"""
Objects.
"""


class Field(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return 'Field(name=%r, type=%r)' % (
            self.name,
            self.type,
        )

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.type == other.type,
        ])

    def __ne__(self, other):
        return not self == other


class Type(object):
    def __init__(self, name, fields):
        self.name = name
        self.fields = list(fields)

    def __repr__(self):
        return 'Type(name=%r, fields=%r)' % (self.name, self.fields)

    def __eq__(self, other):
        return self.name == other.name and self.fields == other.fields

    def __ne__(self, other):
        return not self == other


class Argument(object):
    def __init__(self, name, type, mode):
        self.name = name
        self.type = type
        self.mode = mode

    def __repr__(self):
        return 'Argument(name=%r, type=%r, mode=%r)' % (
            self.name,
            self.type,
            self.mode,
        )

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.type == other.type,
            self.mode == other.mode,
        ])

    def __ne__(self, other):
        return not self == other


class Function(object):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = list(arguments)

    def __repr__(self):
        return 'Function(name=%r, arguments=%r)' % (
            self.name,
            self.arguments,
        )

    def __eq__(self, other):
        return self.name == other.name and self.arguments == other.arguments

    def __ne__(self, other):
        return not self == other


class Definition(object):
    def __init__(self, types, functions):
        self.types = list(types)
        self.functions = list(functions)

    def __repr__(self):
        return 'Definition(types=%r, functions=%r)' % (
            self.types,
            self.functions,
        )

    def __eq__(self, other):
        return self.types == other.types and self.functions == other.functions

    def __ne__(self, other):
        return not self == other
