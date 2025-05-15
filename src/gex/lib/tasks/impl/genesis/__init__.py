'''Implementation of genesis: Sega Genesis and Mega Drive Collection'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class GenesisTask(BaseTask):
    '''Implments genesis: Sega Genesis and Mega Drive Collection'''
    _task_name = "genesis"
    _title = "Sega Genesis and Mega Drive Collection"
    _details_markdown = '''
These are the ROMs just sitting in the uncompressed ROMs folder.
There are a few more regional variants that are only available in PAK files, but this tool doesn't have a Python SGMDC PAK extractor yet 
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Sega Classics")
    _input_folder_desc = "Sega Classics Steam Folder"

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
            if not resolved_file:  # these games are bought separately; some might not be installed
                logger.warning(f"Skipping {file_metadata[filename]}, not found...")
                continue
            if 'copy_to' in file_metadata:
                out_file_entry = [x for x in self._metadata['out']['files'] if x['game'] == file_metadata['copy_to']][0]

                filename = out_file_entry['filename']
                _ = self.verify_out_file(filename, resolved_file['contents'])
                out_path = os.path.join(out_dir, filename)
                with open(out_path, "wb") as out_file:
                    out_file.write(resolved_file['contents'])
            else:
                logger.warning("Compressed ROMs not yet supported!")
        logger.info("Processing complete.")
