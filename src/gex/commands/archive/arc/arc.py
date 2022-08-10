import click

from .extract import extract

@click.group()
def arc():
    """Operations for Capcom MT Engine ARC Archives"""
    pass

arc.add_command(extract)