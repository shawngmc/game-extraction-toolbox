import click

from .extract import extract

@click.group()
def kpka():
    """Operations for Capcom RE Engine KPKA Archives"""

kpka.add_command(extract)
