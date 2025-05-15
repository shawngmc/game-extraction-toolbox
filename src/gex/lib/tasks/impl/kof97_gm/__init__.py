'''Implementation of kof97: The King of Fighters '97: Global Match on Steam and Amazon'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.utils.vendor import snk

logger = logging.getLogger('gextoolbox')

class KingOfFightersGlobalMatchTask(BaseTask):
    '''Implements kof97_gm: The King of Fighters '97: Global Match'''
    _task_name = "kof97_gm"
    _title = "The King of Fighters '97: Global Match"
    _details_markdown = '''
This task covers The King of Fighters '97: Global Match.
Including both Steam and Amazon Prime Gaming versions.

To extract the Amazon version, provide your Amazon Game library as a input directory.

Requires Neo-Geo BIOS ROM.

Based on:
- https://github.com/RedundantCich/goNCommand/blob/main/GoKOF97
- https://www.arcade-projects.com/threads/samurai-shodown-v-perfect-on-real-hardware.13565/page-2
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("THE KING OF FIGHTERS '97 GLOBAL MATCH")
    _input_folder_desc = "Game Library (Amazon, Steam, etc.) folder"

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
            file_path = os.path.join(in_dir, *in_file['rel_path'], file_name)
            if os.path.exists(file_path):
                logger.info(f"Found {file_name}...")
                in_files[file_name] = self.read_datafile(in_dir, in_file)['contents']
            else:
                logger.info(f"File {file_name} not found...")

        logger.info("Processing CROM data...")

        crom_odd, crom_even = snk.unswizzle(in_files['c1.bin'])

        [c1, c3, c5] = transforms.custom_split(contents=crom_odd, chunk_sizes=[8388608, 8388608, 4194304])

        [c2, c4, c6] = transforms.custom_split(contents=crom_even, chunk_sizes=[8388608, 8388608, 4194304])

        m1 = in_files['m1.bin']

        [p1, p2] = transforms.custom_split(contents=in_files['p1.bin'], chunk_sizes=[1048576, 4194304])
        
        s1 = in_files['s1.bin']

        [v1, v2, v3] = transforms.equal_split(contents=in_files['v1.bin'], num_chunks=3)

        file_map = {
            '232-c1.c1': c1,
            '232-c2.c2': c2,
            '232-c3.c3': c3,
            '232-c4.c4': c4,
            '232-c5.c5': c5,
            '232-c6.c6': c6,
            '232-m1.m1': m1,
            "232-p1.p1": p1,
            "232-p2.sp2": p2,
            "232-s1.s1": s1,
            "232-v1.v1": v1,
            "232-v2.v2": v2,
            "232-v3.v3": v3,
        }
        

        filename = 'kof97.zip'
        contents = helpers.build_zip(file_map)

        _ = self.verify_out_file(filename, contents)

        out_path = os.path.join(out_dir, filename)
        with open(out_path, "wb") as out_file:
            logger.info(f"Writing verified {filename}...")
            out_file.write(contents)

        logger.info("Processing complete.")

