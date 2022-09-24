'''Implementation of wonderboy3: Wonder Boy The Dragon's Trap'''
import shutil
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class BubsyTask(BaseTask):
    '''Implements wonderboy3: Wonder Boy The Dragon's Trap'''
    _task_name = "wonderboy3"
    _title = "Wonder Boy The Dragon's Trap"
    _details_markdown = '''
This is just sitting in the install folder. 

Note that the white box instead of the Sega logo is an intentional change for this release.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Wonder Boy The Dragon's Trap")
    _input_folder_desc = "Wonder Boy The Dragon's Trap Steam Folder"

    _game_info_map = {
        'wb3.sms': {
            'filename': 'Wonder Boy 3.sms',
            'name': 'Wonder Boy 3'
        },
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['name'],
            'status': "good",
            'system': "SMS",
            "notes": []},
            self._game_info_map.values())

    def execute(self, in_dir, out_dir):
        file_path = os.path.join(in_dir, 'bin_pc\\rom\\wb3.sms')
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
        logger.info("Processing complete.")
