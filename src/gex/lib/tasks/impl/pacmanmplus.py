'''Implementation of pacmanmplus: Pac Man Museum Plus'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class PacManMuseumPlusTask(BaseTask):
    '''Implements pacmanmplus: Pac Man Museum Plus'''
    _task_name = "pacmanmplus"
    _title = "Pac Man Museum Plus"
    _details_markdown = ''''''
    _default_input_folder = helpers.gen_steam_app_default_folder("PAC-MAN MUSEUM PLUS")
    _input_folder_desc = "Pac Man Museum Plus install folder"

    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }
    _game_info_map = [
        {
            "name": "PAC Land",
            "system": "Arcade",
            "filename": "paclandj.zip",
            "in": {
                "filename": "GamePacland_pacmuseum2021_windows_x64_Release.dll",
                "start": 170352,
                "length": 116880
            },
            "out": [
                { "filename": "pl1-2.1t", "start": 0x00000, "length": 0x400 },
                { "filename": "pl1-1.1r", "start": 0x00400, "length": 0x400 },
                { "filename": "pl1-5.5t", "start": 0x00800, "length": 0x400 },
                { "filename": "pl1-4.4n", "start": 0x00C00, "length": 0x400 },
                { "filename": "pl1-3.6l", "start": 0x01000, "length": 0x400 },
                { "filename": "pl6_01.8b", "start": 0x01400, "length": 0x4000 },
                { "filename": "pl6_02.8d", "start": 0x05400, "length": 0x4000 },
                { "filename": "pl1_3.8e", "start": 0x09400, "length": 0x4000 },
                { "filename": "pl1_4.8f", "start": 0x0D400, "length": 0x4000 },
                { "filename": "pl1_5.8h", "start": 0x11400, "length": 0x4000 },
                { "filename": "pl1_6.8j", "start": 0x15400, "length": 0x4000 },
                { "filename": "pl1_7.3e", "start": 0x19400, "length": 0x2000 },
                { "filename": "cus60-60a1.mcu", "start": 0x1B400, "length": 0x1000 },
                { "filename": "pl6_12.6n", "start": 0x1C400, "length": 0x2000 },
                { "filename": "pl1_13.6t", "start": 0x1E400, "length": 0x2000 },
                { "filename": "pl1_9b.6f", "start": 0x20400, "length": 0x4000 },
                { "filename": "pl1_8.6e", "start": 0x24400, "length": 0x4000 },
                { "filename": "pl1_10b.7e", "start": 0x28400, "length": 0x4000 },
                { "filename": "pl1_11.7f", "start": 0x2C400, "length": 0x4000 }
            ],
            "status": "playable",
            "notes": [4]
        },
        {
            "name": "PAC Attack",
            "system": "SNES",
            "filename": "pacattack.zip",
            "in": {
                "filename": "GameSFC_Pacattack_pacmuseum2021_windows_x64_Release.dll",
                "start": 0,
                "length": 600000
            },
            "out": [],
            "status": 'partial',
            "notes": [1, 8]
        },
        {
            "name": "Super PAC-MAN",
            "system": "Arcade",
            "filename": "superpac.zip",
            "in": {
                "filename": "GameSuperpacman_pacmuseum2021_windows_x64_Release.dll",
                "start": 141616,
                "length": 58144
            },
            "out": [
                {"filename": "sp1-2.1c", "start": 0x2000, "length": 0x2000},
                {"filename": "sp1-1.1b", "start": 0x4000, "length": 0x2000},
                {"filename": "spc-3.1k", "start": 0x6000, "length": 0x1000},
                {"filename": "sp1-6.3c", "start": 0x8000, "length": 0x1000},
                {"filename": "spv-2.3f", "start": 0x9000, "length": 0x2000},
                {"filename": "superpac.4c", "start": 0xE000, "length": 0x20},
                {"filename": "superpac.4e", "start": 0xE020, "length": 0x100},
                {"filename": "superpac.3l", "start": 0xE120, "length": 0x100},
                {"filename": "superpac.3m", "start": 0xE220, "length": 0x100}
            ],
            "status": 'good',
            "notes": []
        },
        {
            "name": "PAC Motos",
            "system": "Wii",
            "filename": "N/A",
            "status": 'no-rom',
            "notes": [2]
        },
        {
            "name": "PAC'N Roll Remix",
            "system": "Wii",
            "filename": "N/A",
            "status": 'no-rom',
            "notes": [2]
        },
        {
            "name": "PAC-MAN BATTLE ROYALE",
            "system": "Arcade",
            "filename": "N/A",
            "status": 'no-rom',
            "notes": [2]
        },
        {
            "name": "PAC'N Roll Remix",
            "system": "Mobile",
            "filename": "N/A",
            "status": 'no-rom',
            "notes": [2]
        },
        # PAC-IN-TIME
        # Official ROM is 1,048,576
        # DLL is 1,062,400
        # So, it really does need to be compressed!
        # binwalk -e -M doesn't find anything
        {
            "name": "PAC-IN-TIME",
            "system": "SNES",
            "filename": "pacintime.zip",
            "in": {
                "filename": "GameSFC_Pacintime_pacmuseum2021_windows_x64_Release.dll",
                "start": 0,
                "length": 1062400
            },
            "out": [],
            "status": 'partial',
            "notes": [1, 8]
        },
        {
            "name": "PAC and Pal",
            "system": "Arcade",
            "filename": "pacnpal.zip",
            "in": {
                "filename": "GamePacandpal_pacmuseum2021_windows_x64_Release.dll",
                "start": 141424,
                "length": 58144
            },
            "out": [
                {"filename": "pap1-3b.1d", "start": 0x0000, "length": 0x2000},
                {"filename": "pap1-2b.1c", "start": 0x2000, "length": 0x2000},
                {"filename": "pap3-1.1b", "start": 0x4000, "length": 0x2000},
                {"filename": "pap1-4.1k", "start": 0x6000, "length": 0x1000},
                {"filename": "pap1-6.3c", "start": 0x8000, "length": 0x1000},
                {"filename": "pap1-5.3f", "start": 0x9000, "length": 0x2000},
                {"filename": "pap1-6.4c", "start": 0xE000, "length": 0x20},
                {"filename": "pap1-5.4e", "start": 0xE020, "length": 0x100},
                {"filename": "pap1-4.3l", "start": 0xE120, "length": 0x100},
                {"filename": "pap1-3.3m", "start": 0xE220, "length": 0x100}
            ],
            "status": 'good',
            "notes": []
        },
        {
            "name": "PAC-MANIA",
            "system": "Arcade",
            "filename": "pacmania.zip",
            "in": {
                "filename": "GamePacmania_Pacmuseum2021_windows_x64_Release.dll",
                "start": 208768,
                "length": 1445930
            },
            "out": [
                {"filename": "pn2_v0.bin", "start": 0x000000, "length": 0x10000},
                {"filename": "pn_chr-0.bin", "start": 0x01000A, "length": 0x20000},
                {"filename": "pn_chr-1.bin", "start": 0x03000A, "length": 0x20000},
                {"filename": "pn_chr-2.bin", "start": 0x05000A, "length": 0x20000},
                {"filename": "pn_chr-3.bin", "start": 0x07000A, "length": 0x20000},
                {"filename": "pn2_c8.bin", "start": 0x090012, "length": 0x10000},
                {"filename": "pn_obj-0.bin", "start": 0x0A0012, "length": 0x20000},
                {"filename": "pnx_obj1.bin", "start": 0x0C0012, "length": 0x20000},
                {"filename": "pn_prg-6.bin", "start": 0x0E002A, "length": 0x20000},
                {"filename": "pn2_p7.bin", "start": 0x10002A, "length": 0x10000},
                {"filename": "pn2_s0.bin", "start": 0x11002A, "length": 0x10000},
                {"filename": "pn2_s1.bin", "start": 0x127FF0, "length": 0x10000},
                {"filename": "cus64-64a1.mcu", "start": 0x16002A, "length": 0x1000}
            ],
            "status": 'playable',
            "notes": [3]
        },
        {
            "name": "PAC-MAN",
            "system": "Arcade",
            "filename": "puckman.zip",
            "in": {
                "filename": "GamePacman_pacmuseum2021_windows_x64_Release.dll",
                "start": 139008,
                "length": 77344
            },
            "out": [
                {"filename": "pm1_prg1.6e", "start": 0x00000, "length": 0x800},
                {"filename": "pm1_prg2.6k", "start": 0x00800, "length": 0x800},
                {"filename": "pm1_prg3.6f", "start": 0x01000, "length": 0x800},
                {"filename": "pm1_prg4.6m", "start": 0x01800, "length": 0x800},
                {"filename": "pm1_prg5.6h", "start": 0x02000, "length": 0x800},
                {"filename": "pm1_prg6.6n", "start": 0x02800, "length": 0x800},
                {"filename": "pm1_prg7.6j", "start": 0x03000, "length": 0x800},
                {"filename": "pm1_prg8.6p", "start": 0x03800, "length": 0x800},
                # 0x04000 - 0x10000: Empty
                {"filename": "pm1-3.1m", "start": 0x10000, "length": 0x100},
                {"filename": "pm1-1.7f", "start": 0x10100, "length": 0x20},
                {"filename": "pm1-4.4a", "start": 0x10120, "length": 0x100},
                # 0x10220 - 0x10A20: ???
                {"filename": "pm1_chg1.5e", "start": 0x10A20, "length": 0x800},
                {"filename": "pm1_chg2.5h", "start": 0x11220, "length": 0x800},
                {"filename": "pm1_chg3.5f", "start": 0x11A20, "length": 0x800},
                {"filename": "pm1_chg4.5j", "start": 0x12220, "length": 0x800},
                {"filename": "pm1-2.3m", "start": 0x12A20, "length": 0x100},
                # 0x12A20 - 0x12E20: ???
            ],
            "status": 'playable',
            "notes": [4]
        },
        {
            "name": "PAC-MAN ARRANGEMENT Arcade Ver.",
            "system": "Arcade",
            "filename": "pacman_arrangement_arcade.zip",
            "in": {
                "filename": "GamePacmanarrangement_pacmuseum2021_windows_x64_Release.dll",
                "start": 423008,
                "length": 7864320
            },
            "status": 'partial',
            "notes": [1, 5]
        },
        {
            "name": "PAC-MAN ARRANGEMENT Console Ver.",
            "system": "???",
            "filename": "pacman_arrangement_console.zip",
            "in": {
                "filename": "GamePacmanarrangement_pacmuseum2021_windows_x64_Release.dll",
                "start": 423008,
                "length": 7864320
            },
            "status": 'partial',
            "notes": [1, 6]
        },
        {
            "name": "PAC-MAN CHAMPIONSHIP EDITION",
            "system": "Windows Port",
            "filename": "N/A",
            "status": 'no-rom',
            "notes": [2, 7]
        }
    ]

    _out_file_notes = {
        "1": "This tool cannot create a playable extraction for this title.",
        "2": "This title not ROM-based (a rebuild or a native Windows port), so no extraction is possible.",
        "3": "Along with some CRC mismatches, this game renders upside-down. MAME and RetroArchMAME have slightly different ways to fix this per game.",
        "4": "There are minor CRC mismatches, but this ROM works properly.",
        "5": "MAME does not appear to support this Arcade title, which was originally part of Namco Classic Collection Vol. 2.",
        "6": "This title is likely a native/DirectX port for XBox 360, and not a packagable ROM.",
        "7": "This title appears to launch with a Bandai Namco splash and is likely a native/DirectX port.",
        "8": "These SNES titles do not appear to be raw or LZMA compressed in the DLL, and cannot yet be extracted."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': x['status'],
            'system': x['system'],
            "notes": x['notes']},
            self._game_info_map)

    def execute(self, in_dir, out_dir):
        for game in self._game_info_map:
            if game.get('status') == "no-rom":
                logger.info(f"Skipping {game['name']} as there is no ROM to extract...")
                continue

            is_partial = game.get('status') == "partial"
            if not self._props.get('include-partials') and is_partial:
                logger.info(f"Skipping {game['name']} as this tool cannot extract a working copy...")
                continue

            src_file = os.path.join(in_dir, r"PAC-MAN MUSEUM+_Data\Plugins\x86_64", game['in']['filename'])
            if not os.path.exists(src_file):
                logger.info(f"Skipping {game['name']} as this tool cannot find it in the given Steam library folder...")
                continue

            logger.info(f"Extracting {game['name']}...")
            with open(src_file, 'rb') as dll_file:
                contents = dll_file.read()
                zip_files = {}

                contents = transforms.cut(contents, game['in']['start'], length=game['in']['length'])
                if game['system'] == "Arcade":
                    lzd = lzma.LZMADecompressor()
                    contents = lzd.decompress(contents)
                    if is_partial:
                        zip_files["decompressed_blob"] = contents

                    for work_file in game.get('out') or []:
                        zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])
                else:
                    if is_partial:
                        zip_files["blob"] = contents

                    for work_file in game.get('out') or []:
                        zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])

                filename = f"partial_{game['filename']}" if  is_partial else game['filename']
                logger.info(f"Saving {filename}...")
                with open(os.path.join(out_dir, filename), "wb") as out_file:
                    out_file.write(helpers.build_zip(zip_files))

        logger.info("Processing complete.")
