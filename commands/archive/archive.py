import click

from .arc.arc import arc
from .ibis.ibis import ibis
from .kpka.kpka import kpka

@click.group()
def archive():
    """Tools for working with various types of archives"""
    pass

archive.add_command(arc)
archive.add_command(ibis)
archive.add_command(kpka)