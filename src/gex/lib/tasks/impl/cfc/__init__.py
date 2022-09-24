'''Implementation of cfc: Capcom Fighting Collection'''
import re
import glob
import logging
import os

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class CFCTask(BaseTask):
    '''Implements cfc: Capcom Fighting Collection'''
    _task_name = "cfc"
    _title = "Capcom Fighting Collection"
    _details_markdown = '''
This is reverse-engineered based on the CBEYB work from https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below. All CRCs are currently mismatched.
'''
    _out_file_list = [
        {
            "game": "Darkstalkers: The Night Warriors (U)",
            "system": "Arcade",
            "filename": "dstlku.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Darkstalkers: The Night Warriors (J)",
            "system": "Arcade",
            "filename": "vampj.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Night Warriors:Darkstalkers' Revenge (U)",
            "system": "Arcade",
            "filename": "nwarru.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Night Warriors:Darkstalkers' Revenge (J)",
            "system": "Arcade",
            "filename": "vhuntjr2.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Vampire Savior: The Lord of Vampire (U)",
            "system": "Arcade",
            "filename": "vsavu.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Vampire Hunter 2: Darkstalkers Revenge (J)",
            "system": "Arcade",
            "filename": "vhunt2.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Vampire Savior 2: The Lord of Vampire (J)",
            "system": "Arcade",
            "filename": "vsav2.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Cyberbots: Fullmetal Madness (U)",
            "system": "Arcade",
            "filename": "cybotsj.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Cyberbots: Fullmetal Madness (J)",
            "system": "Arcade",
            "filename": "cybotsu.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Super Puzzle Fighter II Turbo (U)",
            "system": "Arcade",
            "filename": "spf2tu.zip",
            "status": "playable",
            "notes": [1, 3]
        },
        {
            "game": "Super Puzzle Fighter II Turbo (J)",
            "system": "Arcade",
            "filename": "spf2xj.zip",
            "status": "playable",
            "notes": [1, 3]
        },
        {
            "game": "Super Gem Fighter Mini Mix (U)",
            "system": "Arcade",
            "filename": "sgemf.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Super Gem Fighter Mini Mix (J)",
            "system": "Arcade",
            "filename": "pfghtj.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Hyper Street Fighter II: Anniversary Edition (U)",
            "system": "Arcade",
            "filename": "hsf2.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Hyper Street Fighter II: Anniversary Edition (J)",
            "system": "Arcade",
            "filename": "hsf2j.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Red Earth (U)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [2]
        },
        {
            "game": "Warzard (J)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [2]
        }
    ]
    _out_file_notes = {
        "1": "These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require",
        "2": "This CPS3 game cannot yet be extracted.",
        "3": "The US version of this does not have a valid MAME release.",
        "4": "The JP version of this is using an older internal file naming convention."
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("CAPCOM FIGHTING COLLECTION")
    _input_folder_desc = "CFC Steam folder"

    def execute(self, in_dir, out_dir):
        pak_files = self._find_files(in_dir)
        for file_path in pak_files:
            file_name = os.path.basename(file_path)
            pkg_name = self._pkg_name_map.get(file_name)
            if pkg_name is not None:
                logger.info(f"Extracting {file_name}: {pkg_name}")
                try:
                    with open(file_path, "rb") as curr_file:
                        file_content = bytearray(curr_file.read())
                        arc_contents = arc.extract(file_content)
                        output_files = []

                        # Get the bin entry
                        merged_rom_contents = None
                        for _, arc_content in arc_contents.items():
                            if arc_content['path'].startswith('bin'):
                                merged_rom_contents = arc_content['contents']

                        handler_func = self.find_handler_func(pkg_name)
                        if merged_rom_contents is not None and handler_func is not None:
                            output_files = handler_func(merged_rom_contents)

                            for output_file in output_files:
                                with open(os.path.join(out_dir, output_file['filename']), "wb") as out_file:
                                    out_file.write(output_file['contents'])
                        elif merged_rom_contents is None:
                            logger.warning(
                                "Could not find merged rom data in arc.")
                        elif handler_func is None:
                            logger.warning(
                                "Could not find matching handler function.")
                except Exception as _:
                    logger.warning(f'Error while processing {file_path}!')
            else:
                logger.info(f'Skipping unmatched file {file_path}!')
        logger.info("Processing complete.")

    _pkg_name_map = {
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

    def _find_files(self, base_path):
        arc_path = os.path.join(base_path, "nativeDX11x64", "arc", "pc")
        candidate_files = glob.glob(arc_path + '/game_*.arc')
        archive_list = []
        for candidate in candidate_files:
            if re.search(r'game_\d\d.arc', candidate):
                archive_list.append(candidate)
        return archive_list

    ################################################################################
    # Darkstalkers/Vampire: The Night Warriors                                     #
    ################################################################################

    _vam_gfx_filenames = [
        'vam.13m',
        'vam.14m',
        'vam.15m',
        'vam.16m',
        'vam.17m',
        'vam.18m',
        'vam.19m',
        'vam.20m'
    ]

    _vam_audiocpu_filenames = [
        'vam.01',
        'vam.02'
    ]

    _vam_qsound_filenames = [
        'vam.11m',
        'vam.12m'
    ]

    def _handle_vampj(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vam_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x1400000), split=[0x400000, 0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1C00040, self._vam_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1C50040, 0x400000, self._vam_qsound_filenames)

        out_files.append({'filename': 'vampj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_dstlku(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vam_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x1400000), split=[0x400000, 0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1C00040, self._vam_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1C50040, 0x400000, self._vam_qsound_filenames)

        out_files.append({'filename': 'dstlku.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Vampire Hunter/Night Warriors: Darkstalkers' Revenge                         #
    ################################################################################

    _vph_gfx_filenames = [
        'vph.13m',
        'vph.14m',
        'vph.15m',
        'vph.16m',
        'vph.17m',
        'vph.18m',
        'vph.19m',
        'vph.20m'
    ]

    _vph_audiocpu_filenames = [
        'vph.01',
        'vph.02'
    ]

    _vph_qsound_filenames = [
        'vph.11m',
        'vph.12m'
    ]

    def _handle_vhuntjr2(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vph_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vph_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, self._vph_qsound_filenames)

        out_files.append({'filename': 'vhuntjr2.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_nwarru(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vph_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vph_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, self._vph_qsound_filenames)

        out_files.append({'filename': 'nwarru.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Vampire Savior: The Lord of Vampire                                          #
    ################################################################################

    _vm3_gfx_filenames = [
        'vm3.13m',
        'vm3.14m',
        'vm3.15m',
        'vm3.16m',
        'vm3.17m',
        'vm3.18m',
        'vm3.19m',
        'vm3.20m'
    ]

    _vm3_audiocpu_filenames = [
        'vm3.01',
        'vm3.02'
    ]

    _vm3_qsound_filenames = [
        'vm3.11m',
        'vm3.12m'
    ]

    def _handle_vsavj(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vm3_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vm3_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._vm3_qsound_filenames)

        out_files.append({'filename': 'vsavj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_vsavu(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vm3_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vm3_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._vm3_qsound_filenames)

        out_files.append({'filename': 'vsavu.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Vampire Hunter 2: Darkstalkers Revenge                                       #
    ################################################################################

    _vh2_gfx_filenames = [
        'vh2.13m',
        'vh2.14m',
        'vh2.15m',
        'vh2.16m',
        'vh2.17m',
        'vh2.18m',
        'vh2.19m',
        'vh2.20m'
    ]

    _vh2_audiocpu_filenames = [
        'vh2.01',
        'vh2.02'
    ]

    _vh2_qsound_filenames = [
        'vh2.11m',
        'vh2.12m'
    ]

    def _handle_vhunt2(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vh2_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vh2_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._vh2_qsound_filenames)

        out_files.append({'filename': 'vhunt2.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Vampire Savior 2: The Lord of Vampire                                        #
    ################################################################################

    _vs2_gfx_filenames = [
        'vs2.13m',
        'vs2.14m',
        'vs2.15m',
        'vs2.16m',
        'vs2.17m',
        'vs2.18m',
        'vs2.19m',
        'vs2.20m'
    ]

    _vs2_audiocpu_filenames = [
        'vs2.01',
        'vs2.02'
    ]

    _vs2_qsound_filenames = [
        'vs2.11m',
        'vs2.12m'
    ]

    def _handle_vsav2(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._vs2_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._vs2_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._vs2_qsound_filenames)

        out_files.append({'filename': 'vsav2.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Cyberbots: Fullmetal Madness                                                 #
    ################################################################################

    _cybots_gfx_filenames = [
        'cyb.13m',
        'cyb.14m',
        'cyb.15m',
        'cyb.16m',
        'cyb.17m',
        'cyb.18m',
        'cyb.19m',
        'cyb.20m'
    ]

    _cybots_audiocpu_filenames = [
        'cyb.01',
        'cyb.02'
    ]

    _cybots_qsound_filenames = [
        'cyb.11m',
        'cyb.12m'
    ]

    def _handle_cybotsj(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._cybots_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._cybots_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, self._cybots_qsound_filenames)

        out_files.append({'filename': 'cybotsj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_cybotsu(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._cybots_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._cybots_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, self._cybots_qsound_filenames)

        out_files.append({'filename': 'cybotsu.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Super Puzzle Fighter II Turbo                                                #
    ################################################################################

    _pzf_gfx_filenames = [
        'pzf.14m',
        'pzf.16m',
        'pzf.18m',
        'pzf.20m'
    ]

    _pzf_audiocpu_filenames = [
        'pzf.01',
        'pzf.02'
    ]

    _pzf_qsound_filenames = [
        'pzf.11m',
        'pzf.12m'
    ]

    def _handle_spf2xj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "pzfj.03a",
            "pzf.04"
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x100000, 2, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._pzf_gfx_filenames, helpers.slice_helper(
            0x1000040, length=0x400000), split=[0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1400040, self._pzf_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1450040, 0x400000, self._pzf_qsound_filenames)

        out_files.append({'filename': 'spf2xj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_spf2tu(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "pzfu.03a",
            "pzf.04"
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x100000, 2, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._pzf_gfx_filenames, helpers.slice_helper(
            0x1000040, length=0x400000), split=[0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1400040, self._pzf_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1450040, 0x400000, self._pzf_qsound_filenames)

        out_files.append({'filename': 'spf2tu.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Super Gem Fighter Mini Mix                                                   #
    ################################################################################

    _pcf_gfx_filenames = [
        'pcf.13m',
        'pcf.14m',
        'pcf.15m',
        'pcf.16m',
        'pcf.17m',
        'pcf.18m',
        'pcf.19m',
        'pcf.20m'
    ]

    _pcf_audiocpu_filenames = [
        'pcf.01',
        'pcf.02'
    ]

    _pcf_qsound_filenames = [
        'pcf.11m',
        'pcf.12m'
    ]

    def _handle_pfghtj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "pcfj.03",
            "pcf.04",
            "pcf.05",
            "pcf.06",
            "pcf.07"
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x280000, 5, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._pcf_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x1400000), split=[0x400000, 0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1C00040, self._pcf_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1C50040, 0x800000, self._pcf_qsound_filenames)

        out_files.append({'filename': 'pfghtj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_sgemf(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "pcfu.03a",
            "pcf.04"
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x280000, 5, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._pcf_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x1400000), split=[0x400000, 0x100000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x1C00040, self._pcf_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x1C50040, 0x800000, self._pcf_qsound_filenames)

        out_files.append({'filename': 'sgemf.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Hyper Street Fighter II: Anniversary Edition                                 #
    ################################################################################

    _hs2_gfx_filenames = [
        'hs2.13m',
        'hs2.15m',
        'hs2.17m',
        'hs2.19m'
    ]

    _hs2_audiocpu_filenames = [
        'hs2.01',
        'hs2.02'
    ]

    _hs2_qsound_filenames = [
        'hs2.11m'
    ]

    def _handle_hsf2j(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._hs2_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x800000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._hs2_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._hs2_qsound_filenames, num_chunks=1)

        out_files.append({'filename': 'hsf2j.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    def _handle_hsf2(self, merged_contents):
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
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(self._hs2_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x800000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, self._hs2_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, self._hs2_qsound_filenames, num_chunks=1)

        out_files.append({'filename': 'hsf2.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})

        return out_files

    ################################################################################
    # Red Earth                                                                    #
    ################################################################################
    # game_90.arc: Warzard (JP)
    # game_91.arc: Red Earth

    # This does not appear to be the old NO-CD release (0.139 would target it!)

    # This is CPS3.
    # The actual ROM is small - only 512KB - but there doesn't appear to be an exact match offhand.
    # The majority of the data is in a CHD - but there doesn't appear to be an exact match offhand.

    # Warzard has a 'JACK' header, but Red Earth has an 'IBIS' header. Likely same format.

    # There are very 'word like' sections that cryptanalysis can be done with.
    # EX: 0x1A490
    #    orig: M:noadnouT:yuT:e
    #  endian: :MondaonTuy:Tue:
    # This section is pretty clearly days of week, date format strings and months of year.
    # It LOOKS like every 4 charcters are backwards
    #     sep: M:no | adno | uT:y | uT:e
    #  4 char: on:M | onda | y:Tu | e:Tue
    #  merged: on:Monday:Tue:Tue
    # Doing this to the whole file gets us a lot of readable text (Days/Months/Error Strings)...
    # But that readable text isn't in the romfile or compressed CHD.
    # Did they pre-decompress the CHD for performance?

    # There are CD001 headers - is this an ISO IMAGE?!
    # https://en.wikipedia.org/wiki/ISO_9660#Specifications
    # 2 Tracks:
    #  0x1A1CF: hCD001� - type 68, ver 0 (invalid)
    #  0x1D80C: hCD001� - type 68, ver 0 (invalid)
    # There would be 32,768 bytes (0x8000) in a 'system area' before the first CD001 header
    # This would mean the image starts at 0x1A1CF - 0x8000 = 0x121CF
    # This is 0x0 - 0x121CF is NOT big enough to fit the 0x80000 ROM. Nor is 0x0 - 0x1A1CF.
    # More importantly - this isn't a valid ISO 9660
    # The volume versions are invalid, there's not a primary or terminator...

    # 0x0 - 0x40 is the IBIS/JACK header.
    # 0x40 - 0x1FF40 matches 0x0 - 0x1FF00 in the dump from MAME.
    # After that, however, the files differ substantially - the vast majority of the file from CFC is blank.

    # After 0x80040 there needs to be the equivalent of the .CHD file for the game. (TLDR, CPS3 games had a ROM and a CD-ROM, and MAME uses the .CHD to represent the CDROM.)

    # However, even a larger dump saveo warzard-full.bin,0,2080000 looks like it has the CHD header, etc.

    # def _handle_warzard(self, merged_contents):
    #     out_files = []
    #     func_map = {}

    #     def endian(contents):
    #         contents = transforms.byte_shuffle(contents, 4, [3, 2, 1, 0])
    #         return { 'endian.bin': contents }

    #     func_map['endian'] = endian
    #     out_files.append(
    #         {'filename': 'warzard.zip', 'contents': helpers.build_rom(merged_contents, func_map)}
    #     )
    #     return out_files

    # def _handle_redearth(self, merged_contents):
    #     out_files = []
    #     func_map = {}

    #     def endian(contents):
    #         contents = transforms.byte_shuffle(contents, 4, [3, 2, 1, 0])
    #         return { 'endian.bin': contents }

    #     func_map['endian'] = endian
    #     out_files.append(
    #         {'filename': 'redearth.zip', 'contents': helpers.build_rom(merged_contents, func_map)}
    #     )
    #     return out_files
