'''Implementation of basic zip splice task (for arcade ROMs, primarily)'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class ZipSpliceTask(BaseTask):
    '''Implements basic zip splice task (for arcade ROMs, primarily)'''

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
            zip_files = {}

            for filename, section in file_meta['zip_files'].items():
                if section.get('type') == 'placeholder':
                    length = int(section['length'], 16)
                    file_content = bytearray(b'\x00' * length)
                else:
                    start = int(section['start'], 16)
                    length = int(section['length'], 16)
                    file_content = transforms.cut(source_data, start, length=length)

                patches = section.get('patch')
                if patches and len(patches.keys()) > 0:
                    for loc, data in patches.items():
                        file_content[int(loc)] = data.to_bytes(1, 'little')[0]

                zip_files[filename] = file_content

            game_data = helpers.build_zip(zip_files)
            filename = file_meta['filename']
            _ = self.verify_out_file(filename, game_data)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(game_data)

        logger.info("Processing complete.")
