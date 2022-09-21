'''Extraction code for Atari 2600 ROMs'''
import glob
import logging
import os
import shutil

logger = logging.getLogger('gextoolbox')


game_name_map = {
    '3d_tic.bin': '3-D Tic-Tac-Toe',
    'advnture.bin': 'Adventure',
    'airseabt.bin': 'Air-Sea Battle',
    'asteroid.bin': 'Asteroids',
    'backgamn.bin': 'Backgammon',
    'basmath.bin': 'Basic Math',
    'basketbl.bin': 'Basketball',
    'black_j.bin': 'Blackjack',
    'Bowling.bin': 'Bowling',
    'braingms.bin': 'Brain Games',
    'breakout.bin': 'Breakout',
    'canyonb.bin': 'Canyon Bomber',
    'casino.bin': 'Casino',
    'centiped.bin': 'Centipede',
    'pelesocr.bin': 'Championship Soccer',
    'vidcheck.bin': 'Checkers',
    'vidchess.bin': 'Chess',
    'circatri.bin': 'Circus Atari',
    'codebrk.bin': 'Codebreaker',
    'combat.bin': 'Combat',
    'combat2.bin': 'Combat 2',
    'concentr.bin': 'Concentration',
    'cryscast.bin': 'Crystal Castles',
    'demondim.bin': 'Demons to Diamonds',
    'dsrtfalc.bin': 'Desert Falcon',
    'dodge_em.bin': 'Dodge Em',
    'doubdunk.bin': 'Double Dunk',
    'fatalrun.bin': 'Fatal Run',
    'flagcap.bin': 'Flag Capture',
    'football.bin': 'Football',
    'golf.bin': 'Golf',
    'grav2600.bin': 'Gravitar',
    'hangman.bin': 'Hangman',
    'haunthse.bin': 'Haunted House',
    'homerun.bin': 'Home Run',
    'human_cb.bin': 'Human Cannonball',
    'mazecrz.bin': 'Maze Craze',
    'milliped.bin': 'Millipede',
    'min_golf.bin': 'Miniature Golf',
    'misscomm.bin': 'Missile Command',
    'nightdrv.bin': 'Night Driver',
    'ofthwall.bin': 'Off the Wall',
    'outlaw.bin': 'Outlaw',
    'quadrun.bin': 'Quadrun',
    'indy500.bin': 'Race',
    'radarlok.bin': 'Radar Lock',
    'rs_baseb.bin': 'RealSports Baseball',
    'rsbasket.bin': 'RealSports Basketball',
    'rsboxing.bin': 'RealSports Boxing',
    'rs_footb.bin': 'RealSports Football',
    'rssoccer.bin': 'RealSports Soccer',
    'rstennis.bin': 'RealSports Tennis',
    'rs_volly.bin': 'RealSports Volleyball',
    'ret2hh.bin': 'Return to Haunted House',
    'SaveMary_NTSC.bin': 'Save Mary',
    'secretq.bin': 'Secret Quest',
    'sentinel.bin': 'Sentinel',
    'skydiver.bin': 'Sky Diver',
    'slotmach.bin': 'Slot Machine',
    'slotrace.bin': 'Slot Racers',
    'spacewar.bin': 'Space War',
    'sprntmas.bin': 'Sprint Master',
    'starraid.bin': 'Star Raiders',
    'starship.bin': 'Star Ship',
    'steplchs.bin': 'Steeplechase',
    'stlrtrak.bin': 'Stellar Track',
    'stunt.bin': 'Stunt Cycle',
    'streetrc.bin': 'Street Racer',
    'subcmdr.bin': 'Submarine Commander',
    'sprbaseb.bin': 'Super Baseball',
    'superbrk.bin': 'Super Breakout',
    'sprfootb.bin': 'Super Football',
    'surround.bin': 'Surround',
    'sq_earth.bin': 'Sword Quest Earthworld',
    'sq_fire.bin': 'Sword Quest Fireworld',
    'sq_water.bin': 'Sword Quest Waterworld',
    'temp2600.bin': 'Tempest',
    'vidcube.bin': 'Video Cube',
    'vid_olym.bin': 'Video Olympics',
    'vidpin.bin': 'Video Pinball',
    'warl2600.bin': 'Warlords',
    'yar_rev.bin': 'Yars Revenge',
}


def _info_transform(game_name):
    transformed_name = game_name.replace(" ", "")
    return {
        'filename': f'{transformed_name}.a26',
        'name': game_name
    }


game_info_map = {k: _info_transform(v) for k, v in game_name_map.items()}


def get_game_list():
    '''Transform the game map for documentation'''
    return map(lambda x: {
        'filename': x['filename'],
        'game': f"{x['name']}",
        'system': "Atari 2600",
        'status': "good",
        "notes": []},
        game_info_map.values())


def find_files(base_path):
    '''Find the files this task supports'''
    uncomp_rom_path = os.path.join(
        base_path, "AtariVault_Data", "StreamingAssets", "FOCAL_Emulator")
    archive_list = glob.glob(uncomp_rom_path + '/*.*')
    return archive_list


def copy(in_dir, out_dir):
    '''Copy/rename 2600 ROMs'''
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
