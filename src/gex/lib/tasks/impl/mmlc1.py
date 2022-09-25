'''Implementation of mmlc1: Mega Man Legacy Collection 1'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MegaManLegacyCollection1Task(BaseTask):
    '''Implements mmlc1: Mega Man Legacy Collection 1'''
    _task_name = "mmlc1"
    _title = "Mega Man Legacy Collection 1"
    _details_markdown = '''
Based on MMLC & DAC Extractor - https://github.com/HTV04/mmlc-dac-extractor
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("Suzy")
    _input_folder_desc = "'Suzy' Folder (Steam MMLC install folder)"

    _game_info_list = [
        {
            'filename': 'rockman.nes',
            'name': 'Rockman',
            'sections': {
                'prg': {'start': 0x512230, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        },
        {
            'filename': 'rockman2.nes',
            'name': 'Rockman 2 - Dr Wily no Nazo',
            'sections': {
                'prg': {'start': 0x2F20F0, 'length': 0x40000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'rockman3.nes',
            'name': 'Rockman 3 - Dr Wily no Saigo!',
            'sections': {
                'prg': {'start': 0x332130, 'length': 0x60000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x10\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'rockman4.nes',
            'name': 'Rockman 4 - Aratanaru Yabou!!',
            'sections': {
                'prg': {'start': 0x392170, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x20\x00\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'rockman5.nes',
            'name': 'Rockman 5 - Blues no Wana!',
            'sections': {
                'prg': {'start': 0x4121B0, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x20\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'rockman6.nes',
            'name': 'Rockman 6 - Shijou Saidai no Tatakai!!',
            'sections': {
                'prg': {'start': 0x4921F0, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x20\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman.nes',
            'name': 'Mega Man',
            'sections': {
                'prg': {'start': 0x2AEEB0, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman2.nes',
            'name': 'Mega Man 2',
            'sections': {
                'prg': {'start': 0x8ED70, 'length': 0x40000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman3.nes',
            'name': 'Mega Man 3',
            'sections': {
                'prg': {'start': 0xCEDB0, 'length': 0x40000},
                'cha': {'start': 0x10EDB0, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman4.nes',
            'name': 'Mega Man 4',
            'sections': {
                'prg': {'start': 0x12EDF0, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x20\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman5.nes',
            'name': 'Mega Man 5',
            'sections': {
                'prg': {'start': 0x1AEE30, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x10\x20\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'megaman6.nes',
            'name': 'Mega Man 6',
            'sections': {
                'prg': {'start': 0x22EE70, 'length': 0x80000}
            },
            'header': b'\x4E\x45\x53\x1A\x20\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        }
    ]

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': "good",
            'system': "NES",
            "notes": []},
            self._game_info_list)

    def execute(self, in_dir, out_dir):
        exe_path = os.path.join(in_dir, 'Proteus.exe')
        with open(exe_path, 'rb') as exe_file:
            exe_data = exe_file.read()

            for game_info in self._game_info_list:
                logger.info(f"Extracting {game_info['name']}...")
                game_data = bytearray()
                game_data.extend(game_info['header'])
                for section in game_info['sections'].values():
                    game_data.extend(exe_data[section['start']:section['start']+section['length']])

                with open(os.path.join(out_dir, game_info['filename']), "wb") as out_file:
                    out_file.write(game_data)

        logger.info("Processing complete.")
