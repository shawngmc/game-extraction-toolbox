'''Implementation of waku7: ACA Waku Waku 7'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.tasks.impl.waku7 import utils
from gex.lib.utils.blob import hash as hash_helper

logger = logging.getLogger('gextoolbox')

class WakuWaku7Task(BaseTask):
    '''Implements waku7: Waku Waku 7'''
    _task_name = "waku7"
    _title = "Waku Waku 7"
    _details_markdown = '''
This task covers Waku Waku 7.
Including both Steam and Amazon Prime Gaming versions.

Based on:
- https://github.com/RedundantCich/goNCommand/blob/main/GoKOF97
- https://www.arcade-projects.com/threads/samurai-shodown-v-perfect-on-real-hardware.13565/page-2
    '''

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        in_files = {}
        
        for in_file in self._metadata['in']['files'].values():
            file_name = in_file['filename']
            file_path = os.path.join(in_dir, file_name)
            if os.path.exists(file_path):
                logger.info(f"Found {file_name}...")
                in_files[file_name] = self.read_datafile(in_dir, in_file)['contents']
            else:
                logger.info(f"File {file_name} not found...")

        logger.info("Processing CROM data...")

        crom_odd, crom_even = utils.unswizzle(in_files['c1.bin'])

        [c1, c3, c5] = transforms.equal_split(contents=crom_odd, num_chunks=3)

        [c2, c4, c6] = transforms.equal_split(contents=crom_even, num_chunks=3)

        # [c1, c2, c3, c4, c5, c6] = transforms.equal_split(contents=in_files['c1.bin'], num_chunks=6)

        m1 = in_files['m1.bin']

        [p1, p2] = transforms.custom_split(contents=in_files['p1.bin'], chunk_sizes=[1048576, 2097152])
        
        s1 = in_files['s1.bin']

        [v1, v2] = transforms.equal_split(contents=in_files['v1.bin'], num_chunks=2)

        file_map = {
            '225-c1.c1': c1,
            '225-c2.c2': c2,
            '225-c3.c3': c3,
            '225-c4.c4': c4,
            '225-c5.c5': c5,
            '225-c6.c6': c6,
            '225-m1.m1': m1,
            "225-p1.p1": p1,
            "225-p2.sp2": p2,
            "225-s1.s1": s1,
            "225-v1.v1": v1,
            "225-v2.v2": v2,
        }
        

        filename = 'wakuwak7.zip'
        contents = helpers.build_zip(file_map)

        _ = self.verify_out_file(filename, contents)

        out_path = os.path.join(out_dir, filename)
        with open(out_path, "wb") as out_file:
            logger.info(f"Writing verified {filename}...")
            out_file.write(contents)

        logger.info("Processing complete.")

