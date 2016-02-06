"""
Unit tests for scripts.
"""

import os
import yaml

from click.testing import CliRunner
from functools import partial
from pytest import (
    fixture,
    yield_fixture,
)

from pygen.scripts import pygen


@fixture
def runner():
    return CliRunner()


@yield_fixture
def isolated_filesystem(runner):
    with runner.isolated_filesystem() as fs:
        yield fs


@fixture
def run(runner, isolated_filesystem):
    return partial(runner.invoke, pygen)


@fixture
def index_file(tmpdir):
    class IndexFile(object):
        def __init__(self):
            self.file = tmpdir.join('index.yml')
            self.path = str(self.file)

        def write(self, data):
            self.file.write(yaml.dump(data))

    return IndexFile()


@fixture
def context_url(tmpdir):
    class ContextUrl(object):
        def __init__(self):
            self.file = tmpdir.join('data.yml')
            self.path = str(self.file)

        def write(self, data):
            self.file.write(yaml.dump(data))

    return ContextUrl()


@fixture
def template_file(tmpdir):
    class TemplateFile(object):
        def __init__(self):
            self.file = tmpdir.join('template.txt')
            self.path = str(self.file)
            self.name = os.path.basename(self.path)

        def write(self, data):
            self.file.write(data)

    return TemplateFile()


def test_pygen_no_args(run):
    result = run([])
    assert result.exit_code == 2


def test_pygen_simple_run(run, tmpdir, index_file, template_file, context_url):
    index_file.write({
        'targets': {
            'a': {
                'template_name': template_file.name,
                'filename': 'out.txt',
            },
        },
    })
    template_file.write("my file is {{ x }}.")
    context_url.write({
        'x': "nice",
    })

    # We make the output directory ourselves to trigger an non-fatal exception.
    output_root = tmpdir.mkdir('output')
    result = run(['-o', str(output_root), index_file.path, context_url.path])
    assert result.exit_code == 0

    content = tmpdir.join('output', 'out.txt').read()
    assert content == "my file is nice."
