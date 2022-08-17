import click
import click_log
import logging

from gex.commands.archive.archive import archive
from gex.commands.file.file import file
from gex.commands.finder.finder import finder
from gex.commands.postprocess.postprocess import postprocess
from gex.commands.version import version

logger = logging.getLogger('gextoolbox')
click_log.basic_config(logger)

@click.group()
def cli():
    pass

cli.add_command(archive)
cli.add_command(file)
cli.add_command(finder)
cli.add_command(postprocess)
cli.add_command(version)

if __name__ == '__main__':
    cli()