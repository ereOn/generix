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


@click.command(help="Generate code from a definition file.")
@click.option('-d', '--debug', is_flag=True)
@click.argument('definition_file', type=click.File())
def gxgen(debug, definition_file):
    pinfo(
        "Parsing definition file: {definition_filename}.",
        definition_filename=hl(definition_file.name),
    )

    try:
        definition = parse_file(definition_file)

        pinfo(
            "Found {types_count} type(s) and {functions_count} function(s).",
            types_count=hl(len(definition.types)),
            functions_count=hl(len(definition.functions)),
        )

        if debug:
            pinfo(
                "Found types are as follow:\n- {types}",
                types='\n- '.join(
                    identifier(type.name) for type in definition.types,
                ),
            )
            pinfo(
                "Found functions are as follow:\n- {functions}",
                functions='\n- '.join(
                    identifier(function.name)
                    for function in definition.functions,
                ),
            )

    except Exception as ex:
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
