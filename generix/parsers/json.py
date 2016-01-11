"""
A JSON file parser.
"""

import json

from .base import BaseParser


class JsonParser(BaseParser):
    extensions = {'.json'}

    def load(self, file):
        return json.load(file)

    def loads(self, s):
        return json.loads(s)
