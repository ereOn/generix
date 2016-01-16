"""
Tests for the JSON parser.
"""

from unittest import TestCase

from pygen.parsers.json import JsonParser
from six import StringIO


class JsonParserTests(TestCase):
    def setUp(self):
        self.parser = JsonParser()

    def test_load(self):
        file = StringIO('{"a": 1}')
        result = self.parser.load(file=file)
        self.assertEqual({'a': 1}, result)

    def test_loads(self):
        result = self.parser.loads('{"a": 1}')
        self.assertEqual({'a': 1}, result)
