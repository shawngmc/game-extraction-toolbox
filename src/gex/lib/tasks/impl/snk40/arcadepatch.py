'''Extraction code for Arcade ROMs from SNK40 Patch Bundle'''
import logging
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.snk40 import utils
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "Chopper I",
        "system": "Arcade",
        "filename": "chopperb.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Chopper I",
        "system": "Arcade",
        "filename": "legofair.zip",
        'status': 'good',
        "notes": [3]
    },
    {
        "game": "Fantasy",
        "system": "Arcade",
        "filename": "fantasyj.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Fantasy",
        "system": "Arcade",
        "filename": "fantasyu.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Time Soldiers",
        "system": "Arcade",
        "filename": "btlfield.zip",
        'status': 'good',
        "notes": [3]
    },
    {
        "game": "Time Soldiers",
        "system": "Arcade",
        "filename": "timesold.zip",
        'status': 'good',
        "notes": [3]
    },
    {
        "game": "Munch Mobile (Joyful Road)",
        "system": "Arcade",
        "filename": "mnchmobl.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Munch Mobile (Joyful Road)",
        "system": "Arcade",
        "filename": "joyfulr.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Sasuke vs. Commander",
        "system": "Arcade",
        "filename": "sasuke.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Ozma Wars",
        "system": "Arcade",
        "filename": "ozmawars.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Paddle Mania",
        "system": "Arcade",
        "filename": "paddlema.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Bermuda Triangle",
        "system": "Arcade",
        "filename": "bermudata.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "World Wars",
        "system": "Arcade",
        "filename": "worldwar.zip",
        "status": "playable",
        "notes": [2]
    },
    {
        "game": "MarvinsMaze",
        "system": "Arcade",
        "filename": "marvins.zip",
        'status': 'good',
        "notes": []
    }
]

def extract(bundle_contents):
    '''Extract Arcade ROMs from patch bundle'''
    out_files = []
    contents = bundle_contents['patch']
    out_files.extend(_handle_chopper(contents))
    out_files.extend(_handle_fantasy(contents))
    out_files.extend(_handle_timesoldiers(contents))
    out_files.extend(_handle_munchmobile(contents))
    out_files.extend(_handle_sasuke(contents))
    out_files.extend(_handle_ozmawars(contents))
    out_files.extend(_handle_paddlemania(contents))
    out_files.extend(_handle_bermuda(contents))
    out_files.extend(_handle_worldwars(contents))
    out_files.extend(_handle_marvin(contents))
    return out_files

def _handle_chopper(bundle_contents):
    out_files = []

    # CHOPPERB
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("chopper.maincpu", "kk1.8g")
    func_map['sub'] = helpers.name_file_helper("chopper.sub", "kk4.6g")
    prom_file_names = [
        "1.9w",
        "3.9u",
        "2.9v"
    ]
    func_map['prom'] = helpers.equal_split_helper("chopper.proms", prom_file_names)
    func_map['audiocpu'] = helpers.name_file_helper("chopper.audiocpu", "kk3.3d")
    func_map['tx'] = helpers.name_file_helper("chopper.tx_tiles", "kk5.8p")
    bg_file_names = [
        "kk10.8y",
        "kk11.8z",
        "kk12.8ab",
        "kk13.8ac"
    ]
    func_map['bg'] = helpers.equal_split_helper("chopper.bg_tiles", bg_file_names)
    sp16_file_names = [
        "kk9.3k",
        "kk8.3l",
        "kk7.3n",
        "kk6.3p"
    ]
    func_map['sp16'] = helpers.equal_split_helper("chopper.sp16_tiles", sp16_file_names)
    sp32_file_names = [
        "kk18.3ab",
        "kk19.2ad",
        "kk20.3y",
        "kk21.3aa",
        "kk14.3v",
        "kk15.3x",
        "kk16.3s",
        "kk17.3t"
    ]
    func_map['sp32'] = helpers.equal_split_helper("chopper.sp32_tiles", sp32_file_names)
    func_map['ym2'] = helpers.name_file_helper("chopper.ym2", "kk2.3j")
    func_map['plds'] = helpers.name_file_helper("chopper.plds", "p-a1.2c")
    out_files.append(utils.build_snk_rom("chopperb.zip", bundle_contents, func_map))

    # LEGOFAIR
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("legofair.maincpu", "kk1.4m")
    func_map['sub'] = helpers.name_file_helper("legofair.sub", "kk4.8m")
    prom_file_names = [
        "1.1k",
        "2.1l",
        "3.2k"
    ]
    func_map['prom'] = helpers.equal_split_helper("chopper.proms", prom_file_names)
    func_map['audiocpu'] = helpers.name_file_helper("chopper.audiocpu", "kk3.6j")
    func_map['tx'] = helpers.name_file_helper("chopper.tx_tiles", "kk5.3a")
    bg_file_names = [
        "kk10.1a",
        "kk11.1b",
        "kk12.1d",
        "kk13.1e"
    ]
    func_map['bg'] = helpers.equal_split_helper("chopper.bg_tiles", bg_file_names)
    sp16_file_names = [
        "kk9.3g",
        "kk8.3e",
        "kk7.3d",
        "kk6.3b"
    ]
    func_map['sp16'] = helpers.equal_split_helper("chopper.sp16_tiles", sp16_file_names)
    sp32_file_names = [
        "kk18.8m",
        "kk19.8n",
        "kk20.8p",
        "kk21.8s",
        "kk14.7p",
        "kk15.7s",
        "kk16.8j",
        "kk17.8k"
    ]
    func_map['sp32'] = helpers.equal_split_helper("chopper.sp32_tiles", sp32_file_names)
    func_map['ym2'] = helpers.name_file_helper("chopper.ym2", "kk2.5b")
    func_map['plds'] = helpers.name_file_helper("chopper.plds", "p-a1.8b")
    ph_files = {
        'horizon.6h': 0x400,
        'vertical.7h': 0x400
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("legofair.zip", bundle_contents, func_map))

    return out_files

def _handle_fantasy(bundle_contents):
    out_files = []
    # COMMON
    func_map = {}
    gfx1_file_names = [
        "fs10ic50.bin",
        "fs11ic51.bin"
    ]
    func_map['gfx1'] = helpers.equal_split_helper("fantasyu.gfx1", gfx1_file_names)
    snk6502_file_names = [
        "fs_b_51.bin",
        "fs_a_52.bin",
        "fs_c_53.bin"
    ]
    func_map['snk6502'] = helpers.equal_split_helper("fantasyu.snk6502", snk6502_file_names)
    speech_file_names = [
        "fs_d_7.bin",
        "fs_e_8.bin",
        "fs_f_11.bin"
    ]
    func_map['speech'] = helpers.equal_split_helper("fantasyu.speech", speech_file_names)
    logger.info("Processing fantasy common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # FANTASYJ
    func_map = {}
    prom_file_names = [
        "prom-8.bpr",
        "prom-7.bpr"
    ]
    func_map['prom'] = helpers.equal_split_helper("fantasyj.proms", prom_file_names)
    maincpu_file_names = [
        "fs5jic12.bin",
        "fs1jic7.bin",
        "fs2jic8.bin",
        "fs3jic9.bin",
        "fs4jic10.bin",
        "fs6jic14.bin",
        "fs7jic15.bin",
        "fs8jic16.bin",
        "fs9jic17.bin"
    ]
    func_map['maincpu'] = helpers.equal_split_helper("fantasyj.maincpu", maincpu_file_names)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("fantasyj.zip", bundle_contents, func_map))

    # FANTASYU
    func_map = {}
    prom_file_names = [
        "fantasy.ic7",
        "fantasy.ic6"
    ]
    func_map['prom'] = helpers.equal_split_helper("fantasyu.proms", prom_file_names)
    maincpu_file_names = [
        "ic12.cpu",
        "ic07.cpu",
        "ic08.cpu",
        "ic09.cpu",
        "ic10.cpu",
        "ic14.cpu",
        "ic15.cpu",
        "ic16.cpu",
        "ic17.cpu"
    ]
    func_map['maincpu'] = helpers.equal_split_helper("fantasyu.maincpu", maincpu_file_names)

    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("fantasyu.zip", bundle_contents, func_map))

    return out_files

def _handle_timesoldiers(bundle_contents):
    out_files = []

    # Common
    func_map = {}
    z80_file_names = [
        "bf.7",
        "bf.8",
        "bf.9"
    ]
    func_map['z80'] = helpers.equal_split_helper("TimeSoldiers.z80", z80_file_names)
    gfx2_file_names = [
        "bf.10",
        "bf.14",
        "bf.18",
        "bf.11",
        "bf.15",
        "bf.19",
        "bf.12",
        "bf.16",
        "bf.20",
        "bf.13",
        "bf.17",
        "bf.21"
    ]
    def timesold_gfx2(in_file_name, filenames):
        def process(in_files):
            contents = in_files[in_file_name]
            contents = transforms.splice_out(contents, start=15*131072, length=131072)
            contents = transforms.splice_out(contents, start=11*131072, length=131072)
            contents = transforms.splice_out(contents, start=7*131072, length=131072)
            contents = transforms.splice_out(contents, start=3*131072, length=131072)
            chunks = transforms.equal_split(contents, len(filenames))
            return dict(zip(filenames, chunks))
        return process
    func_map['gfx2'] = timesold_gfx2("TimeSoldiers.gfx2.rom", gfx2_file_names)

    logger.info("Processing timesold common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)


    def timesold_maincpu_common(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, 2)
            chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return maincpu

    # TIMESOLD
    func_map = {}
    maincpu_file_names = [
        "bf.3",
        "bf.4",
        "bf.1",
        "bf.2"
    ]
    func_map['maincpu'] = timesold_maincpu_common("TimeSoldiers.3.68k", maincpu_file_names)
    gfx1_file_names = [
        "bf.6",
        "bf.5"
    ]
    func_map['gfx1'] = helpers.deinterleave_helper("TimeSoldiers.u.gfx1.rom",
        gfx1_file_names, num_ways=2, word_size=1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("timesold.zip", bundle_contents, func_map))

    # BTLFIELD
    func_map = {}
    maincpu_file_names = [
        "bfv1_03.bin",
        "bfv1_04.bin",
        "bf.1",
        "bf.2"
    ]
    func_map['maincpu'] = timesold_maincpu_common("TimeSoldiers.j.68k", maincpu_file_names)
    gfx1_file_names = [
        "bfv1_06.bin",
        "bfv1_05.bin"
    ]
    func_map['gfx1'] = helpers.deinterleave_helper("TimeSoldiers.j.gfx1.rom",
        gfx1_file_names, num_ways=2, word_size=1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("btlfield.zip", bundle_contents, func_map))

    return out_files

def _handle_munchmobile(bundle_contents):
    out_files = []

    # Common
    func_map = {}
    func_map['audiocpu'] = helpers.name_file_helper("joyfulr.audiocpu", "mu.2j")
    func_map['proms'] = helpers.name_file_helper("joyfulr.proms", "a2001.clr")
    gfx1_file_names = [
        "s1.10a",
        "s2.10b"
    ]
    func_map['gfx1'] = helpers.equal_split_helper("joyfulr.gfx1", gfx1_file_names)
    gfx2_file_names = [
        "b1.2c",
        "b2.2b"
    ]
    func_map['gfx2'] = helpers.equal_split_helper("joyfulr.gfx2", gfx2_file_names)
    func_map['gfx4'] = helpers.name_file_helper("joyfulr.gfx4", "h")

    logger.info("Processing joyfulr common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # JOYFULR
    func_map = {}
    maincpu_file_names = [
        "m1j.10e",
        "m2j.10d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper("joyfulr.maincpu", maincpu_file_names)
    gfx3_file_names = [
        "f1j.1g",
        "f2j.3g",
        "f3j.5g"
    ]
    func_map['gfx3'] = helpers.equal_split_helper("joyfulr.gfx3", gfx3_file_names)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("joyfulr.zip", bundle_contents, func_map))

    # MNCHMOBL
    func_map = {}
    maincpu_file_names = [
        "m1.10e",
        "m2.10d"
    ]
    func_map['maincpu'] = helpers.equal_split_helper("mnchmobl.maincpu", maincpu_file_names)
    gfx3_file_names = [
        "f1.1g",
        "f2.3g",
        "f3.5g"
    ]
    func_map['gfx3'] = helpers.equal_split_helper("mnchmobl.gfx3", gfx3_file_names)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("mnchmobl.zip", bundle_contents, func_map))

    return out_files

def _handle_sasuke(bundle_contents):
    out_files = []

    func_map = {}
    maincpu_file_names = [
        "sc1",
        "sc2",
        "sc3",
        "sc4",
        "sc5",
        "sc6",
        "sc7",
        "sc8",
        "sc9",
        "sc10"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('sasuke.maincpu', maincpu_file_names)
    gfx1_file_names = [
        "mcs_c",
        "mcs_d"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('sasuke.gfx1', gfx1_file_names)
    func_map['proms'] = helpers.name_file_helper("sasuke.proms", "sasuke.clr")
    func_map['snk6502'] = helpers.name_file_helper("sasuke.snk6502", "sc11")
    out_files.append(utils.build_snk_rom("sasuke.zip", bundle_contents, func_map))

    return out_files

def _handle_ozmawars(bundle_contents):
    out_files = []

    func_map = {}
    maincpu_file_names = [
        "mw01",
        "mw02",
        "mw03",
        "mw04",
        "mw05",
        "mw06"
    ]
    def ozmawars_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            contents = transforms.splice_out(contents, start = 8192, end = 16384)
            chunks = transforms.equal_split(contents, len(filenames))
            return dict(zip(filenames, chunks))
        return maincpu
    func_map['gfx2'] = ozmawars_maincpu("ozmawars.maincpu", maincpu_file_names)
    prom_file_names = [
        "01.1",
        "02.2"
    ]
    func_map['prom'] = helpers.equal_split_helper('moonbase.proms', prom_file_names)
    out_files.append(utils.build_snk_rom("ozmawars.zip", bundle_contents, func_map))

    return out_files

def _handle_paddlemania(bundle_contents):
    func_map = {}
    out_files = []

    prom_file_map = {
        "padlem.a": 0x100,
        "padlem.b": 0x100,
        "padlem.c": 0x100,
        "padlem.17j": 0x400,
        "padlem.16j": 0x400
    }
    func_map['prom'] = helpers.custom_split_helper('PaddleMania.proms.rom', prom_file_map)
    func_map['audiocpu'] = helpers.name_file_helper('PaddleMania.z80', 'padlem.18c')
    func_map['color_prom'] = helpers.name_file_helper('PaddleMania.clut.rom', 'padlem.18n')
    maincpu_file_names = [
        "padlem.6g",
        "padlem.3g",
        "padlem.6h",
        "padlem.3h"
    ]
    def padlem_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return maincpu
    func_map['maincpu'] = padlem_maincpu('PaddleMania.1.68k', maincpu_file_names)
    gfx1_file_names = [
        "padlem.9m",
        "padlem.16m",
        "padlem.9n",
        "padlem.16n",
        "padlem.6m",
        "padlem.13m",
        "padlem.6n",
        "padlem.13n"
    ]
    func_map['gfx1'] = padlem_maincpu('PaddleMania.gfx1.rom', gfx1_file_names)
    out_files.append(utils.build_snk_rom("paddlema.zip", bundle_contents, func_map))

    return out_files


def _handle_bermuda(bundle_contents):
    '''Extract Bermuda Triangle / World Wars'''
    out_files = []

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
        'horizon.5h': 0x400,
        'vertical.7h': 0x400
    }
    func_map['ph'] = helpers.placeholder_helper(ph_files)
    logger.info("Processing World Wars common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # BERMUDATA
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("WorldWars.j.0.z80", "wwu4.4p")
    func_map['sub'] = helpers.name_file_helper("WorldWars.j.1.z80", "wwu5.8p")
    func_map['audiocpu'] = helpers.name_file_helper("WorldWars.j.2.z80", "wwu3.7k")
    func_map['tx'] = helpers.name_file_helper("WorldWars.j.tx", "wwu6.3a")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    pal_filenames = [
        "u2bt.2l",
        "u1bt.1k",
        "u3bt.1l"
    ]
    func_map['pal'] = utils.simple_palette_helper('WorldWars.j.pal', pal_filenames)
    out_files.append(utils.build_snk_rom("bermudata.zip", bundle_contents, func_map))

    return out_files


def _handle_worldwars(bundle_contents):
    '''Extract World Wars'''
    out_files = []
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
    adpcm_filenames = [
        "p4.5e",
        "p5.5g"
    ]
    func_map['adpcm'] = helpers.equal_split_helper('WorldWars.adpcm', adpcm_filenames)
    mame_name = "worldwar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    return out_files

def _handle_marvin(bundle_contents):
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
    pals_filenames = [
        "marvmaze.j2",
        "marvmaze.j1",
        "marvmaze.j3"
    ]
    func_map['pal'] = utils.palette_rebuild_helper(pals_filenames, 'MarvinsMaze.pal')
    out_files.append(utils.build_snk_rom("marvins.zip", bundle_contents, func_map))

    return out_files
