import traceback
import glob
import zipfile
import logging
import os
import io
import UnityPy

from gex.lib.archive import kpka
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

# Standard processing:
# - Assume each zip in the KPKA is a game
# - Assume that the zip has a subfolder with the intended 'mame name' of the game

title = "Collection of SaGa Final Fantasy Legend"
description = ""
default_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Sa・Ga COLLECTION"
in_dir_desc = "Collection of SaGa Steam folder"

game_info_map = {
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

def find_files(base_path):
    bundle_path = os.path.join(base_path, 'Sa・Ga COLLECTION_Data', 'StreamingAssets', 'aa', 'Windows', 'StandaloneWindows64', 'rom*.bundle') 
    print(bundle_path)
    archive_list = glob.glob(bundle_path)
    return archive_list

def main(steam_dir, out_path):
    bundle_files = find_files(steam_dir)
    print(bundle_files)
    for file_path in bundle_files:
        file_name = os.path.basename(file_path)
        game_info = game_info_map.get(file_name)
        if game_info:
            logger.info(f"Extracting {file_path}: {game_info['name']}") 
            try:
                unity_bundle = UnityPy.load(file_path)
                rom_asset = unity_bundle.container.get(game_info['asset_path'])
                if rom_asset:
                    rom_data = rom_asset.read()
                    with open(os.path.join(out_path, game_info['filename']), "wb") as out_file:
                        out_file.write(rom_data.script)
            except Exception as e:
                traceback.print_exc()
                logger.warning(f'Error while processing {file_path}!') 
        else:
            logger.info(f'Skipping {file_path} as it contains no known ROMS!') 

    logger.info("""
        Processing complete. 
    """)
