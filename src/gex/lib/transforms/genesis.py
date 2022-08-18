

# Extraction Script for Capcom Fighting Collection

# General Extraction Process
# - Extract ARC Archive
# - Pull bin/ROMNAME file
# - Split it into parts using offsets/length
#   - Header (60b)
#   - MainCPU (???k)
#   - ??? inv gfx (???k) 
#   - AudioCPU (???k)
#   - QSound (???k)
# - Process each part
#   - maincpu: geometry
#   - gfx: geometry, deinterleave, endian swap?
#   - audiocpu: geometry
#   - qsound: geometry + endian swap

import shutil
import traceback
import glob
import logging
import os

from gex.lib.archive import kpka

logger = logging.getLogger('gextoolbox')

title = "Sega Genesis and Mega Drive Collection"
description = ""
default_folder = "C:\Program Files (x86)\Steam\steamapps\common\Sega Classics"
in_dir_desc = "Sega Classics Steam Folder"

game_info_map = {
    'ALEXKIDD_U.68K': {
        'filename': 'AlexKiddInTheEnchantedCastle.bin',
        'name': 'Alex Kidd in the Enchanted Castle',
        'region': 'US'
    },
    'AlienSoldier_Europe.SGD': {
        'filename': 'AlienSoldier.bin',
        'name': 'Alien Soldier',
        'region': 'Euro'
    },
    'AlienStorm_USA.SGD': {
        'filename': 'AlienStorm.bin',
        'name': 'Alien Storm',
        'region': 'US'
    },
    'ALTEREDB_UE.68K': {
        'filename': 'AlteredBeast.bin',
        'name': 'Altered Beast',
        'region': 'US/Euro'
    },
    'BEYONDOA_E.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_E.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'England'
    },
    'BEYONDOA_F.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_F.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'France'
    },
    'BEYONDOA_G.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_G.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'Germany'
    },
    'BEYONDOA_J.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_J.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'Japan'
    },
    'BEYONDOA_S.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_S.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'Spain'
    },
    'BEYONDOA_U.68K': {
        'filename': 'BeyondOasisAKAStoryofThor_U.bin',
        'name': 'Beyond Oasis / Story of Thor',
        'region': 'US'
    },
    'BONANZAB_JE.68K': {
        'filename': 'BonanzaBros.bin',
        'name': 'Bonanza Bros.',
        'region': 'Japan/Euro'
    },
    'COLUMNS_W.68K': {
        'filename': 'Columns.bin',
        'name': 'Columns',
        'region': 'World'
    },
    'Columns3_USA.SGD': {
        'filename': 'ColumnsIII.bin',
        'name': 'Columns III',
        'region': 'US'
    },
    'COMIXZON_U.68K': {
        'filename': 'ComixZone.bin',
        'name': 'Comix Zone',
        'region': 'US'
    },
    'CrackDown_USA.SGD': {
        'filename': 'CrackDown.bin',
        'name': 'Crack Down',
        'region': 'US'
    },
    'Crying_USA.SGD': {
        'filename': 'BioHazardBattle.bin',
        'name': 'Bio Hazard Battle',
        'region': 'US'
    },
    'DECAP_UE.68K': {
        'filename': 'DecapAttack.bin',
        'name': 'Decap Attack',
        'region': 'US/Euro'
    },
    'DYNAHEAD_J.68K': {
        'filename': 'DynamiteHeaddy_J.bin',
        'name': 'Dynamite Headdy',
        'region': 'Japan'
    },
    'DYNAHEAD_UE.68K': {
        'filename': 'DynamiteHeaddy_UE.bin',
        'name': 'Dynamite Headdy',
        'region': 'US/Euro'
    },
    'ECCO_UE.68K': {
        'filename': 'EccoTheDolphin.bin',
        'name': 'Ecco the Dolphin',
        'region': 'US/Euro'
    },
    'ECCO2_U.68K': {
        'filename': 'EccoTheTidesOfTime.bin',
        'name': 'Ecco - The Tides of Time',
        'region': 'US'
    },
    'eccojr.smd': {
        'filename': 'EccoJr.bin',
        'name': 'Ecco Jr.',
        'region': ''
    },
    'ESWAT_U.68K': {
        'filename': 'ESWATCityUnderSiege.bin',
        'name': 'ESWAT - City Under Siege',
        'region': 'US'
    },
    'EternalChampions_USA.SGD': {
        'filename': 'EternalChampions.bin',
        'name': 'Eternal Champions',
        'region': 'US'
    },
    'FATALLAB_JU.68K': {
        'filename': 'FatalLabyrinth.bin',
        'name': 'Fatal Labyrinth',
        'region': 'Japan/US'
    },
    'FLICKY_UE.68K': {
        'filename': 'Flicky.bin',
        'name': 'Flicky',
        'region': 'US/Euro'
    },
    'GAING_UE.68K': {
        'filename': 'GainGround.bin',
        'name': 'Gain Ground',
        'region': 'US/Euro'
    },
    'GalaxyForceII_UE.SGD': {
        'filename': 'GalaxyForceII.bin',
        'name': 'Galaxy Force II',
        'region': 'US/Euro'
    },
    'GAXE_W.68K': {
        'filename': 'GoldenAxe.bin',
        'name': 'Golden Axe',
        'region': 'World'
    },
    'GAXE2_W.68K': {
        'filename': 'GoldenAxe2.bin',
        'name': 'Golden Axe 2',
        'region': 'World'
    },
    'GAXE3_J.68K': {
        'filename': 'GoldenAxe3.bin',
        'name': 'Golden Axe 3',
        'region': 'Japan'
    },
    'Gunstar Heroes U.bin': {
        'filename': 'GunstarHeroes.bin',
        'name': 'Gunstar Heroes',
        'region': 'US'
    },
    'KIDCHAM_UE.68K': {
        'filename': 'KidChameleon.bin',
        'name': 'Kid Chameleon',
        'region': 'US/Euro'
    },
    'LandStalker_USA.SGD': {
        'filename': 'Landstalker.bin',
        'name': 'Landstalker',
        'region': 'US'
    },
    'LightCrusader_USA.SGD': {
        'filename': 'LightCrusader.bin',
        'name': 'Light Crusader',
        'region': 'US'
    },
    'MonsterLair_JUE.SGD': {
        'filename': 'WonderBoyIIIMonsterLair.bin',
        'name': 'Wonder Boy III - Monster Lair',
        'region': 'Japan/US/Euro'
    },
    'MonsterWorld3.SGD': {
        'filename': 'WonderBoyVMonsterWorldIII.bin',
        'name': 'Wonder Boy V - Monster World III',
        'region': 'Japan'
    },
    'MonsterWorld3_USA.SGD': {
        'filename': 'WonderBoyInMonsterWorld.bin',
        'name': 'Wonder Boy in Monster World',
        'region': 'US'
    },
    'PhantasyStar2_UE_GreenCrossFix.SGD': {
        'filename': 'PhantasyStar2_ModdedCross.bin',
        'name': 'Phantasy Star 2 (Modded Green Cross Fix)',
        'region': 'US/Euro'
    },
    'PhantasyStar3_USA.SGD': {
        'filename': 'PhantasyStar3_ModdedUSA.bin',
        'name': 'Phantasy Star 3 (Modded USA)',
        'region': 'US'
    },
    'PhantasyStar4.SGD': {
        'filename': 'PhantasyStar4.bin',
        'name': 'Phantasy Star 4',
        'region': ''
    },
    'RISTAR_UE.68K': {
        'filename': 'Ristar.bin',
        'name': 'Ristar',
        'region': 'US/Euro'
    },
    'ROBOTNIK_U.68K': {
        'filename': 'DrRobotniksMeanBeanMachine.bin',
        'name': 'Dr. Robotnik\'s Mean Bean Machine',
        'region': 'US'
    },
    'ShadowDancer.SGD': {
        'filename': 'ShadowDancerTheSecretofShinobi.bin',
        'name': 'Shadow Dancer: The Secret of Shinobi (Shinobi 2)',
        'region': ''
    },
    'SHINING2_U.68K': {
        'filename': 'ShiningForce2.nin',
        'name': 'Shining Force 2',
        'region': 'US'
    },
    'SHININGD_UE.68K': {
        'filename': 'ShiningInTheDarkness.bin',
        'name': 'Shining in the Darkness',
        'region': 'US/Euro'
    },
    'SHININGF_U.68K': {
        'filename': 'ShiningForce.bin',
        'name': 'Shining Force',
        'region': 'US'
    },
    'SHINOBI3_U.68K': {
        'filename': 'Shinobi3.bin',
        'name': 'Shinobi 3',
        'region': 'US'
    },
    'Sonic_Knuckles_wSonic3.bin': {
        'filename': 'Sonic3andKnuckles.bin',
        'name': 'Sonic 3 & Knuckles',
        'region': ''
    },
    'SONIC_W.68K': {
        'filename': 'Sonic.bin',
        'name': 'Sonic the Hedgehog',
        'region': 'World'
    },
    'SONIC2_W.68K': {
        'filename': 'Sonic2.bin',
        'name': 'Sonic 2',
        'region': 'World'
    },
    'SONIC3D_UE.68K': {
        'filename': 'Sonic3D.bin',
        'name': 'Sonic 3D',
        'region': 'US/Euro'
    },
    'SONICSPI_U.68K': {
        'filename': 'SonicSpinball.bin',
        'name': 'Sonic Spinball',
        'region': 'US'
    },
    'sov.smd': {
        'filename': 'SwordOfVermillion.bin',
        'name': 'Sword of Vermillion',
        'region': ''
    },
    'SPACEHARRIERII.bin': {
        'filename': 'SpaceHarrierII.bin',
        'name': 'Space Harrier II',
        'region': ''
    },
    'STHUNDER_W.68K': {
        'filename': 'StreetsOfRage_W.bin',
        'name': 'Streets of Rage',
        'region': 'World'
    },
    'STREETS_W.68K': {
        'filename': 'StreetsOfRage.bin',
        'name': 'Streets of Rage',
        'region': 'World'
    },
    'STREETS2_U.68K': {
        'filename': 'StreetsOfRage2.bin',
        'name': 'Streets of Rage 2',
        'region': 'US'
    },
    'STREETS3_E.68K': {
        'filename': 'StreetsOfRage3_E.bin',
        'name': 'Streets of Rage 3',
        'region': 'Euro'
    },
    'STREETS3_J.68K': {
        'filename': 'StreetsOfRage3_J.bin',
        'name': 'Streets of Rage 3',
        'region': 'Japan'
    },
    'STREETS3_U.68K': {
        'filename': 'StreetsOfRage3_U.bin',
        'name': 'Streets of Rage 3',
        'region': 'US'
    },
    'TheSuperShinobi_JUE.SGD': {
        'filename': 'RevengeOfShinobi.bin',
        'name': 'Revenge of Shinobi (aka The Super Shinobi)',
        'region': 'Japan/US/Euro'
    },
    'ToeJamEarl.SGD': {
        'filename': 'ToeJamAndEarl.bin',
        'name': 'ToeJam and Earl',
        'region': ''
    },
    'ToeJamEarl2_USA.SGD': {
        'filename': 'ToeJamAndEarlInPanicOnFunkotron.bin',
        'name': 'ToeJam and Earl In Panic On Funkotron',
        'region': 'US'
    },
    'VECTMAN_UE.68K': {
        'filename': 'VectorMan.bin',
        'name': 'VectorMan',
        'region': 'US/Euro'
    },
    'VECTMAN2_U.68K': {
        'filename': 'VectorMan2.bin',
        'name': 'VectorMan 2',
        'region': 'US'
    },
    'VIRTUAFIGHTER2.bin': {
        'filename': 'VirtuaFighter2.bin',
        'name': 'Virtua Fighter 2',
        'region': ''
    }
}

def find_files(base_path):
    uncomp_rom_path = os.path.join(base_path, "uncompressed ROMs") 
    archive_list = glob.glob(uncomp_rom_path +'/*.*')
    # TODO: Add Pak roms to search - possibly only the non-dupes?
    return archive_list

def main(game_base_dir, out_path):
    rom_files = find_files(game_base_dir)
    for file_path in rom_files:
        # TODO: Add a handler for the pak compressed ones
        file_name = os.path.basename(file_path)
        game_info = game_info_map.get(file_name)
        if not game_info == None:
            display_name = game_info['name']
            if game_info['region']:
                display_name += f' ({game_info["region"]})'
            logger.info(f"Extracting {file_name}: {display_name}") 
            try:
                shutil.copyfile(file_path, os.path.join(out_path, game_info['filename']))
            except Exception as e:
                traceback.print_exc()
                logger.warning(f'Error while processing {file_path}!') 
        else:
            logger.info(f'Skipping unmatched file {file_path}!') 
    logger.info("""
        Processing complete. 
    """)
