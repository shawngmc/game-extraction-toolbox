'''Implementation of mmbnlc2: Mega Man Battle Network Legacy Collection 2'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MegaManLegacyCollection1Task(BaseTask):
    '''Implements mmbnlc2: Mega Man Battle Network Legacy Collection 2'''
    _task_name = "mmbnlc2"
    _title = "Mega Man Battle Network Legacy Collection 2"
    _details_markdown = '''
Based on zip file discoveries from https://github.com/farmerbb/RED-Project/issues/101
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("MegaMan_BattleNetwork_LegacyCollection_Vol2")
    _input_folder_desc = "'MegaMan_BattleNetwork_LegacyCollection_Vol2' Folder (Steam MMBNLC1 install folder)"

    def execute(self, in_dir, out_dir):
        bundle_contents = {}
        for file_ref, file_metadata in self._metadata['in']['files'].items():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            bundle_contents[file_ref] = resolved_file['contents']

        out_files = []
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe4.dat'], "zip", {
                "MegaMan Battle Network 4 Red Sun.gba": "exe4/rom_e.srl",
                "RockMan.EXE 4 Tournament Red Sun.gba": "exe4/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe4b.dat'], "zip", {
                "MegaMan Battle Network 4 Blue Moon.gba": "exe4b/rom_b_e.srl",
                "RockMan.EXE 4 Tournament Blue Moon.gba": "exe4b/rom_b.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe5.dat'], "zip", {
                "MegaMan Battle Network 5 Team Blue.gba": "exe5/rom_e.srl",
                "RockMan.EXE 5 Tournament Team of Blues.gba": "exe5/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe5k.dat'], "zip", {
                "MegaMan Battle Network 5 Team Colonel.gba": "exe5k/rom_k_e.srl",
                "RockMan.EXE 5 Tournament Team of Colonel.gba": "exe5k/rom_k.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe6.dat'], "zip", {
                "MegaMan Battle Network 6 Cybeast Gregar.gba": "exe6/rom_e.srl",
                "RockMan.EXE 6 Tournament Cyber Beast Glaga.gba": "exe6/rom.srl"
            })
        )
        out_files.extend(
            helpers.pull_files_from_archive(bundle_contents['exe6f.dat'], "zip", {
                "MegaMan Battle Network 6 Cybeast Falzar.gba": "exe6f/rom_f_e.srl",
                "RockMan.EXE 6 Tournament Cyber Beast Falzer.gba": "exe6f/rom_f.srl"
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