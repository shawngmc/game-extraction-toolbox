import click

from .list import list_files

@click.group(name='zip')
def zip_cli():
    """Operations for ZIP Archives"""

zip_cli.add_command(list_files)
