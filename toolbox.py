import click

from commands.archive.archive import archive
from commands.file.file import file
from commands.finder.finder import finder
from commands.postprocess.postprocess import postprocess

@click.group()
def cli():
    pass

cli.add_command(archive)
cli.add_command(file)
cli.add_command(finder)
cli.add_command(postprocess)

if __name__ == '__main__':
    cli()