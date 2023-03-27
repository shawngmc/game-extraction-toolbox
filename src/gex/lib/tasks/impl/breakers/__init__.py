'''Implementation of breakers: Breakers Collection'''
import logging
import os
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class DisneyClassicsTask(BaseTask):
    '''Implements breakers: Breakers Collection'''
    _task_name = "breakers"
    _title = "Breakers Collection"
    _details_markdown = ''''''
    _default_input_folder = helpers.gen_steam_app_default_folder(
        "Breakers Collection")
    _input_folder_desc = "Breakers Collection Steam folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        in_files = self.read_all_datafiles(in_dir)

        output_files = []
        output_files.append(self._handle_breakers(in_files))
        output_files.append(self._handle_breakrev(in_files))
        
        for out_file_entry in output_files:
            _ = self.verify_out_file(out_file_entry['filename'], out_file_entry['contents'])
            out_path = os.path.join(out_dir, out_file_entry['filename'])
            with open(out_path, "wb") as out_file:
                out_file.write(out_file_entry['contents'])
                
        logger.info("Processing complete.")

    def _handle_breakers(self, in_files):
        out_files = {}
        out_files['230-p1.p1'] = in_files['230-m68k.swbin']['contents']
        out_files['230-c1.c1'] = in_files['230-p1.spr']['contents']
        out_files['230-c2.c2'] = in_files['230-p2.spr']['contents']
        out_files['230-c3.c3'] = in_files['230-p3.spr']['contents']
        out_files['230-c4.c4'] = in_files['230-p4.spr']['contents']
        out_files['230-s1.s1'] = in_files['230-sfix.dat']['contents']
        out_files['230-v1.v1'] = in_files['230-snd1.pcm']['contents']
        out_files['230-v2.v2'] = in_files['230-snd2.pcm']['contents']
        out_files['230-m1.m1'] = in_files['230-z80.bin']['contents']
        return {'filename': 'breakers.zip', 'contents': helpers.build_zip(out_files)}

    def _handle_breakrev(self, in_files):
        out_files = {}
        out_files['245-p1.p1'] = in_files['245-m68k.swbin']['contents']
        out_files['245-c1.c1'] = in_files['245-p1.spr']['contents']
        out_files['245-c2.c2'] = in_files['245-p2.spr']['contents']
        out_files['245-c3.c3'] = in_files['245-p3.spr']['contents']
        out_files['245-c4.c4'] = in_files['245-p4.spr']['contents']
        out_files['245-c5.c5'] = in_files['245-p5.spr']['contents']
        out_files['245-c6.c6'] = in_files['245-p6.spr']['contents']
        out_files['245-s1.s1'] = in_files['245-sfix.dat']['contents']
        out_files['245-v1.v1'] = in_files['245-snd1.pcm']['contents']
        out_files['245-v2.v2'] = in_files['245-snd2.pcm']['contents']
        out_files['245-m1.m1'] = in_files['245-z80.bin']['contents']
        return {'filename': 'breakrev.zip', 'contents': helpers.build_zip(out_files)}
