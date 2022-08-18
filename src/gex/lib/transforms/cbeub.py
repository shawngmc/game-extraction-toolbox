

# Extraction Script for Capcom Beat 'em Up Bundle

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

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

title = "Capcom Beat 'em Up Bundle"
description = ""
default_folder = "C:\Program Files (x86)\Steam\steamapps\common\CBEUB"
in_dir_desc = "CBEUB Steam folder"

pkg_name_map = {
    "game_00.arc": "ffightj",
    "game_01.arc": "ffight",
    "game_10.arc": "kodj",
    "game_11.arc": "kod",
    "game_20.arc": "captcommj",
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
        chunks = transforms.split_bit_shuffle(contents, word_size_bytes=8, bit_order=bit_order, num_ways=num_deinterleave_split)

        # Split it
        if do_split:
            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(transforms.equal_split(oldchunk, num_chunks = 2))
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
        chunks.extend(transforms.equal_split(qsound_contents, num_chunks=2))

        return dict(zip(filenames, chunks))
    return audio


################################################################################
# START Final Fight                                                            #
################################################################################
# game_00.arc: Final Fight (JP)
# game_01.arc: Final Fight

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
        chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.equal_split(oldchunk, num_chunks = 2))
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
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x200000, gfx_filenames, 4, False)

    audio_filenames = [
        'ff_09.12b',
        'ff_18.11c',
        'ff_19.12c'
    ]
    func_map['audio'] = audio_common(0x600040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        's224b.1a': 0x117,
        'iob1.11e': 0x117
        }
    func_map['placeholders'] = placeholder_generator(ph_files)

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
        chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.equal_split(oldchunk, num_chunks = 4))
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
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x200000, gfx_filenames, 8, True)

    audio_filenames = [
        'ff_23.bin',
        'ffj_30.bin',
        'ffj_31.bin'
    ]
    func_map['audio'] = audio_common(0x600040, audio_filenames)
    
    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        's222b.1a': 0x117,
        'lwio.12c': 0x117
        }
    func_map['placeholders'] = placeholder_generator(ph_files)
    
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


def handle_kod(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "kde_37a.11f", 
        "kde_38a.12f", 
        "kd_35.9f", 
        "kd_36a.10f",
        "kde_30a.11e", 
        "kde_31a.12e", 
        "kd_28.9e", 
        "kd_29.10e"
    ]
    def maincpu(contents):
        contents = contents[0x40:0x100040]
        chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.equal_split(oldchunk, num_chunks = 4))
        chunks = new_chunks

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "kd-5m.4a",
        "kd-6m.4c",
        "kd-7m.6a",
        "kd-8m.6c",
        "kd-1m.3a",
        "kd-2m.3c",
        "kd-3m.5a",
        "kd-4m.5c"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'kd_9.12a',
        'kd_18.11c',
        'kd_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'kd29b.1a': 0x117,
        'iob1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'kod.zip', 'contents': zip_contents})

    return out_files



def handle_kodj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "kdj_37a.11f",
        "kdj_38a.12f",
        "kdj_30a.11e",
        "kdj_31a.12e",
        "kd_33.6f"
    ]
    def maincpu(contents):
        chunk_5 = contents[0x080040:0x100040]
        contents = contents[0x40:0x080040]
        chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.equal_split(oldchunk, num_chunks = 2))
        chunks = new_chunks

        # Add 5th non-interleaved chunk
        chunks.append(chunk_5)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "kd_06.8a",
        "kd_15.8c",
        "kd_08.10a",
        "kd_17.10c",
        "kd_05.7a",
        "kd_14.7c",
        "kd_07.9a",
        "kd_16.9c"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'kd_09.12a',
        'kd_18.11c',
        'kd_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'kd29b.1a': 0x117,
        'iob1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'kodj.zip', 'contents': zip_contents})

    return out_files


################################################################################
# END The King of Dragons                                                      #
################################################################################


################################################################################
# START Captain Commando                                                       #
################################################################################
# game_20.arc: Captain Commando (JP)
# game_21.arc: Captain Commando

def handle_captcomm(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "cce_23f.8f",
        "cc_28f.9f",
        "cc_22f.7f",
        "cc_24f.9e"
    ]
    def maincpu(contents):
        # Only the last 2 128k chunks actually need deinterleaved...
        maincpu_area = contents[0x40:0x140040]
        deint_chunks = transforms.deinterleave(maincpu_area[0x100000:0x140000], num_ways=2, word_size=1)

        chunks = []
        chunks.append(maincpu_area[0x0:0x80000])
        chunks.append(deint_chunks[0])
        chunks.append(maincpu_area[0x80000:0x100000])
        chunks.append(deint_chunks[1])

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "cc-5m.3a",
        "cc-6m.7a",
        "cc-7m.5a",
        "cc-8m.9a",
        "cc-1m.4a",
        "cc-2m.8a",
        "cc-3m.6a",
        "cc-4m.10a"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'cc_09.11a',
        'cc_18.11c',
        'cc_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'cc63b.1a': 0x117,
        'iob1.12d': 0x117,
        'ccprg1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632b.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'captcomm.zip', 'contents': zip_contents})

    return out_files



def handle_captcommj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "ccj_23f.8f",
        "ccj_28f.9f",
        "ccj_22f.7f",
        "ccj_24f.9e"
    ]
    def maincpu(contents):
        # Only the last 2 128k chunks actually need deinterleaved...
        maincpu_area = contents[0x40:0x140040]
        deint_chunks = transforms.deinterleave(maincpu_area[0x100000:0x140000], num_ways=2, word_size=1)

        chunks = []
        chunks.append(maincpu_area[0x0:0x80000])
        chunks.append(deint_chunks[0])
        chunks.append(maincpu_area[0x80000:0x100000])
        chunks.append(deint_chunks[1])

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "cc_01.3a",
        "cc_05.7a",
        "cc_02.4a",
        "cc_06.8a",
        "cc_03.5a",
        "cc_07.9a",
        "cc_04.6a",
        "cc_08.10a"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)
    
    audio_filenames = [
        'ccj_09.12a',
        'ccj_18.11c',
        'ccj_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'cc63b.1a': 0x117,
        'iob1.12d': 0x117,
        'ccprg1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'captcommj.zip', 'contents': zip_contents})

    return out_files


################################################################################
# END Captain Commando                                                         #
################################################################################


################################################################################
# START Knights of the Round                                                   #
################################################################################
# game_30.arc: Knights of the Round (JP)
# game_31.arc: Knights of the Round



def handle_knights(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "kr_23e.8f",
        "kr_22.7f"
    ]
    def maincpu(contents):
        # Only the last 2 128k chunks actually need deinterleaved...
        maincpu_area = contents[0x40:0x100040]
        chunks = transforms.equal_split(maincpu_area, num_chunks=2)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "kr-5m.3a",
        "kr-6m.7a",
        "kr-7m.5a",
        "kr-8m.9a",
        "kr-1m.4a",
        "kr-2m.8a",
        "kr-3m.6a",
        "kr-4m.10a"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'kr_09.11a',
        'kr_18.11c',
        'kr_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'kr63b.1a': 0x117,
        'iob1.12d': 0x117,
        'bprg1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'knights.zip', 'contents': zip_contents})

    return out_files



def handle_knightsj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "kr_23j.8f",
        "kr_22.7f"
    ]
    def maincpu(contents):
        # Only the last 2 128k chunks actually need deinterleaved...
        maincpu_area = contents[0x40:0x100040]
        chunks = transforms.equal_split(maincpu_area, num_chunks=2)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "kr_01.3a",
        "kr_05.7a",
        "kr_02.4a",
        "kr_06.8a",
        "kr_03.5a",
        "kr_07.9a",
        "kr_04.6a",
        "kr_08.10a"
    ]
    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'kr_09.12a',
        'kr_18.11c',
        'kr_19.12c'
    ]
    func_map['audio'] = audio_common(0x800040, audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'kr63b.1a': 0x117,
        'iob1.12d': 0x117,
        'bprg1.11d': 0x117,
        'ioc1.ic7': 0x104,
        'c632.ic1': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'knightsj.zip', 'contents': zip_contents})

    return out_files


################################################################################
# END Knights of the Round                                                     #
################################################################################


################################################################################
# START Warriors of Fate                                                       #
################################################################################
# game_40.arc: Warriors of Fate (JP)
# game_41.arc: Warriors of Fate

# wof map from script
#           0x000000    0x000040                IBIS Header
# maincpu   0x000040    0x100040                OK
#           0x100040    0x400040                Padding (All FF)
# gfx       0x400040    0x800040                OK
# audiocpu  0x800040    0x828040   (with gap)   BAD CRC, but looks like the audiocpu code from other ROMS (version header)
#           |
#           |  0x800040    0x808040                Different data - does not look like most audiocpu - no version header, a lot of it looks like junk filler
#           |  0x808040    0x810040                Padding (All FF) - similar padding is only 0x075DB - 0x08000 in tk2_qa.5k
#           |  0x810040    0x828040                Matches 0x08000 - 0x20000 in wof's tk2_qa.5k
#           0x828040    0x830040                Unknown
#           0x830040    0x850040                Padding (All FF)
# qsound    0x850040    0xA50040                OK


def wof_audio_common(filenames):
    def audio(contents):
        start = 0x800040
        chunks = []

        # Add the audio CPU
        audiocpu_content = contents[start:start+0x8000] + contents[start+0x10000:start+0x28000]
        chunks.append(audiocpu_content)

        # Add the qsound
        qsound_start = start+0x50000
        qsound_contents = contents[qsound_start:qsound_start+0x200000]
        chunks.extend(transforms.equal_split(qsound_contents, num_chunks=4))

        return dict(zip(filenames, chunks))
    return audio

def handle_wof(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "tk2e_23c.8f",
        "tk2e_22c.7f"
    ]
    def maincpu(contents):
        maincpu_area = contents[0x40:0x100040]
        chunks = transforms.equal_split(maincpu_area, num_chunks=2)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "tk2-1m.3a",
        "tk2-5m.7a",
        "tk2-3m.5a",
        "tk2-7m.9a",
        "tk2-2m.4a",
        "tk2-6m.8a",
        "tk2-4m.6a",
        "tk2-8m.10a"
    ]

    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'tk2_qa.5k',
        'tk2-q1.1k',
        'tk2-q2.2k',
        'tk2-q3.3k',
        'tk2-q4.4k'
    ]
    func_map['audio'] = wof_audio_common(audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg2': 0x117,
        'rom1': 0x117,
        'tk263b.1a': 0x117,
        'iob1.12d': 0x117,
        'bprg1.11d': 0x117,
        'ioc1.ic1': 0x104,
        'd7l1.7l': 0x117,
        'd8l1.8l': 0x117,
        'd9k1.9k': 0x117,
        'd10f1.10f': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'wof.zip', 'contents': zip_contents})

    return out_files

def handle_wofj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [
        "tk2j_23c.8f",
        "tk2j_22c.7f"
    ]
    def maincpu(contents):
        maincpu_area = contents[0x40:0x100040]
        chunks = transforms.equal_split(maincpu_area, num_chunks=2)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    gfx_filenames = [
        "tk2_01.3a",
        "tk2_05.7a",
        "tk2_02.4a",
        "tk2_06.8a",
        "tk2_03.5a",
        "tk2_07.9a",
        "tk2_04.6a",
        "tk2_08.10a"
    ]

    func_map['gfx'] = deshuffle_gfx_common(0x400040, 0x400000, gfx_filenames, 4, True)

    audio_filenames = [
        'tk2_qa.5k',
        'tk2-q1.1k',
        'tk2-q2.2k',
        'tk2-q3.3k',
        'tk2-q4.4k'
    ]
    func_map['audio'] = wof_audio_common(audio_filenames)

    ph_files = {
        'buf1': 0x117,
        'ioa1': 0x117,
        'prg1': 0x117,
        'sou1': 0x117,
        'rom1': 0x117,
        'tk263b.1a': 0x117,
        'iob1.12d': 0x117,
        'bprg1.11d': 0x117,
        'ioc1.ic1': 0x104,
        'd7l1.7l': 0x117,
        'd8l1.8l': 0x117,
        'd9k1.9k': 0x117,
        'd10f1.10f': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    zip_contents = merged_rom_handler(merged_contents, func_map)
    out_files.append({'filename': 'wofj.zip', 'contents': zip_contents})

    return out_files

################################################################################
# END Warriors of Fate                                                         #
################################################################################


################################################################################
# START Armored Warriors                                                       #
################################################################################
# game_50.arc: Powered Gear: Strategic Variant Armor Equipment (JP)
# game_51.arc: Armored Warriors

def armwar_gfx_common(contents):
    # Cut out the section
    contents = contents[0x0800040:0x1C00040]

    # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
    contents = capcom.common_gfx_deshuffle(contents)

    # Split it
    chunks = transforms.equal_split(contents, num_chunks=20)

    # Interleave each pair of chunks
    new_chunks = []
    for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
        new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
    chunks = new_chunks

    # Merge the chunks back together
    contents = transforms.merge(chunks)

    # Deinterleave the chunks into our files
    new_chunks = []
    chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)
    for chunk in chunks:
        new_chunks.extend(transforms.custom_split(chunk, [0x400000, 0x100000]))
    chunks = new_chunks
    filenames = [
        'pwg.13m',
        'pwg.14m',
        'pwg.15m',
        'pwg.16m',
        'pwg.17m',
        'pwg.18m',
        'pwg.19m',
        'pwg.20m'
    ]
    return dict(zip(filenames, chunks))

def armwar_audiocpu_common(contents):
    chunks = []
    chunks.append(contents[0x1C00040:0x1C08040] + contents[0x1C10040:0x1C28040])
    chunks.append(contents[0x1C28040:0x1C48040])
    filenames = [
        'pwg.01',
        'pwg.02'
    ]
    return dict(zip(filenames, chunks))
    
def armwar_qsound_common(contents):
    contents = contents[0x1C50040:0x2050040]
    chunks = transforms.equal_split(contents, num_chunks=2)
    chunks = transforms.swap_endian_all(chunks)
    filenames = [
        'pwg.11m',
        'pwg.12m'
    ]
    return dict(zip(filenames, chunks))

def handle_armwar(merged_contents):
    out_files = []

    def maincpu(contents):
        contents = contents[0x40:0x400040]
        chunks = transforms.equal_split(contents, num_chunks=8)
        filenames = [   
            "pwge.03c",
            "pwge.04c",
            "pwge.05b",
            "pwg.06",
            "pwg.07",
            "pwg.08",
            "pwg.09a",
            "pwg.10"
        ]
        return dict(zip(filenames, chunks))
    func_map = {}
    func_map['maincpu'] = maincpu
    func_map['gfx'] = armwar_gfx_common
    func_map['audiocpu'] = armwar_audiocpu_common
    func_map['qsound'] = armwar_qsound_common
    out_files.append({'filename': 'armwar.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
    return out_files

def handle_pgear(merged_contents):
    out_files = []

    def maincpu(contents):
        contents = contents[0x40:0x400040]
        chunks = transforms.equal_split(contents, num_chunks=8)
        filenames = [   
            "pwgj.03a",
            "pwgj.04a",
            "pwgj.05a",
            "pwg.06",
            "pwg.07",
            "pwg.08",
            "pwg.09a",
            "pwg.10"
        ]
        return dict(zip(filenames, chunks))
    func_map = {}
    func_map['maincpu'] = maincpu
    func_map['gfx'] = armwar_gfx_common
    func_map['audiocpu'] = armwar_audiocpu_common
    func_map['qsound'] = armwar_qsound_common
    out_files.append({'filename': 'pgear.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
    return out_files

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

    contents = capcom.common_gfx_deshuffle(contents)

    # Split it
    chunks = transforms.equal_split(contents, num_chunks=16)

    # Interleave each pair of chunks
    new_chunks = []
    for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
        new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
    chunks = new_chunks

    # Merge the chunks back together
    contents = transforms.merge(chunks)

    # Deinterleave the chunks into our 4 files
    chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)
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
    chunks = transforms.equal_split(contents, num_chunks=2)
    chunks = transforms.swap_endian_all(chunks)
    filenames = [
        'btc.11m',
        'btc.12m'
    ]
    return dict(zip(filenames, chunks))


def handle_batcir(merged_contents):
    out_files = []

    def maincpu(contents):
        contents = contents[0x40:0x380040]
        chunks = transforms.equal_split(contents, num_chunks=7)
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
        chunks = transforms.equal_split(contents, num_chunks=7)
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
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in new_data.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()


def main(game_base_dir, out_path):
    pak_files = find_files(game_base_dir)
    for file_path in pak_files:
        file_name = os.path.basename(file_path)
        pkg_name = pkg_name_map[file_name]
        logger.info(f"Extracting {file_name}: {pkg_name}") 
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
                    logger.warning("Could not find merged rom data in arc.")
                elif handler_func == None:
                    logger.warning("Could not find matching handler function.")
        except Exception as e:
            traceback.print_exc()
            logger.warning(f'Error while processing {file_path}!') 

    logger.info("""
        Processing complete. 
    """)
