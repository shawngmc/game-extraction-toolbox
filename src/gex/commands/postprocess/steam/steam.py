import click

from .details import details
from .extract import extract
from .list import list

@click.group()
def steam():
    """Extract from Steam Apps"""
    pass

steam.add_command(details)
steam.add_command(extract)
steam.add_command(list)