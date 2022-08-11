import click
import logging
import importlib
import sys

@click.command()
@click.option('--srcdir', 'src_dir', help = 'path required by the transform set', required=True)
@click.option('--destdir', 'dest_dir', help = 'path to send reassembled ROMs to', required=True)
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
def extract(src_dir, dest_dir, task):
    """Run a task to pull from Steam app or Content pulls (via depot download)"""

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    transform_module = importlib.import_module(f'gex.lib.transforms.{task}')
    transform_module.main(src_dir, dest_dir)
