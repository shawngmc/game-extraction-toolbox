import traceback
import os
from gex.lib.archive import kpka
from gex.lib.file import identify
from gex.lib.utils import helper
import click

@click.command()
@click.option('--in', 'in_file', help = 'path to input KPKA archive', required=True)
@click.option('--out', 'out_dir', help = 'path to output folder (must exist)', required=True)
def extract(in_file, out_dir):
    """Extract the contents of a KPKA archive"""
    try:
        with open(in_file, "rb") as curr_file:
            file_content = bytearray(curr_file.read())
            kpka_contents = kpka.extract(file_content)

            # Extract files
            for offset, file_entry in kpka_contents.items():
                contents = file_entry['contents']
                filename = f'{hex(offset)}_{len(file_entry["contents"])}.dat'

                try:
                    type_id = identify.enhanced_magic_from_buffer(contents)
                    print(type_id)
                except:
                    print(f'Cannot typecheck!')

                out_file_path = os.path.join(helper.cleanpath(out_dir), filename)
                print(out_file_path)
                with open(out_file_path, "wb") as out_file:
                    out_file.write(contents)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        print('Error While Opening the file!') 



