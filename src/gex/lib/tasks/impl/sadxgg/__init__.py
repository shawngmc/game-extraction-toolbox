'''Implementation of sadxgg: Sonic Adventure DX - Game Gear'''
import logging
import os

from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.archive.prs import DecompressPrs

logger = logging.getLogger('gextoolbox')

class SonicAdventureDXGameGearTask(BaseTask):
    '''Implements sadxgg: Sonic Adventure DX - Game Gear'''
    _task_name = "sadxgg"
    _title = "Sonic Adventure DX - Game Gear"
    _details_markdown = '''
Largely based on:
Romextract.sh - https://gitlab.com/vaiski/romextract/tree/master

However, this doesn't use an external PRS tool and is intended to target Sonic Adventure DX from Steam.
PRS Code from: https://forums.qhimm.com/index.php?topic=11225.0
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("Sonic Adventure DX")
    _input_folder_desc = "Sonic Adventure DX Steam folder"


    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        '''Copy/rename the ROM files'''
        for file_metadata in self._metadata['in']['files'].values():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            out_file_entry = [x for x in self._metadata['out']['files'] if x['game'] == file_metadata['copy_to']][0]

            # Process the file
            logger.info(f"Decompressing {out_file_entry['game']}...")
            prs = DecompressPrs(resolved_file['contents'])
            contents = prs.decompress()
            filename = out_file_entry['filename']

            logger.info(f"Verifying {out_file_entry['game']}...")
            _ = self.verify_out_file(filename, contents)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(contents)
        logger.info("Processing complete.")
