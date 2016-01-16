"""
A YAML file parser.
"""

from __future__ import absolute_import

import yaml

from six import StringIO

from .base import BaseParser


class YamlParser(BaseParser):
    extensions = {'.yml', '.yaml'}

    def load(self, file):
        return yaml.load(file)

    def loads(self, s):
        return yaml.load(StringIO(s))
