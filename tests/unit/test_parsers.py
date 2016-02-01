"""
Unit tests for the parsers utility functions.
"""

import warnings
import pytest

from mock import (
    MagicMock,
    patch,
    mock_open,
)

from pygen.parsers import (
    get_parser_class_map,
    get_parser_for_type,
    read_context_from_url,
)
from pygen.exceptions import NoParserError


@patch('pygen.parsers.pkg_resources.iter_entry_points')
def test_get_parser_class_map_import_error(iter_entry_points):
    entry_point = MagicMock()
    entry_point.load.side_effect = ImportError
    iter_entry_points.return_value = [entry_point]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = get_parser_class_map()

    assert result == {}


@patch('pygen.parsers.pkg_resources.iter_entry_points')
def test_get_parser_class_map_registered_twice(iter_entry_points):
    class_ = MagicMock()
    class_.mimetypes = ['foo']
    entry_point = MagicMock()
    entry_point.load.return_value = class_

    iter_entry_points.return_value = [
        entry_point,
        entry_point,
    ]

    result = get_parser_class_map()

    assert result == {
        'foo': class_,
    }


@patch('pygen.parsers.pkg_resources.iter_entry_points')
def test_get_parser_class_map_already_registered(iter_entry_points):
    def get_entry_point_for_mimetypes(mimetypes):
        class_ = MagicMock()
        class_.mimetypes = mimetypes
        entry_point = MagicMock()
        entry_point.load.return_value = class_
        return entry_point

    iter_entry_points.return_value = [
        get_entry_point_for_mimetypes(['foo']),
        get_entry_point_for_mimetypes(['bar', 'foo']),
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = get_parser_class_map()

    assert result == {
        'foo': iter_entry_points.return_value[0].load.return_value,
        'bar': iter_entry_points.return_value[1].load.return_value,
    }


@patch('pygen.parsers.parser_class_map')
def test_get_parser_for_type_no_parser_error(parser_class_map):
    parser_class_map.get.return_value = None

    with pytest.raises(NoParserError) as error:
        get_parser_for_type('foo')

    parser_class_map.get.assert_called_once_with('foo')
    assert error.value.mimetype == 'foo'
    assert error.value.mimetypes == set()


@patch('pygen.parsers.parser_class_map')
def test_get_parser_for_type(parser_class_map):
    class_ = MagicMock()
    parser_class_map.get.return_value = class_

    result = get_parser_for_type('foo')

    parser_class_map.get.assert_called_once_with('foo')
    assert result == class_()


@patch('pygen.parsers.parser_class_map')
def test_read_context_from_url_file(parser_class_map):
    content = 'my_content'
    class_ = MagicMock()
    class_().load.return_value = content
    parser_class_map.get.return_value = class_

    with patch('pygen.parsers.open', mock_open(read_data="foo")):
        result = read_context_from_url('file://foo.txt')

    parser_class_map.get.assert_called_once_with('text/plain')
    assert result == 'my_content'


@patch('pygen.parsers.parser_class_map')
def test_read_context_from_url_http(parser_class_map):
    content = 'my_content'
    class_ = MagicMock()
    class_().loads.return_value = content
    parser_class_map.get.return_value = class_
    request = MagicMock()
    request.headers = {'Content-Type': 'text/plain'}

    with patch('pygen.parsers.requests.get', return_value=request):
        result = read_context_from_url('http://foo.txt')

    parser_class_map.get.assert_called_once_with('text/plain')
    assert result == 'my_content'
