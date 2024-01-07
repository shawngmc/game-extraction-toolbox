'''Implementation of neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.tasks.impl.kof97_gm import utils
from gex.lib.utils.blob import hash as hash_helper
from gex.lib.utils.vendor import capcom

logger = logging.getLogger('gextoolbox')

class MarvelVsCapcomTask(BaseTask):
    '''Implements mvsc: Marvel VS Capcom: Clash of Super Heroes'''
    _task_name = "mvsc"
    _title = "Marvel VS Capcom: Clash of Super Heroes"
    _details_markdown = '''
Marvel VS Capcom: Clash of Super Heroes
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
            file_path = os.path.join(in_dir, file_name)
            if os.path.exists(file_path):
                logger.info(f"Found {file_name}...")
                in_files[file_name] = self.read_datafile(in_dir, in_file)['contents']
            else:
                logger.info(f"File {file_name} not found...")

        gfx = in_files['gfx.rom']
        main = in_files['main.rom']

        vrom_filenames = [
            "mvc.13m",
            "mvc.14m",
            "mvc.15m",
            "mvc.16m",
            "mvc.17m",
            "mvc.18m",
            "mvc.19m",
            "mvc.20m"
        ]

        file_map = self._deshuffle_gfx_common(
            vrom_filenames,
            32,
            final_split = [0x400000, 0x400000]
        )(gfx)

        maincpu_filenames = [
            "mvcu.03d",
            "mvcu.04d",
            "mvc.05a",
            "mvc.06a",
            "mvc.07",
            "mvc.08",
            "mvc.09",
            "mvc.10",
        ]

        main = transforms.swap_endian(main)
        chunks = transforms.equal_split(main, num_chunks = 16)

        file_map.update(dict(zip(maincpu_filenames, chunks)))

        contents = helpers.build_zip(file_map)

        out_path = os.path.join(out_dir, 'mvscu.zip')
        with open(out_path, "wb") as out_file:
            out_file.write(contents)

        logger.info("Processing complete.")

    def _deshuffle_gfx_common(self, filenames, num_interim_split, final_split = None):
        def gfx(contents):
            # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
            contents = capcom.common_gfx_deshuffle(contents)

            # Split into even chunks
            chunks = transforms.equal_split(contents, num_chunks=num_interim_split)

            # Interleave each pair of chunks
            new_chunks = []
            for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
                new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
            chunks = new_chunks

            # Merge the chunks back together
            contents = transforms.merge(chunks)

            # Deinterleave the chunks into our 4 files
            chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)

            # Do final split if provided
            if final_split:
                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(transforms.custom_split(oldchunk, final_split))
                chunks = new_chunks

            return dict(zip(filenames, chunks))
        return gfx

