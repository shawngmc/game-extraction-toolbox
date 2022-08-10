import click

from gex.commands.archive.archive import archive
from gex.commands.file.file import file
from gex.commands.finder.finder import finder
from gex.commands.postprocess.postprocess import postprocess

@click.group()
def cli():
    pass

cli.add_command(archive)
cli.add_command(file)
cli.add_command(finder)
cli.add_command(postprocess)

if __name__ == '__main__':
    cli()