'''Extraction code for Atari Arcade ROMs'''
import logging
import os
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.utils import gfx_rebuilder

logger = logging.getLogger('gextoolbox')

def _handle_mhavoc(in_files, game_desc):
    zip_files = {}

    # Major Havoc.bin
    contents = in_files.get('Major Havoc.bin')['contents']
    chunks = transforms.custom_split(contents, [0x1000, 0x4000, 0x4000])
    zip_files['136025.210'] = transforms.pad(chunks[0], 0x2000)
    zip_files['136025.216'] = chunks[1]
    zip_files['136025.217'] = chunks[2]

    # Major Havoc alpha banks.bin
    contents = in_files.get('Major Havoc alpha banks.bin')['contents']
    chunks = transforms.equal_split(contents, 2)
    zip_files['136025.215'] = chunks[0]
    zip_files['136025.318'] = chunks[1]

    # Major Havoc gamma.bin
    contents = in_files.get('Major Havoc gamma.bin')['contents']
    zip_files['136025.108'] = contents

    # Major Havoc vector banks.bin
    contents = in_files.get('Major Havoc vector banks.bin')['contents']
    chunks = transforms.equal_split(contents, 2)
    zip_files['136025.106'] = chunks[0]
    zip_files['136025.107'] = chunks[1]

    return [{
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_montecar(in_files, game_desc):
    zip_files = {}

    # MonteCarlo.bin
    contents = in_files.get('MonteCarlo.bin')['contents']
    chunks = transforms.equal_split(contents, 4)
    zip_files['35763-01.h1'] = chunks[0]
    zip_files['35763-01.f1'] = chunks[1]
    zip_files['35763-01.d1'] = chunks[2]
    zip_files['35763-01.c1'] = chunks[3]

    # MonteCarloColors.bin
    contents = in_files.get('MonteCarloColors.bin')['contents']
    zip_files['35785-01.e7'] = contents

    # Bitmaps
    bitmaps = [
        "MonteCarloSprites1.bmp",
        "MonteCarloSprites2.bmp",
        "MonteCarloTiles1.bmp",
        "MonteCarloTiles2.bmp"
    ]
    for bitmap_file in bitmaps:
        contents = in_files.get(bitmap_file)['contents']
        zip_files[bitmap_file] = contents

    return [{
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_redbaron(in_files, game_desc):
    zip_files = {}

    # Red Baron.bin
    contents = in_files.get('Red Baron.bin')['contents']
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
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_sprint2(in_files, game_desc):
    zip_files = {}

    # Sprint2.bin
    contents = in_files.get('Sprint2.bin')['contents']
    chunks = transforms.equal_split(contents, 4)
    zip_files['6290-01.b1'] = chunks[0]
    zip_files['6291-01.c1'] = chunks[1]
    zip_files['6404.d1'] = chunks[2]
    zip_files['6405.e1'] = chunks[3]

    # Sprint2Sprites.bmp
    contents = in_files.get('Sprint2Sprites.bmp')['contents']
    contents = gfx_rebuilder.reverse_bmp(contents)
    sprint2_car_layout = {
        'width': 16,
        'height': 8,
        'total': 32,
        'planes': 1,
        'planeoffset': [0],
        'xoffset': [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0,
                0xf, 0xe, 0xd, 0xc, 0xb, 0xa, 0x9, 0x8],
        'yoffset': [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70],
        'charincrement': 0x80
    }
    contents = gfx_rebuilder.reencode_gfx(contents, sprint2_car_layout)
    chunks = transforms.deinterleave_nibble(contents, 2)
    zip_files['6399-01.j6'] = chunks[0]
    zip_files['6398-01.k6'] = chunks[1]

    # Sprint2Tiles.bmp
    contents = in_files.get('Sprint2Tiles.bmp')['contents']
    contents = gfx_rebuilder.reverse_bmp(contents)
    sprint2_tile_layout = {
        'width': 8,
        'height': 8,
        'total': 64,
        'planes': 1,
        'planeoffset': [0],
        'xoffset': [0, 1, 2, 3, 4, 5, 6, 7],
        'yoffset': [0x00, 0x08, 0x10, 0x18, 0x20, 0x28, 0x30, 0x38],
        'charincrement': 0x40
    }
    contents = gfx_rebuilder.reencode_gfx(contents, sprint2_tile_layout)
    chunks = transforms.deinterleave_nibble(contents, 2)
    zip_files['6396-01.p4'] = chunks[0]
    zip_files['6397-01.r4'] = chunks[1]

    zip_files['6400-01.m2'] = bytearray(0x100)
    zip_files['6401-01.e2'] = bytearray(0x20)

    return [{
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(zip_files)
    }]

# def _handle_canyon(in_files, game_desc):
#     zip_files = {}

#     # CanyonBomber.bin
#     contents = in_files.get('CanyonBomber.bin')['contents']
#     chunks = transforms.custom_split(contents, [1024, 1024, 2048])
#     nib_chunks = transforms.deinterleave_nibble(chunks[0], 2)
#     zip_files['9503-01.p1'] = nib_chunks[0]
#     zip_files['9499-01.j1'] = nib_chunks[1]
#     zip_files['9496-01.d1'] = chunks[2]

#     # CanyonBomberSprites.bmp
#     contents = in_files.get('CanyonBomberSprites.bmp')['contents']
#     contents = gfx_rebuilder.reverse_bmp(contents)
#     _SPRITE_LAYOUT = {
#         'width': 32,
#         'height': 16,
#         'total': 4,
#         'planes': 1,
#         'planeoffset': [0],
#         'xoffset': [0x007, 0x006, 0x005, 0x004, 0x003, 0x002, 0x001, 0x000,
#             0x00F, 0x00E, 0x00D, 0x00C, 0x00B, 0x00A, 0x009, 0x008,
#             0x107, 0x106, 0x105, 0x104, 0x103, 0x102, 0x101, 0x100,
#             0x10F, 0x10E, 0x10D, 0x10C, 0x10B, 0x10A, 0x109, 0x108],
#         'yoffset': [0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
#             0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0],
#         'charincrement': 0x200
#     }
#     contents = gfx_rebuilder.reencode_gfx(contents, _SPRITE_LAYOUT)
#     chunks = transforms.deinterleave_nibble(contents, 2)
#     zip_files['9505-01.n5'] = chunks[0]
#     zip_files['9506-01.m5'] = chunks[1]

#     # CanyonBomberTiles.bmp
#     # Something is wrong with the math on this one,
#     # and I think it's a discrepancy vs. the mame tile layout
#     contents = in_files.get('CanyonBomberTiles.bmp')['contents']
#     contents = gfx_rebuilder.reverse_bmp(contents)
#     zip_files['tiles_temp'] = contents
#     _TILE_LAYOUT = {
#         'width': 8,
#         'height': 8,
#         'total': 64,
#         'planes': 1,
#         'planeoffset': [0],
#         'xoffset': [4, 5, 6, 7, 0, 1, 2, 3],
#         'yoffset': [0x00, 0x08, 0x10, 0x18, 0x20, 0x28, 0x30, 0x38],
#         'charincrement': 0x80
#     }
#     contents = gfx_rebuilder.reencode_gfx(contents, _TILE_LAYOUT)
#     zip_files['9492-01.n8'] = contents

#     return [{
#         'filename': f"{game_desc['mame_name']}.zip",
#         'contents': helpers.build_zip(zip_files)
#     }]

def _handle_avalnche(in_files, game_desc):
    # Avalanche.bin
    contents = in_files.get('Avalanche.bin')['contents']
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
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(zip_files)
    }]

def _handle_standard(in_files, game_desc):
    out_files = []

    contents = list(in_files.values())[0]['contents']

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
        'filename': game_desc['filename'],
        'contents': helpers.build_zip(dict(zip(filenames, chunks)))
    })

    return out_files

def extract(in_dir, out_dir, class_ref, include_partials):
    '''Extract Atari Arcade ROMs'''
    funcs = globals()
    for game in class_ref._metadata['out']['files']:
        if game['set'] == 'Arcade' and game['status'] != 'no-rom':
            is_partial = game['status'] == 'partial'
            if is_partial and not include_partials:
                continue

            logger.info(f"Reading {game['game']}...")

            # Read the input files
            in_files = {}
            for in_file_ref in game['in_files']:
                file_metadata = class_ref._metadata['in']['files'].get(in_file_ref)
                datafile = class_ref.read_datafile(in_dir, file_metadata)
                in_files[datafile['name']] = {
                    "contents": datafile['contents'],
                    "metadata": file_metadata
                }

            if is_partial:
                logger.info(f"Copying partially extracted {game['game']}...")

                if 'handler' in game:
                    handler_func = funcs[game['handler']]
                    output_files = handler_func(in_files, game)
                else:
                    zip_files = {}
                    for filename in game['in_files']:
                        zip_files[filename] = in_files[filename]['contents']

                    output_files = [{
                        'filename': game['filename'],
                        'contents': helpers.build_zip(zip_files)
                    }]
            else:
                logger.info(f"Extracting {game['game']}...")
                if 'handler' in game:
                    handler_func = funcs[game['handler']]
                else:
                    handler_func = _handle_standard
                output_files = handler_func(in_files, game)
            
            for output_file in output_files:
                filename = output_file['filename']
                logger.info(f"Writing {game['game']} to {filename}...")
                _ = class_ref.verify_out_file(filename, output_file['contents'])
                out_path = os.path.join(out_dir, filename)
                with open(out_path, "wb") as out_file:
                    out_file.write(output_file['contents'])
