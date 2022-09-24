'''Implementation of snk40: SNK 40th Anniversary Collection'''
import glob
import logging
import os
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.snk40 import partials, nes, arcadedlc, arcademain, arcadepatch

logger = logging.getLogger('gextoolbox')

class SNK40thAnniversaryCollectionTask(BaseTask):
    '''Implements snk40: SNK 40th Anniversary Collection'''
    _task_name = "snk40"
    _title = "SNK 40th Anniversary Collection"
    _details_markdown = '''
Based on:
- https://gitlab.com/vaiski/romextract/-/blob/master/scripts/STEAM-865940.sh
- https://github.com/lioneltrs/buildROM
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("SNK 40th Anniversary Collection")
    _input_folder_desc = "SNK 40th install folder"
    _prop_info = {
        "include-arcade": {
            "description": "Include the fully-formed arcade games that are in SNK 40th",
            "default": True,
            "type": "Boolean"
        },
        "include-nes": {
            "description": "Include the NES ports that are included in SNK 40th",
            "default": True,
            "type": "Boolean"
        },
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }

    _out_file_list = []
    _out_file_list.extend(arcadedlc.out_file_info)
    _out_file_list.extend(arcademain.out_file_info)
    _out_file_list.extend(arcadepatch.out_file_info)
    _out_file_list.extend(nes.out_file_info)
    _out_file_list.extend(partials.out_file_info)

    _out_file_notes = {
        "1": "This is not extracted as there are missing files, such as Missing PROMs. Add '--prop include-partials=True' to include these.",
        "2": "This is playable, but is a bad dump, 1+ files with a bad CRC, and/or 1+ files with empty placeholders.",
        "3": "This requires MAME 0.139 to play.",
        "4": "There are some variants that MAME does not have info on - this partial contains all the Bermuda Triangle/World Wars files for research."
    }

    def execute(self, in_dir, out_dir):

        bundle_contents = self._read_all_bundles(in_dir)

        out_files = []

        if self._props.get('include-nes'):
            out_files.extend(nes.extract(bundle_contents))
        if self._props.get('include-arcade'):
            out_files.extend(arcademain.extract(bundle_contents))
            out_files.extend(arcadedlc.extract(bundle_contents))
            out_files.extend(arcadepatch.extract(bundle_contents))
        if self._props.get('include-partials'):
            out_files.extend(partials.extract(bundle_contents))

        if out_files:
            for out_file_entry in out_files:
                out_path = os.path.join(out_dir, out_file_entry['filename'])
                with open(out_path, "wb") as out_file:
                    logger.info(f"Writing {out_file_entry['filename']}...")
                    out_file.write(out_file_entry['contents'])

        logger.info("Processing complete.")

    _pkg_name_map = {
        'bundleMain.mbundle': 'main',
        'bundleDLC1.mbundle': 'dlc',
        'bundlePatch1.mbundle': 'patch'
    }

    def _read_all_bundles(self, in_dir):
        bundle_contents = {}
        bundle_files = self._find_files(in_dir)
        for file_path in bundle_files:
            with open(file_path, 'rb') as in_file:
                file_name = os.path.basename(file_path)
                pkg_name = self._pkg_name_map.get(file_name)
                if pkg_name is not None:
                    logger.info(f'Reading files for {file_name}...')
                    contents = in_file.read()
                    reader = BPListReader(contents)
                    parsed = reader.parse()
                    bundle_contents[pkg_name] = parsed
        return bundle_contents

    def _find_files(self, base_path):
        bundle_path = os.path.join(base_path, "Bundle", '*.mbundle')
        archive_list = glob.glob(bundle_path)
        return archive_list
