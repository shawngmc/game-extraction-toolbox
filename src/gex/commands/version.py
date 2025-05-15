import click
from  importlib import metadata

@click.command()
def version():
    """Return build info"""
    version = metadata.version('game-extraction-toolbox')
    print(f'Game Extraction Toolbox v{version}')
