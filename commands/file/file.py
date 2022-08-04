import click

from .deinterleave import deinterleave
from .identify import identify
from .slice import slice

@click.group()
def file():
    """Generic file operations"""
    pass

file.add_command(deinterleave)
file.add_command(identify)
file.add_command(slice)