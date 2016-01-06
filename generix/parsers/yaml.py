"""
A YAML file parser.
"""

import yaml

from .base import BaseParser


class YamlParser(BaseParser):
    def load_from_file(self, file):
        return self.validate(yaml.load(file))
