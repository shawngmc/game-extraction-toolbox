import click
from gex.lib.transforms import *
import inspect

@click.command()
def list():
    """List Available Tasks"""
    for global_name, transform_module in globals().items():
        if inspect.ismodule(transform_module) and transform_module.__package__ == 'gex.lib.transforms':
            print(f'{global_name}: {transform_module.title}')
            if len(transform_module.description) > 0:
                print(f'  {transform_module.description}')
            print(f'  Expected input dir: {transform_module.in_dir_desc} (ex. {transform_module.default_folder})')
