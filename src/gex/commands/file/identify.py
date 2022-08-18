import click
import click_log
import logging

logger = logging.getLogger('gextoolbox')

from gex.lib.file import identify as identify_plus

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click_log.simple_verbosity_option(logger)
def identify(in_file):
    type_id = identify_plus.enhanced_magic_from_path(in_file)
    logger.info(type_id)