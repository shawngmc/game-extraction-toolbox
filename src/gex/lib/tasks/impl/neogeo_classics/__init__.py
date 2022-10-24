'''Implementation of neogeo_classics: Neo Geo Classics by SNK Playmore'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class NeoGeoClassicsTask(BaseTask):
    '''Implements neogeo_classics: Neo Geo Classics by SNK Playmore'''
    _task_name = "neogeo_classics"
    _title = "Neo Geo Classics by SNK Playmore"
    _details_markdown = '''
This task covers a variety of SNK Neo Geo releases on Steam, GOG, Humble Store and Amazon Games.
In some cases, these games simply have ZIP files for the ROM; in other cases, the files are in a subfolder.

This also covers most collections/bundles, but only if they install as separate titles. 
As of right now, the only exception known is Samurai Shodown Neogeo Collection.
    '''
    _default_input_folder = r"C:\Program Files (x86)\GOG Galaxy\Games"
    _input_folder_desc = "Game Library (Amazon, Steam, etc.) folder"

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
        title_data = self._metadata['titles']

        # Find folders
        for title_name, title_data in title_data.values():
            found_folder = self._check_dirs(in_dir, title_data['folders'])

            if found_folder:
                logger.info(f"Found {found_folder} for title {title_name}...")
            else:
                logger.info(f"No folder found for title {title_name}...")


    #     for game in self._metadata['out']['files']:
    #         if game.get('status') == "no-rom":
    #             logger.info(f"Skipping {game['game']} as there is no ROM to extract...")
    #             continue

    #         is_partial = game.get('status') == "partial"
    #         if not self._props.get('include-partials') and is_partial:
    #             logger.info(f"Skipping {game['game']} as this tool cannot extract a working copy...")
    #             continue

    #         # read the matching input file
    #         pkg_name = game['extract']['in_file']
    #         in_file_entry = self._metadata['in']['files'][pkg_name]
    #         contents = self.read_datafile(in_dir, in_file_entry)['contents']

    #         logger.info(f"Extracting {game['game']}...")
    #         zip_files = {}

    #         contents = transforms.cut(contents, game['extract']['start'], length=game['extract']['length'])
    #         if game['system'] == "Arcade":
    #             lzd = lzma.LZMADecompressor()
    #             contents = lzd.decompress(contents)
    #             if is_partial:
    #                 zip_files["decompressed_blob"] = contents

    #             work_files = game.get('zip_files') or {}
    #             for work_filename, geometry in work_files.items():
    #                 start = int(geometry['start'], 16)
    #                 length = int(geometry['length'], 16)
    #                 zip_files[work_filename] = transforms.cut(contents, start, length=length)
    #         else:
    #             if is_partial:
    #                 zip_files["blob"] = contents

    #             for work_file in game.get('out') or []:
    #                 zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])

    #         game_data = helpers.build_zip(zip_files)
    #         filename = f"partial_{game['filename']}" if is_partial else game['filename']
    #         if not is_partial:
    #             _ = self.verify_out_file(filename, game_data)
    #         else:
    #             logger.info(f"Skipping verification for partial extract {filename}.")
    #         out_path = os.path.join(out_dir, filename)
    #         with open(out_path, "wb") as out_file:
    #             out_file.write(game_data)

        logger.info("Processing complete.")
