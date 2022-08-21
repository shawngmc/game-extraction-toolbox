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

 **Game**                                                     | **Platform**      | **Filename**  
---------------------------------------------------------|---------------|-----------------------------------------  
**Blackthorne Patched**                                      | Sega 32X      | Blackthorne_U_Patched.32x  
**Blackthorne**                                              | SNES          | Blackthorne.sfc  
**Blackthorne w/ Z-Patch**                                   | SNES          | Blackthorne_ZPatch.sfc  
**Radical Psycho Machine Racing**                            | SNES          | RadicalPsychoMachineRacing.sfc  
**Rock n' Roll Racing**                                      | Genesis       | RockAndRollRacing_U.bin  
**Rock n' Roll Racing**                                      | SNES          | RockAndRollRacing.sfc  
**Rock n' Roll Racing Definitive Edition A**                 | SNES          | RockAndRollRacing_DefinitiveA.sfc  
**Rock n' Roll Racing Definitive Edition B**                 | SNES          | RockAndRollRacing_DefinitiveB.sfc  
**The Lost Vikings**                                         | Genesis       | LostVikings_U.bin  
**The Lost Vikings**                                         | SNES          | LostVikings.sfc  
**The Lost Vikings Definitive Edition**                      | SNES          | LostVikings_Definitive.sfc  
**The Lost Vikings 2**                                       | SNES          | LostVikings2.sfc  

    '''
    _default_input_folder = r"C:\Program Files (x86)\Blizzard Arcade Collection"
    _input_folder_desc = "Blizzard Arcade Collection install folder"
    _short_description = ""


    _game_info_map = {
        'Blackthorne (U) (32X) [patched].32x': {
            'path': r'Sega\32X\Blackthorne (U) (32X) [patched].32x',
            'filename': 'Blackthorne_U_Patched.32x',
            'name': 'Blackthorne',
            'version': '32X'
        },
        'Blackthorne.bin': {
            'path': r'SNES\Blackthorne.bin',
            'filename': 'Blackthorne.sfc',
            'name': 'Blackthorne',
            'version': 'SNES'
        },
        'BlackthorneLZPatch.bin': {
            'path': r'SNES\BlackthorneLZPatch.bin',
            'filename': 'Blackthorne_ZPatch.sfc',
            'name': 'Blackthorne',
            'version': 'SNES (Z-Patched)'
        },
        'RockNRollRacing.bin': {
            'path': r'SNES\RockNRollRacing.bin',
            'filename': 'RockAndRollRacing.sfc',
            'name': 'Rock n Roll Racing',
            'version': 'SNES'
        },
        "Rock n' Roll Racing (U) [_].bin": {
            'path': r"Sega\Genesis\Rock n' Roll Racing (U) [_].bin",
            'filename': 'RockAndRollRacing_U.bin',
            'name': 'Rock n Roll Racing',
            'version': 'Genesis'
        },
        'RockNRollRacingDefinitiveA.bin': {
            'path': r'SNES\RockNRollRacingDefinitiveA.bin',
            'filename': 'RockAndRollRacing_DefinitiveA.sfc',
            'name': 'Rock n Roll Racing',
            'version': 'SNES (Definitive Edition A)'
        },
        'RockNRollRacingDefinitiveB.bin': {
            'path': r'SNES\RockNRollRacingDefinitiveB.bin',
            'filename': 'RockAndRollRacing_DefinitiveB.sfc',
            'name': 'Rock n Roll Racing',
            'version': 'SNES (Definitive Edition B)'
        },
        'Lost Vikings, The (U) [_].bin': {
            'path': r'Sega\Genesis\Lost Vikings, The (U) [_].bin',
            'filename': 'LostVikings_U.bin',
            'name': 'The Lost Vikings',
            'version': 'Genesis'
        },
        'LostVikings.bin': {
            'path': r'SNES\LostVikings.bin',
            'filename': 'LostVikings.sfc',
            'name': 'The Lost Vikings',
            'version': 'SNES'
        },
        'LostVikingsDE.bin': {
            'path': r'SNES\LostVikingsDE.bin',
            'filename': 'LostVikings_Definitive.sfc',
            'name': 'The Lost Vikings',
            'version': 'SNES (Definitive Edition)'
        },
        'LostVikings2.bin': {
            'path': r'SNES\LostVikings2.bin',
            'filename': 'LostVikings2.sfc',
            'name': 'The Lost Vikings 2',
            'version': 'SNES'
        },
        'RadicalPsychoMachineRacing.bin': {
            'path': r'SNES\RadicalPsychoMachineRacing.bin',
            'filename': 'RadicalPsychoMachineRacing.sfc',
            'name': 'Radical Psycho Machine Racing',
            'version': 'SNES'
        }
    }

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
                display_name = game_info['name']
                display_name += f' ({game_info["version"]})'
                logger.info(f"Copying {file_name}: {display_name}")
                try:
                    shutil.copyfile(file_path, os.path.join(out_dir, game_info['filename']))
                except OSError as error:
                    logger.warning(f'Error while processing {file_path}!')
                    logger.warning(error)
            else:
                logger.info(f'Skipping unmatched file {file_path}!')
        logger.info("Processing complete.")
