'''Extraction code for Atari 5200 ROMs'''
import glob
import logging
import os
import shutil

logger = logging.getLogger('gextoolbox')


game_name_map = {
    "asteroids.bin": "Asteroids",
    "centipede.bin": "Centipede",
    "countermeasure.bin": "Countermeasure",
    "millipede.bin": "Millipede",
    "missile_command.bin": "Missile Command",
    "realsports_baseball.bin": "RealSports Baseball",
    "realsports_basketball.bin": "RealSports Basketball",
    "realsports_football.bin": "RealSports Football",
    "realsports_soccer.bin": "RealSports Soccer",
    "realsports_tennis.bin": "RealSports Tennis",
    "star_raiders.bin": "Star Raiders",
    "super_breakout.bin": "Super Breakout",
    "final_legacy.bin": "Final Legacy",
    "microgammon.bin": "Micro-Gammon",
    "miniature_golf.bin": "Miniature Golf",
    "xari_arena.bin": "Xari Arena",
    "bios.bin": "5200 BIOS"
}


def _info_transform(game_name):
    transformed_name = game_name.replace(" ", "")
    return {
        'filename': f'{transformed_name}.a52',
        'name': game_name
    }


game_info_map = {k: _info_transform(v) for k, v in game_name_map.items()}


def get_game_list():
    '''Transform the game map for documentation'''
    return map(lambda x: {
        'filename': x['filename'],
        'game': f"{x['name']}",
        'system': "Atari 5200",
        'status': "good",
        "notes": []},
        game_info_map.values())


def find_files(base_path):
    '''Find the files this task supports'''
    uncomp_rom_path = os.path.join(
        base_path, "AtariVault_Data", "StreamingAssets", "FOCAL_Emulator", "5200")
    archive_list = glob.glob(uncomp_rom_path + '/*.*')
    return archive_list


def copy(in_dir, out_dir):
    '''Copy/rename 5200 ROMs'''
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
            except OSError as error:
                logger.warning(f'Error while processing {file_path}!')
                logger.warning(error)
        else:
            logger.debug(f'Skipping unmatched file {file_path}!')
