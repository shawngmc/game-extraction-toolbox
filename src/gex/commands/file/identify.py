import logging
import click
import click_log
from gex.lib.file import identify as identify_plus

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click_log.simple_verbosity_option(logger)
def identify(in_file):
    '''Identify a file using libmagic and some custom checks'''
    type_id = identify_plus.enhanced_magic_from_path(in_file)
    logger.info(type_id)
