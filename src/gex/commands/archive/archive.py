import click

from .arc.arc import arc
from .kpka.kpka import kpka

@click.group()
def archive():
    """Tools for working with various types of archives"""

archive.add_command(arc)
archive.add_command(kpka)
