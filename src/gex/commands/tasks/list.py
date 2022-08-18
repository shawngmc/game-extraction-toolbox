import click
from gex.lib.transforms import *
import inspect

from gex.lib.utils import helper

@click.command()
def list():
    """List available extraction tasks"""
    for global_name, transform_module in globals().items():
        if inspect.ismodule(transform_module) and transform_module.__package__ == 'gex.lib.transforms':
            helper.task_module_print_header(global_name, transform_module)
