"""
Common parser methods.
"""

import os
import pkg_resources
import warnings

from ..exceptions import (
    NoParserError,
    CyclicDependencyError,
)
from ..objects import Definition


def get_parser_class_map():
    result = {}

    for entry_point in pkg_resources.iter_entry_points(
        group='generix_parsers',
    ):
        try:
            class_ = entry_point.load()
        except ImportError as ex:
            warnings.warn(
                "Exception while loading generix parser %r. It won't be "
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


def get_parser_from_file(file):
    extension = os.path.splitext(file.name)[-1]
    parser_class = parser_class_map.get(extension)

    if not parser_class:
        raise NoParserError(
            filename=file.name,
            extensions=set(parser_class_map),
        )

    return parser_class()


def merge_definitions(*definitions):
    definitions = iter(definitions)
    definition = next(definitions)

    for d in definitions:
        definition = Definition(
            requires=[],
            types=definition.types + d.types,
            functions=definition.functions + d.functions,
        )

    return definition


def parse_file(file, requires=()):
    name = os.path.normpath(os.path.abspath(file.name))

    if name in requires:
        raise CyclicDependencyError(cycle=requires + (name,))

    dir_path = os.path.dirname(name)
    definition = get_parser_from_file(file).load_from_file(file)

    return merge_definitions(*[
        parse_file(
            open(os.path.join(dir_path, require)),
            requires=requires + (name,),
        )
        for require in definition.requires
    ] + [definition])
