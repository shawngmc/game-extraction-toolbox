import logging
import click
import gex.lib.tasks.impl as impl

logger = logging.getLogger('gextoolbox')

from gex.lib.utils import helper

@click.command()
def list():
    """List available extraction tasks"""
    for task in impl.__all__:
        task_class = helper.load_task(task)
        if task_class:
            logger.info(f"{task_class.get_task_name().rjust(10, ' ')}: {task_class.get_title()}")
