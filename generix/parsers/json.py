"""
A JSON file parser.
"""

import json

from .base import BaseParser


class JsonParser(BaseParser):
    extensions = {'.json'}

    def read_data(self, file):
        return json.load(file)
