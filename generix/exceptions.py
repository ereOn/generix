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
