'''Implementation of snk40: SNK 40th Anniversary Collection'''
import glob
import logging
import os
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.snk40 import nes, arcadedlc, arcademain, arcadepatch

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
        }
    }

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        bundle_contents = {}
        for file_ref, file_metadata in self._metadata['in']['files'].items():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            reader = BPListReader(resolved_file['contents'])
            parsed = reader.parse()
            bundle_contents[file_ref] = parsed

        out_files = []

        if self._props.get('include-nes'):
            out_files.extend(nes.extract(bundle_contents))
        if self._props.get('include-arcade'):
            out_files.extend(arcademain.extract(bundle_contents))
            out_files.extend(arcadedlc.extract(bundle_contents))
            out_files.extend(arcadepatch.extract(bundle_contents))

        if out_files:
            for out_file_entry in out_files:
                filename = out_file_entry['filename']
                _ = self.verify_out_file(filename, out_file_entry ['contents'])
                out_path = os.path.join(out_dir, filename)
                with open(out_path, "wb") as out_file:
                    logger.info(f"Writing {filename}...")
                    out_file.write(out_file_entry['contents'])

        logger.info("Processing complete.")
