import os
import logging
import click
import click_log

from gex.lib.utils import helper

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--srcdir', 'src_dir',
    help = 'path required by the transform set - see task for details', default=None)
@click.option('--destdir', 'dest_dir', help = 'path to send reassembled ROMs to', required=True)
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
@click.option("--prop", 'props', multiple=True, help = 'per task config options; see task details for supported options', default=[])
@click_log.simple_verbosity_option(logger)
def extract(src_dir, dest_dir, task, props):
    """Run a task to extract roms from Steam/GOG/etc. games"""

    # Load the task module
    task_class = helper.load_task(task)

    # If there isn't a src_dir set, pull in the default
    if not src_dir:
        src_dir = task_class.get_default_input_folder()
        # If there isn't a default, exit
        if not src_dir:
            logger.error(f"Task {task} requires a source dir; see task details for more info")
            exit()

    # Make sure input dir exists
    if not os.path.exists(src_dir):
        logger.error(f"Source dir {src_dir} does not exist; see task details for more info")
        exit()

    # Ensure the output folder exists or can be made
    helper.preparepath(dest_dir)

    task_class.set_props(props)

    task_class.execute(src_dir, dest_dir)
