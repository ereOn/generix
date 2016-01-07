"""
A JSON file parser.
"""

import json

from .base import BaseParser


class JsonParser(BaseParser):
    extensions = {'.json'}

    def load_from_file(self, file):
        return self.validate(json.load(file))
