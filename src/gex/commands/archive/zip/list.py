import os
import logging
import click
import click_log
from texttable import Texttable
from gex.lib.archive import zip as zip_lib

logger = logging.getLogger('gextoolbox')

@click.command(name='list')
@click.option('--in', 'in_file', help = 'path to input ZIP archive', required=True)
@click_log.simple_verbosity_option(logger)
def list_files(in_file):
    """List the contents of a ZIP archive"""
    try:
        with open(in_file, "rb") as curr_file:
            file_content = bytearray(curr_file.read())
            zip_metas = zip_lib.get_metadata(file_content)
            print(zip_metas)

            table = Texttable()
            table.add_row(["Filename", "Size", "CRC"])
            for zip_meta in zip_metas.values():
                table.add_row([zip_meta['filename'], zip_meta['size'], zip_meta['crc']])
            print(table.draw())

    except Exception as error:
        logger.error(error)
        logger.error('Error While Opening the file!')
