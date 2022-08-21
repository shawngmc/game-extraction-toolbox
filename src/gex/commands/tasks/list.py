import logging
import click
import gex.lib.tasks.impl as impl
from gex.lib.utils import helper

logger = logging.getLogger('gextoolbox')

@click.command(name='list')
def list_cli():
    """List available extraction tasks"""
    for task in impl.__all__:
        task_class = helper.load_task(task)
        if task_class:
            logger.info(f"{task_class.get_task_name().rjust(15, ' ')}: {task_class.get_title()}")
