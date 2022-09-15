'''Extraction code for Atari Arcade ROMs'''
import logging
import os
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
            "CanyonBomber.bin",
            "CanyonBomberSprites.bmp",
            "CanyonBomberTiles.bmp"
        ],
        "mame_name": "canyon",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Centipede",
        "files": [
            "Centipede.bin",
            "Centipede.bmp"
        ],
        "mame_name": "centiped",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Crystal Castles",
        "files": [
            "Crystal Castles.bin",
            "Crystal Castles.bmp"
        ],
        "mame_name": "ccastles",
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
    {
        "name": "Liberator",
        "files": [
            "Liberator.bin",
            "Liberator.bmp",
            "Liberator Projection.bin"
        ],
        "mame_name": "liberatr",
        "partial": True,
        "notes": [6]
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
    {
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
            "Millipede.bin",
            "Millipede.bmp"
        ],
        "mame_name": "milliped",
        "partial": True,
        "notes": [6]
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
    {
        "name": "Red Baron",
        "files": [
            "Red Baron.bin"
        ],
        "mame_name": "redbaron",
        "handler": "_handle_redbaron"
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
    { # Look at avault2mame.js
        "name": "Sprint2",
        "files": [
            "Sprint2.bin",
            "Sprint2Sprites.bmp",
            "Sprint2Tiles.bmp"
        ],
        "mame_name": "sprint2",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Super Breakout",
        "files": [
            "Super Breakout.bin",
            "Super Breakout vector.bmp",
            "Super Breakout.bmp"
        ],
        "mame_name": "sbrkout",
        "partial": True,
        "notes": [6]
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
            "Warlords.bin",
            "Warlords Background.bmp",
            "Warlords.bmp"
        ],
        "mame_name": "warlords",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Avalanche",
        "files": [
            "Avalanche.bin"
        ],
        "mame_name": "avalnche",
        "handler": "_handle_avalnche"
    },
    {
        "name": "Atari Baseball",
        "files": [
            "AtariBaseball.bin",
            "AtariBaseballTiles1.bmp",
            "AtariBaseballTiles2.bmp"
        ],
        "mame_name": "abaseb",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Atari Basketball",
        "files": [
            "AtariBasketball.bin",
            "AtariBasketballTiles.bmp",
            "AtariBasketballSprites.bmp"
        ],
        "mame_name": "bsktball",
        "partial": True
    },
    {
        "name": "Destroyer",
        "files": [
            "Destroyer.bin",
            "DestroyerSprites1.bmp",
            "DestroyerSprites2.bmp",
            "DestroyerTiles.bmp",
            "DestroyerWaves.bmp"
        ],
        "mame_name": "destroyr1",
        "partial": True
    },
    {
        "name": "Dominos",
        "files": [
            "Dominos.bin",
            "DominosTiles.bmp"
        ],
        "mame_name": "dominos",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Fire Truck",
        "files": [
            "FireTruck.bin",
            "FireTruckSprites1.bmp",
            "FireTruckSprites2.bmp",
            "FireTruckTiles1.bmp",
            "FireTruckTiles2.bmp"
        ],
        "mame_name": "firetrk",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Atari Football",
        "files": [
            "AtariFootball.bin",
            "AtariFootballTiles1.bmp",
            "AtariFootballTiles2.bmp"
        ],
        "mame_name": "atarifb",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Maze Invaders",
        "files": [
            "MazeInvaders.bin",
            "MazeInvaders.bmp"
        ],
        "mame_name": "mazeinv",
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
            "Poolshark.bin",
            "PoolsharkSprites.bmp",
            "PoolsharkTiles.bmp"
        ],
        "mame_name": "poolshrk",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Sky Diver",
        "files": [
            "SkydiverROM.bin",
            "SkydiverSprites.bmp",
            "SkydiverTiles.bmp"
        ],
        "mame_name": "skydiver",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Atari Soccer",
        "files": [
            "AtariSoccer.bin",
            "AtariSoccerSprites.bmp",
            "AtariSoccerTiles1.bmp",
            "AtariSoccerTiles2.bmp"
        ],
        "mame_name": "soccer",
        "partial": True,
        "notes": [6]
    },
    {
        "name": "Super Bug",
        "files": [
            "SuperBug.bin",
            "SuperBugSprites.bmp",
            "SuperBugTiles1.bmp",
            "SuperBugTiles2.bmp"
        ],
        "mame_name": "superbug",
        "partial": True,
        "notes": [6]
    }
]


def get_game_list():
    '''Transform the game map for documentation'''
    return map(lambda x: {
        'filename': f"{x['mame_name']}{'-partial' if 'partial' in x and x['partial'] is True else ''}.zip",
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
        'filename': f"{game_desc['mame_name']}-partial.zip",
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_redbaron(in_dir, game_desc):
    zip_files = {}

    # Red Baron.bin
    with open(os.path.join(in_dir, "Red Baron.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())
        chunks = transforms.equal_split(contents, 9)
        zip_files['35763-01.h1'] = chunks[0]


        zip_files["037587.01"] = transforms.merge([chunks[0] + chunks[2]])
        zip_files["037000.01e"] = chunks[1]
        zip_files["036998.01e"] = chunks[3]
        zip_files["036997.01e"] = chunks[4]
        zip_files["036996.01e"] = chunks[5]
        zip_files["036995.01e"] = chunks[6]
        zip_files["037006.01e"] = chunks[7]
        zip_files["037007.01e"] = chunks[8]

    return [{
        'filename': f"{game_desc['mame_name']}.zip",
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_avalnche(in_dir, game_desc):
    # Avalanche.bin
    with open(os.path.join(in_dir, "Avalanche.bin"), "rb") as curr_file:
        contents = bytearray(curr_file.read())

        chunks = transforms.equal_split(contents, 3)
        new_chunks = []
        for chunk in chunks:
            new_chunks.extend(transforms.deinterleave_nibble(chunk, 2))

        filenames = [
            "30612.d2",
            "30615.d3",
            "30613.e2",
            "30616.e3",
            "30611.c2",
            "30614.c3",
        ]
        zip_files = dict(zip(filenames, new_chunks))

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
    '''Extract Partial Atari Arcade ROMs'''
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
                zip_files = {}
                for filename in game['files']:
                    with open(os.path.join(rom_path, filename), "rb") as curr_file:
                        contents = bytearray(curr_file.read())
                        zip_files[filename] = contents
                
                with open(os.path.join(out_dir, f"{game['mame_name']}-partial.zip"), "wb") as out_file:
                    out_file.write(helpers.build_zip(zip_files))
                        
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
