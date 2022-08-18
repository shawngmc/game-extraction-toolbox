import click

from .details import details
from .extract import extract
from .list import list

@click.group()
def tasks():
    """Tasks are scripts to extract ROMs from various PC Releases (Steam, GOG, etc.)"""
    pass

tasks.add_command(details)
tasks.add_command(extract)
tasks.add_command(list)