'''Implementation of mmbnlc1: Mega Man Battle Network Legacy Collection 1'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MegaManLegacyCollection1Task(BaseTask):
    '''Implements mmbnlc1: Mega Man Battle Network Legacy Collection 1'''
    _task_name = "mmbnlc1"
    _title = "Mega Man Battle Network Legacy Collection 1"
    _details_markdown = '''
Based on zip file discoveries from https://github.com/farmerbb/RED-Project/issues/101
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("MegaMan_BattleNetwork_LegacyCollection_Vol1")
    _input_folder_desc = "'MegaMan_BattleNetwork_LegacyCollection_Vol1' Folder (Steam MMBNLC1 install folder)"

    def execute(self, in_dir, out_dir):
        bundle_contents = {}
        for file_ref, file_metadata in self._metadata['in']['files'].items():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            bundle_contents[file_ref] = resolved_file['contents']

        out_files = []

        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe1.dat'], "zip", {
                "MegaMan Battle Network.gba": "exe1/rom_e.srl",
                "RockMan.EXE.gba": "exe1/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe2j.dat'], "zip", {
                "MegaMan Battle Network 2.gba": "exe2j/rom_e.srl",
                "RockMan.EXE 2.gba": "exe2j/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe3.dat'], "zip", {
                "MegaMan Battle Network 3 White.gba": "exe3/rom_e.srl",
                "RockMan.EXE 3.gba": "exe3/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe3b.dat'], "zip", {
                "MegaMan Battle Network 3 Blue.gba": "exe3b/rom_b_e.srl",
                "RockMan.EXE 3 Black.gba": "exe3b/rom_b.srl"
            })
        )

        for out_file_entry in out_files:
            filename = out_file_entry['filename']
            _ = self.verify_out_file(filename, out_file_entry ['contents'])
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                logger.info(f"Writing {filename}...")
                out_file.write(out_file_entry['contents'])

        logger.info("Processing complete.")