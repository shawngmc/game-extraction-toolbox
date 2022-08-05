import click
import os
import glob
import importlib

@click.command()
def list():
    """List Available Tasks"""
    available_libs = glob.glob(os.path.join('lib', 'transforms', '*.py'))
    
    for available_lib in available_libs:
        module_name = os.path.splitext(os.path.basename(available_lib))[0]
        transform_module = importlib.import_module(f'lib.transforms.{module_name}')
        print(f'{module_name}: {transform_module.title}')
        print(f'  {transform_module.description}')
        print(f'  Expected input dir: {transform_module.in_dir_desc}')
