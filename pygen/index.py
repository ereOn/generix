"""
Index class.
"""

import yaml

from voluptuous import (
    Required,
    Schema,
)

from .scope import Scope
from .target import Target


class Index(object):
    """
    An index is a collection of targets.
    """
    @classmethod
    def load(cls, stream):
        data = yaml.load(stream)
        schema = Schema({
            Required('targets', default={}): {
                str: {
                    'template_name': str,
                    'filename': str,
                    Required('scopes', default={}): {
                        str: Scope.from_string
                    },
                },
            },
        })
        targets = {
            target_name: Target(**target)
            for target_name, target in schema(data)['targets'].items()
        }
        return cls(targets=targets)

    def __init__(self, targets):
        """
        Initialize a new index.

        :param targets: A dictionary of targets indexed by their names.
        """
        self.targets = targets

    def generate(self, environment, context):
        """
        Generator that yields all the rendered pairs for the targets, using the
        specified environment and context.

        :param environment: The Jinja2 template environment.
        :param context: The root context to use.
        :yields: Triplets of (target_name, filename, content) for the targets.
        """
        for target_name, target in self.targets.items():
            for filename, content in target.generate(
                environment=environment,
                context=context,
            ):
                yield target_name, filename, content
