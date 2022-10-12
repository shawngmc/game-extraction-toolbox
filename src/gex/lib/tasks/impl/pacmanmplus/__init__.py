'''Implementation of pacmanmplus: Pac Man Museum Plus'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class PacManMuseumPlusTask(BaseTask):
    '''Implements pacmanmplus: Pac Man Museum Plus'''
    _task_name = "pacmanmplus"
    _title = "Pac Man Museum Plus"
    _details_markdown = ''''''
    _default_input_folder = helpers.gen_steam_app_default_folder("PAC-MAN MUSEUM PLUS")
    _input_folder_desc = "Pac Man Museum Plus install folder"

    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }

    # PAC-IN-TIME
    # Official ROM is 1,048,576
    # DLL is 1,062,400
    # So, it really does need to be compressed!
    # binwalk -e -M doesn't find anything

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }


    def execute(self, in_dir, out_dir):
        for game in self._metadata['out']['files']:
            if game.get('status') == "no-rom":
                logger.info(f"Skipping {game['game']} as there is no ROM to extract...")
                continue

            is_partial = game.get('status') == "partial"
            if not self._props.get('include-partials') and is_partial:
                logger.info(f"Skipping {game['game']} as this tool cannot extract a working copy...")
                continue

            # read the matching input file
            pkg_name = game['extract']['in_file']
            in_file_entry = self._metadata['in']['files'][pkg_name]
            contents = self.read_datafile(in_dir, in_file_entry)['contents']

            logger.info(f"Extracting {game['game']}...")
            zip_files = {}

            contents = transforms.cut(contents, game['extract']['start'], length=game['extract']['length'])
            if game['system'] == "Arcade":
                lzd = lzma.LZMADecompressor()
                contents = lzd.decompress(contents)
                if is_partial:
                    zip_files["decompressed_blob"] = contents

                work_files = game.get('zip_files') or {}
                for work_filename, geometry in work_files.items():
                    start = int(geometry['start'], 16)
                    length = int(geometry['length'], 16)
                    zip_files[work_filename] = transforms.cut(contents, start, length=length)
            else:
                if is_partial:
                    zip_files["blob"] = contents

                for work_file in game.get('out') or []:
                    zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])

            game_data = helpers.build_zip(zip_files)
            filename = f"partial_{game['filename']}" if is_partial else game['filename']
            if not is_partial:
                _ = self.verify_out_file(filename, game_data)
            else:
                logger.info(f"Skipping verification for partial extract {filename}.")
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                out_file.write(game_data)

        logger.info("Processing complete.")
