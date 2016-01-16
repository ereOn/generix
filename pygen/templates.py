"""
Templates.
"""

import os
import yaml

from jinja2 import (
    Environment,
    FileSystemLoader,
)
from voluptuous import (
    Any,
    Required,
    Schema,
)

from .scope import (
    Scope,
    parse_scope,
)


class TemplatesManager(object):
    def __init__(self, root):
        self.root = os.path.normpath(os.path.abspath(root))
        self.loader = FileSystemLoader(self.root)
        self.environment = Environment(
            loader=self.loader,
            keep_trailing_newline=True,
        )

        # Read the index file.
        index_data = yaml.load(open(os.path.join(self.root, 'index.yml')))
        index_schema = Schema({
            Required('targets', default={}): {
                str: {
                    'source': self.environment.get_template,
                    'destination': self.environment.from_string,
                    Required('scope', default=Scope()): parse_scope,
                    Required('alias', default=None): Any(None, str),
                },
            },
            Required('default_targets', default=[]): [str],
        })
        self.index = index_schema(index_data)

    @property
    def default_targets(self):
        targets = self.index['default_targets']

        if targets:
            return {
                target: value
                for target, value in self.targets.items()
                if target in targets
            }
        else:
            return self.targets

    @property
    def targets(self):
        return self.index['targets']

    def render(self, target_name, definition):
        """
        Render a target according to a specified definition.

        :param target_name: The target name.
        :paran definition: The definition.
        :yields: Tuples of (destination_file_name, content).

        .. note::
            Unless they are absolute, filenames are relative to the output
            directory.
        """
        target = self.targets[target_name]
        source = target['source']
        destination = target['destination']
        scope = target['scope']
        alias = target['alias']
        context = scope.resolve(definition)

        if not isinstance(context, (list, tuple)):
            context = [context]

        if alias:
            context = [{alias: ctx} for ctx in context]

        for kwargs in context:
            yield destination.render(**kwargs), source.render(**kwargs)
