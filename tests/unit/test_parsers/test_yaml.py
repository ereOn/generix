"""
JsonParser tests.
"""

from mock import (
    call,
    patch,
)
from six import StringIO

from pygen.parsers.yaml import YamlParser


@patch('mimetypes.add_type')
def test_register(add_type):
    YamlParser.register()
    assert add_type.mock_calls == [
        call('application/vnd.yaml', '.yaml'),
        call('application/vnd.yaml', '.yml'),
        call('application/x-yaml', '.yaml'),
        call('application/x-yaml', '.yml'),
        call('application/yaml', '.yaml'),
        call('application/yaml', '.yml'),
        call('text/vnd.yaml', '.yaml'),
        call('text/vnd.yaml', '.yml'),
        call('text/x-yaml', '.yaml'),
        call('text/x-yaml', '.yml'),
        call('text/yaml', '.yaml'),
        call('text/yaml', '.yml'),
    ]


def test_load():
    parser = YamlParser()
    result = parser.load(StringIO("[1, 2, 3]"))
    assert result == [1, 2, 3]


def test_loads():
    parser = YamlParser()
    result = parser.loads("[1, 2, 3]")
    assert result == [1, 2, 3]
