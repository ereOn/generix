"""
Command line scripts.
"""

import click
import os

from .parsers import parse_file
from .templates import TemplatesManager


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
@click.argument('templates-root', type=click.Path(exists=True))
@click.argument('definition-file', type=click.File())
@click.option(
    '-o',
    '--output-root',
    type=click.Path(exists=False),
    default='output',
)
def gxgen(debug, templates_root, definition_file, output_root):
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

        pinfo(
            "Loading templates from: {templates_root}.",
            templates_root=hl(templates_root),
        )
        templates_manager = TemplatesManager(templates_root)

        pinfo("Output root is at: {output_root}", output_root=hl(output_root))

        try:
            os.makedirs(output_root)
        except IOError:
            pass

        for target_name in templates_manager.targets:
            templates_manager.render(target_name, definition)

    except Exception as ex:
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
