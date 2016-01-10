"""
Exceptions.
"""


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


class DuplicateTypeError(RuntimeError):
    """
    A type was defined more than once.
    """

    def __init__(self, type, current_type):
        super(DuplicateTypeError, self).__init__(
            "Can't redefine type {type.name!r} as {type!r} since it was "
            "already defined as {current_type!r}.".format(
                type=type,
                current_type=current_type,
            ),
        )
        self.type = type
        self.current_type = current_type


class CyclicDependencyError(RuntimeError):
    """
    An infinite recursion was detected in the requires.
    """

    def __init__(self, cycle):
        super(CyclicDependencyError, self).__init__(
            "An infinite recursion was detected in the `requires` statements. "
            "The cycle is: {cycle}".format(
                cycle=' -> '.join(cycle),
            ),
        )
        self.cycle = cycle
