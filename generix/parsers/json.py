"""
A JSON file parser.
"""

import json


class JsonParser(object):
    def load_from_file(self, file):
        return json.load(file)
