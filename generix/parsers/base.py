"""
The base parser.
"""

import os

from functools import partial

from voluptuous import (
    Invalid,
    Required,
    Schema,
)

from ..exceptions import CyclicDependencyError
from ..objects import Definition


class BaseParser(object):
    def get_file_name(self, file):
        return os.path.relpath(os.path.normpath(os.path.abspath(file.name)))

    def parse_data(self, data, stack):
        return Schema({
            Required('requires', default=[]): partial(
                self.parse_files,
                stack=stack,
            ),
            Required('definition'): Definition.parse,
        })(data)

    def parse_files(self, file_names, stack):
        files = []

        for index, file_name in enumerate(file_names):
            try:
                files.append(self.parse_file(file_name, stack=stack))
            except Invalid as ex:
                ex.path = [index]
                raise

        return files

    def parse_file(self, file_name, stack):
        try:
            file = open(file_name)
        except Exception as ex:
            raise Invalid(ex)

        return self.parse(file, stack)

    def parse(self, file, stack=()):
        file_name = self.get_file_name(file)

        if file_name in stack:
            raise CyclicDependencyError(cycle=stack + (file_name,))

        result = self.parse_data(
            self.read_data(file),
            stack=stack + (file_name,),
        )
        return Definition.merge(
            *(result['requires'] + [result['definition']])
        )
