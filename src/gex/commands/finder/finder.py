import click

from .bulk import bulk

@click.group()
def finder():
    """Search operations"""

finder.add_command(bulk)
