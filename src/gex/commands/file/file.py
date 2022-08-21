import click

from .deinterleave import deinterleave
from .hash import hash_cli
from .identify import identify
from .slice import slice_cli

@click.group()
def file():
    """Generic file operations"""

file.add_command(deinterleave)
file.add_command(hash_cli)
file.add_command(identify)
file.add_command(slice_cli)
