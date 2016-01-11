"""
A YAML file parser.
"""

import yaml

from .base import BaseParser


class YamlParser(BaseParser):
    extensions = {'.yml', '.yaml'}

    def load(self, file):
        return yaml.load(file)

    def loads(self, s):
        return yaml.loads(s)
