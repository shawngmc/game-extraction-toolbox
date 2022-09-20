'''Extraction code for Atari 2600 Prototypes ROMs'''
import glob
import logging
import os
import shutil

logger = logging.getLogger('gextoolbox')

game_name_map = {
    "adventureii.bin": "Adventure II",
    "aquavent.bin": "Aquaventure",
    "frog_pond_8_27_82.bin": "Frog Pond",
    "holemole.bin": "Holey Moley",
    "motorodeo_ntsc.bin": "Motorodeo",
    "saboteur.bin": "Saboteur",
    "wizard.bin": "Wizard",
    "yarsreturn.bin": "Yars Return"
}


def _info_transform(game_name):
    transformed_name = game_name.replace(" ", "")
    return {
        'filename': f'{transformed_name}_Prototype.a26',
        'name': game_name
    }


game_info_map = {k: _info_transform(v) for k, v in game_name_map.items()}


def get_game_list():
    '''Transform the game map for documentation'''
    return map(lambda x: {
        'filename': x['filename'],
        'game': f"{x['name']}",
        'system': "Atari 2600 (Prototype)",
        "notes": []},
        game_info_map.values())


def find_files(base_path):
    '''Find the files this task supports'''
    uncomp_rom_path = os.path.join(
        base_path, "AtariVault_Data", "StreamingAssets", "FOCAL_Emulator", "vol3")
    archive_list = glob.glob(uncomp_rom_path + '/*.*')
    return archive_list


def copy(in_dir, out_dir):
    '''Copy/rename Prototype 2600 ROMs'''
    rom_files = find_files(in_dir)
    for file_path in rom_files:
        file_name = os.path.basename(file_path)
        game_info = game_info_map.get(file_name)
        if game_info is not None:
            display_name = game_info['name']
            logger.info(
                f"Copying {file_name} to {game_info['filename']}: {display_name}")
            try:
                shutil.copyfile(file_path, os.path.join(
                    out_dir, game_info['filename']))
            except Exception as _:
                logger.warning(f'Error while processing {file_path}!')
        else:
            logger.debug(f'Skipping unmatched file {file_path}!')
