import click

from .bulk import bulk

@click.group()
def finder():
    """Search operations"""
    pass

finder.add_command(bulk)