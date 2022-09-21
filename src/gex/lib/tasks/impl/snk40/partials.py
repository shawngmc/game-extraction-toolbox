'''Extraction code for incomplete ROMs'''
import logging
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.snk40 import utils

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "Bermuda Triangle/World Wars",
        "system": "Arcade",
        "filename": "partial-bermudatriangle-worldwar.zip",
        "status": "partial",
        "notes": [4]
    }
]


def extract(bundle_contents):
    '''Extract all partial ROMs'''
    out_files = []

    out_files.extend(_handle_btww_all(bundle_contents['patch']))

    return out_files


def _handle_btww_all(bundle_contents):
    '''Extract Bermuda Triangle / World Wars'''
    out_files = []
    
    target_files = [
        "BermudaTriangle.0.z80",
        "BermudaTriangle.1.z80",
        "BermudaTriangle.2.z80",
        "BermudaTriangle.adpcm",
        "BermudaTriangle.bg",
        "BermudaTriangle.j.0.z80",
        "BermudaTriangle.j.2.z80",
        "BermudaTriangle.j.adpcm",
        "BermudaTriangle.pal",
        "BermudaTriangle.sp",
        "BermudaTriangle.sp32",
        "BermudaTriangle.tx",
        "WorldWars.0.z80",
        "WorldWars.1.z80",
        "WorldWars.2.z80",
        "WorldWars.adpcm",
        "WorldWars.bg",
        "WorldWars.j.0.z80",
        "WorldWars.j.1.z80",
        "WorldWars.j.2.z80",
        "WorldWars.j.pal",
        "WorldWars.j.tx",
        "WorldWars.pal",
        "WorldWars.sp",
        "WorldWars.sp32",
        "WorldWars.tx"
    ]

    zip_files = {}
    for target_file in target_files:
        zip_files[target_file] = bundle_contents[target_file]

    archive_name = "partial-bermudatriangle-worldwar.zip"
    logger.info(f"Building {archive_name}...")
    out_files.append(
        {'filename': archive_name, 'contents': helpers.build_zip(zip_files)}
    )
    logger.info(f"Extracted {archive_name}.")

    return out_files
