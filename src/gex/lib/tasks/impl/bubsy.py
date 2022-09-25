'''Implementation of bubsy: Bubsy Two-Fur'''
import shutil
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class BubsyTask(BaseTask):
    '''Implements bubsy: Bubsy Two-Fur'''
    _task_name = "bubsy"
    _title = "Bubsy Two-Fur"
    _details_markdown = '''
These are the ROMs just sitting in the install folder. 
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Bubsy Two-Fur")
    _input_folder_desc = "Bubsy Two-Fur Steam Folder"

    _game_info_map = {
        'bubsy_1': {
            'filename': 'Bubsy.sfc',
            'name': 'Bubsy'
        },
        'bubsy_2': {
            'filename': 'Bubsy2.sfc',
            'name': 'Bubsy 2'
        }
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': "good",
            'system': "SNES",
            "notes": []},
            self._game_info_map.values())

    def _find_files(self, base_path):
        new_paths = []
        for filename in self._game_info_map:
            new_path = os.path.join(base_path, filename)
            if os.path.exists(new_path):
                new_paths.append(new_path)
            else:
                logging.warning(f"Could not find {filename} in {base_path}")
        return new_paths

    def execute(self, in_dir, out_dir):
        rom_files = self._find_files(in_dir)
        for file_path in rom_files:
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if game_info is not None:
                display_name = game_info['name']
                logger.info(f"Copying {file_name}: {display_name}")
                try:
                    shutil.copyfile(file_path, os.path.join(out_dir, game_info['filename']))
                except OSError as error:
                    logger.warning(f'Error while processing {file_path}!')
                    logger.warning(error)
            else:
                logger.info(f'Skipping unmatched file {file_path}!')
        logger.info("Processing complete.")
