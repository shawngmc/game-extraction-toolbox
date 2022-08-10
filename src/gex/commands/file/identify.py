import click
from gex.lib.file import identify as identify_plus

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
def identify(in_file):
    type_id = identify_plus.enhanced_magic_from_path(in_file)
    print(type_id)