"""
A JSON file parser.
"""

import json


class JsonParser(object):
    extensions = {'.json'}

    def load_from_file(self, file):
        return json.load(file)
