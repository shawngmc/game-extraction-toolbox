import logging
import click
import click_log

from gex.commands.archive.archive import archive
from gex.commands.file.file import file
from gex.commands.finder.finder import finder
from gex.commands.postprocess.postprocess import postprocess
from gex.commands.tasks.tasks import tasks
from gex.commands.version import version

logger = logging.getLogger('gextoolbox')
logger.setLevel(logging.INFO)
click_log.basic_config(logger)

@click.group()
def cli():
    pass

cli.add_command(archive)
cli.add_command(file)
cli.add_command(finder)
cli.add_command(postprocess)
cli.add_command(tasks)
cli.add_command(version)

if __name__ == '__main__':
    cli()
