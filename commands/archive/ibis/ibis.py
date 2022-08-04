import click

from .extract import extract

@click.group()
def ibis():
    """Operations for Capcom IBIS Archives"""
    pass

ibis.add_command(extract)