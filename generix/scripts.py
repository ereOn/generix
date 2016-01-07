"""
Command line scripts.
"""

import click

from .parsers import (
    merge_definitions,
    parse_files,
)


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
@click.argument('definition_files', nargs=-1, type=click.File())
def gxgen(debug, definition_files):
    pinfo(
        "Parsing definition file(s): {definition_filenames}.",
        definition_filenames=', '.join(hl(df.name) for df in definition_files),
    )

    try:
        definitions = parse_files(*definition_files)
        definition = merge_definitions(*definitions)

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
