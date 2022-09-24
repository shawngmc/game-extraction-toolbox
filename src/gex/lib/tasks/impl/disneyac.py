'''Implemntation of disneyac: Disney Afternoon Collection'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class DisneyAfternoonCollectionTask(BaseTask):
    '''Implemnts disneyac: Disney Afternoon Collection'''
    _task_name = "disneyac"
    _title = "Disney Afternoon Collection"
    _details_markdown = '''
Based on MMLC & DAC Extractor - https://github.com/HTV04/mmlc-dac-extractor
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("DisneyAfternoon")
    _input_folder_desc = "DisneyAfternoon Folder (Steam install folder)"

    _game_info_list = [
        {
            'filename': 'Chip n Dale - Rescue Rangers (DAC).nes',
            'name': 'Chip n Dale - Rescue Rangers',
            'sections': {
                'prg': {'start': 0x7F2F30, 'length': 0x40000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x10\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'Chip n Dale - Rescue Rangers 2 (DAC).nes',
            'name': 'Chip n Dale - Rescue Rangers 2',
            'sections': {
                'prg': {'start': 0x832F30, 'length': 0x40000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x10\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'Darkwing Duck (DAC).nes',
            'name': 'Darkwing Duck',
            'sections': {
                'prg': {'start': 0x792F30, 'length': 0x20000},
                'cha': {'start': 0x772F30, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x10\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'DuckTales (DAC).nes',
            'name': 'DuckTales',
            'sections': {
                'prg': {'start': 0x7B2F30, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'DuckTales 2 (DAC).nes',
            'name': 'DuckTales 2',
            'sections': {
                'prg': {'start': 0x7D2F30, 'length': 0x20000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x00\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        },
        {
            'filename': 'TaleSpin (DAC).nes',
            'name': 'TaleSpin',
            'sections': {
                'prg': {'start': 0x872F30, 'length': 0x40000}
            },
            'header': b'\x4E\x45\x53\x1A\x08\x10\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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
        exe_path = os.path.join(in_dir, 'capcom_disney_afternoon.exe')
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
