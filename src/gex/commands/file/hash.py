import os
import click
import click_log
import logging

from gex.lib.utils.blob.transforms import hash

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--type', 'hash_type', help = 'type of checksum/hash to calculate', type=click.Choice(['CRC', 'MD5', 'SHA1'], case_sensitive=False), required=True)
@click_log.simple_verbosity_option(logger)
def hash(in_file, hash_type):
    try: 
        with open(in_file, "rb") as f:
            in_data = f.read()
    except IOError:
        logger.error(f"Error reading {in_file}!")
        exit()
    
    if hash_type == 'CRC':
        checksum = hash.get_crc(in_data)
    elif hash_type == 'MD5':
        checksum = hash.get_md5(in_data)
    elif hash_type == 'SHA1':
        checksum = hash.get_sha1(in_data)

    logger.info(f'{os.path.basename(in_file)} {hash_type}: {checksum}')
