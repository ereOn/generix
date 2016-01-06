from setuptools import (
    setup,
    find_packages,
)

setup(
    name='generix',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    maintainer='Julien Kauffmann',
    maintainer_email='julien.kauffmann@freelan.org',
    version=open('VERSION').read().strip(),
    description=(
        "A flexible code generator tool."
    ),
    long_description="""\
generix is a flexible and extensible code generator tool.
""",
    packages=find_packages(exclude=[
        'tests',
    ]),
    install_requires=[
        'six==1.9.0',
        'Jinja2==2.8',
        'click==6.2',
        'PyYAML==3.11',
        'voluptuous==0.8.8',
    ],
    entry_points={
        'console_scripts': [
            'gxgen = generix.scripts:gxgen',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
    ],
)
