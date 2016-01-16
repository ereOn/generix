"""
Command line scripts.
"""

import click
import os
import yaml

from .parsers import parse_file
from .templates import TemplatesManager


def hl(obj):
    return click.style(str(obj), fg='yellow', bold=True)


def pinfo(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='white')


def pdebug(msg, *args, **kwargs):
    click.secho(str(msg).format(*args, **kwargs), fg='black', bold=True)


@click.command(help="Generate code from a definition file.")
@click.option(
    '-d',
    '--debug',
    is_flag=True,
    help="Enable debug output and traceback logging. Use this when something "
    "is not working and you really can't figure out what from the error "
    "messages only.",
)
@click.option(
    '-o',
    '--output-root',
    type=click.Path(exists=False),
    default='output',
    help="The default output directory to put generated files in. If no "
    "output directory is specified, the default `output` is used.",
)
@click.option(
    '-t',
    '--target',
    'targets',
    type=str,
    multiple=True,
    help="A target to build. Can be repeated multiple times. If no target "
    "is specified, the default targets are used. If no default targets are "
    "defined, all targets are used.",
)
@click.argument('templates-root', type=click.Path(exists=True))
@click.argument('definition-file', type=click.File())
def pygen(debug, output_root, targets, templates_root, definition_file):
    if debug:
        pdebug(
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
                definition=yaml.dump(definition),
            )

        pinfo(
            "Loading templates from: {templates_root}.",
            templates_root=hl(templates_root),
        )
        templates_manager = TemplatesManager(templates_root)

        pinfo("Output root is at: {output_root}", output_root=hl(output_root))

        try:
            os.makedirs(output_root)
        except OSError:
            pass

        if not targets:
            targets = templates_manager.default_targets

        for index, target_name in enumerate(sorted(targets)):
            progress = float(index) / len(targets)
            pinfo(
                "[{progress:3d}%] Generating target `{target_name}`.",
                progress=int(progress * 100.0),
                target_name=hl(target_name),
            )

            for destination_file_name, content in templates_manager.render(
                target_name,
                definition,
            ):
                output_file_name = os.path.join(
                    output_root,
                    destination_file_name,
                )
                pinfo(
                    "Writing {output_file_name}.",
                    output_file_name=hl(output_file_name.replace('\\', '/')),
                )

                with open(output_file_name, 'w') as destination_file:
                    destination_file.write(content)  # pragma: no branch

        pinfo("[100%] Done.")

    except Exception as ex:
        if debug:
            raise
        else:
            raise click.ClickException(str(ex))
