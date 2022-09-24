'''Implementation of blizzarcade: Blizzard Arcade Collection'''
import logging
import os
import shutil
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class BlizzArcadeTask(BaseTask):
    '''Implements blizzarcade: Blizzard Arcade Collection'''
    _task_name = "blizzarcade"
    _title = "Blizzard Arcade Collection"
    _details_markdown = '''
These are the ROMs just sitting in the assets/roms folder.
'''
    _default_input_folder = r"C:\Program Files (x86)\Blizzard Arcade Collection"
    _input_folder_desc = "Blizzard Arcade Collection install folder"

    _game_info_map = {
        'Blackthorne (U) (32X) [patched].32x': {
            'path': r'Sega\32X\Blackthorne (U) (32X) [patched].32x',
            'filename': 'Blackthorne_U_Patched.32x',
            'name': 'Blackthorne',
            'system': '32X'
        },
        'Blackthorne.bin': {
            'path': r'SNES\Blackthorne.bin',
            'filename': 'Blackthorne.sfc',
            'name': 'Blackthorne',
            'system': 'SNES'
        },
        'BlackthorneLZPatch.bin': {
            'path': r'SNES\BlackthorneLZPatch.bin',
            'filename': 'Blackthorne_ZPatch.sfc',
            'name': 'Blackthorne',
            'system': 'SNES',
            'version': 'Z-Patched'
        },
        'RockNRollRacing.bin': {
            'path': r'SNES\RockNRollRacing.bin',
            'filename': 'RockAndRollRacing.sfc',
            'name': 'Rock n Roll Racing',
            'system': 'SNES'
        },
        "Rock n' Roll Racing (U) [_].bin": {
            'path': r"Sega\Genesis\Rock n' Roll Racing (U) [_].bin",
            'filename': 'RockAndRollRacing_U.bin',
            'name': 'Rock n Roll Racing',
            'system': 'Genesis'
        },
        'RockNRollRacingDefinitiveA.bin': {
            'path': r'SNES\RockNRollRacingDefinitiveA.bin',
            'filename': 'RockAndRollRacing_DefinitiveA.sfc',
            'name': 'Rock n Roll Racing',
            'system': 'SNES',
            'version': 'Definitive Edition A'
        },
        'RockNRollRacingDefinitiveB.bin': {
            'path': r'SNES\RockNRollRacingDefinitiveB.bin',
            'filename': 'RockAndRollRacing_DefinitiveB.sfc',
            'name': 'Rock n Roll Racing',
            'system': 'SNES',
            'version': 'Definitive Edition B'
        },
        'Lost Vikings, The (U) [_].bin': {
            'path': r'Sega\Genesis\Lost Vikings, The (U) [_].bin',
            'filename': 'LostVikings_U.bin',
            'name': 'The Lost Vikings',
            'system': 'Genesis'
        },
        'LostVikings.bin': {
            'path': r'SNES\LostVikings.bin',
            'filename': 'LostVikings.sfc',
            'name': 'The Lost Vikings',
            'system': 'SNES'
        },
        'LostVikingsDE.bin': {
            'path': r'SNES\LostVikingsDE.bin',
            'filename': 'LostVikings_Definitive.sfc',
            'name': 'The Lost Vikings',
            'system': 'SNES',
            'version': 'Definitive Edition'
        },
        'LostVikings2.bin': {
            'path': r'SNES\LostVikings2.bin',
            'filename': 'LostVikings2.sfc',
            'name': 'The Lost Vikings 2',
            'system': 'SNES'
        },
        'RadicalPsychoMachineRacing.bin': {
            'path': r'SNES\RadicalPsychoMachineRacing.bin',
            'filename': 'RadicalPsychoMachineRacing.sfc',
            'name': 'Radical Psycho Machine Racing',
            'system': 'SNES'
        }
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': "good",
            'system': x['system'],
            "notes": []},
            self._game_info_map.values())

    def _find_files(self, base_path):
        new_paths = []
        for game_info in self._game_info_map.values():
            new_path = os.path.join(base_path, 'assets', 'roms', game_info['path'])
            if os.path.exists(new_path):
                new_paths.append(new_path)
            else:
                logging.warning(f"Could not find {game_info['path']} in {base_path}")
        return new_paths

    def execute(self, in_dir, out_dir):
        rom_files = self._find_files(in_dir)
        for file_path in rom_files:
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if game_info is not None:
                display_name = f"{game_info['name']} ({game_info['system']}{(' ' + game_info['version']) if game_info.get('version') else ''})"
                logger.info(f"Copying {file_name}: {display_name}")
                try:
                    shutil.copyfile(file_path, os.path.join(out_dir, game_info['filename']))
                except OSError as error:
                    logger.warning(f'Error while processing {file_path}!')
                    logger.warning(error)
            else:
                logger.info(f'Skipping unmatched file {file_path}!')
        logger.info("Processing complete.")
