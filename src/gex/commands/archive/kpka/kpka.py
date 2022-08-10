import click

from .extract import extract

@click.group()
def kpka():
    """Operations for Capcom RE Engine KPKA Archives"""
    pass

kpka.add_command(extract)