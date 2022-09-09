'''Extraction code for incomplete ROMs'''
import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Guerilla War",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Psycho Soldier",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "TNKIII",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Ikari I",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Ikari 2 Victory Road",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Bermuda Triangle",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "World Wars",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "MarvinsMaze",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Athena",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    }
]

def extract(bundle_contents):
    '''Extract all partial ROMs'''
    out_files = []
    out_files.extend(extract_tnk3(bundle_contents['main']))
    out_files.extend(extract_victoryroad(bundle_contents['main']))
    out_files.extend(extract_aso(bundle_contents['main']))
    out_files.extend(extract_athena(bundle_contents['main']))
    out_files.extend(extract_ikari(bundle_contents['main']))
    out_files.extend(extract_guerilla(bundle_contents['main']))
    out_files.extend(extract_psycho(bundle_contents['main']))

    out_files.extend(extract_bermuda(bundle_contents['patch']))
    out_files.extend(extract_marvin(bundle_contents['patch']))

    # for key, value in bundle_contents['patch'].items():
    #     if key.startswith("BermudaTriangle"):
    #         out_files.append({'filename': key, 'contents': value})
    # for key, value in bundle_contents['patch'].items():
    #     if key.startswith("WorldWar"):
    #         out_files.append({'filename': key, 'contents': value})

    return out_files
    
def extract_victoryroad(bundle_contents):
    '''Extract Ikari 2 Victory Road'''
    print("NYI")
    out_files = []

    for key, value in bundle_contents.items():
        if key.startswith("VictoryRoad"):
            print(f'{key}: {len(value)}')

    # VICTROAD Common
    func_map = {}
    func_map['sub'] = helpers.name_file_helper("VictoryRoad.1.z80", "p2.8p")
    sp32_filenames = [
        "p11.4m",
        "p14.2m",
        "p12.4p",
        "p15.2p",
        "p13.4r",
        "p16.2r"
    ]
    func_map['sp32'] = helpers.equal_split_helper('VictoryRoad.sp32', sp32_filenames)
    bg_filenames = [
        "p17.4c",
        "p18.2c",
        "p19.4b",
        "p20.2b"
    ]
    func_map['bg'] = helpers.equal_split_helper('VictoryRoad.bg', bg_filenames)
    logger.info("Processing Victory Road common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # DOGOSOKE
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("VictoryRoad.j.0.z80", "p1.4p")
    func_map['audiocpu'] = helpers.name_file_helper("VictoryRoad.j.2.z80", "p3.7k")
    adpcm_filenames = [
        "p4.5e",
        "p5.5g"
    ]
    func_map['adpcm'] = helpers.equal_split_helper('VictoryRoad.j.adpcm', adpcm_filenames)
    func_map['tx'] = helpers.name_file_helper("VictoryRoad.j.tx", "p7.3b")
    sp_filenames = [
        "p8.3d",
        "p9.3f",
        "p10.3h"
    ]
    func_map['sp'] = helpers.equal_split_helper('VictoryRoad.j.sp', sp_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "dogosoke.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # VICTROAD
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("VictoryRoad.0.z80", "p1.4p")
    func_map['audiocpu'] = helpers.name_file_helper("VictoryRoad.2.z80", "p3.7k")
    adpcm_filenames = [
        "p4.5e",
        "p5.5g"
    ]
    func_map['adpcm'] = helpers.equal_split_helper('VictoryRoad.adpcm', adpcm_filenames)
    func_map['tx'] = helpers.name_file_helper("VictoryRoad.tx", "p7.3b")
    sp_filenames = [
        "p8.3d",
        "p9.3f",
        "p10.3h"
    ]
    func_map['sp'] = helpers.equal_split_helper('VictoryRoad.sp', sp_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "victroad.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    
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
    func_map['audiocpu'] = helpers.equal_split_helper('ASOArmoredScrumObject.2.z80', audiocpu_filenames)
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
    logger.info("Processing ASO common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    # ASO
    func_map = {}
    maincpu_filenames = [
        "p1.8d",
        "p2.7d",
        "p3.5d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('ASOArmoredScrumObject.0.z80', maincpu_filenames)
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
    func_map['maincpu'] = helpers.equal_split_helper('ASOArmoredScrumObject.b.0.z80', maincpu_filenames)
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
    func_map['maincpu'] = helpers.equal_split_helper('ASOArmoredScrumObject.c.0.z80', maincpu_filenames)
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
    mame_name = "athena.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_ikari(bundle_contents):
    '''Extract Ikari Warriors'''
    print("NYI")
    out_files = []
    for key, value in bundle_contents.items():
        if key.startswith("IkariWarriors"):
            print(f'{key}: {len(value)}')

    # Ikari Common
    func_map = {}
    sp32_filenames = [
        "p11.4m",
        "p14.2m",
        "p12.4p",
        "p15.2p",
        "p13.4r",
        "p16.2r"
    ]
    func_map['sp32'] = helpers.equal_split_helper('IkariWarriors.sp32', sp32_filenames)
    logger.info("Processing Ikari common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # Ikari US Common
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("IkariWarriors.tx", "p7.3b")
    sp_filenames = [
        "p8.3d",
        "p9.3f",
        "p10.3h"
    ]
    func_map['sp'] = helpers.equal_split_helper('IkariWarriors.sp', sp_filenames)
    bg_filenames = [
        "p17.4d",
        "p18.2d",
        "p19.4b",
        "p20.2b"
    ]
    func_map['bg'] = helpers.equal_split_helper('IkariWarriors.bg', bg_filenames)
    logger.info("Processing Ikari US common files...")
    us_common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # Ikari Sub Common
    func_map = {}
    sub_file_map = {
        "p3.8l": 0x4000,
        "p4.8k": 0x8000
    }
    func_map['audiocpu'] = helpers.custom_split_helper('IkariWarriors.a.1.z80', sub_file_map)
    logger.info("Processing Ikari Sub common files...")
    sub_common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # Ikari AudioCPU Common
    func_map = {}
    audiocpu_file_map = {
        "p5.6e": 0x4000,
        "p6.6f": 0x8000
    }
    func_map['audiocpu'] = helpers.custom_split_helper('IkariWarriors.a.2.z80', audiocpu_file_map)
    logger.info("Processing Ikari AudioCPU Common files...")
    audiocpu_common_file_map = helpers.process_rom_files(bundle_contents, func_map)
    
    # IKARIA
    func_map = {}
    maincpu_file_map = {
        "p1.4l": 0x4000,
        "p2.4k": 0x8000
    }
    func_map['maincpu'] = helpers.custom_split_helper('IkariWarriors.a.0.z80', maincpu_file_map)
    func_map['sub'] = helpers.existing_files_helper(sub_common_file_map)
    func_map['audiocpu'] = helpers.existing_files_helper(audiocpu_common_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['us_common'] = helpers.existing_files_helper(us_common_file_map)
    mame_name = "ikaria.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    

    # IKARIJP
    func_map = {}
    maincpu_file_map = {
        "p1.4l": 0x4000,
        "p2.4k": 0x8000
    }
    func_map['maincpu'] = helpers.custom_split_helper('IkariWarriors.j.0.z80', maincpu_file_map)
    sub_file_map = {
        "p3.8l": 0x4000,
        "p4.8k": 0x8000
    }
    func_map['sub'] = helpers.custom_split_helper('IkariWarriors.j.1.z80', sub_file_map)
    func_map['audiocpu'] = helpers.existing_files_helper(audiocpu_common_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['tx'] = helpers.name_file_helper("IkariWarriors.j.tx", "p7.3b")
    sp_filenames = [
        "p8.3d",
        "p9.3f",
        "p10.3h"
    ]
    func_map['sp'] = helpers.equal_split_helper('IkariWarriors.j.sp', sp_filenames)
    bg_filenames = [
        "p17.4d",
        "p18.2d",
        "p19.4b",
        "p20.2b"
    ]
    func_map['bg'] = helpers.equal_split_helper('IkariWarriors.j.bg', bg_filenames)
    mame_name = "ikarijp.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # IKARI
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("IkariWarriors.0.z80", "1.4p")
    func_map['sub'] = helpers.name_file_helper("IkariWarriors.1.z80", "2.8p")
    func_map['audiocpu'] = helpers.name_file_helper("IkariWarriors.2.z80", "3.7k")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['us_common'] = helpers.existing_files_helper(us_common_file_map)
    mame_name = "ikari.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # IKARINC
    func_map = {}
    maincpu_file_map = {
        "p1.4l": 0x4000,
        "p2.4k": 0x8000
    }
    func_map['maincpu'] = helpers.custom_split_helper('IkariWarriors.nc.0.z80', maincpu_file_map)
    func_map['sub'] = helpers.existing_files_helper(sub_common_file_map)
    func_map['audiocpu'] = helpers.existing_files_helper(audiocpu_common_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['us_common'] = helpers.existing_files_helper(us_common_file_map)
    mame_name = "ikarinc.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")


    return out_files

def extract_guerilla(bundle_contents):
    '''Extract Guerilla Wars'''
    print("NYI")
    out_files = []
    for key, value in bundle_contents.items():
        if key.startswith("GuerillaWar"):
            print(f'{key}: {len(value)}')

    # GWAR Common
    func_map = {}
    sp_filenames = [
        "gw6.2j",
        "7.2l",
        "gw8.2m",
        "gw9.2p"
    ]
    func_map['sp'] = helpers.equal_split_helper('GuerillaWar.sp', sp_filenames)
    sp32_filenames = [
        "16.2ab",
        "17.2ad",
        "14.2y",
        "15.2aa",
        "12.2v",
        "13.2w",
        "10.2s",
        "11.2t"
    ]
    func_map['sp32'] = helpers.equal_split_helper('GuerillaWar.sp32', sp32_filenames)
    bg_filenames = [
        "18.8x",
        "19.8z",
        "gw20.8aa",
        "21.8ac"
    ]
    func_map['bg'] = helpers.equal_split_helper('GuerillaWar.bg', bg_filenames)
    func_map['adpcm'] = helpers.name_file_helper("GuerillaWar.adpcm", "4.2j")
    logger.info("Processing GWAR common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    # GWAR Audio Common
    func_map = {}
    func_map['sub'] = helpers.name_file_helper("GuerillaWar.1.z80", "2.6g")
    func_map['audiocpu'] = helpers.name_file_helper("GuerillaWar.2.z80", "3.7g")
    logger.info("Processing GWAR audio common files...")
    audio_common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # GWAR
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.tx", "gw5.8p")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.0.z80", "1.2g")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['audio'] = helpers.existing_files_helper(audio_common_file_map)
    mame_name = "gwar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # # GWARA
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.tx", "gv5.3a")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.a.0.z80", "gv3_1.4p")
    func_map['sub'] = helpers.name_file_helper("GuerillaWar.a.1.z80", "gv4.8p")
    func_map['audiocpu'] = helpers.name_file_helper("GuerillaWar.a.2.z80", "gv2.7k")
    func_map['common'] = helpers.common_rename_helper(common_file_map, {
        "4.2j": "gv1.5g",
        "gw6.2j": "gv9.3g",
        "7.2l": "gv8.3e",
        "gw8.2m": "gv7.3d",
        "gw9.2p": "gv6.3b",
        "16.2ab": "gv14.8l",
        "17.2ad": "gv15.8n",
        "14.2y": "gv16.8p",
        "15.2aa": "gv17.8s",
        "12.2v": "gv18.7p",
        "13.2w": "gv19.7s",
        "10.2s": "gv20.8j",
        "11.2t": "gv21.8k",
        "18.8x": "gv13.2a",
        "19.8z": "gv12.2b",
        "gw20.8aa": "gv11.2d",
        "21.8ac": "gv10.2e"
    })
    mame_name = "gwara.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # GWARB
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.tx", "gv5.3a")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.b.0.z80", "g01")
    func_map['audio'] = helpers.common_rename_helper(audio_common_file_map, {
        "2.6g": "g02",
        "3.7g": "g03"
    })
    func_map['common'] = helpers.common_rename_helper(common_file_map, {
        "4.2j": "gv1.5g",
        "gw6.2j": "gv9.3g",
        "7.2l": "gv8.3e",
        "gw8.2m": "gv7.3d",
        "gw9.2p": "gv6.3b",
        "16.2ab": "gv14.8l",
        "17.2ad": "gv15.8n",
        "14.2y": "gv16.8p",
        "15.2aa": "gv17.8s",
        "12.2v": "gv18.7p",
        "13.2w": "gv19.7s",
        "10.2s": "gv20.8j",
        "11.2t": "gv21.8k",
        "18.8x": "gv13.2a",
        "19.8z": "gv12.2b",
        "gw20.8aa": "gv11.2d",
        "21.8ac": "gv10.2e"
    })
    mame_name = "gwarb.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # GWARJ
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.j.tx", "gw5.8p")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.j.0.z80", "1.2g")
    func_map['audio'] = helpers.existing_files_helper(audio_common_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "gwarj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_psycho(bundle_contents):
    '''Extract Psycho Soldier'''
    print("NYI")
    out_files = []

    # PSYCHO Common
    func_map = {}
    func_map['sub'] = helpers.name_file_helper("PsychoSoldier.1.z80", "ps6.8m")
    func_map['tx'] = helpers.name_file_helper("PsychoSoldier.tx", "ps8.3a")
    bg_filenames = [
        "ps16.1f",
        "ps15.1d",
        "ps14.1c",
        "ps13.1a"
    ]
    func_map['bg'] = helpers.equal_split_helper('PsychoSoldier.bg', bg_filenames)
    sp_filenames = [
        "ps12.3g",
        "ps11.3e",
        "ps10.3c",
        "ps9.3b"
    ]
    func_map['sp'] = helpers.equal_split_helper('PsychoSoldier.sp', sp_filenames)
    sp32_filenames = [
        "ps17.10f",
        "ps18.10h",
        "ps19.10j",
        "ps20.10l",
        "ps21.10m",
        "ps22.10n",
        "ps23.10r",
        "ps24.10s"
    ]
    func_map['sp32'] = helpers.equal_split_helper('PsychoSoldier.sp32', sp32_filenames)
    logger.info("Processing Psycho Soldier common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    # PSYCHOS
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("PsychoSoldier.0.z80", "ps7.4m")
    func_map['sub'] = helpers.name_file_helper("PsychoSoldier.2.z80", "ps5.6j")
    adpcm_filenames = [
        "ps1.5b",
        "ps2.5c",
        "ps3.5d",
        "ps4.5f"
    ]
    func_map['adpcm'] = helpers.equal_split_helper('PsychoSoldier.adpcm', adpcm_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "psychos.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # PSYCHOSJ
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("PsychoSoldier.j.0.z80", "ps7.4m")
    func_map['sub'] = helpers.name_file_helper("PsychoSoldier.j.2.z80", "ps5.6j")
    adpcm_filenames = [
        "ps1.5b",
        "ps2.5c",
        "ps3.5d",
        "ps4.5f"
    ]
    func_map['adpcm'] = helpers.equal_split_helper('PsychoSoldier.adpcm', adpcm_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "psychosj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def extract_bermuda(bundle_contents):
    '''Extract Bermuda Triangle / World Wars'''
    print("NYI")
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
    logger.info("Processing World Wars common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # WORLDWAR
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("WorldWars.0.z80", "ww4.4p")
    func_map['sub'] = helpers.name_file_helper("WorldWars.1.z80", "ww5.8p")
    func_map['audiocpu'] = helpers.name_file_helper("WorldWars.2.z80", "ww3.7k")
    func_map['tx'] = helpers.name_file_helper("WorldWars.tx", "ww6.3a")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "worldwar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # BERMUDATA
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("WorldWars.j.0.z80", "wwu4.4p")
    func_map['sub'] = helpers.name_file_helper("WorldWars.j.1.z80", "wwu5.8p")
    func_map['audiocpu'] = helpers.name_file_helper("WorldWars.j.2.z80", "wwu3.7k")
    func_map['tx'] = helpers.name_file_helper("WorldWars.j.tx", "wwu6.3a")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "bermudata.zip"
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
