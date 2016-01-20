"""
Templates.
"""

import os

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from .index import Index
from .target import Target
from .scope import Scope


class Templates(object):
    """
    Represents a collection of templates and their index.
    """
    @classmethod
    def from_path(cls, path):
        path = os.path.normpath(os.path.abspath(path))
        loader = FileSystemLoader(path)
        environment = Environment(
            loader=loader,
            keep_trailing_newline=True,
        )

        with open(os.path.join(path, 'index.yml')) as index_file:
            index = Index.load(index_file)

        return cls(environment=environment, index=index)

    def __init__(self, environment, index):
        """
        Initialize a new templates collection.

        :param environment: The Jinja2 template environment.
        :param index: The `Index` associated to those templates.
        """
        self.environment = environment
        self.index = index

    def generate(self, context):
        """
        Generator that yields all the rendered pairs for the targets, using the
        specified context.

        :param context: The root context to use.
        :yields: Triplets of (target_name, filename, content) for the targets.
        """
        for item in self.index.generate(
            environment=self.environment,
            context=context,
        ):
            yield item
