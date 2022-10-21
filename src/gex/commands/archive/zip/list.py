import os
import logging
import click
import click_log
from texttable import Texttable
from gex.lib.archive import zip as zip_lib

logger = logging.getLogger('gextoolbox')

@click.command(name='list')
@click.option('--in', 'in_file', help = 'path to input ZIP archive', required=True)
@click.option('--format', type=click.Choice(['table', 'verify-json'], case_sensitive=False), default="table")
@click_log.simple_verbosity_option(logger)
def list_files(in_file, format):
    """List the contents of a ZIP archive"""
    try:
        with open(in_file, "rb") as curr_file:
            file_content = bytearray(curr_file.read())
            zip_metas = zip_lib.get_metadata(file_content)

            format = format.lower()
            if format == "table":
                table = Texttable()
                table.add_row(["Filename", "Size", "CRC"])
                table.set_cols_dtype(["t", "t", "t"])
                for zip_meta in zip_metas.values():
                    table.add_row([zip_meta['filename'], zip_meta['size'], zip_meta['crc']])
                print(table.draw())
            elif format == "verify-json":
                print('"verify": {')
                print('    "type": "zip",')
                print('    "entries": {')
                values = list(zip_metas.values())
                for zip_meta in values:
                    line = '        "'
                    line += zip_meta.get("filename")
                    line += '": {"size": '
                    line += str(zip_meta.get("size"))
                    line += ', "crc": "'
                    line += zip_meta.get("crc")
                    line += '"}'
                    if zip_meta != values[-1]:
                        line += ','
                    print(line)
                print('    }')
                print('}')

    except Exception as error:
        logger.error(error)
        logger.error('Error While Opening the file!')
