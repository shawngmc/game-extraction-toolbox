'''Implementation of mmxlc1: Mega Man X Legacy Collection 1'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MegaManXLegacyCollection1Task(BaseTask):
    '''Implements mmxlc1: Mega Man X Legacy Collection 1'''
    _task_name = "mmxlc1"
    _title = "Mega Man X Legacy Collection 1"
    _details_markdown = '''
Based on: https://github.com/s3phir0th115/MMXLC1-Rom-Extractor/blob/master/mmxlc_rom_extract.py

Mega Man X4 does not appear to be ROM based, but investigation is ongoing.
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("Mega Man X Legacy Collection")
    _input_folder_desc = "Steam MMxLC install folder"
    _out_file_notes = {}
    _game_info_list = [
        {
            'filename': 'rockmanx.sfc',
            'name': 'Rockman X',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0xB8C4E0, 'length': 0x180000}
            }
        },
        {
            'filename': 'rockmanx2.sfc',
            'name': 'Rockman X2',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0xF8C4E0, 'length': 0x180000}
            }
        },
        {
            'filename': 'rockmanx3.sfc',
            'name': 'Rockman X3',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0x128C4E0, 'length': 0x200000}
            }
        },
        {
            'filename': 'N/A',
            'name': 'Rockman X4',
            "system": "Playstation",
            "status": "no-rom"
        },
        {
            'filename': 'megamanx.sfc',
            'name': 'Mega Man X',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0xD8C4E0, 'length': 0x180000}
            }
        },
        {
            'filename': 'megamanx2.sfc',
            'name': 'Mega Man X2',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0x110C4E0, 'length': 0x180000}
            }
        },
        {
            'filename': 'megamanx3.sfc',
            'name': 'Mega Man X3',
            "system": "SNES",
            "status": "good",
            'sections': {
                'rom': {'start': 0x148C4E0, 'length': 0x200000}
            }
        },
        {
            'filename': 'N/A',
            'name': 'Mega Man X4',
            "system": "Playstation",
            "status": "no-rom"
        }
    ]

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': x['status'],
            'system': x['system'],
            "notes": []},
            self._game_info_list)

    def execute(self, in_dir, out_dir):
        exe_path = os.path.join(in_dir, 'RXC1.exe')
        with open(exe_path, 'rb') as exe_file:
            exe_data = exe_file.read()

            for game_info in self._game_info_list:
                if game_info['status'] == 'good':
                    logger.info(f"Extracting {game_info['name']}...")
                    game_data = bytearray()
                    for section in game_info['sections'].values():
                        game_data.extend(exe_data[section['start']:section['start']+section['length']])

                    with open(os.path.join(out_dir, game_info['filename']), "wb") as out_file:
                        out_file.write(game_data)

        logger.info("Processing complete.")
