'''Implementation of basic copy-only task'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class CopyTask(BaseTask):
    '''Implements basic copy-only task'''

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

            filename = out_file_entry['filename']
            _ = self.verify_out_file(filename, resolved_file['contents'])
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(resolved_file['contents'])
        logger.info("Processing complete.")