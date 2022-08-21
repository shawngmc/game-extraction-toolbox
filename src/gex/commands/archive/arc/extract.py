import os
import logging
import click
import click_log
from gex.lib.archive import arc
from gex.lib.file import identify
from gex.lib.utils import helper

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input ARC archive', required=True)
@click.option('--out', 'out_dir', help = 'path to output folder (must exist)', required=True)
@click_log.simple_verbosity_option(logger)
def extract(in_file, out_dir):
    """Extract the contents of a ARC archive"""
    try:
        with open(in_file, "rb") as curr_file:
            file_content = bytearray(curr_file.read())
            arc_contents = arc.extract(file_content)

            # Extract files
            for _, file_entry in arc_contents.items():
                contents = file_entry['contents']

                try:
                    type_id = identify.enhanced_magic_from_buffer(contents)
                    if not type_id == identify.ARC:
                        logger.warning(f'Found {type_id} file, will try to extract anyway...')
                except Exception as _:
                    logger.warning('Cannot typecheck!')

                out_file_path = os.path.join(
                    helper.cleanpath(out_dir),
                    file_entry['path'].replace("\\", os.sep)
                )
                os.makedirs(os.path.dirname(out_file_path), exist_ok = True)
                with open(out_file_path, "wb") as out_file:
                    out_file.write(contents)

        logger.info('Extraction complete.')
    except Exception as error:
        logger.error(error)
        logger.error('Error While Opening the file!')
