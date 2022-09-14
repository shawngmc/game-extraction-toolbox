'''Extraction code for Atari Arcade ROMs'''
import logging
import os
import shutil
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')


games = [
    {
        "name": "Asteroids",
        "files": [
            "Asteroids.bin"
        ],
        "mame_name": "asteroid",
        "split": [
            "035145.02",
            "035144.02",
            "035143.02",
            "035127.02"
        ]
    },
    {
        "name": "Asteroids Deluxe",
        "files": [
            "Asteroids Deluxe.bin"
        ],
        "mame_name": "astdelux",
        "split": [
            "036430.02",
            "036431.02",
            "036432.02",
            "036433.03",
            "036800.02",
            "036799.01"
        ]
    },
    {
        "name": "Black Widow",
        "files": [
            "Black Widow.bin"
        ],
        "mame_name": "bwidow",
        "truncate": 38912,
        "split": {
            "136017.107": 2048,
            "136017.108": 4096,
            "136017.109": 4096,
            "136017.110": 4096,
            "136017.101": 4096,
            "136017.102": 4096,
            "136017.103": 4096,
            "136017.104": 4096,
            "136017.105": 4096,
            "136017.106": 4096
        },
        "notes": [2]
    },
    {
        "name": "Canyon Bomber",
        "files": [
            "CanyonBomber.bin"
        ],
        "partial": True
    },
    {
        "name": "Centipede",
        "files": [
            "Centipede.bin"
        ],
        "partial": True
    },
    {
        "name": "Crystal Castles",
        "files": [
            "Crystal Castles.bin"
        ],
        "partial": True
    },
    {
        "name": "Gravitar",
        "files": [
            "Gravitar.bin"
        ],
        "mame_name": "gravitar",
        "truncate": 38912,
        "split": {
            "136010.210": 2048,
            "136010.207": 4096,
            "136010.208": 4096,
            "136010.309": 4096,
            "136010.301": 4096,
            "136010.302": 4096,
            "136010.303": 4096,
            "136010.304": 4096,
            "136010.305": 4096,
            "136010.306": 4096
        },
        "notes": []
    },
    {  # Might be able to use combined
        "name": "Liberator",
        "files": [
            "Liberator.bin",
            "Liberator Projection.bin"
        ],
        "partial": True
    },
    {
        "name": "Lunar Lander",
        "files": [
            "Lunar Lander.bin"
        ],
        "mame_name": "llander",
        "split": [
            "034599.01",
            "034598.01",
            "034571.02",
            "034572.02",
            "034597.01",
            "034570.01",
            "034569.02"
        ],
        "notes": [2]
    },
    {  # Might be able to use combined
        "name": "Major Havoc",
        "files": [
            "Major Havoc alpha banks.bin",
            "Major Havoc gamma.bin",
            "Major Havoc vector banks.bin",
            "Major Havoc.bin"
        ],
        "mame_name": "mhavoc",
        "handler": "_handle_mhavoc"
    },
    {
        "name": "Millipede",
        "files": [
            "Millipede.bin"
        ],
        "partial": True
    },
    {
        "name": "Missile Command",
        "files": [
            "Missile Command.bin"
        ],
        "mame_name": "missile",
        "split": [
            "035820.02",
            "035821.02",
            "035822.02",
            "035823.02",
            "035824.02",
            "035825.02"
        ]
    },
    {  # Appears to be redbarona variant instead of redbaron - try making a MAME current package?
        "name": "Red Baron",
        "files": [
            "Red Baron.bin"
        ],
        "mame_name": "redbaron",
        "partial": True
        # "split": {
        #     "037007.01e": 2048,
        #     "037000.01e": 2048,
        #     "037006.01e": 2048,
        #     "036998.01e": 2048,
        #     "036997.01e": 2048,
        #     "036996.01e": 2048,
        #     "036995.01e": 2048,
        #     "037587.01": 4096
        # }
    },
    {
        "name": "Space Duel",
        "files": [
            "Space Duel.bin"
        ],
        "mame_name": "spacduel",
        "split": {
            "136006.106": 2048,
            "136006.107": 4096,
            "136006.201": 4096,
            "136006.102": 4096,
            "136006.103": 4096,
            "136006.104": 4096,
            "136006.105": 4096
        }
    },
    {
        "name": "Sprint2",
        "files": [
            "Sprint2.bin"
        ],
        "partial": True
    },
    {
        "name": "Stunt Cycle",
        "files": [
            "stunt.bin"
        ],
        "partial": True
    },
    {
        "name": "Super Breakout",
        "files": [
            "Super Breakout.bin"
        ],
        "partial": True
    },
    {
        "name": "Tempest",
        "files": [
            "Tempest.bin"
        ],
        "mame_name": "tempest3",
        "split": [
            "237.002",
            "136.002",
            "235.002",
            "134.002",
            "133.002",
            "138.002"
        ]
    },
    {
        "name": "Warlords",
        "files": [
            "Warlords.bin"
        ],
        "partial": True
    },
    {
        "name": "Avalanche",
        "files": [
            "Avalanche.bin"
        ],
        "partial": True
    },
    {
        "name": "Atari Baseball",
        "files": [
            "AtariBaseball.bin"
        ],
        "partial": True
    },
    {
        "name": "Atari Basketball",
        "files": [
            "AtariBasketball.bin"
        ],
        "partial": True
    },
    {
        "name": "Destroyer",
        "files": [
            "Destroyer.bin"
        ],
        "partial": True
    },
    {
        "name": "Dominos",
        "files": [
            "Dominos.bin"
        ],
        "partial": True
    },
    {
        "name": "Fire Truck",
        "files": [
            "FireTruck.bin"
        ],
        "partial": True
    },
    {
        "name": "Atari Football",
        "files": [
            "AtariFootball.bin"
        ],
        "partial": True
    },
    {
        "name": "Maze Invaders",
        "files": [
            "MazeInvaders.bin",
            "MazeInvaders.bmp"
        ],
        "mame_name": "mazeinv",
        "handler": "_handle_mazeinv",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Monte Carlo",
        "files": [
            "MonteCarlo.bin",
            "MonteCarloColors.bin",
            "MonteCarloSprites1.bmp",
            "MonteCarloSprites2.bmp",
            "MonteCarloTiles1.bmp",
            "MonteCarloTiles2.bmp"
        ],
        "mame_name": "montecar",
        "handler": "_handle_montecar",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Pool Shark",
        "files": [
            "Poolshark.bin"
        ],
        "partial": True
    },
    {
        "name": "Sky Diver",
        "files": [
            "SkydiverROM.bin"
        ],
        "partial": True
    },
    {
        "name": "Atari Soccer",
        "files": [
            "AtariSoccer.bin"
        ],
        "partial": True
    },
    {
        "name": "Super Bug",
        "files": [
            "SuperBug.bin"
        ],
        "partial": True
    }
]


def get_game_list():
    '''Transform the game map for documentation'''
    return map(lambda x: {
        'filename': f"{x['mame_name']}.zip" if 'mame_name' in x else "N/A",
        'game': x['name'],
        'system': "Arcade",
        "notes": [[1] if 'mame_name' in x else None] + [[5] if 'unextractable' in x and x['unextractable'] else None] + [x['notes'] if 'notes' in x else None]}, games)

def _handle_mhavoc(in_dir, game_desc):
    zip_files = {}
    # Major Havoc.bin
    with open(os.path.join(in_dir, "Major Havoc.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.custom_split(contents, [0x1000, 0x4000, 0x4000])
        zip_files['136025.210'] = transforms.pad(chunks[0], 0x2000)
        zip_files['136025.216'] = chunks[1]
        zip_files['136025.217'] = chunks[2]

    # Major Havoc alpha banks.bin
    with open(os.path.join(in_dir, "Major Havoc alpha banks.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.equal_split(contents, 2)
        zip_files['136025.215'] = chunks[0]
        zip_files['136025.318'] = chunks[1]

    # Major Havoc gamma.bin
    with open(os.path.join(in_dir, "Major Havoc gamma.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        zip_files['136025.108'] = contents

    # Major Havoc vector banks.bin
    with open(os.path.join(in_dir, "Major Havoc vector banks.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.equal_split(contents, 2)
        zip_files['136025.106'] = chunks[0]
        zip_files['136025.107'] = chunks[1]

    return [{
        'filename': f"{game_desc['mame_name']}.zip",
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_montecar(in_dir, game_desc):
    zip_files = {}

    # MonteCarlo.bin
    with open(os.path.join(in_dir, "MonteCarlo.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.equal_split(contents, 4)
        zip_files['35763-01.h1'] = chunks[0]
        zip_files['35763-01.f1'] = chunks[1]
        zip_files['35763-01.d1'] = chunks[2]
        zip_files['35763-01.c1'] = chunks[3]

    # MonteCarloColors.bin
    with open(os.path.join(in_dir, "MonteCarloColors.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        zip_files['35785-01.e7'] = contents

    # Bitmaps    
    bitmaps = [
        "MonteCarloSprites1.bmp",
        "MonteCarloSprites2.bmp",
        "MonteCarloTiles1.bmp",
        "MonteCarloTiles2.bmp"
    ]
    for bitmap_file in bitmaps:
        with open(os.path.join(in_dir, bitmap_file), "rb") as curr_file:
            contents = bytearray(curr_file.read())
            zip_files[bitmap_file] = contents

    return [{
        'filename': f"{game_desc['mame_name']}.zip",
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_mazeinv(in_dir, game_desc):
    zip_files = {}

    # MazeInvaders.bin
    with open(os.path.join(in_dir, "MazeInvaders.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.equal_split(contents, 5)
        zip_files['a'] = chunks[0]
        zip_files['b'] = chunks[1]
        zip_files['c'] = chunks[2]
        zip_files['d'] = chunks[3]
        zip_files['e'] = chunks[4]

    # Bitmaps    
    bitmaps = [
        "MazeInvaders.bmp",
    ]
    for bitmap_file in bitmaps:
        with open(os.path.join(in_dir, bitmap_file), "rb") as curr_file:
            contents = bytearray(curr_file.read())
            zip_files[bitmap_file] = contents

    return [{
        'filename': f"{game_desc['mame_name']}.zip",
        'contents': helpers.build_zip(zip_files)
    }]


def _handle_standard(in_dir, game_desc):
    out_files = []
    with open(os.path.join(in_dir, game_desc['files'][0]), "rb") as curr_file:
        contents = bytearray(curr_file.read())

        # Truncate
        if 'truncate' in game_desc:
            contents = transforms.truncate(contents, game_desc['truncate'])

        # Split
        split_data = game_desc['split']
        if isinstance(split_data, list):
            chunks = transforms.equal_split(contents, len(game_desc['split']))
            filenames = split_data
        elif isinstance(split_data, dict):
            filenames = list(split_data.keys())
            sizes = list(split_data.values())
            chunks = transforms.custom_split(contents, sizes)
        else:
            logger.error("Invalid split type!")
            return []
        out_files.append({
            'filename': f"{game_desc['mame_name']}.zip",
            'contents': helpers.build_zip(dict(zip(filenames, chunks)))
        })
    return out_files


def extract_partials(in_dir, out_dir):
    '''Extract Atari Arcade ROMs'''
    rom_path = os.path.join(in_dir, "AtariVault_Data",
                            "StreamingAssets", "FOCAL_Emulator")

    output_files = []
    funcs = globals()
    for game in games:
        if 'partial' in game and game['partial'] is True:
            logger.info(f"Copying partially extracted {game['name']}...")
            
            if 'handler' in game:
                handler_func = funcs[game['handler']]
                output_files += handler_func(rom_path, game)
            else:
                for file in game['files']:
                    file_path = os.path.join(rom_path, file)
                    try:
                        shutil.copyfile(file_path, os.path.join(out_dir, file))
                    except Exception as _:
                        logger.warning(f'Error while processing {file_path}!')
                        
    for output_file in output_files:
        logger.info(f"Writing {output_file['filename']}...")
        out_path = os.path.join(out_dir, output_file['filename'])
        with open(out_path, "wb") as out_file:
            out_file.write(output_file['contents'])


def extract(in_dir, out_dir):
    '''Extract Atari Arcade ROMs'''
    rom_path = os.path.join(in_dir, "AtariVault_Data",
                            "StreamingAssets", "FOCAL_Emulator")

    output_files = []
    funcs = globals()
    for game in games:
        if 'partial' not in game or game['partial'] is False:
            logger.info(f"Extracting {game['name']}...")
            if 'handler' in game:
                handler_func = funcs[game['handler']]
            else:
                handler_func = _handle_standard
            output_files += handler_func(rom_path, game)
    logger.info("Saving games...")
    for output_file in output_files:
        logger.info(f"Writing {output_file['filename']}...")
        out_path = os.path.join(out_dir, output_file['filename'])
        with open(out_path, "wb") as out_file:
            out_file.write(output_file['contents'])
