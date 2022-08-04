import click

@click.command()
@click.option('--in', 'in_file', help = 'path to input file', required=True)
@click.option('--out1', 'out_file1', help = 'path to output file 1', required=True)
@click.option('--out2', 'out_file2', help = 'path to output file 2', required=True)
def deinterleave(in_file, out_file1, out_file2):
    in_data = read_bin_file(in_file)
    # Original 1 and 1 
    # CHANNEL_COUNT = 2
    # deinterleaved = [in_data[idx::CHANNEL_COUNT] for idx in range(CHANNEL_COUNT)]
    # write_bin_file(deinterleaved[0], out_file1)
    # write_bin_file(deinterleaved[1], out_file2)
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

