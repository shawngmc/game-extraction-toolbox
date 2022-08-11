import click
import pkg_resources

@click.command()
def version():
    """Return build info"""
    version = pkg_resources.get_distribution('game-extraction-toolbox').version
    print(f'Game Extraction Toolbox v{version}')
