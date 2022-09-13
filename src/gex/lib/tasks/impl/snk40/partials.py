'''Extraction code for incomplete ROMs'''
import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "aso.zip",
        "notes": [1] # Fail CRC on Palette
    },
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "alphamis.zip",
        "notes": [1] # Fail CRC on Palette
    },
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "arian.zip",
        "notes": [1] # Fail CRC on Palette
    },
    {
        "game": "TNKIII",
        "system": "Arcade",
        "filename": "tnk3.zip",
        "notes": [1] # Colors broken (Pal CRC Mismatch)
    },
    {
        "game": "TNKIII (J)",
        "system": "Arcade",
        "filename": "tnk3j.zip",
        "notes": [1] # Colors broken (Pal CRC Mismatch)
    },
    {
        "game": "World Wars",
        "system": "Arcade",
        "filename": "worldwar.zip",
        "notes": [2] # PH files, not working
    },
    {
        "game": "MarvinsMaze",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1] # Colors broken (Pal CRC Mismatch)
    },
    {
        "game": "Athena",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1] # Colors broken (Pal CRC Mismatch)
    }
]

def _pal_helper(in_file_ref, pal_filenames):
    '''Rebuild RGB Palette ROMs'''
    def palette(in_files):
        in_data = in_files[in_file_ref]
        pal_contents = transforms.deinterleave_nibble(in_data, 4)
        del pal_contents[2] # Remove the spacing entry
        return dict(zip(pal_filenames, pal_contents))
    return palette

def extract(bundle_contents):
    '''Extract all partial ROMs'''
    out_files = []
    out_files.extend(extract_tnk3(bundle_contents['main']))
    out_files.extend(extract_aso(bundle_contents['main']))
    out_files.extend(extract_athena(bundle_contents['main']))

    out_files.extend(extract_bermuda(bundle_contents['patch']))
    out_files.extend(extract_marvin(bundle_contents['patch']))

    # for key, value in bundle_contents['dlc'].items():
    #     # if key.endswith(".proms") or key.endswith(".pal"):
    #     out_files.append({'filename': key, 'contents': value})
    for key, value in bundle_contents['main'].items():
        if key.endswith(".proms") or key.endswith(".pal"):
            out_files.append({'filename': key, 'contents': value})
    for key, value in bundle_contents['patch'].items():
        if key.endswith(".proms") or key.endswith(".pal"):
            out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['main'].items():
    #     out_files.append({'filename': key, 'contents': value})
        # if key.endswith(".proms"):
        #     out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['patch'].items():
    #     print(key)
        # if key.endswith(".proms") or key.endswith(".pal"):
        #     out_files.append({'filename': key, 'contents': value})

    return out_files

def extract_aso(bundle_contents):
    '''Extract Armored Scrum Object'''
    print("NYI")
    out_files = []
    for key, value in bundle_contents.items():
        if key.startswith("ASOArmoredScrumObject"):
            print(f'{key}: {len(value)}')

    # ASO Common
    func_map = {}
    func_map['bg'] = helpers.name_file_helper("ASOArmoredScrumObject.bg", "p10.14h")
    audiocpu_filenames = [
        "p7.4f",
        "p8.3f",
        "p9.2f"
    ]
    func_map['audiocpu'] = helpers.equal_split_helper(
        'ASOArmoredScrumObject.2.z80', audiocpu_filenames)
    sp_filenames = [
        "p11.11h",
        "p12.9h",
        "p13.8h"
    ]
    def aso_sp(in_files):
        contents = in_files['ASOArmoredScrumObject.sp']
        chunks = transforms.equal_split(contents, num_chunks = 12)

        p11 = transforms.merge([chunks[2] + chunks[3] + chunks[0] + chunks[1]])
        p12 = transforms.merge([chunks[6] + chunks[7] + chunks[4] + chunks[5]])
        p13 = transforms.merge([chunks[10] + chunks[11] + chunks[8] + chunks[9]])

        chunks = [p11, p12, p13]

        return dict(zip(sp_filenames, chunks))
    func_map['sp'] = aso_sp
    pal_filenames = [
        "mb7122h.13f",
        "mb7122h.12f",
        "mb7122h.14f"
    ]
    func_map['pal'] = _pal_helper('ASOArmoredScrumObject.pal', pal_filenames)
    logger.info("Processing ASO common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    # ASO
    func_map = {}
    maincpu_filenames = [
        "p1.8d",
        "p2.7d",
        "p3.5d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper(
        'ASOArmoredScrumObject.0.z80', maincpu_filenames)
    sub_filenames = [
        "p4.3d",
        "p5.2d",
        "p6.1d"
    ]
    func_map['sub'] = helpers.equal_split_helper('ASOArmoredScrumObject.1.z80', sub_filenames)
    func_map['tx'] = helpers.name_file_helper("ASOArmoredScrumObject.tx", "p14.1h")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "aso.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # ALPHAMIS
    func_map = {}
    maincpu_filenames = [
        "p1.8d",
        "p2.7d",
        "p3.5d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper(
        'ASOArmoredScrumObject.b.0.z80', maincpu_filenames)
    sub_filenames = [
        "p4.3d",
        "p5.2d",
        "p6.1d"
    ]
    func_map['sub'] = helpers.equal_split_helper('ASOArmoredScrumObject.b.1.z80', sub_filenames)
    func_map['tx'] = helpers.name_file_helper("ASOArmoredScrumObject.b.tx", "p14.1h")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "alphamis.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # ARIAN
    func_map = {}
    maincpu_filenames = [
        "p1.8d",
        "p2.7d",
        "p3.5d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper(
        'ASOArmoredScrumObject.c.0.z80', maincpu_filenames)
    sub_filenames = [
        "p4.3d",
        "p5.2d",
        "p6.1d"
    ]
    func_map['sub'] = helpers.equal_split_helper('ASOArmoredScrumObject.c.1.z80', sub_filenames)
    func_map['tx'] = helpers.name_file_helper("ASOArmoredScrumObject.c.tx", "p14.1h")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "arian.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_athena(bundle_contents):
    '''Extract Athena'''
    out_files = []

    func_map = {}
    sub_file_map = {
        "p3.8p": 0x4000,
        "p4.8m": 0x8000
    }
    func_map['sub'] = helpers.custom_split_helper('Athena.1.z80', sub_file_map)
    audiocpu_file_map = {
        "p5.6g": 0x4000,
        "p6.6k": 0x8000
    }
    func_map['audiocpu'] = helpers.custom_split_helper('Athena.2.z80', audiocpu_file_map)
    sp_filenames = [
        "p7.2p",
        "p8.2s",
        "p9.2t"
    ]
    func_map['sp'] = helpers.equal_split_helper('Athena.sp', sp_filenames)

    maincpu_file_map = {
        "p1.4p": 0x4000,
        "p2.4m": 0x8000
    }
    func_map['maincpu'] = helpers.custom_split_helper('Athena.0.z80', maincpu_file_map)
    func_map['tx'] = helpers.name_file_helper("Athena.tx", "p11.2d")
    func_map['bg'] = helpers.name_file_helper("Athena.bg", "p10.2b")
    pal_filenames = [
        "2.1b",
        "1.1c",
        "3.2c"
    ]
    func_map['pal'] = _pal_helper('Athena.pal', pal_filenames)
    mame_name = "athena.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_bermuda(bundle_contents):
    '''Extract Bermuda Triangle / World Wars'''
    out_files = []
    for key, value in bundle_contents.items():
        if key.startswith("BermudaTriangle"):
            print(f'{key}: {len(value)}')

    # Bermuda Triangle Common
    # BermudaTriangle.1.z80
    # BermudaTriangle.bg
    # BermudaTriangle.sp
    # BermudaTriangle.sp32
    # BermudaTriangle.tx

    # BermudaTriangle.0.z80
    # BermudaTriangle.2.z80
    # BermudaTriangle.adpcm

    # BermudaTriangle.j.0.z80
    # BermudaTriangle.j.2.z80
    # BermudaTriangle.j.adpcm

    # World Wars Common
    func_map = {}
    bg_filenames = [
        "ww11.1e",
        "ww12.1d",
        "ww13.1b",
        "ww14.1a"
    ]
    func_map['bg'] = helpers.equal_split_helper('WorldWars.bg', bg_filenames)
    sp_filenames = [
        "ww10.3g",
        "ww9.3e",
        "ww8.3d",
        "ww7.3b"
    ]
    func_map['sp'] = helpers.equal_split_helper('WorldWars.sp', sp_filenames)
    sp32_filenames = [
        "ww21.7p",
        "ww22.7s",
        "ww19.8h",
        "ww20.8k",
        "ww15.8m",
        "ww16.8n",
        "ww17.8p",
        "ww18.8s"
    ]
    func_map['sp32'] = helpers.equal_split_helper('WorldWars.sp32', sp32_filenames)
    ph_files = {
        'l.1d': 0x1000,
        'l.2d': 0x1000,
        'horizon.5h': 0x400,
        'vertical.7h': 0x400
    }
    func_map['ph'] = helpers.placeholder_helper(ph_files)
    logger.info("Processing World Wars common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # WORLDWAR
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("WorldWars.0.z80", "ww4.4p")
    func_map['sub'] = helpers.name_file_helper("WorldWars.1.z80", "ww5.8p")
    func_map['audiocpu'] = helpers.name_file_helper("WorldWars.2.z80", "ww3.7k")
    func_map['tx'] = helpers.name_file_helper("WorldWars.tx", "ww6.3a")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    pal_filenames = [
        "2.1l",
        "1.1k",
        "3.2l"
    ]
    func_map['pal'] = _pal_helper('WorldWars.pal', pal_filenames)
    mame_name = "worldwar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_marvin(bundle_contents):
    '''Extract Marvin's Maze'''
    out_files = []
    func_map = {}
    maincpu_filenames = [
        "pa1",
        "pa2",
        "pa3"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('MarvinsMaze.0.z80', maincpu_filenames)
    func_map['sub'] = helpers.name_file_helper("MarvinsMaze.1.z80", "pb1")
    audiocpu_filenames = [
        "m1",
        "m2"
    ]
    func_map['audiocpu'] = helpers.equal_split_helper('MarvinsMaze.2.z80', audiocpu_filenames)
    func_map['bg'] = helpers.name_file_helper("MarvinsMaze.bg", "b2")
    func_map['fg'] = helpers.name_file_helper("MarvinsMaze.fg", "b1")
    sp_filenames = [
        "f1",
        "f2",
        "f3"
    ]
    func_map['sp'] = helpers.equal_split_helper('MarvinsMaze.sp', sp_filenames)
    func_map['tx'] = helpers.name_file_helper("MarvinsMaze.tx", "s1")
    pal_filenames = [
        "marvmaze.j2",
        "marvmaze.j1",
        "marvmaze.j3"
    ]
    func_map['pal'] = _pal_helper('MarvinsMaze.pal', pal_filenames)
    mame_name = "marvins.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_tnk3(bundle_contents):
    '''Extract TnkIII'''
    out_files = []

    # # TNK3 Common
    func_map = {}
    sub_filenames = [
        "p4.2e",
        "p5.2f",
        "p6.2h"
    ]
    func_map['sub'] = helpers.equal_split_helper('TNKIII.1.z80', sub_filenames)
    audiocpu_filenames = [
        "p10.6f",
        "p11.6d"
    ]
    func_map['audiocpu'] = helpers.equal_split_helper('TNKIII.2.z80', audiocpu_filenames)
    bg_filenames = [
        "p12.3d",
        "p13.3c"
    ]
    func_map['bg'] = helpers.equal_split_helper('TNKIII.bg', bg_filenames)
    sp_filenames = [
        "p7.7h",
        "p8.7f",
        "p9.7e"
    ]
    func_map['sp'] = helpers.equal_split_helper('TNKIII.sp', sp_filenames)
    pal_filenames = [
        "1.5g",
        "2.5f",
        "0.5h"
    ]
    func_map['pal'] = _pal_helper('TNKIII.pal', pal_filenames)
    logger.info("Processing TNK3 common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    # # TNK3
    func_map = {}
    maincpu_filenames = [
        "p1.4e",
        "p2.4f",
        "p3.4h"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('TNKIII.0.z80', maincpu_filenames)
    func_map['tx'] = helpers.name_file_helper("TNKIII.tx", "p14.1e")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "tnk3.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # TNK3J
    func_map = {}
    maincpu_filenames = [
        "p1.4e",
        "p2.4f",
        "p3.4h"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('TNKIII.j.0.z80', maincpu_filenames)
    func_map['tx'] = helpers.name_file_helper("TNKIII.j.tx", "p14.1e")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "tnk3j.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files
