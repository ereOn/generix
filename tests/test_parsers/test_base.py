"""
Tests for the base parser.
"""

from unittest import TestCase

from pygen.parsers.base import BaseParser


class BaseParserTests(TestCase):
    def test_register(self):
        # This is just to satisfy coverage.
        BaseParser.register()
