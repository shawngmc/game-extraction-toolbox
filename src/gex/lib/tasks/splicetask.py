'''Implementation of basic splice task'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class SpliceTask(BaseTask):
    '''Implements basic splice task'''

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        '''Splice out the ROM files'''
        resolved_file = self.read_datafile(in_dir, self._metadata['in']['files']['source'])
        source_data = resolved_file['contents']

        extractable_roms = [x for x in self._metadata['out']['files'] if x['status'] != 'no-rom']
        for file_meta in extractable_roms:
            logger.info(f"Extracting {file_meta['game']}...")
            game_data = bytearray()
            if 'header' in file_meta:
                game_data.extend(bytearray.fromhex(file_meta['header']))

            for section in file_meta['sections'].values():
                start = int(section['start'], 16)
                length = int(section['length'], 16)
                game_data.extend(source_data[start:start+length])

            filename = file_meta['filename']
            _ = self.verify_out_file(filename, game_data)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(game_data)

        logger.info("Processing complete.")
