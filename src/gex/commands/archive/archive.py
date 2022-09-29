import click

from .arc.arc import arc
from .kpka.kpka import kpka
from .zip.zip import zip_cli

@click.group()
def archive():
    """Tools for working with various types of archives"""

archive.add_command(arc)
archive.add_command(kpka)
archive.add_command(zip_cli)
