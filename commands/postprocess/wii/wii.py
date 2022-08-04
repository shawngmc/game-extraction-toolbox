import click

from .cleanrip import cleanrip

@click.group()
def wii():
    """Cleanup Processing Wii Rips"""
    pass

wii.add_command(cleanrip)