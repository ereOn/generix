"""
JsonParser tests.
"""

from mock import (
    call,
    patch,
)
from six import StringIO

from pygen.parsers.json import JsonParser


@patch('mimetypes.add_type')
def test_register(add_type):
    JsonParser.register()
    assert add_type.mock_calls == [
        call('application/json', '.json'),
        call('text/json', '.json'),
    ]


def test_load():
    parser = JsonParser()
    result = parser.load(StringIO("[1, 2, 3]"))
    assert result == [1, 2, 3]


def test_loads():
    parser = JsonParser()
    result = parser.loads("[1, 2, 3]")
    assert result == [1, 2, 3]
