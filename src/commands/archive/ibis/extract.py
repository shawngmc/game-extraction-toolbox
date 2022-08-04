import traceback
import magic
import os
import io
from lib.archive import arc
from lib.file import identify
from lib.utils import helper
import click

@click.command()
@click.option('--in', 'in_file', help = 'path to input ARC archive', required=True)
@click.option('--out', 'out_dir', help = 'path to output folder (must exist)', required=True)
def extract(in_file, out_dir):
    """Extract the contents of a ARC archive"""
    try:
        with open(in_file, "rb") as curr_file:
            file_content = bytearray(curr_file.read())
            arc_contents = arc.extract(file_content)

            # Extract files
            for offset, file_entry in arc_contents.items():
                contents = file_entry['contents']

                try:
                    type_id = identify.enhanced_magic_from_buffer(contents)
                    print(type_id)
                except:
                    print(f'Cannot typecheck!')

                out_file_path = os.path.join(helper.cleanpath(out_dir), file_entry['path'].replace("\\", os.sep))
                print(out_file_path)
                os.makedirs(os.path.dirname(out_file_path), exist_ok = True)
                print(out_file_path)
                with open(out_file_path, "wb") as out_file:
                    out_file.write(contents)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        print('Error While Opening the file!') 



