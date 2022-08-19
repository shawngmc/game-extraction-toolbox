
import shutil
import traceback
import logging
import os

from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox') 

class BubsyTask(BaseTask):
    _task_name = "bubsy"
    _title = "Bubsy Two-Fur"
    _details_markdown = '''
These are the ROMs just sitting in the install folder

**Game**          |  **Filename**  
--------------|----------------  
**Bubsy**         |  Bubsy.sfc   
**Bubsy 2**       |  Bubsy2.sfc   
    '''
    _default_input_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Bubsy Two-Fur"
    _input_folder_desc = "Bubsy Two-Fur Steam Folder"
    _short_description = ""


    def execute(self, in_dir, out_dir):
        rom_files = self._find_files(in_dir)
        for file_path in rom_files:
            # TODO: Add a handler for the pak compressed ones
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if not game_info == None:
                display_name = game_info['name']
                if game_info['region']:
                    display_name += f' ({game_info["region"]})'
                logger.info(f"Copying {file_name}: {display_name}") 
                try:
                    shutil.copyfile(file_path, os.path.join(out_dir, game_info['filename']))
                except Exception as e:
                    traceback.print_exc()
                    logger.warning(f'Error while processing {file_path}!') 
            else:
                logger.info(f'Skipping unmatched file {file_path}!') 
        logger.info("Processing complete.")

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

    def _find_files(self, base_path):
        new_paths = []
        for filename in self._game_info_map.keys():
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
            if not game_info == None:
                display_name = game_info['name']
                logger.info(f"Copying {file_name}: {display_name}") 
                try:
                    shutil.copyfile(file_path, os.path.join(out_dir, game_info['filename']))
                except Exception as e:
                    traceback.print_exc()
                    logger.warning(f'Error while processing {file_path}!') 
            else:
                logger.info(f'Skipping unmatched file {file_path}!') 
        logger.info("Processing complete.")

