"""
Unit tests for the parsers utility functions.
"""

import warnings

from mock import (
    MagicMock,
    patch,
    mock_open,
)
from unittest import TestCase

from pygen.parsers import (
    get_parser_class_map,
    get_parser_for_type,
    read_context_from_url,
)
from pygen.exceptions import NoParserError


class ParsersTests(TestCase):
    @patch('pygen.parsers.pkg_resources.iter_entry_points')
    def test_get_parser_class_map_import_error(self, iter_entry_points):
        entry_point = MagicMock()
        entry_point.load.side_effect = ImportError
        iter_entry_points.return_value = [entry_point]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = get_parser_class_map()

        self.assertEqual({}, result)

    @patch('pygen.parsers.pkg_resources.iter_entry_points')
    def test_get_parser_class_map_registered_twice(self, iter_entry_points):
        class_ = MagicMock()
        class_.mimetypes = ['foo']
        entry_point = MagicMock()
        entry_point.load.return_value = class_

        iter_entry_points.return_value = [
            entry_point,
            entry_point,
        ]

        result = get_parser_class_map()

        self.assertEqual(
            {
                'foo': class_,
            },
            result,
        )

    @patch('pygen.parsers.pkg_resources.iter_entry_points')
    def test_get_parser_class_map_already_registered(self, iter_entry_points):
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

        self.assertEqual(
            {
                'foo': iter_entry_points.return_value[0].load.return_value,
                'bar': iter_entry_points.return_value[1].load.return_value,
            },
            result,
        )

    @patch('pygen.parsers.parser_class_map')
    def test_get_parser_for_type_no_parser_error(self, parser_class_map):
        parser_class_map.get.return_value = None

        with self.assertRaises(NoParserError) as error:
            get_parser_for_type('foo')

        parser_class_map.get.assert_called_once_with('foo')
        self.assertEqual('foo', error.exception.mimetype)
        self.assertEqual(set(), error.exception.mimetypes)

    @patch('pygen.parsers.parser_class_map')
    def test_get_parser_for_type(self, parser_class_map):
        class_ = MagicMock()
        parser_class_map.get.return_value = class_

        result = get_parser_for_type('foo')

        parser_class_map.get.assert_called_once_with('foo')
        self.assertEqual(class_(), result)

    @patch('pygen.parsers.parser_class_map')
    def test_read_context_from_url_file(self, parser_class_map):
        content = 'my_content'
        class_ = MagicMock()
        class_().load.return_value = content
        parser_class_map.get.return_value = class_

        with patch('pygen.parsers.open', mock_open(read_data="foo")):
            result = read_context_from_url('file://foo.txt')

        parser_class_map.get.assert_called_once_with('text/plain')
        self.assertEqual('my_content', result)

    @patch('pygen.parsers.parser_class_map')
    def test_read_context_from_url_http(self, parser_class_map):
        content = 'my_content'
        class_ = MagicMock()
        class_().loads.return_value = content
        parser_class_map.get.return_value = class_
        request = MagicMock()
        request.headers = {'Content-Type': 'text/plain'}

        with patch('pygen.parsers.requests.get', return_value=request):
            result = read_context_from_url('http://foo.txt')

        parser_class_map.get.assert_called_once_with('text/plain')
        self.assertEqual('my_content', result)
