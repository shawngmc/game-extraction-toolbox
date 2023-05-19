'''Implementation of neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.utils.vendor import snk

logger = logging.getLogger('gextoolbox')

class NeoGeoClassicsHumbleTask(BaseTask):
    '''Implements neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
    _task_name = "neogeo_classics_humble"
    _title = "Neo Geo Classics by SNK Playmore on Humble Store"
    _details_markdown = '''
This task covers a variety of SNK Neo Geo releases Humble Store.
In some cases, these games simply have ZIP files for the ROM; in other cases, the files are in a subfolder.

This also covers most collections/bundles, but only if they install as separate titles. 
As of right now, the only exception known is Samurai Shodown Neogeo Collection.
    '''
    _default_input_folder = r"C:\Program Files (x86)\NeoGeo 25th Anniversery"
    _input_folder_desc = "Root install folder for the NeoGeo 25th Anniversary bundle"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def _check_dirs(self, in_dir, child_dirs):
        for child_dir in child_dirs:
            path = os.path.join(in_dir, child_dir)
            if os.path.exists(path):
                return path
        return None

    def execute(self, in_dir, out_dir):
        in_files = self._metadata['in']['files']

        current_neogeo_bios_ver = None

        # Find folders
        folders = list(set(map(lambda x: x['rel_path'][0], in_files.values())))
        found_folders = []
        for folder in folders:
            path = os.path.join(in_dir, folder)
            if os.path.exists(path):
                logger.info(f"Found {folder}...")
                found_folders.append(folder)
            else:
                logger.info(f"No {folder} folder found...")

        # Process titles
        out_files = {}
        for folder in found_folders:
            if folder == "Baseball Stars 2":
                title_in_files = [v for v in in_files.values() if v['rel_path'][0] == folder]
                out_files['bstars2.zip'] = self._handle_bstars2(in_dir, title_in_files)
            else:
                title_in_files = [v for v in in_files.values() if v['rel_path'][0] == folder]

                title_neogeo = next(v for v in title_in_files if v['filename'] == "neogeo.zip")
                title_gameroms = [v for v in title_in_files if v['filename'] != "neogeo.zip"]

                for title_gamerom in title_gameroms:
                    zip_path = os.path.join(in_dir, *title_gamerom['rel_path'], title_gamerom['filename'])
                    if os.path.exists(zip_path):
                        logger.info(f"Found zip {zip_path}...")
                        read_file_entry = self.read_datafile(in_dir, title_gamerom)
                        out_files[title_gamerom['filename']] = read_file_entry['contents']

                if title_neogeo:
                    title_bios_version = list(title_neogeo['versions'].keys())[0]
                    if title_bios_version == 'enhanced' and current_neogeo_bios_ver != 'enhanced':
                        zip_path = os.path.join(in_dir, *title_neogeo['rel_path'], title_neogeo['filename'])
                        if os.path.exists(zip_path):
                            logger.info(f"Found enhanced NeoGeo BIOS zip {zip_path}...")
                            read_file_entry = self.read_datafile(in_dir, title_neogeo)
                            out_files[title_neogeo['filename']] = read_file_entry['contents']
                            current_neogeo_bios_ver = 'enhanced'
                    elif title_bios_version == 'basic' and current_neogeo_bios_ver is None:
                        zip_path = os.path.join(in_dir, *title_neogeo['rel_path'], title_neogeo['filename'])
                        if os.path.exists(zip_path):
                            logger.info(f"Found basic NeoGeo BIOS zip {zip_path}...")
                            read_file_entry = self.read_datafile(in_dir, title_neogeo)
                            out_files[title_neogeo['filename']] = read_file_entry['contents']
                            current_neogeo_bios_ver = 'basic'


        # Write out the files
        for filename, contents in out_files.items():
            _ = self.verify_out_file(filename, contents)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                logger.info(f"Writing verified {filename}...")
                out_file.write(contents)

        logger.info("Processing complete.")

    def _handle_bstars2(self, in_dir, title_in_files):
        # Read the bstars2 files
        bundle_contents = {}
        for file_metadata in title_in_files:
            bundle_contents[file_metadata['filename']] = self.read_datafile(in_dir, file_metadata)['contents']

        func_map = {}
        def bstars2_maincpu(in_files):
            contents = in_files['bstars2_game_m68k']

            chunks = transforms.equal_split(contents, num_chunks=2)

            return {"041-p1.p1": chunks[0]}
        func_map['maincpu'] = bstars2_maincpu
        adpcm_file_map = {
            '041-v1.v1': 0x100000,
            '041-v2.v2': 0x100000,
            '041-v3.v3': 0x80000
        }
        func_map['adpcm'] = helpers.custom_split_helper('bstars2_adpcm', adpcm_file_map)
        func_map['zoom'] = helpers.name_file_helper("bstars2_zoom_table", "000-lo.lo")

        # Audio CPU seems to officially duplicate the data?
        def bstars2_audiocpu(in_files):
            contents = in_files['bstars2_game_z80']

            return {"041-m1.m1": transforms.merge([contents, contents])}
        func_map['audiocpu'] = bstars2_audiocpu

        def bstars2_sprites(in_files):
            contents = in_files['bstars2_tiles']
            deoptimized = snk.deoptimize_sprites(contents)
            filenames = [
                "041-c1.c1",
                "041-c2.c2",
                "041-c3.c3",
                "041-c4.c4",
            ]
            chunks = transforms.equal_split(deoptimized, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['sprites'] = bstars2_sprites

        def bstars2_fixed(in_files):
            contents = in_files['bstars2_game_sfix']

            return {"041-s1.s1": snk.sfix_reorder(contents)}
        func_map['fixed'] = bstars2_fixed

        return helpers.build_rom(bundle_contents, func_map)
