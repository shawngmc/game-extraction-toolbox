import logging
import click
import click_log

from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--out', 'out_file_base',
    help = 'path to output file base name (ex. ./my.file)', required=True)
@click.option('--ways', 'num_ways',
    help = 'number of ways to deinterleave, default is 2-way', default=2)
@click.option('--word', 'word_size',
    help = 'size of word (number of bytes) to put in each file, default is 2 bytes', default=2)
@click_log.simple_verbosity_option(logger)
def deinterleave(in_file, out_file_base, num_ways, word_size):
    '''CLI tool to deinterleave a file into num_ways files by word_size bytes'''
    in_data = read_bin_file(in_file)
    deinterleaved_chunks = transforms.deinterleave(in_data, num_ways, word_size)

    for idx, chunk in enumerate(deinterleaved_chunks):
        filename = f'{out_file_base}.{idx}'
        write_bin_file(chunk, filename)

    logger.info("Done.")

def read_bin_file(path):
    try:
        with open(path, "rb") as file:
            content = file.read()
            return content
    except IOError:
        logger.error(f"Error reading {path}!")
        exit()

def write_bin_file(data, path):
    try:
        with open(path, "wb") as file:
            file.write(data)
    except IOError:
        logger.error(f"Error writing {path}!")
        exit()
