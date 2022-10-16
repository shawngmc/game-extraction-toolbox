'''Implementation of ssp: Sega Smash Pack'''
import logging
import os
import glob
from gex.lib.archive.kvq import extract
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

ENCODE_STRING_BYTES = bytearray('Encoded for KGen Ultra / Sega Smash Pack / Snake KML 1999! ', 'ascii')

class SSPTask(BaseTask):
    '''Implements ssp: Sega Smash Pack'''
    _task_name = "ssp"
    _title = "Sega Smash Pack"
    _details_markdown = '''
Based on: https://github.com/zZeck/SegaSmashPackPCUtils

These ROMs are pulled out of kvq files. 
    '''
    _default_input_folder = r"C:\Sega\Smash Pack\MyGames"
    _input_folder_desc = "Sega Smash Pack folder"
    _out_file_notes = {}

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']} ({x['region']})",
            'system': "Genesis",
            'status': 'good'
,            "notes": []},
            self._game_info_map.values())
        self._out_file_notes = {}

    def execute(self, in_dir, out_dir):
        rom_files = self._find_files(in_dir)
        for file_path in rom_files:
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if game_info is not None:
                display_name = game_info['name']
                if game_info['region']:
                    display_name += f' ({game_info["region"]})'
                logger.info(f"Copying {file_name}: {display_name}")
                try:
                    with open(file_path, 'rb') as kvq_file:
                        kvq_bytes = kvq_file.read()
                        rom_bytes = extract(kvq_bytes, ENCODE_STRING_BYTES)
                        with open(os.path.join(out_dir, game_info['filename']), 'wb') as out_file:
                            out_file.write(rom_bytes)
                except OSError as error:
                    logger.warning(f'Error while processing {file_path}!')
                    logger.warning(error)
            else:
                logger.info(f'Skipping unmatched file {file_path}!')
        logger.info("Processing complete.")

    _game_info_map = {
        'Altered Beast.kvq': {
            'filename': 'AlteredBeast.bin',
            'name': 'Altered Beast',
            'region': 'US/Euro'
        },
        'Columns.kvq': {
            'filename': 'Columns.bin',
            'name': 'Columns',
            'region': 'World'
        },
        'Golden Axe.kvq': {
            'filename': 'GoldenAxe.bin',
            'name': 'Golden Axe',
            'region': 'World'
        },
        'Outrun.kvq': {
            'filename': 'Outrun.bin',
            'name': 'Outrun',
            'region': 'World'
        },
        'Phantasy Star II.kvq': {
            'filename': 'PhantasyStar2.bin',
            'name': 'Phantasy Star 2',
            'region': 'US/Euro'
        },
        'Sonic Spinball.kvq': {
            'filename': 'SonicSpinball.bin',
            'name': 'Sonic Spinball',
            'region': 'US'
        },
        'Super Shinobi.kvq': {
            'filename': 'RevengeOfShinobiBeta.bin',
            'name': 'Revenge of Shinobi Beta',
            'region': 'Japan'
        },
        'Vectorman.kvq': {
            'filename': 'VectorMan.bin',
            'name': 'VectorMan',
            'region': 'US/Euro'
        }
    }

    def _find_files(self, base_path):
        archive_list = glob.glob(base_path +'/*.*')
        return archive_list