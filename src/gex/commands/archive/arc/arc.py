import click

from .extract import extract

@click.group()
def arc():
    """Operations for Capcom MT Engine ARC Archives"""

arc.add_command(extract)
