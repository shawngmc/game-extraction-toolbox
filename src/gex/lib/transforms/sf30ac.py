

# Extraction Script for Capcom Fighting Collection

# General Extraction Process
# - Extract ARC Archive
# - Pull bin/ROMNAME file
# - Split it into parts using offsets/length
#   - Header (60b)
#   - MainCPU (???k)
#   - ??? inv gfx (???k) 
#   - AudioCPU (???k)
#   - QSound (???k)
# - Process each part
#   - maincpu: geometry
#   - gfx: geometry, deinterleave, endian swap?
#   - audiocpu: geometry
#   - qsound: geometry + endian swap

import re
import traceback
import glob
import zipfile
import logging
import os
import io

from gex.lib.archive import arc, ibis
from gex.lib.utils import blob

from bplist.bplist import BPListReader

title = "Street Fighter 30th Anniversary Collection"
description = "NYI"
in_dir_desc = "SF30AC base folder (Ex. C:\Program Files (x86)\Steam\steamapps\common\Street Fighter 30th Anniversary Collection)"

pkg_name_map = {
    # "game_00.arc": "vampj",
    # "game_01.arc": "dstlku",
    # "game_10.arc": "vhuntjr2",
    # "game_11.arc": "nwarru",
    # "game_20.arc": "vsavj",
    # "game_21.arc": "vsavu",
    # "game_30.arc": "vhunt2",
    # "game_40.arc": "vsav2",
    # "game_50.arc": "cybotsj",
    # "game_51.arc": "cybotsu",
    # "game_60.arc": "spf2xj",
    # "game_61.arc": "spf2tu",
    # "game_70.arc": "pfghtj",
    # "game_71.arc": "sgemf",
    # "game_80.arc": "hsf2j",
    # "game_81.arc": "hsf2",
    # "game_90.arc": "warzard",
    # "game_91.arc": "redearth",
}

def write_temp_file(contents, path):
    with open(path, 'wb') as out_file:
        out_file.write(contents)

def find_files(base_path):
    bundle_path = os.path.join(base_path, "Bundle", '*.mbundle') 
    print(bundle_path)
    archive_list = glob.glob(bundle_path)
    return archive_list


def merged_rom_handler(merged_contents, func_map):
    new_data = dict()
    for func in func_map.values():
        new_data.update(func(bytearray(merged_contents)))

    # Build the new zip file
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w") as new_archive:
        for name, data in new_data.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()


def main(game_base_dir, out_path):
    bundle_files = find_files(game_base_dir)
    for file_path in bundle_files:
        print(file_path)
        with open(file_path, 'rb') as fp:
            contents = fp.read()
            toc_end = b'\x4F\x12\x00'
            toc_end_index = contents.find(toc_end)
            print(toc_end_index)
            toc = contents[0:toc_end_index]

            reader = BPListReader(toc)
            parsed = reader.parse()
            print(parsed)
            print(len(parsed))
    
    # Now 'parsed' is a dictionary of values.
        # file_name = os.path.basename(file_path)
        # pkg_name = pkg_name_map.get(file_name)
        # if not pkg_name == None:
        #     logging.info(f"Extracting {file_name}: {pkg_name}") 
        #     try:
        #         with open(file_path, "rb") as curr_file:
        #             file_content = bytearray(curr_file.read())
        #             arc_contents = arc.extract(file_content)
        #             output_files = []

        #             # Get the bin entry
        #             merged_rom_contents = None
        #             for key, arc_content in arc_contents.items():
        #                 if arc_content['path'].startswith('bin'):
        #                     merged_rom_contents = arc_content['contents']

        #             handler_func = globals().get(f'handle_{pkg_name}')

        #             if merged_rom_contents != None and handler_func != None:
        #                 output_files = handler_func(merged_rom_contents)
                            
        #                 for output_file in output_files:
        #                     with open(os.path.join(out_path, output_file['filename']), "wb") as out_file:
        #                         out_file.write(output_file['contents'])
        #             elif merged_rom_contents == None:
        #                 print("Could not find merged rom data in arc.")
        #             elif handler_func == None:
        #                 print("Could not find matching handler function.")
        #     except Exception as e:
        #         traceback.print_exc()
        #         logging.warning(f'Error while processing {file_path}!') 
        # else:
        #     logging.info(f'Skipping unmatched file {file_path}!') 
    logging.info("""
        Processing complete. 
    """)
