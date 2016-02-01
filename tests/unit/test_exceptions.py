"""
Exceptions tests.
"""

from pygen.exceptions import (
    InvalidScope,
    NoParserError,
)


def test_invalid_scope_instanciation():
    value = InvalidScope(scope=['a', 'b'])
    assert value.scope == ['a', 'b']


def test_no_parser_error_instanciation():
    value = NoParserError(mimetype='foo/bar', mimetypes=['foo/foo'])
    assert value.mimetype == 'foo/bar'
    assert value.mimetypes == ['foo/foo']
