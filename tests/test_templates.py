"""
Unit tests for templates.
"""

import yaml

from jinja2 import DictLoader
from mock import (
    patch,
    mock_open,
)
from unittest import TestCase

from pygen.templates import TemplatesManager


class TemplatesTests(TestCase):
    definition = {
        'fruits': [
            {
                'name': 'apple',
            },
            {
                'name': 'pear',
            },
        ],
    }
    index = yaml.dump({
        'targets': {
            'apple': {
                'source': 'apple.html',
                'destination': '{{ catalog.fruits[0].name }}.html',
                'alias': 'catalog',
            },
        },
    })
    index_default_targets = yaml.dump({
        'targets': {
            'apple': {
                'source': 'apple.html',
                'destination': '{{ catalog.fruits[0].name }}.html',
                'alias': 'catalog',
            },
            'pear': {
                'source': 'pear.html',
                'destination': '{{ name }}.html',
                'scope': 'fruits.1',
            },
            'fruits': {
                'source': 'fruit.html',
                'destination': '{{ fruit.name }}.html',
                'scope': 'fruits',
                'alias': 'fruit',
            }
        },
        'default_targets': ['apple', 'mango'],
    })
    templates = {
        'apple.html': '<p>{{ catalog.fruits[0].name }}</p>',
        'pear.html': '<p>{{ name }}</p>',
        'fruit.html': '<p>{{ fruit.name }}</p>',
    }

    def setUp(self):
        patcher = patch(
            'pygen.templates.FileSystemLoader',
            return_value=DictLoader(self.templates),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    @patch('pygen.templates.open', mock_open(read_data='{}'))
    def test_templates_manager_default_initialization(self):
        manager = TemplatesManager(root='/foo')
        self.assertEqual({}, manager.targets)
        self.assertEqual({}, manager.default_targets)

    @patch('pygen.templates.open', mock_open(read_data=index))
    def test_templates_manager_initialization(self):
        manager = TemplatesManager(root='/foo')
        self.assertEqual({'apple'}, set(manager.targets))
        self.assertEqual({'apple'}, set(manager.default_targets))

    @patch('pygen.templates.open', mock_open(read_data=index_default_targets))
    def test_templates_manager_initialization_with_default_targets(self):
        manager = TemplatesManager(root='/foo')
        self.assertEqual({'apple', 'pear', 'fruits'}, set(manager.targets))
        self.assertEqual({'apple'}, set(manager.default_targets))

    @patch('pygen.templates.open', mock_open(read_data=index_default_targets))
    def test_templates_manager_render(self):
        manager = TemplatesManager(root='/foo')

        results = manager.render('apple', self.definition)

        file_name, content = next(results)
        self.assertEqual('apple.html', file_name)
        self.assertEqual('<p>apple</p>', content)

        with self.assertRaises(StopIteration):
            next(results)

        results = manager.render('pear', self.definition)

        file_name, content = next(results)
        self.assertEqual('pear.html', file_name)
        self.assertEqual('<p>pear</p>', content)

        with self.assertRaises(StopIteration):
            next(results)

        results = manager.render('fruits', self.definition)

        file_name, content = next(results)
        self.assertEqual('apple.html', file_name)
        self.assertEqual('<p>apple</p>', content)

        file_name, content = next(results)
        self.assertEqual('pear.html', file_name)
        self.assertEqual('<p>pear</p>', content)

        with self.assertRaises(StopIteration):
            next(results)
