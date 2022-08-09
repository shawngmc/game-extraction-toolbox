

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

from lib.archive import arc, ibis
from lib.utils import blob

title = "Capcom Fighting Collection"
description = "NYI"
in_dir_desc = "CFC base folder (Ex. C:\Program Files (x86)\Steam\steamapps\common\CAPCOM FIGHTING COLLECTION)"

pkg_name_map = {
    "game_00.arc": "vampj",
    "game_01.arc": "dstlku",
    "game_10.arc": "vhuntjr2",
    "game_11.arc": "nwarru",
    "game_20.arc": "vsavj",
    "game_21.arc": "vsavu",
    "game_30.arc": "vhunt2",
    "game_40.arc": "vsav2",
    "game_50.arc": "cybotsj",
    "game_51.arc": "cybotsu",
    "game_60.arc": "spf2xj",
    "game_61.arc": "spf2tu",
    "game_70.arc": "pfghtj",
    "game_71.arc": "sgemf",
    "game_80.arc": "hsf2j",
    "game_81.arc": "hsf2",
    "game_90.arc": "warzard",
    "game_91.arc": "redearth",
}

def write_temp_file(contents, path):
    with open(path, 'wb') as out_file:
        out_file.write(contents)

def find_files(base_path):
    arc_path = os.path.join(base_path, "nativeDX11x64", "arc", "pc") 
    candidate_files = glob.glob(arc_path +'/game_*.arc')
    archive_list = []
    for candidate in candidate_files:
        if re.search(r'game_\d\d.arc', candidate):
            archive_list.append(candidate)
    return archive_list

def placeholder_generator(file_map):
    def create_placeholders(contents):
        out_files = {}
        for filename, size in file_map.items():
            out_files[filename] = bytes(size*b'\0')
        return out_files  
    return create_placeholders


def deshuffle_gfx_common(start, length, filenames, num_deinterleave_split, do_split):
    def gfx(contents):
        # Cut out the section
        contents = contents[start:start+length]

        # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
        bit_order = [
            7, 3, 15, 11, 23, 19, 31, 27,
            6, 2, 14, 10, 22, 18, 30, 26,
            5, 1, 13, 9, 21, 17, 29, 25,
            4, 0, 12, 8, 20, 16, 28, 24,
            39, 35, 47, 43, 55, 51, 63, 59,
            38, 34, 46, 42, 54, 50, 62, 58, 
            37, 33, 45, 41, 53, 49, 61, 57, 
            36, 32, 44, 40, 52, 48, 60, 56
        ]
        chunks = blob.split_bit_shuffle(contents, word_size_bytes=8, bit_order=bit_order, num_ways=num_deinterleave_split)

        # Split it
        if do_split:
            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(blob.equal_split(oldchunk, num_chunks = 2))
            chunks = new_chunks

        return dict(zip(filenames, chunks))
    return gfx

    
def audio_common(start, filenames):
    def audio(contents):
        chunks = []

        # Add the audio CPU
        chunks.append(contents[start:start+0x8000] + contents[start+0x10000:start+0x18000])

        # Add the qsound
        qsound_start = start+0x18000
        qsound_contents = contents[qsound_start:qsound_start+0x40000]
        chunks.extend(blob.equal_split(qsound_contents, num_chunks=2))

        return dict(zip(filenames, chunks))
    return audio


################################################################################
# START Darkstalkers/Vampire: The Night Warriors                               #
################################################################################
# game_00.arc: Vampire: The Night Warriors (JP)
# game_01.arc: Darkstalkers: The Night Warriors

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu - OK!
#   0x0400040   0x0800040       ???
#   0x0800040   0x1C00040       gfx - OK!
#   0x1C00040   0x1C48040       audiocpu - OK!
#   0x1C48040   0x1C50040       ???
#   0x1C50040   0x2050040       qsound - OK!

vam_gfx_filenames = [
    'vam.13m',
    'vam.14m',
    'vam.15m',
    'vam.16m',
    'vam.17m',
    'vam.18m',
    'vam.19m',
    'vam.20m'
]

vam_audiocpu_filenames = [
    'vam.01',
    'vam.02'
]

vam_qsound_filenames = [
    'vam.11m',
    'vam.12m'
]

def vampj(merged_contents): 
    out_files = []   
    func_map = {}

    maincpu_filenames = [   
        "vamj.03b",
        "vamj.04b",
        "vamj.05b",
        "vamj.06b",
        "vamj.07b",
        "vamj.08b",
        "vamj.09b",
        "vamj.10b"
    ]
    func_map['maincpu'] = ibis.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = ibis.gfx_cps2(0x0800040, 0x1400000, vam_gfx_filenames, split=[0x400000, 0x100000])
    func_map['audiocpu'] = ibis.audiocpu_cps2(0x1C00040, vam_audiocpu_filenames)
    func_map['qsound'] = ibis.qsound_cps2(0x1C50040, 0x400000, vam_qsound_filenames)

    out_files.append({'filename': 'vampj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files


def handle_dstlku(merged_contents): 
    out_files = []   
    func_map = {}

    maincpu_filenames = [   
        "vamu.03b",
        "vamu.04b",
        "vamu.05b",
        "vamu.06b",
        "vamu.07b",
        "vamu.08b",
        "vamu.09b",
        "vamu.10b"
    ]
    func_map['maincpu'] = ibis.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = ibis.gfx_cps2(0x0800040, 0x1400000, vam_gfx_filenames, split=[0x400000, 0x100000])
    func_map['audiocpu'] = ibis.audiocpu_cps2(0x1C00040, vam_audiocpu_filenames)
    func_map['qsound'] = ibis.qsound_cps2(0x1C50040, 0x400000, vam_qsound_filenames)

    out_files.append({'filename': 'dstlku.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Darkstalkers/Vampire: The Night Warriors                                 #
################################################################################


################################################################################
# START Vampire Hunter/Night Warriors: Darkstalkers' Revenge                   #
################################################################################
# game_00.arc: Vampire: The Night Warriors (JP)
# game_01.arc: Darkstalkers: The Night Warriors

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x2C50040       qsound

vph_gfx_filenames = [
    'vph.13m',
    'vph.14m',
    'vph.15m',
    'vph.16m',
    'vph.17m',
    'vph.18m',
    'vph.19m',
    'vph.20m'
]

vph_audiocpu_filenames = [
    'vph.01',
    'vph.02'
]

vph_qsound_filenames = [
    'vph.11m',
    'vph.12m'
]

def handle_vhuntjr2(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "vphj.03b",
        "vphj.04a",
        "vphj.05a",
        "vphj.06a",
        "vphj.07a",
        "vphj.08a",
        "vphj.09a",
        "vphj.10a"
    ]
    func_map['maincpu'] = ibis.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = ibis.gfx_cps2(0x0800040, 0x2000000, vph_gfx_filenames, split=[0x400000, 0x400000])
    func_map['audiocpu'] = ibis.audiocpu_cps2(0x2800040, vph_audiocpu_filenames)
    func_map['qsound'] = ibis.qsound_cps2(0x2850040, 0x400000, vph_qsound_filenames)

    out_files.append({'filename': 'vhuntjr2.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files


def handle_nwarru(merged_contents): 
    out_files = []

    maincpu_filenames = [   
        "vphu.03b",
        "vphu.04a",
        "vphu.05a",
        "vphu.06a",
        "vphu.07a",
        "vphu.08a",
        "vphu.09a",
        "vphu.10a"
    ]

    func_map = {}
    func_map['maincpu'] = ibis.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = ibis.gfx_cps2(0x0800040, 0x2000000, vph_gfx_filenames, split=[0x400000, 0x400000])
    func_map['audiocpu'] = ibis.audiocpu_cps2(0x2800040, vph_audiocpu_filenames)
    func_map['qsound'] = ibis.qsound_cps2(0x2850040, 0x400000, vph_qsound_filenames)

    out_files.append({'filename': 'nwarru.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Vampire Hunter/Night Warriors: Darkstalkers' Revenge                     #
################################################################################



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
    pak_files = find_files(game_base_dir)
    for file_path in pak_files:
        file_name = os.path.basename(file_path)
        pkg_name = pkg_name_map[file_name]
        logging.info(f"Extracting {file_name}: {pkg_name}") 
        try:
            with open(file_path, "rb") as curr_file:
                file_content = bytearray(curr_file.read())
                arc_contents = arc.extract(file_content)
                output_files = []

                # Get the bin entry
                merged_rom_contents = None
                for key, arc_content in arc_contents.items():
                    if arc_content['path'].startswith('bin'):
                        merged_rom_contents = arc_content['contents']

                handler_func = globals().get(f'handle_{pkg_name}')

                if merged_rom_contents != None and handler_func != None:
                    output_files = handler_func(merged_rom_contents)
                        
                    for output_file in output_files:
                        with open(os.path.join(out_path, output_file['filename']), "wb") as out_file:
                            out_file.write(output_file['contents'])
                elif merged_rom_contents == None:
                    print("Could not find merged rom data in arc.")
                elif handler_func == None:
                    print("Could not find matching handler function.")
        except Exception as e:
            traceback.print_exc()
            logging.warning(f'Error while processing {file_path}!') 

    logging.info("""
        Processing complete. 
    """)
