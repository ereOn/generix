"""
Unit tests for the scripts.
"""

import os
import yaml

from click.testing import CliRunner
from unittest import TestCase

from pygen.scripts import pygen


class ScriptsTests(TestCase):
    index = {
        'targets': {
            'fruits': {
                'source': 'fruit.html',
                'destination': '{{ fruit.name }}.html',
                'scope': 'fruits',
                'alias': 'fruit',
            },
            'error': {
                'source': 'fruit.html',
                'destination': '{{ fruit.name }}.html',
                'scope': 'fruits',
            }
        },
    }
    definition = {
        'fruits': [
            {
                'name': 'apple',
            },
            {
                'name': 'pear',
            },
        ]
    }
    templates = {
        'fruit.html': '<p>{{ fruit.name }}</p>',
    }

    def setUp(self):
        self.runner = CliRunner()

    def test_pygen_no_args(self):
        result = self.runner.invoke(pygen)
        self.assertEqual(2, result.exit_code)
        self.assertEqual('''
Usage: pygen [OPTIONS] TEMPLATES_ROOT DEFINITION_FILE

Error: Missing argument "templates-root".
'''.lstrip(),
            result.output,
        )

    def test_pygen_error(self):
        with self.runner.isolated_filesystem():
            os.makedirs('templates')

            with open(
                os.path.join('templates', 'index.yml'),
                'w',
            ) as index_file:
                yaml.dump(self.index, index_file)

            for template, content in self.templates.items():
                with open(
                    os.path.join('templates', template),
                    'w',
                ) as template_file:
                    template_file.write(content)

            with open('definition.yml', 'w') as definition_file:
                yaml.dump(self.definition, definition_file)

            result = self.runner.invoke(
                pygen,
                ['templates', 'definition.yml'],
            )

        self.assertEqual(1, result.exit_code)
        self.assertEqual(r'''
Successfully loaded definition file at definition.yml.
Loading templates from: templates.
Output root is at: output
[  0%] Generating target `error`.
Error: 'fruit' is undefined
'''.lstrip(),
            result.output,
        )

    def test_pygen_error_debug(self):
        with self.runner.isolated_filesystem():
            os.makedirs('templates')

            with open(
                os.path.join('templates', 'index.yml'),
                'w',
            ) as index_file:
                yaml.dump(self.index, index_file)

            for template, content in self.templates.items():
                with open(
                    os.path.join('templates', template),
                    'w',
                ) as template_file:
                    template_file.write(content)

            with open('definition.yml', 'w') as definition_file:
                yaml.dump(self.definition, definition_file)

            result = self.runner.invoke(
                pygen,
                ['-d', 'templates', 'definition.yml'],
            )

        self.assertEqual(-1, result.exit_code)
        self.assertEqual(r'''
Parsing definition file: definition.yml.
Successfully loaded definition file at definition.yml.
Definition file is as follow:
fruits:
- {name: apple}
- {name: pear}

Loading templates from: templates.
Output root is at: output
[  0%] Generating target `error`.
'''.lstrip(),
            result.output,
        )

    def test_pygen_simple(self):
        with self.runner.isolated_filesystem():
            os.makedirs('templates')

            with open(
                os.path.join('templates', 'index.yml'),
                'w',
            ) as index_file:
                yaml.dump(self.index, index_file)

            for template, content in self.templates.items():
                with open(
                    os.path.join('templates', template),
                    'w',
                ) as template_file:
                    template_file.write(content)

            with open('definition.yml', 'w') as definition_file:
                yaml.dump(self.definition, definition_file)

            result = self.runner.invoke(
                pygen,
                ['-t', 'fruits', 'templates', 'definition.yml'],
            )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(r'''
Successfully loaded definition file at definition.yml.
Loading templates from: templates.
Output root is at: output
[  0%] Generating target `fruits`.
Writing output/apple.html.
Writing output/pear.html.
[100%] Done.
'''.lstrip(),
            result.output,
        )

    def test_pygen_simple_debug(self):
        with self.runner.isolated_filesystem():
            os.makedirs('templates')
            os.makedirs('output')

            with open(
                os.path.join('templates', 'index.yml'),
                'w',
            ) as index_file:
                yaml.dump(self.index, index_file)

            for template, content in self.templates.items():
                with open(
                    os.path.join('templates', template),
                    'w',
                ) as template_file:
                    template_file.write(content)

            with open('definition.yml', 'w') as definition_file:
                yaml.dump(self.definition, definition_file)

            result = self.runner.invoke(
                pygen,
                ['-d', '-t', 'fruits', 'templates', 'definition.yml'],
            )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(r'''
Parsing definition file: definition.yml.
Successfully loaded definition file at definition.yml.
Definition file is as follow:
fruits:
- {name: apple}
- {name: pear}

Loading templates from: templates.
Output root is at: output
[  0%] Generating target `fruits`.
Writing output/apple.html.
Writing output/pear.html.
[100%] Done.
'''.lstrip(),
            result.output,
        )
