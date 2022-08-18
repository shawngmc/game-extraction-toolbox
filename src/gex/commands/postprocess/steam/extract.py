import click
import importlib
import click_log
import logging

from gex.lib.utils import helper

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--srcdir', 'src_dir', help = 'path required by the transform set', required=True)
@click.option('--destdir', 'dest_dir', help = 'path to send reassembled ROMs to', required=True)
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
@click_log.simple_verbosity_option(logger)
def extract(src_dir, dest_dir, task):
    """Run a task to pull from Steam app or Content pulls (via depot download)"""

    # Ensure the output folder exists or can be made
    helper.preparepath(dest_dir)

    transform_module = importlib.import_module(f'gex.lib.transforms.{task}')
    transform_module.main(src_dir, dest_dir)
