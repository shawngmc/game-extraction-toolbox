'''Extraction code for incomplete ROMs'''
import logging
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.snk40 import utils
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "World Wars",
        "system": "Arcade",
        "filename": "worldwar.zip",
        "notes": [2] # PH files, not working
    }
]


def extract(bundle_contents):
    '''Extract all partial ROMs'''
    out_files = []

    out_files.extend(extract_bermuda(bundle_contents['patch']))

    # for key, value in bundle_contents['dlc'].items():
    #     # if key.endswith(".proms") or key.endswith(".pal"):
    #     out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['main'].items():
    #     if key.endswith(".proms") or key.endswith(".pal"):
    #         out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['patch'].items():
    #     if key.endswith(".proms") or key.endswith(".pal"):
    #         out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['main'].items():
    #     out_files.append({'filename': key, 'contents': value})
        # if key.endswith(".proms"):
        #     out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['patch'].items():
    #     print(key)
        # if key.endswith(".proms") or key.endswith(".pal"):
        #     out_files.append({'filename': key, 'contents': value})

    return out_files


def extract_bermuda(bundle_contents):
    '''Extract Bermuda Triangle / World Wars'''
    out_files = []
    # for key, value in bundle_contents.items():
    #     if key.startswith("BermudaTriangle"):
    #         print(f'{key}: {len(value)}')

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
    func_map['pal'] = utils.simple_palette_helper('WorldWars.pal', pal_filenames)
    mame_name = "worldwar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files
