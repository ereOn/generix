"""
Base parser tests.
"""

from pygen.parsers.base import BaseParser


def test_register():
    parser = BaseParser()

    # The call does nothing: we just ensure coverage is complete.
    parser.register()
