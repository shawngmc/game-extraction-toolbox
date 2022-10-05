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
    _default_input_folder = helpers.gen_steam_app_default_folder("Suzy")
    _input_folder_desc = "'Suzy' Folder (Steam MMLC install folder)"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        resolved_file = self.read_datafile(in_dir, self._metadata['in']['files']['proteus'])
        exe_data = resolved_file['contents']

        for file_meta in self._metadata['out']['files']:
            logger.info(f"Extracting {file_meta['game']}...")
            game_data = bytearray.fromhex(file_meta['header'])
            for section in file_meta['sections'].values():
                start = int(section['start'], 16)
                length = int(section['length'], 16)
                game_data.extend(exe_data[start:start+length])

            filename = file_meta['filename']
            verified = self.verify_out_file(filename, game_data)
            if verified:
                logger.info(f"Verified {filename}.")
            else:
                logger.info(f"Could NOT verify {filename}.")
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(game_data)

        logger.info("Processing complete.")
