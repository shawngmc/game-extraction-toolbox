import click
import sys
import zlib

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--out', 'out_file', help = 'path to output file', required=True)
@click.option('--start', help = 'position to start in file', required=True, default=0, type=int)
@click.option('--length', help = 'length to copy in bytes', required=True, type=int)
def slice(in_file, out_file, start, length):
    """Slice a portion of a file to a new file"""

    def read_bin_file(path):
        try: 
            with open(path, "rb") as f:
                content = f.read()
                return content
        except IOError:
            print(f"Error reading {path}!")   

    def write_bin_file(data, path):
        try: 
            with open(path, "wb") as f:
                f.write(data)
        except IOError:
            print(f"Error writing {path}!")  


    print(f"Pulling {length} bytes from {in_file} starting at {start}")
    print(f"Saving to {out_file}")

    in_data = read_bin_file(in_file)
    out_data = in_data[int(start):int(start + length)]
    write_bin_file(out_data, out_file)
    crc_val = zlib.crc32(out_data)

    print(f"Saved to {out_file} and calculated CRC {hex(crc_val)}")