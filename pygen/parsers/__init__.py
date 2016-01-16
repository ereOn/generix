"""
Common parser methods.
"""

import os
import pkg_resources
import warnings

from ..exceptions import NoParserError


def get_parser_class_map():
    result = {}

    for entry_point in pkg_resources.iter_entry_points(
        group='pygen_parsers',
    ):
        try:
            class_ = entry_point.load()
        except ImportError as ex:
            warnings.warn(
                "Exception while loading pygen parser %r. It won't be "
                "available. Exception was: %s" % (entry_point.name, ex),
                RuntimeWarning,
            )
            continue

        for extension in class_.extensions:
            if extension in result:
                current_class = result[extension]

                if current_class != class_:
                    warnings.warn(
                        "Could not register extension %r with parser %r as it "
                        "is already registered with a different parser "
                        "(%r)." % (
                            extension,
                            class_,
                            current_class,
                        ),
                        RuntimeWarning,
                    )
            else:
                result[extension] = class_

    return result


parser_class_map = get_parser_class_map()


def get_parser_from_file_name(file_name):
    extension = os.path.splitext(file_name)[-1]
    parser_class = parser_class_map.get(extension)

    if not parser_class:
        raise NoParserError(
            filename=file_name,
            extensions=set(parser_class_map),
        )

    return parser_class()


def get_parser_from_file(file):
    return get_parser_from_file_name(file_name=file.name)


def parse_file(file):
    parser = get_parser_from_file(file)
    return parser.load(file)
