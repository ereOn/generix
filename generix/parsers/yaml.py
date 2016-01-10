"""
A YAML file parser.
"""

import yaml

from .base import BaseParser


class YamlParser(BaseParser):
    extensions = {'.yml', '.yaml'}

    def read_data(self, file):
        return yaml.load(file)
