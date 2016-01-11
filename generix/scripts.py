"""
Command line scripts.
"""

import click

from .parsers import parse_file


def hl(obj):
    return click.style(str(obj), fg='yellow', bold=True)


def identifier(obj):
    return click.style(str(obj), fg='cyan', bold=True)


def pinfo(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='white')


def pdebug(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='black', bold=True)


def perror(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='red', bold=True)


@click.command(help="Generate code from a definition file.")
@click.option('-d', '--debug', is_flag=True)
@click.argument('definition_file', type=click.File())
def gxgen(debug, definition_file):
    pinfo(
        "Parsing definition file: {definition_file_name}.",
        definition_file_name=hl(definition_file.name),
    )

    try:
        definition = parse_file(definition_file)

        pinfo(
            "Successfully loaded definition file at {definition_file_name}.",
            definition_file_name=hl(definition_file.name),
        )

        if debug:
            pdebug(
                "Definition file is as follow:\n{definition}",
                definition=definition,
            )

    except Exception as ex:
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
