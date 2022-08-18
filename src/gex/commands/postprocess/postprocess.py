import click

from .wii.wii import wii

@click.group()
def postprocess():
    """Cleanup Processing for Various Rip Types"""
    pass

postprocess.add_command(wii)