#!/usr/bin/env python

from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'bplist',
        'Click',
        'psutil',
        'python-magic-bin',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'gextoolbox = gex.toolbox:cli'
        ]
    }
)