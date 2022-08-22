import logging
import click
import click_log

logger = logging.getLogger('gextoolbox')

@click.command(name='slice')
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--out', 'out_file', help = 'path to output file', required=True)
@click.option('--start', help = 'position to start in file', required=True, default=0, type=int)
@click.option('--length', help = 'length to copy in bytes', required=True, type=int)
@click_log.simple_verbosity_option(logger)
def slice_cli(in_file, out_file, start, length):
    """Slice a portion of a file to a new file"""

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


    logger.info(f"Pulling {length} bytes from {in_file} starting at {start}")
    logger.info(f"Saving to {out_file}")

    in_data = read_bin_file(in_file)
    out_data = in_data[int(start):int(start + length)]
    write_bin_file(out_data, out_file)

    logger.info(f"Saved to {out_file}")
