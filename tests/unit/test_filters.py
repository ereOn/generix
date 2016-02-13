"""
Filters unit tests.
"""

from pygen.filters import (
    snake_case,
    camel_case,
    pascal_case,
)


def test_snake_case():
    assert snake_case('') == ''
    assert snake_case('snake_case') == 'snake_case'
    assert snake_case('camelCase') == 'camel_case'
    assert snake_case('PascalCase') == 'pascal_case'
    assert snake_case('getURL') == 'get_url'
    assert snake_case('getHTTPResponseCode') == 'get_http_response_code'


def test_camel_case():
    assert camel_case('') == ''
    assert camel_case('snake_case') == 'snakeCase'
    assert camel_case('camelCase') == 'camelCase'
    assert camel_case('PascalCase') == 'pascalCase'
    assert camel_case('getURL') == 'getURL'
    assert camel_case('getHTTPResponseCode') == 'getHTTPResponseCode'


def test_pascal_case():
    assert pascal_case('') == ''
    assert pascal_case('snake_case') == 'SnakeCase'
    assert pascal_case('camelCase') == 'CamelCase'
    assert pascal_case('PascalCase') == 'PascalCase'
    assert pascal_case('getURL') == 'GetURL'
    assert pascal_case('getHTTPResponseCode') == 'GetHTTPResponseCode'
