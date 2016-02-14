import os

from functools import partial
from filecmp import dircmp

from click.testing import CliRunner
from pytest import (
    fixture,
    mark,
)

from pygen.scripts import pygen


@fixture
def chwd(request, folder):
    cwd = os.getcwd()
    os.chdir(folder)
    request.addfinalizer(partial(os.chdir, cwd))
    return folder


@fixture
def runner(chwd):
    cli_runner = CliRunner()

    def run(*args):
        return cli_runner.invoke(pygen, [str(x) for x in args])

    return run


def compare_folders(left, right):
    cmp = dircmp(str(left), str(right))
    assert cmp.left_only == []
    assert cmp.right_only == []
    assert cmp.diff_files == []


@mark.parametrize('folder,index_file,data_file', [
    ('examples/fruits', 'index.yml', 'data.yml'),
    ('examples/vehicles', 'index.yml', 'data.json'),
    ('examples/words', 'index.yml', 'data.yml'),
    ('examples/classes', 'index.yml', 'data.yml'),
])
def test_examples(tmpdir, runner, index_file, data_file):
    result = runner(index_file, data_file, '-o', tmpdir.join('output'))
    assert result.exit_code == 0

    compare_folders('output', tmpdir.join('output'))
