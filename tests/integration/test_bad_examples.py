import os

from functools import partial

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


@mark.parametrize('folder,index_file,data_file', [
    ('bad_examples/invalid_scope', 'index.yml', 'data.yml'),
])
def test_examples(tmpdir, runner, index_file, data_file):
    result = runner(index_file, data_file, '-o', tmpdir.join('output'))
    assert result.exit_code == -1
