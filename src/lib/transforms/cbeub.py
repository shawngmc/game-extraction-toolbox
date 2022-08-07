

# Extraction Script for Capcom Beat 'em Up Bundle

# Game Mapping
#  game_00.arc: Final Fight (JP)
#   - maincpu
#     - geometry: offset 0x00040, length 0x100000
#     - split: 4
#     - deinterleave: 2 bytes
#     - name
#   - gfx
#     - geometry: offset 0x400040, length 0x200000
#     - split: 2
#     - deinterleave: 8
#     - name
#   - audiocpu
#     - geometry: offset 0x600040, length 0x018000
#     - splice_out: offset 0x8000, length 0x2000
#     - split: 2
#     - name
#   - qsound
#     - geometry: offset 0x618040, length 0x040000
#     - split: 2
#     - name




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

# Typical Base Path: C:\Program Files (x86)\Steam\steamapps\common\CBEUB

import re
import traceback
import glob
import zipfile
import logging
import os
import io

from lib.archive import arc
from lib.utils import blob

title = "Capcom Beat 'em Up Bundle"
description = "NYI"
in_dir_desc = "NYI"

pkg_name_map = {
    "game_00.arc": "ffightj",
    "game_01.arc": "ffight",
    "game_10.arc": "kodj",
    "game_11.arc": "kod",
    "game_20.arc": "captcomj",
    "game_21.arc": "captcomm",
    "game_30.arc": "knightsj",
    "game_31.arc": "knights",
    "game_40.arc": "wofj",
    "game_41.arc": "wof",
    "game_50.arc": "pgear",
    "game_51.arc": "armwar",
    "game_60.arc": "batcirj",
    "game_61.arc": "batcir",
}

def write_temp_file(contents, path):
    with open(path, 'wb') as out_file:
        out_file.write(contents)

def find_files(base_path):
    arc_path = os.path.join(base_path, "nativeDX11x64", "arc") 
    candidate_files = glob.glob(arc_path +'/game_*.arc')
    archive_list = []
    for candidate in candidate_files:
        if re.search(r'game_\d\d.arc', candidate):
            archive_list.append(candidate)
    return archive_list



################################################################################
# START Final Fight                                                            #
################################################################################
# game_00.arc: Final Fight (JP)
# game_01.arc: Final Fight


# bcut.exe ffightj  gfx.bin  0x400040 0x200000
# BSwap.exe d b gfx.bin vrom.txt gfx.0 gfx.1 gfx.2 gfx.3 gfx.4 gfx.5 gfx.6 gfx.7
# bcut.exe gfx.0  %TDIR%\ffj_09.4b    0x00000  0x20000
# bcut.exe gfx.1  %TDIR%\ffj_01.4a    0x00000  0x20000
# bcut.exe gfx.2  %TDIR%\ffj_13.9b    0x00000  0x20000
# bcut.exe gfx.3  %TDIR%\ffj_05.9a    0x00000  0x20000
# bcut.exe gfx.4  %TDIR%\ffj_24.5e    0x00000  0x20000
# bcut.exe gfx.5  %TDIR%\ffj_17.5c    0x00000  0x20000
# bcut.exe gfx.6  %TDIR%\ffj_38.8h    0x00000  0x20000
# bcut.exe gfx.7  %TDIR%\ffj_32.8f    0x00000  0x20000
# bcut.exe gfx.0  %TDIR%\ffj_10.5b    0x20000  0x20000
# bcut.exe gfx.1  %TDIR%\ffj_02.5a    0x20000  0x20000
# bcut.exe gfx.2  %TDIR%\ffj_14.10b   0x20000  0x20000
# bcut.exe gfx.3  %TDIR%\ffj_06.10a   0x20000  0x20000
# bcut.exe gfx.4  %TDIR%\ffj_25.7e    0x20000  0x20000
# bcut.exe gfx.5  %TDIR%\ffj_18.7c    0x20000  0x20000
# bcut.exe gfx.6  %TDIR%\ffj_39.9h    0x20000  0x20000
# bcut.exe gfx.7  %TDIR%\ffj_33.9f    0x20000  0x20000
# del gfx.*

# fsutil file createnew %TDIR%\buf1      0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\ioa1      0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\prg1      0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\rom1      0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\sou1      0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\s222b.1a  0x117                           & rem CRC mismatch
# fsutil file createnew %TDIR%\lwio.12c  0x117                           & rem CRC mismatch

# powershell compress-archive -Path %TDIR%\* -DestinationPath %NAME%.zip -Force

# rm -r tmp

def ffight_qsound_common(filenames):
    def qsound(contents):
        contents = contents[0x618040:0x658040]
        chunks = blob.equal_split(contents, num_chunks=2)
        return dict(zip(filenames, chunks))
    return qsound


def ffight_audiocpu_common(filenames):
    def audiocpu(contents):
        chunks = []
        chunks.append(contents[0x600040:0x608040] + contents[0x610040:0x618040])
        return dict(zip(filenames, chunks))
    return audiocpu

def ffight_gfx_common(filenames, num_deinterleave_split, do_split):
    def gfx(contents):
        # Cut out the section
        contents = contents[0x400040:0x600040]

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


def handle_ffight(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "ff_42.11h",
        "ffe_43.12h",
        "ff_36.11f",
        "ff_37.12f",
        "ff-32m.8h"
    ]
    def maincpu(contents):
        chunk_5 = contents[0x080040:0x100040]
        contents = contents[0x40:0x080040]
        chunks = blob.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(blob.equal_split(oldchunk, num_chunks = 2))
        chunks = new_chunks

        # Add 5th non-interleaved chunk
        chunks.append(chunk_5)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "ff-5m.7a",
        "ff-7m.9a",
        "ff-1m.3a",
        "ff-3m.5a"
    ]
    func_map['gfx'] = ffight_gfx_common(gfx_filenames, 4, False)

    audiocpu_filenames = [
        'ff_09.12b'
    ]
    func_map['audiocpu'] = ffight_audiocpu_common(audiocpu_filenames)

    qsound_filenames = [
        'ff_18.11c',
        'ff_19.12c'
    ]
    func_map['qsound'] = ffight_qsound_common(qsound_filenames)


    def ffight_placeholder_files(contents):
        filenames = [
            'buf1',
            'ioa1',
            'prg1',
            'rom1',
            'sou1',
            's224b.1a',
            'iob1.11e',
        ]
        return dict(zip(filenames, [bytes(0x117*b'\0')]*len(filenames)))
    func_map['placeholders'] = ffight_placeholder_files

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'ffight.zip', 'contents': zip_contents})

    return out_files


def handle_ffightj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "ff42.bin",
        "ff43.bin",
        "ffj_40.10h",
        "ffj_41.11h",
        "ff36.bin",
        "ff37.bin",
        "ffj_34.10f",
        "ffj_35.11f"
    ]
    def maincpu(contents):
        contents = contents[0x40:0x100040]
        chunks = blob.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(blob.equal_split(oldchunk, num_chunks = 4))
        chunks = new_chunks
        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "ffj_09.4b",
        "ffj_10.5b",
        "ffj_01.4a",
        "ffj_02.5a",
        "ffj_13.9b",
        "ffj_14.10b",
        "ffj_05.9a",
        "ffj_06.10a",
        "ffj_24.5e",
        "ffj_25.7e",
        "ffj_17.5c",
        "ffj_18.7c",
        "ffj_38.8h",
        "ffj_39.9h",
        "ffj_32.8f",
        "ffj_33.9f"
    ]
    func_map['gfx'] = ffight_gfx_common(gfx_filenames, 8, True)

    audiocpu_filenames = [
        'ff_23.bin'
    ]
    func_map['audiocpu'] = ffight_audiocpu_common(audiocpu_filenames)

    qsound_filenames = [
        'ffj_30.bin',
        'ffj_31.bin'
    ]
    func_map['qsound'] = ffight_qsound_common(qsound_filenames)
    
    def ffightj_placeholder_files(contents):
        filenames = [
            'buf1',
            'ioa1',
            'prg1',
            'rom1',
            'sou1',
            's222b.1a',
            'lwio.12c',
        ]
        return dict(zip(filenames, [bytes(0x117*b'\0')]*len(filenames)))
    func_map['placeholders'] = ffightj_placeholder_files
    
    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'ffightj.zip', 'contents': zip_contents})

    return out_files

################################################################################
# END Final Fight                                                              #
################################################################################


################################################################################
# START The King of Dragons                                                    #
################################################################################
# game_10.arc: The King of Dragons (JP)
# game_11.arc: The King of Dragons


################################################################################
# END The King of Dragons                                                      #
################################################################################


################################################################################
# START Captain Commando                                                       #
################################################################################
# game_20.arc: Captain Commando (JP)
# game_21.arc: Captain Commando


################################################################################
# END Captain Commando                                                         #
################################################################################


################################################################################
# START Knights of the Round                                                   #
################################################################################
# game_30.arc: Knights of the Round (JP)
# game_31.arc: Knights of the Round


################################################################################
# END Knights of the Round                                                     #
################################################################################


################################################################################
# START Warriors of Fate                                                       #
################################################################################
# game_40.arc: Warriors of Fate (JP)
# game_41.arc: Warriors of Fate


################################################################################
# END Warriors of Fate                                                         #
################################################################################


################################################################################
# START Armored Warriors                                                       #
################################################################################
# game_50.arc: Powered Gear: Strategic Variant Armor Equipment (JP)
# game_51.arc: Armored Warriors


################################################################################
# END Armored Warriors                                                         #
################################################################################

################################################################################
# START Battle Circuit                                                         #
################################################################################
# game_60.arc: Battle Circuit (JP)
# game_61.arc: Battle Circuit
# Battle Circuit has some weird graphics interleaving that took some time to recreate from the Japanese script.
# None the less, it's in - and only the maincpu differs between the two!

def batcir_gfx_common(contents):
    # Cut out the section
    contents = contents[0x0800040:0x1800040]

    # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
    bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18, 30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]
    contents = blob.bit_shuffle(contents, word_size_bytes=4, bit_order=bit_order)

    # Split it
    chunks = blob.equal_split(contents, num_chunks=16)

    # Interleave each pair of chunks
    new_chunks = []
    for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
        new_chunks.append(blob.interleave([oddchunk, evenchunk], word_size=8))
    chunks = new_chunks

    # Merge the chunks back together
    contents = blob.merge(chunks)

    # Deinterleave the chunks into our 4 files
    chunks = blob.deinterleave(contents, num_ways = 4, word_size=2)
    filenames = [
        'btc.13m',
        'btc.15m',
        'btc.17m',
        'btc.19m'
    ]
    return dict(zip(filenames, chunks))

def batcir_audiocpu_common(contents):
    chunks = []
    chunks.append(contents[0x1800040:0x1808040] + contents[0x1810040:0x1828040])
    chunks.append(contents[0x1828040:0x1848040])
    filenames = [
        'btc.01',
        'btc.02'
    ]
    return dict(zip(filenames, chunks))
    
def batcir_qsound_common(contents):
    contents = contents[0x1850040:0x1C50040]
    chunks = blob.equal_split(contents, num_chunks=2)
    chunks = blob.swap_endian_all(chunks)
    filenames = [
        'btc.11m',
        'btc.12m'
    ]
    return dict(zip(filenames, chunks))


def handle_batcir(merged_contents):
    out_files = []

    def maincpu(contents):
        contents = contents[0x40:0x380040]
        chunks = blob.equal_split(contents, num_chunks=7)
        filenames = [   
            "btce.03", 
            "btce.04", 
            "btce.05", 
            "btce.06", 
            "btc.07", 
            "btc.08", 
            "btc.09"
        ]
        return dict(zip(filenames, chunks))
    func_map = {}
    func_map['maincpu'] = maincpu
    func_map['gfx'] = batcir_gfx_common
    func_map['audiocpu'] = batcir_audiocpu_common
    func_map['qsound'] = batcir_qsound_common
    out_files.append({'filename': 'batcir.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
    return out_files


def handle_batcirj(merged_contents):
    out_files = []

    def maincpu(contents):
        contents = contents[0x40:0x380040]
        chunks = blob.equal_split(contents, num_chunks=7)
        filenames = [   
            "btcj.03", 
            "btcj.04", 
            "btcj.05", 
            "btcj.06", 
            "btc.07", 
            "btc.08", 
            "btc.09"
        ]
        return dict(zip(filenames, chunks))
    func_map = {}
    func_map['maincpu'] = maincpu
    func_map['gfx'] = batcir_gfx_common
    func_map['audiocpu'] = batcir_audiocpu_common
    func_map['qsound'] = batcir_qsound_common
    out_files.append({'filename': 'batcirj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
    return out_files


################################################################################
# END Battle Circuit                                                           #
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


# def ffightj(file_content, archive_meta):
#     arc_files = arc.extract(file_content)

#     target_file = [x for x in arc_files if x['path'] == "bin\ffightj"][0]
#     contents = target_file['contents']

#     # maincpu
#     maincpu = contents[0x40:0x40+0x100000]

#   - maincpu
#     - geometry: offset 0x00040, length 0x100000
#     - split: 4
#     - deinterleave: 2 bytes
#     - name
#   - gfx
#     - geometry: offset 0x400040, length 0x200000
#     - split: 2
#     - deinterleave: 8
#     - name
#   - audiocpu
#     - geometry: offset 0x600040, length 0x018000
#     - splice_out: offset 0x8000, length 0x2000
#     - split: 2
#     - name
#   - qsound
#     - geometry: offset 0x618040, length 0x040000
#     - split: 2
#     - name
    # print("NYI")



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
