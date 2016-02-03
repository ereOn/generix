"""
Target unit tests.
"""

from pytest import (
    fixture,
    raises,
)

from jinja2 import (
    Environment,
    DictLoader,
)

from pygen.scope import Scope
from pygen.target import Target


@fixture
def context():
    return {
        'a': {
            'b': 'c',
            'd': 'e',
        },
        'f': 'g',
        'h': [
            'i',
            'j',
            'k',
        ],
        'l': [
            'm',
            'n',
        ],
    }


def test_generate_scoped_contexts_no_scopes(context):
    target = Target(
        template_name='foo.txt.tpl',
        filename='foo.txt',
        scopes={},
    )
    result = target.generate_scoped_contexts(context)
    assert next(result) == context

    with raises(StopIteration):
        next(result)


def test_generate_scoped_contexts_simple_scopes(context):
    target = Target(
        template_name='foo.txt.tpl',
        filename='foo.txt',
        scopes={
            'one': Scope(['a', 'b']),
            'two': Scope(['f']),
            'three': Scope(['h']),
        },
    )
    result = target.generate_scoped_contexts(context)
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': ['i', 'j', 'k'],
    }

    with raises(StopIteration):
        next(result)


def test_generate_scoped_contexts_iterable_scopes(context):
    target = Target(
        template_name='foo.txt.tpl',
        filename='foo.txt',
        scopes={
            'one': Scope(['a', 'b']),
            'two': Scope(['f']),
            'three': Scope(['h'], is_iterable=True),
            'four': Scope(['l'], is_iterable=True),
        },
    )
    result = target.generate_scoped_contexts(context)
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'i',
        'four': 'm',
    }
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'j',
        'four': 'm',
    }
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'k',
        'four': 'm',
    }
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'i',
        'four': 'n',
    }
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'j',
        'four': 'n',
    }
    assert next(result) == {
        'one': 'c',
        'two': 'g',
        'three': 'k',
        'four': 'n',
    }

    with raises(StopIteration):
        next(result)


def test_get_template():
    target = Target(
        template_name='foo.txt.tpl',
        filename='foo{{ x }}.txt',
        scopes={},
    )
    environment = Environment(loader=DictLoader({
        'foo.txt.tpl': 'foo {{ x }}',
    }))
    target_template = target.get_template(environment)
    assert target_template.template.render({'x': 42}) == 'foo 42'
    assert target_template.filename_template.render({'x': 42}) == 'foo42.txt'


def test_generate():
    target = Target(
        template_name='foo.txt.tpl',
        filename='foo{{ x }}.txt',
        scopes={'x': Scope.from_string('numbers...')},
    )
    environment = Environment(loader=DictLoader({
        'foo.txt.tpl': 'foo {{ x }}',
    }))
    context = {'numbers': [42, 7]}
    result = target.generate(environment, context)

    assert next(result) == ('foo42.txt', 'foo 42')
    assert next(result) == ('foo7.txt', 'foo 7')

    with raises(StopIteration):
        next(result)
