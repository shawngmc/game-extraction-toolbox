import logging
import os
import click
import click_log
from gex.lib.utils.blob import hash as hash_helper

logger = logging.getLogger('gextoolbox')

@click.command(name="hash")
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--type', 'hash_type', help = 'type of checksum/hash to calculate',
    type=click.Choice(['CRC', 'MD5', 'SHA1'], case_sensitive=False), required=True)
@click_log.simple_verbosity_option(logger)
def hash_cli(in_file, hash_type):
    '''CLI tool to hash a file with the specified algorithm'''
    try:
        with open(in_file, "rb") as file:
            in_data = file.read()
    except IOError:
        logger.error(f"Error reading {in_file}!")
        exit()

    if hash_type == 'CRC':
        checksum = hash_helper.get_crc(in_data)
    elif hash_type == 'MD5':
        checksum = hash_helper.get_md5(in_data)
    elif hash_type == 'SHA1':
        checksum = hash_helper.get_sha1(in_data)

    logger.info(f'{os.path.basename(in_file)} {hash_type}: {checksum}')
