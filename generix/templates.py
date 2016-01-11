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
    Required,
    Schema,
)


class TemplatesManager(object):
    def __init__(self, root):
        self.root = os.path.normpath(os.path.abspath(root))
        self.loader = FileSystemLoader(self.root)
        self.environment = Environment(loader=self.loader)

        # Read the index file.
        index_data = yaml.load(open(os.path.join(self.root, 'index.yml')))
        index_schema = Schema({
            Required('targets', default={}): {
                str: {
                    'source': str,
                    'destination': str,
                    'scope': str,
                },
            },
        })
        self.index = index_schema(index_data)

    @property
    def targets(self):
        return self.index['targets']

    def render(self, target_name, definition):
        target = self.targets[target_name]
        template = self.environment.get_template(target['source'])
        kwargs = {
            #TODO: Don't hardcode that.
            'class': definition['classes'][0],
        }
        print(template.render(**kwargs))
