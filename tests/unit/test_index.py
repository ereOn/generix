"""
Index tests.
"""

import yaml

from mock import (
    MagicMock,
    patch,
)
from six import StringIO
from jinja2 import (
    Environment,
    PrefixLoader,
    FileSystemLoader,
)

from pygen.index import Index
from pygen.scope import Scope
from pygen.target import Target


def test_load_no_template_paths():
    stream = StringIO()
    yaml.dump({}, stream)
    stream.seek(0)
    index = Index.load('', stream)
    assert index.targets == {}
    assert index.environment.keep_trailing_newline
    assert isinstance(index.environment.loader, FileSystemLoader)


def test_load_template_paths():
    stream = StringIO()
    yaml.dump({
        'template_paths': {
            'foo': 'foo',
            'bar': 'bar',
        },
    }, stream)
    stream.seek(0)
    index = Index.load('', stream)
    assert index.targets == {}
    assert index.environment.keep_trailing_newline
    assert isinstance(index.environment.loader, PrefixLoader)


@patch('pygen.index.Target', spec=Target)
def test_load_targets(target):
    stream = StringIO()
    yaml.dump({
        'targets': {
            'foo': {
                'template_name': 'foo.txt.tpl',
                'filename': 'foo.txt',
                'scopes': {
                    'path': 'path',
                },
            },
        },
    }, stream)
    stream.seek(0)
    index = Index.load('', stream)
    target.assert_called_once_with(
        filename='foo.txt',
        template_name='foo.txt.tpl',
        scopes={
            'path': Scope(['path']),
        },
    )
    assert index.targets == {
        'foo': target(),
    }


def test_generate():
    targets = {
        'foo': MagicMock(spec=Target),
        'bar': MagicMock(spec=Target),
    }
    targets['foo'].generate.return_value = (
        ('foo1', 'myfoo1'),
        ('foo2', 'myfoo2'),
    )
    targets['bar'].generate.return_value = (
        ('bar1', 'mybar1'),
    )
    context = {}
    index = Index(environment=MagicMock(spec=Environment), targets=targets)
    result = list(index.generate(context=context))

    assert result == [
        ('bar', 'bar1', 'mybar1'),
        ('foo', 'foo1', 'myfoo1'),
        ('foo', 'foo2', 'myfoo2'),
    ]
