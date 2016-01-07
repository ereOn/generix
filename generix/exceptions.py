"""
Exceptions.
"""

from voluptuous import Invalid


class NoParserError(RuntimeError):
    """
    No parser was found for a given filename.
    """

    def __init__(self, filename, extensions):
        super(NoParserError, self).__init__(
            "No parser found for file {filename!r}. Supported extensions are: "
            "{extensions}".format(
                filename=filename,
                extensions=', '.join(extensions),
            ),
        )
        self.filename = filename
        self.extensions = extensions


class DuplicateTypeError(Invalid):
    """
    A type was defined more than once.
    """

    def __init__(self, type, current_type):
        super(DuplicateTypeError, self).__init__(
            "Can't redefine type {type.name!r} as {type} since it was already "
            "defined as {current_type}.".format(
                type=type,
                current_type=current_type,
            ),
        )
        self.type = type
        self.current_type = current_type


class UnknownTypeError(Invalid):
    """
    An unknown type was specified.
    """

    def __init__(self, type_name, types):
        super(UnknownTypeError, self).__init__(
            "Unknown type {type_name!r} was not found in: {types}".format(
                type_name=type_name,
                types=list(types),
            ),
        )
        self.type_name = type_name
        self.types = types
