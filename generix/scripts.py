"""
Command line scripts.
"""

import click

from .parsers.yaml import YamlParser


@click.command(help="Generate code from a definition file.")
@click.option('--debug', is_flag=True)
@click.argument('definition_file', type=click.File())
def gxgen(debug, definition_file):
    parser = YamlParser()
    click.echo(definition_file.name)
    click.echo(parser.load_from_file(definition_file))
