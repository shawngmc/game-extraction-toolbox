'''Implementation of neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
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

        merged_rom_data = {
            "Baseball Stars 2": {
                'filename': 'bstars2.zip',
                'function': snk.handle_bstars2
            }
        }

        # Process titles
        out_files = {}
        for folder in found_folders:
            if folder in merged_rom_data:
                # Read the files
                title_in_files = [v for v in in_files.values() if v['rel_path'][0] == folder]
                bundle_contents = {}
                for file_metadata in title_in_files:
                    bundle_contents[file_metadata['filename']] = self.read_datafile(in_dir, file_metadata)['contents']

                logger.info(f"Read vendor version of {folder}; this release may take a while...")
                out_name = merged_rom_data[folder]['filename']
                handle_func = merged_rom_data[folder]['function']
                out_files[out_name] = handle_func(bundle_contents)
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
