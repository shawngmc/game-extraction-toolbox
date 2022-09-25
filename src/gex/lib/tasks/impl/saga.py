'''Implmentation of saga: Collection of SaGa Final Fantasy Legend'''
import glob
import logging
import os
import UnityPy
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class SagaTask(BaseTask):
    '''Implments saga: Collection of SaGa Final Fantasy Legend'''
    _task_name = "saga"
    _title = "Collection of SaGa Final Fantasy Legend"
    _details_markdown = '''
These are extracted from the Unity asset bundle files.
See https://github.com/farmerbb/RED-Project/issues/39 for more info.
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("Sa・Ga COLLECTION")
    _input_folder_desc = "Collection of SaGa Steam folder"

    def execute(self, in_dir, out_dir):
        bundle_files = self._find_files(in_dir)
        for file_path in bundle_files:
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if game_info:
                logger.info(f"Extracting {file_path}: {game_info['name']}")
                try:
                    unity_bundle = UnityPy.load(file_path)
                    rom_asset = unity_bundle.container.get(game_info['asset_path'])
                    if rom_asset:
                        rom_data = rom_asset.read()
                        with open(os.path.join(out_dir, game_info['filename']), "wb") as out_file:
                            out_file.write(rom_data.script)
                except Exception as _:
                    logger.warning(f'Error while processing {file_path}!')
            else:
                logger.info(f'Skipping {file_path} as it contains no known ROMS!')

        logger.info("Processing complete.")

    def _find_files(self, base_path):
        bundle_path = os.path.join(base_path, 'Sa・Ga COLLECTION_Data', 'StreamingAssets',
            'aa', 'Windows', 'StandaloneWindows64', 'rom*.bundle')
        archive_list = glob.glob(bundle_path)
        return archive_list


    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'status': "good",
            'system': "Game Boy",
            "notes": []},
            self._game_info_map.values())

    _game_info_map = {
        "romffl1_assets_all_e8aea7590909c1eb45f3809e4f3da68f.bundle": {
            'filename': "FinalFantasyLegend.gb",
            'name': "Final Fantasy Legend 1",
            'asset_path': "Assets/Roms/FFL1.bytes"
        },
        "romffl2_assets_all_5d8137a1fdbca63a9fa7b533aa1d9db0.bundle": {
            'filename': "FinalFantasyLegend2.gb",
            'name': "Final Fantasy Legend 2",
            'asset_path': "Assets/Roms/FFL2.bytes"
        },
        "romffl3_assets_all_5818995041c2c3cbe070bb00b1783274.bundle": {
            'filename': "FinalFantasyLegend3.gb",
            'name': "Final Fantasy Legend 3",
            'asset_path': "Assets/Roms/FFL3.bytes"
        },
        "romjsg1_assets_all_c6047cf2db4f38cbc8f51d592e1a1c76.bundle": {
            'filename': "SaGa.gb",
            'name': "SaGa 1",
            'asset_path': "Assets/Roms/JSG1.bytes"
        },
        "romjsg2_assets_all_148d5b61843deae44f69f2dfcc30e168.bundle": {
            'filename': "SaGa2.gb",
            'name': "SaGa 2",
            'asset_path': "Assets/Roms/JSG2.bytes"
        },
        "romjsg3_assets_all_942cc896cee03850dc45bfc837017e8f.bundle": {
            'filename': "SaGa3.gb",
            'name': "SaGa 3",
            'asset_path': "Assets/Roms/JSG3.bytes"
        }
    }
