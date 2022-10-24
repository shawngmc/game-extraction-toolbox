'''Implementation of ssp2: Sega Smash Pack 2'''
import logging
import os
from gex.lib.archive.kvq import extract
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

ENCODE_STRING_BYTES = bytearray('Encoded for KGen Ultra / Sega Smash Pack II / Snake KML 1999! ', 'ascii')

class SSPTask(BaseTask):
    '''Implements ssp2: Sega Smash Pack 2'''
    _task_name = "ssp2"
    _title = "Sega Smash Pack 2"
    _details_markdown = '''
Based on: https://github.com/zZeck/SegaSmashPackPCUtils

These ROMs are pulled out of kvq files. 
    '''
    _default_input_folder = r"C:\Sega\Smash Pack II"
    _input_folder_desc = "Sega Smash Pack 1 folder"
    _out_file_notes = {}

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }
    def execute(self, in_dir, out_dir):
        for file_metadata in self._metadata['in']['files'].values():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            out_file_entry = [x for x in self._metadata['out']['files'] if x['game'] == file_metadata['copy_to']][0]
            rom_bytes = extract(resolved_file['contents'], ENCODE_STRING_BYTES)
            filename = out_file_entry['filename']
            _ = self.verify_out_file(filename, rom_bytes)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(rom_bytes)
        logger.info("Processing complete.")
