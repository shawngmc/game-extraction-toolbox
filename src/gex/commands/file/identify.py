import logging
import click
import click_log
from gex.lib.file import identify as identify_plus

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click_log.simple_verbosity_option(logger)
def identify(in_file):
    '''Identify a file using some custom libmagic-style checks'''
    type_id = identify_plus.custom_magic_from_path(in_file)
    logger.info(type_id)
