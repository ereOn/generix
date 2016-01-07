"""
Command line scripts.
"""

import click

from .parsers import parse_file

def hl(obj):
    return click.style(str(obj), fg='yellow', bold=True)

def pinfo(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='white')

def pdebug(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='black', bold=True)


@click.command(help="Generate code from a definition file.")
@click.option('--debug', is_flag=True)
@click.argument('definition_file', type=click.File())
def gxgen(debug, definition_file):
    pinfo(
        "Parsing definition file at {definition_filename}.",
        definition_filename=hl(definition_file.name),
    )

    try:
        definition = parse_file(definition_file)

        pinfo(
            "Found {types_count} type(s) and {functions_count} function(s).",
            types_count=hl(len(definition.types)),
            functions_count=hl(len(definition.functions)),
        )
    except RuntimeError as ex:
        raise click.ClickException(str(ex))
