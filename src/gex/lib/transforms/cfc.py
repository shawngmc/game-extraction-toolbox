

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

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

title = "Capcom Fighting Collection"
description = ""
default_folder = "C:\Program Files (x86)\Steam\steamapps\common\CAPCOM FIGHTING COLLECTION"
in_dir_desc = "CFC Steam folder"

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

def handle_vampj(merged_contents): 
    out_files = []   
    func_map = {}

    maincpu_filenames = [   
        "vamj.03a",
        "vamj.04b",
        "vamj.05a",
        "vamj.06a",
        "vamj.07a",
        "vamj.08a",
        "vamj.09a",
        "vamj.10a"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vam_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x1400000), split=[0x400000, 0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1C00040, vam_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1C50040, 0x400000, vam_qsound_filenames)

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
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vam_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x1400000), split=[0x400000, 0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1C00040, vam_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1C50040, 0x400000, vam_qsound_filenames)

    out_files.append({'filename': 'dstlku.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Darkstalkers/Vampire: The Night Warriors                                 #
################################################################################


################################################################################
# START Vampire Hunter/Night Warriors: Darkstalkers' Revenge                   #
################################################################################
# game_10.arc: Vampire: The Night Warriors (JP)
# game_11.arc: Darkstalkers: The Night Warriors

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
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vph_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vph_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x400000, vph_qsound_filenames)

    out_files.append({'filename': 'vhuntjr2.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files


def handle_nwarru(merged_contents): 
    out_files = []

    maincpu_filenames = [   
        "vphu.03f",
        "vphu.04c",
        "vphu.05e",
        "vphu.06c",
        "vphu.07b",
        "vphu.08b",
        "vphu.09b",
        "vphu.10b"
    ]

    func_map = {}
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vph_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vph_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x400000, vph_qsound_filenames)

    out_files.append({'filename': 'nwarru.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Vampire Hunter/Night Warriors: Darkstalkers' Revenge                     #
################################################################################


################################################################################
# START Vampire Savior: The Lord of Vampire                                    #
################################################################################
# game_20.arc: Vampire Savior: The Lord of Vampire (JP)
# game_21.arc: Darkstalkers: The Night Warriors

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x3050040       qsound

vm3_gfx_filenames = [
    'vm3.13m',
    'vm3.14m',
    'vm3.15m',
    'vm3.16m',
    'vm3.17m',
    'vm3.18m',
    'vm3.19m',
    'vm3.20m'
]

vm3_audiocpu_filenames = [
    'vm3.01',
    'vm3.02'
]

vm3_qsound_filenames = [
    'vm3.11m',
    'vm3.12m'
]

def handle_vsavj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "vm3j.03d",
        "vm3j.04d",
        "vm3j.05a",
        "vm3j.06b",
        "vm3j.07b",
        "vm3j.08a",
        "vm3j.09b",
        "vm3j.10b"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vm3_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vm3_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, vm3_qsound_filenames)

    out_files.append({'filename': 'vsavj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

def handle_vsavu(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "vm3u.03d",
        "vm3u.04d",
        "vm3.05a",
        "vm3.06a",
        "vm3.07b",
        "vm3.08a",
        "vm3.09b",
        "vm3.10b"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vm3_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vm3_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, vm3_qsound_filenames)

    out_files.append({'filename': 'vsavu.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Vampire Savior: The Lord of Vampire                                      #
################################################################################


################################################################################
# START Vampire Hunter 2: Darkstalkers Revenge                                 #
################################################################################
# game_30.arc: Vampire Hunter 2: Darkstalkers Revenge (JP)

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x3050040       qsound

vh2_gfx_filenames = [
    'vh2.13m',
    'vh2.14m',
    'vh2.15m',
    'vh2.16m',
    'vh2.17m',
    'vh2.18m',
    'vh2.19m',
    'vh2.20m'
]

vh2_audiocpu_filenames = [
    'vh2.01',
    'vh2.02'
]

vh2_qsound_filenames = [
    'vh2.11m',
    'vh2.12m'
]

def handle_vhunt2(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "vh2j.03a",
        "vh2j.04a",
        "vh2j.05",
        "vh2j.06",
        "vh2j.07",
        "vh2j.08",
        "vh2j.09",
        "vh2j.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vh2_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vh2_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, vh2_qsound_filenames)

    out_files.append({'filename': 'vhunt2.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files


################################################################################
# END Vampire Hunter 2: Darkstalkers Revenge                                   #
################################################################################


################################################################################
# START Vampire Savior 2: The Lord of Vampire                                  #
################################################################################
# game_40.arc: Vampire Savior 2: The Lord of Vampire (JP)

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x3050040       qsound

vs2_gfx_filenames = [
    'vs2.13m',
    'vs2.14m',
    'vs2.15m',
    'vs2.16m',
    'vs2.17m',
    'vs2.18m',
    'vs2.19m',
    'vs2.20m'
]

vs2_audiocpu_filenames = [
    'vs2.01',
    'vs2.02'
]

vs2_qsound_filenames = [
    'vs2.11m',
    'vs2.12m'
]

def handle_vsav2(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "vs2j.03",
        "vs2j.04",
        "vs2j.05",
        "vs2j.06",
        "vs2j.07",
        "vs2j.08",
        "vs2j.09",
        "vs2j.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(vs2_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, vs2_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, vs2_qsound_filenames)

    out_files.append({'filename': 'vsav2.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files


################################################################################
# END Vampire Savior 2: The Lord of Vampire                                    #
################################################################################


################################################################################
# START Cyberbots: Fullmetal Madness                                           #
################################################################################
# game_50.arc: Cyberbots: Fullmetal Madness (JP)
# game_51.arc: Cyberbots: Fullmetal Madness

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0100040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x2C50040       qsound

cybots_gfx_filenames = [
    'cyb.13m',
    'cyb.14m',
    'cyb.15m',
    'cyb.16m',
    'cyb.17m',
    'cyb.18m',
    'cyb.19m',
    'cyb.20m'
]

cybots_audiocpu_filenames = [
    'cyb.01',
    'cyb.02'
]

cybots_qsound_filenames = [
    'cyb.11m',
    'cyb.12m'
]

def handle_cybotsj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "cybj.03",
        "cybj.04",
        "cyb.05",
        "cyb.06",
        "cyb.07",
        "cyb.08",
        "cyb.09",
        "cyb.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(cybots_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, cybots_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x400000, cybots_qsound_filenames)

    out_files.append({'filename': 'cybotsj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

def handle_cybotsu(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "cybu.03",
        "cybu.04",
        "cyb.05",
        "cyb.06",
        "cyb.07",
        "cyb.08",
        "cyb.09",
        "cyb.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(cybots_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x400000, 0x400000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, cybots_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x400000, cybots_qsound_filenames)

    out_files.append({'filename': 'cybotsu.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Cyberbots: Fullmetal Madness                                             #
################################################################################


################################################################################
# START Super Puzzle Fighter II Turbo                                          #
################################################################################
# game_60.arc: Super Puzzle Fighter II X (JP)
# game_61.arc: Super Puzzle Fighter II Turbo

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0100040       maincpu
#   0x0100040   0x1000040       ???
#   0x1000040   0x1400040       gfx
#   0x1400040   0x1448040       audiocpu
#   0x1450040   0x1850040       qsound

pzf_gfx_filenames = [
    'pzf.14m',
    'pzf.16m',
    'pzf.18m',
    'pzf.20m'
]

pzf_audiocpu_filenames = [
    'pzf.01',
    'pzf.02'
]

pzf_qsound_filenames = [
    'pzf.11m',
    'pzf.12m'
]

def handle_spf2xj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "pzfj.03a",
        "pzf.04"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x100000, 2, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(pzf_gfx_filenames, transforms.slice_helper(0x1000040, length = 0x400000), split=[0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1400040, pzf_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1450040, 0x400000, pzf_qsound_filenames)

    out_files.append({'filename': 'spf2xj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

def handle_spf2tu(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "pzfu.03a",
        "pzf.04"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x100000, 2, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(pzf_gfx_filenames, transforms.slice_helper(0x1000040, length = 0x400000), split=[0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1400040, pzf_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1450040, 0x400000, pzf_qsound_filenames)

    out_files.append({'filename': 'spf2tu.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Super Puzzle Fighter II Turbo                                            #
################################################################################

################################################################################
# START Super Gem Fighter Mini Mix                                             #
################################################################################
# game_70.arc: Pocket Fighter (JP)
# game_71.arc: Super Gem Fighter Mini Mix

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0280040       maincpu
#   0x0280040   0x0800040       ???
#   0x0800040   0x1C00040       gfx
#   0x1C00040   0x1C48040       audiocpu
#   0x1C50040   0x2550040       qsound

pcf_gfx_filenames = [
    'pcf.13m',
    'pcf.14m',
    'pcf.15m',
    'pcf.16m',
    'pcf.17m',
    'pcf.18m',
    'pcf.19m',
    'pcf.20m'
]

pcf_audiocpu_filenames = [
    'pcf.01',
    'pcf.02'
]

pcf_qsound_filenames = [
    'pcf.11m',
    'pcf.12m'
]

def handle_pfghtj(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "pcfj.03",
        "pcf.04",
        "pcf.05",
        "pcf.06",
        "pcf.07"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x280000, 5, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(pcf_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x1400000), split=[0x400000, 0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1C00040, pcf_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1C50040, 0x800000, pcf_qsound_filenames)

    out_files.append({'filename': 'pfghtj.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

def handle_sgemf(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "pcfu.03a",
        "pcf.04"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x280000, 5, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(pcf_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x1400000), split=[0x400000, 0x100000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x1C00040, pcf_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x1C50040, 0x800000, pcf_qsound_filenames)

    out_files.append({'filename': 'sgemf.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Super Gem Fighter Mini Mix                                               #
################################################################################


################################################################################
# START Hyper Street Fighter II: Anniversary Edition                           #
################################################################################
# game_80.arc: Hyper Street Fighter II: Anniversary Edition (JP)
# game_81.arc: Hyper Street Fighter II: Anniversary Edition

#   0x0000000   0x0000040       IBIS Header
#   0x0000040   0x0400040       maincpu
#   0x0400040   0x0800040       ???
#   0x0800040   0x2800040       gfx
#   0x2800040   0x2848040       audiocpu
#   0x2848040   0x2850040       ???
#   0x2850040   0x3050040       qsound

hs2_gfx_filenames = [
    'hs2.13m',
    'hs2.15m',
    'hs2.17m',
    'hs2.19m'
]

hs2_audiocpu_filenames = [
    'hs2.01',
    'hs2.02'
]

hs2_qsound_filenames = [
    'hs2.11m'
]

def handle_hsf2j(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "hs2j.03",
        "hs2j.04",
        "hs2j.05",
        "hs2j.06",
        "hs2j.07",
        "hs2j.08",
        "hs2j.09",
        "hs2j.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(hs2_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x800000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, hs2_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, hs2_qsound_filenames, num_chunks=1)

    out_files.append({'filename': 'hsf2j.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

def handle_hsf2(merged_contents): 
    out_files = []
    func_map = {}

    maincpu_filenames = [   
        "hs2u.03",
        "hs2u.04",
        "hs2.05",
        "hs2.06",
        "hs2.07",
        "hs2.08",
        "hs2.09",
        "hs2.10"
    ]
    func_map['maincpu'] = capcom.maincpu_cps2(0x40, 0x400000, 8, maincpu_filenames)
    func_map['gfx'] = capcom.gfx_cps2(hs2_gfx_filenames, transforms.slice_helper(0x0800040, length = 0x2000000), split=[0x800000])
    func_map['audiocpu'] = capcom.audiocpu_cps2(0x2800040, hs2_audiocpu_filenames)
    func_map['qsound'] = capcom.qsound_cps2(0x2850040, 0x800000, hs2_qsound_filenames, num_chunks=1)

    out_files.append({'filename': 'hsf2.zip', 'contents': merged_rom_handler(merged_contents, func_map)})

    return out_files

################################################################################
# END Hyper Street Fighter II: Anniversary Edition                             #
################################################################################

################################################################################
# START Red Earth                                                              #
################################################################################
# game_90.arc: Warzard (JP)
# game_91.arc: Red Earth

# This is CPS3. 
# The actual ROM is small - only 512KB - but there doesn't appear to be an exact match offhand.
# The majority of the data is in a CHD - but there doesn't appear to be an exact match offhand.

# Warzard has a 'JACK' header, but Red Earth has an 'IBIS' header. So they are likely a similar format.

# There are very 'word like' sections that cryptanalysis can be done with.
# EX: 0x1A490
#    orig: M:noadnouT:yuT:e
#  endian: :MondaonTuy:Tue:
# This section is pretty clearly days of week, followed by date format strings and months of year.
# It LOOKS like every 4 charcters are backwards 
#     sep: M:no | adno | uT:y | uT:e
#  4 char: on:M | onda | y:Tu | e:Tue
#  merged: on:Monday:Tue:Tue
# Doing this to the whole file gets us a lot of readable text (Days/Months/Error Strings                                                                                                                                                                                                                                           )... 
# But that readable text isn't in the romfile or compressed CHD.
# Did they pre-decompress the CHD for performance?

# There are CD001 headers - is this an ISO IMAGE?! https://en.wikipedia.org/wiki/ISO_9660#Specifications
# 2 Tracks:
#  0x1A1CF: hCD001� - type 68, ver 0 (invalid)
#  0x1D80C: hCD001� - type 68, ver 0 (invalid)
# There would be 32,768 bytes (0x8000) in a 'system area' before the first CD001 header
# This would mean the image starts at 0x1A1CF - 0x8000 = 0x121CF
# This is 0x0 - 0x121CF is NOT big enough to fit the 0x80000 ROM. Nor is 0x0 - 0x1A1CF. 
# More importantly - this isn't a valid ISO 9660
# The volume versions are invalid, there's not a primary or terminator...

# def handle_warzard(merged_contents): 
#     out_files = []
#     func_map = {}


#     def endian(contents):
#         contents = blob.byte_shuffle(contents, 4, [3, 2, 1, 0])
#         return { 'endian.bin': contents }

#     func_map['endian'] = endian
#     out_files.append({'filename': 'warzard.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
#     return out_files

# def handle_redearth(merged_contents): 
#     out_files = []
#     func_map = {}


#     def endian(contents):
#         contents = blob.byte_shuffle(contents, 4, [3, 2, 1, 0])
#         return { 'endian.bin': contents }

#     func_map['endian'] = endian
#     out_files.append({'filename': 'redearth.zip', 'contents': merged_rom_handler(merged_contents, func_map)})
#     return out_files

################################################################################
# END Red Earth                                                                #
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
        pkg_name = pkg_name_map.get(file_name)
        if not pkg_name == None:
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
        else:
            logger.info(f'Skipping unmatched file {file_path}!') 
    logger.info("""
        Processing complete. 
    """)
