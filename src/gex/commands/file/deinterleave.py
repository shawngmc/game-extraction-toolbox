import click
import click_log
import logging

logger = logging.getLogger('gextoolbox')

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--out1', 'out_file1', help = 'path to output file 1', required=True)
@click.option('--out2', 'out_file2', help = 'path to output file 2', required=True)
@click_log.simple_verbosity_option(logger)
def deinterleave(in_file, out_file1, out_file2):
    in_data = read_bin_file(in_file)
    data1 = bytearray()
    data2 = bytearray()
    for idx in range(len(in_data)):
        mod_val = idx % 4
        if mod_val == 0 or mod_val == 1:
            data1.append(in_data[idx])
        else:
            data2.append(in_data[idx])

    write_bin_file(data1, out_file1)
    write_bin_file(data2, out_file2)
    logger.info("Done.")

def read_bin_file(path):
    try: 
        with open(path, "rb") as f:
            content = f.read()
            return content
    except IOError:
        logger.error(f"Error reading {path}!")
        exit()  

def write_bin_file(data, path):
    try: 
        with open(path, "wb") as f:
            f.write(data)
    except IOError:
        logger.error(f"Error writing {path}!")
        exit()

