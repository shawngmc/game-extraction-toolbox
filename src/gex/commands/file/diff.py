import json
import logging
import os
import click
import click_log
from texttable import Texttable
from gex.lib.utils.blob import hash as hash_helper

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--1', 'file_1', help = 'path to input file 1', required=True)
@click.option('--2', 'file_2', help = 'path to input file 2', required=True)
@click_log.simple_verbosity_option(logger)
def diff(file_1, file_2):
    '''Smarter non-interactive diff tool'''
    try:
        with open(file_1, "rb") as file:
            contents_1 = file.read()
    except IOError:
        logger.error(f"Error reading {file_1}!")
        exit()
    try:
        with open(file_2, "rb") as file:
            contents_2 = file.read()
    except IOError:
        logger.error(f"Error reading {file_2}!")
        exit()


    table = Texttable()
    table.add_row(["", "File 1", "File 2", ""])
    table.set_cols_dtype(["t", "t", "t", "t"])
    filename_1 = os.path.basename(file_1)
    filename_2 = os.path.basename(file_2)
    table.add_row(['filename', filename_1, filename_2, filename_1 == filename_2])
    dir_1 = os.path.abspath(os.path.dirname(file_1))
    dir_2 = os.path.abspath(os.path.dirname(file_2))
    table.add_row(['path', dir_1, dir_2, dir_1 == dir_2])

    # Diff size
    size_1 = len(contents_1)
    size_2 = len(contents_2)
    if size_1 == size_2:
        logger.info(f"File sizes are identical at {size_1} bytes...")
    else:
        logger.info(f"File sizes are different, {size_1} vs {size_2} bytes...")
    table.add_row(['size', size_1, size_2, size_1 == size_2])

    # Diff CRC
    crc_1 = hash_helper.get_crc(contents_1)
    crc_2 = hash_helper.get_crc(contents_2)
    if crc_1 == crc_2:
        logger.info(f"File hashes are identical, {crc_1}...")
    else:
        logger.info(f"File hashes are different, {crc_1} vs {crc_2}...")
    table.add_row(['crc', crc_1, crc_2, crc_1 == crc_2])

    # TODO: Find sliding match if diff size

    # Simple percent comparison
    if size_1 == size_2:
        diff_bytes = {}
        for x in range(0, size_1):
            if contents_1[x] != contents_2[x]:
                diff_bytes[x] = {"1": contents_1[x], "2": contents_2[x]}

        identical_percent = (100 - (len(diff_bytes.keys()) / size_1)) / 100
        
        logger.info(f"Percent similar: {identical_percent:.4%}")

        # Make a patch-y file
        # TODO: Make this a flag
        patch_data = {int(k): v["1"] for k, v in diff_bytes.items()}
        print(json.dumps(patch_data))
    else:
        logger.info("Percentage comparison for differently sized files NYI!")

    print(table.draw())

