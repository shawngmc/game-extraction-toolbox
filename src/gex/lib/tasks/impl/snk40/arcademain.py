'''Extraction code for Arcade ROMs from SNK40 Main Bundle'''
import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.tasks.impl.snk40 import utils

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "aso.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "alphamis.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "arian.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "TNKIII",
        "system": "Arcade",
        "filename": "tnk3.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "TNKIII (J)",
        "system": "Arcade",
        "filename": "tnk3j.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Athena",
        "system": "Arcade",
        "filename": "athena.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "gensitou.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "prehisle.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "prehisleu.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsm.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsm1.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsmj.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsmw.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3j.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3k.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3u.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "Arcade",
        "filename": "pow.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "Arcade",
        "filename": "powj.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguard.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguardc.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguardj.zip",
        'status': 'good',
        "notes": []
    },
    {
        "game": "Guerilla War",
        "system": "Arcade",
        "filename": "gwar.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Guerilla War (A)",
        "system": "Arcade",
        "filename": "gwara.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Guerilla War (B)",
        "system": "Arcade",
        "filename": "gwarb.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Guevara (Guerilla War (J))",
        "system": "Arcade",
        "filename": "gwarj.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Psycho Soldier",
        "system": "Arcade",
        "filename": "psychos.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Psycho Soldier (J)",
        "system": "Arcade",
        "filename": "psychosj.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Ikari I",
        "system": "Arcade",
        "filename": "ikari.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Ikari I (US Alt.)",
        "system": "Arcade",
        "filename": "ikaria.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Ikari I (J, No Continues)",
        "system": "Arcade",
        "filename": "ikarijp.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Ikari I (No Continues)",
        "system": "Arcade",
        "filename": "ikarinc.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Ikari 2 Victory Road",
        "system": "Arcade",
        "filename": "victroad.zip",
        'status': 'playable',
        "notes": [2]
    },
    {
        "game": "Dogou Souken (Ikari 2 Victory Road (J))",
        "system": "Arcade",
        "filename": "dogosoke.zip",
        'status': 'playable',
        "notes": [2]
    }
]

def extract(bundle_contents):
    '''Extract Arcade ROMs from main bundle'''
    out_files = []
    contents = bundle_contents['main']
    out_files.extend(_handle_prehisle(contents))
    out_files.extend(_handle_streetsm(contents))
    out_files.extend(_handle_ikari3(contents))
    out_files.extend(_handle_vanguard(contents))
    out_files.extend(_handle_pow(contents))
    out_files.extend(_handle_psycho(contents))
    out_files.extend(_handle_victoryroad(contents, bundle_contents['patch']))
    out_files.extend(_handle_ikari(contents))
    out_files.extend(_handle_guerilla(contents))
    out_files.extend(_handle_tnk3(contents))
    out_files.extend(_handle_aso(contents))
    out_files.extend(_handle_athena(contents))
    return out_files

def _handle_prehisle(bundle_contents):
    # PREHISLE Common
    func_map = {}
    out_files = []
    func_map['z80'] = helpers.name_file_helper("PrehistoricIsleIn1930.z80", "gt1.1")
    func_map['tx'] = helpers.name_file_helper("PrehistoricIsleIn1930.w.alpha.rom", "gt15.b15")
    func_map['bgrom'] = helpers.name_file_helper("PrehistoricIsleIn1930.bg.rom", "pi8914.b14")
    func_map['fgrom'] = helpers.name_file_helper("PrehistoricIsleIn1930.fg.rom", "pi8916.h16")
    sprite_file_map = {
        "pi8910.k14": 524288,
        "gt5.5": 131072
    }
    func_map['sprites'] = helpers.custom_split_helper(
        "PrehistoricIsleIn1930.sprites.rom", sprite_file_map)
    func_map['bgmap'] = helpers.name_file_helper("PrehistoricIsleIn1930.bg.map", "gt11.11")
    func_map['samples'] = helpers.name_file_helper("PrehistoricIsleIn1930.samples", "gt4.4")
    logger.info("Processing PREHISLE common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    def prehisle_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return maincpu

    # GENSITOU / PREHISLEJ
    func_map = {}
    maincpu_filenames = [
        "gt-j2.2h",
        "gt-j3.3h"
    ]
    func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.j.68k', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("gensitou.zip", bundle_contents, func_map))

    # PREHISLEU
    func_map = {}
    maincpu_filenames = [
        "gt-u2.2h",
        "gt-u3.3h"
    ]
    func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.u.68k', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("prehisleu.zip", bundle_contents, func_map))

    # PREHISLE
    func_map = {}
    maincpu_filenames = [
        "gt-e2.2h",
        "gt-e3.3h"
    ]
    func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.w.68k', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("prehisle.zip", bundle_contents, func_map))
    return out_files

def _handle_streetsm(bundle_contents):
    # STREETS Common
    func_map = {}
    out_files = []
    func_map['soundcpu'] = helpers.name_file_helper("streetsm.soundcpu", "s2-5.16c")
    func_map['upd'] = helpers.name_file_helper("streetsm.upd", "s2-6.18d")
    def streets_gfx2(in_file_name, filenames):
        def gfx2(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, 7)
            del chunks[3] # Middle element is junk
            return dict(zip(filenames, chunks))
        return gfx2
    gfx2_filenames = [
        "stsmart.900",
        "stsmart.902",
        "stsmart.904",
        "stsmart.901",
        "stsmart.903",
        "stsmart.905",
    ]
    func_map['gfx2'] = streets_gfx2('streetsm.gfx2', gfx2_filenames)

    logger.info("Processing STREETS common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # STREETS1 GFX Common
    func_map = {}
    gfx1_filenames = [
        "s2-7.15l",
        "s2-8.15m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('streetsm1.gfx1', gfx1_filenames)
    logger.info("Processing STREETS1 GFX common files...")
    gfx1_file_map = helpers.process_rom_files(bundle_contents, func_map)

    def streets_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return maincpu

    # STREETSM
    func_map = {}
    maincpu_filenames = [
        "s2-1ver2.14h",
        "s2-2ver2.14k"
    ]
    func_map['maincpu'] = streets_maincpu('streetsm.maincpu', maincpu_filenames)
    gfx1_filenames = [
        "s2-9.25l",
        "s2-10.25m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('streetsm.gfx1', gfx1_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("streetsm.zip", bundle_contents, func_map))

    # STREETSM1
    func_map = {}
    maincpu_filenames = [
        "s2-1ver1.9c",
        "s2-2ver1.10c"
    ]
    func_map['maincpu'] = streets_maincpu('streetsm1.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("streetsm1.zip", bundle_contents, func_map))

    # STREETSMJ
    func_map = {}
    maincpu_filenames = [
        "s2v1j_01.bin",
        "s2v1j_02.bin"
    ]
    func_map['maincpu'] = streets_maincpu('streetsmj.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("streetsmj.zip", bundle_contents, func_map))

    # STREETSMW
    func_map = {}
    maincpu_filenames = [
        "s-smart1.bin",
        "s-smart2.bin"
    ]
    func_map['maincpu'] = streets_maincpu('streetsmw.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("streetsmw.zip", bundle_contents, func_map))
    return out_files

def _handle_ikari3(bundle_contents):
    # IKARI3 Common
    func_map = {}
    out_files = []
    func_map['upd'] = helpers.name_file_helper("ikari3.upd", "ik3-6.18e")
    user_filenames = [
        "ik3-1.c8",
        "ik3-4.c12"
    ]
    func_map['user'] = helpers.deinterleave_helper('ikari3.user1',
        user_filenames, num_ways=2, word_size=1)

    logger.info("Processing IKARI3 common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # IKARI3 GFX1 Common
    func_map = {}
    gfx1_filenames = [
        "ik3-7.16l",
        "ik3-8.16m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('ikari3.gfx1', gfx1_filenames)
    logger.info("Processing IKARI3 GFX1 common files...")
    gfx1_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # IKARI3 GFX2 Common
    func_map = {}
    gfx2_filenames = [
        "ik3-23.bin",
        "ik3-13.bin",
        "ik3-22.bin",
        "ik3-12.bin",
        "ik3-21.bin",
        "ik3-11.bin",
        "ik3-20.bin",
        "ik3-10.bin",
        "ik3-19.bin",
        "ik3-9.bin",
        "ik3-14.bin",
        "ik3-24.bin",
        "ik3-15.bin",
        "ik3-25.bin",
        "ik3-16.bin",
        "ik3-26.bin",
        "ik3-17.bin",
        "ik3-27.bin",
        "ik3-18.bin",
        "ik3-28.bin"
    ]
    def ikari3_gfx2_common(in_file_name, filenames):
        def gfx2(in_files):
            contents = in_files[in_file_name]
            contents = transforms.splice_out(contents, start = 1310720, end = 2097152)
            chunks = transforms.equal_split(contents, 10)
            chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return gfx2
    func_map['gfx2'] = ikari3_gfx2_common('ikari3.gfx2', gfx2_filenames)
    logger.info("Processing IKARI3 GFX2 common files...")
    gfx2_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # IKARI3
    func_map = {}
    maincpu_filenames = [
        "ik3-2-ver1.c10",
        "ik3-3-ver1.c9"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('ikari3.maincpu',
        maincpu_filenames, num_ways=2, word_size=1)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
    func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("ikari3.zip", bundle_contents, func_map))

    # IKARI3J
    func_map = {}
    maincpu_filenames = [
        "ik3-2-j.c10",
        "ik3-3-j.c9"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('ikari3j.maincpu',
        maincpu_filenames, num_ways=2, word_size=1)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
    func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("ikari3j.zip", bundle_contents, func_map))

    # IKARI3K
    func_map = {}
    maincpu_filenames = [
        "ik3-2k.c10",
        "ik3-3k.c9"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('ikari3k.maincpu',
        maincpu_filenames, num_ways=2, word_size=1)
    gfx1_filenames = [
        "ik3-7k.16l",
        "ik3-8k.16m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('ikari3k.gfx1', gfx1_filenames)
    gfx2_filenames = [
        "ikari-880d_t53.d2",
        "ikari-880c_t54.c2",
        "ik12.d1",
        "ik11.c1",
        "ikari-880d_t52.b2",
        "ikari-880c_t51.a2",
        "ik10.b1",
        "ik9.a1",
    ]
    def ikari3k_gfx2(in_file_name, filenames):
        def gfx2(in_files):
            contents = in_files[in_file_name]
            contents = transforms.splice_out(contents, start = 1310720, end = 2097152)
            chunks = transforms.custom_split(contents,
                [1024*1024, 1024*256, 1024*1024, 1024*256])
            chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return gfx2
    func_map['gfx2'] = ikari3k_gfx2('ikari3.gfx2', gfx2_filenames)
    func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("ikari3k.zip", bundle_contents, func_map))

    # IKARI3U
    func_map = {}
    maincpu_filenames = [
        "ik3-2.c10",
        "ik3-3.c9"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('ikari3u.maincpu',
        maincpu_filenames, num_ways=2, word_size=1)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
    func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.15d")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("ikari3u.zip", bundle_contents, func_map))

    return out_files

def _handle_vanguard(bundle_contents):
    # VANGUARD Common
    func_map = {}
    out_files = []

    gfx1_filenames = [
        "sk5_ic50.bin",
        "sk5_ic51.bin"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('vanguard.gfx1', gfx1_filenames)

    prom_filenames = [
        "sk5_ic7.bin",
        "sk5_ic6.bin"
    ]
    func_map['prom'] = helpers.equal_split_helper('vanguard.proms', prom_filenames)

    snk6502_filenames = [
        "sk4_ic51.bin",
        "sk4_ic52.bin"
    ]
    func_map['snk6502'] = helpers.equal_split_helper('vanguard.snk6502', snk6502_filenames)

    speech_file_names = [
        "sk6_ic07.bin",
        "sk6_ic08.bin",
        "sk6_ic11.bin"
    ]
    def vanguard_speech(in_file_name, filenames):
        def speech(in_files):
            contents = in_files[in_file_name]
            contents = contents[16384:]
            chunks = transforms.equal_split(contents, len(filenames))
            return dict(zip(filenames, chunks))
        return speech
    func_map['speech'] = vanguard_speech("vanguard.speech", speech_file_names)
    logger.info("Processing VANGUARD common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # VANGUARD
    func_map = {}
    maincpu_filenames = [
        "sk4_ic07.bin",
        "sk4_ic08.bin",
        "sk4_ic09.bin",
        "sk4_ic10.bin",
        "sk4_ic13.bin",
        "sk4_ic14.bin",
        "sk4_ic15.bin",
        "sk4_ic16.bin"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('vanguard.maincpu', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("vanguard.zip", bundle_contents, func_map))

    # VANGUARDC
    func_map = {}
    maincpu_filenames = [
        "sk4_ic07.bin",
        "sk4_ic08.bin",
        "sk4_ic09.bin",
        "4",
        "5",
        "sk4_ic14.bin",
        "sk4_ic15.bin",
        "8"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('vanguardc.maincpu', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("vanguardc.zip", bundle_contents, func_map))

    # VANGUARDJ
    func_map = {}
    maincpu_filenames = [
        "sk4_ic07.bin",
        "sk4_ic08.bin",
        "sk4_ic09.bin",
        "vgj4ic10.bin",
        "vgj5ic13.bin",
        "sk4_ic14.bin",
        "sk4_ic15.bin",
        "sk4_ic16.bin"
    ]
    func_map['maincpu'] = helpers.equal_split_helper('vanguardj.maincpu', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("vanguardj.zip", bundle_contents, func_map))

    return out_files

def _handle_pow(bundle_contents):
    # POW Common
    func_map = {}
    out_files = []

    gfx1_filenames = [
        "dg9.l25",
        "dg10.m25"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('pow.gfx1', gfx1_filenames)

    func_map['soundcpu'] = helpers.name_file_helper('pow.soundcpu', 'dg8.e25')
    func_map['upd'] = helpers.name_file_helper('pow.upd', 'dg7.d20')
    func_map['plds'] = helpers.name_file_helper('pow.plds', 'pal20l10.a6')

    gfx2_file_names = [
        "snk88011a.1a",
        "snk88015a.2a",
        "snk88012a.1b",
        "snk88016a.2b",
        "snk88013a.1c",
        "snk88017a.2c",
        "snk88014a.1d",
        "snk88018a.2d",
        "snk88019a.3a",
        "snk88023a.4a",
        "snk88020a.3b",
        "snk88024a.4b",
        "snk88021a.3c",
        "snk88025a.4c",
        "snk88022a.3d",
        "snk88026a.4d"
    ]
    def pow_gfx2_common(in_file_name, filenames):
        def gfx2(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, 8)
            chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return gfx2
    func_map['gfx2'] = pow_gfx2_common('pow.gfx2', gfx2_file_names)
    logger.info("Processing POW common files...")
    common_file_map = helpers.process_rom_files(bundle_contents, func_map)

    # POW
    func_map = {}
    maincpu_filenames = [
        "dg1ver1.j14",
        "dg2ver1.l14"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('pow.maincpu', maincpu_filenames, 2, 1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("pow.zip", bundle_contents, func_map))

    # POWJ
    func_map = {}
    maincpu_filenames = [
        "1-2",
        "2-2"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('powj.maincpu', maincpu_filenames, 2, 1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("powj.zip", bundle_contents, func_map))

    return out_files

def _handle_victoryroad(bundle_contents, patch_contents):
    '''Extract Ikari 2 Victory Road'''
    out_files = []

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

    # VICTROAD PID Special copy from CHOPPERB
    # Missing victroad:a5004-1.6d is chopperb:p-a1.2c
    func_map = {}
    func_map['plds'] = helpers.name_file_helper("chopper.plds", "a5004-1.6d")
    logger.info("Processing Victory Road common files...")
    victroad_pid_file_map = helpers.process_rom_files(patch_contents, func_map)

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
    ph_files = {
        "1.1d": 4096,
        "1.2d": 4096
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    pal_filenames = [
        "c2.2l",
        "c1.1k",
        "c3.1l"
    ]
    func_map['pal'] = utils.simple_palette_helper('VictoryRoad.j.pal', pal_filenames)
    out_files.append(utils.build_snk_rom("dogosoke.zip", bundle_contents, func_map))

    # VICTROAD
    func_map = {}
    func_map['pid'] = helpers.existing_files_helper(victroad_pid_file_map)
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
    ph_files = {
        "1.1d": 4096,
        "1.2d": 4096,
        "a5004-4.8s": 260,
        "a6002-2.5r": 324,
        "a6002-3.2p": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    pal_filenames = [
        "c2.2l",
        "c1.1k",
        "c3.1l"
    ]
    func_map['pal'] = utils.simple_palette_helper('VictoryRoad.pal', pal_filenames)
    out_files.append(utils.build_snk_rom("victroad.zip", bundle_contents, func_map))

    return out_files

def _handle_ikari(bundle_contents):
    '''Extract Ikari Warriors'''
    out_files = []

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

    # Ikari Palette Common
    func_map = {}
    pal_filenames = [
        "2.2j",
        "1.1h",
        "3.1j"
    ]
    func_map['pal'] = utils.simple_palette_helper('IkariWarriors.pal', pal_filenames)
    logger.info("Processing Ikari Palette common files...")
    palette_common_file_map = helpers.process_rom_files(bundle_contents, func_map)

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
    func_map['palette'] = helpers.existing_files_helper(palette_common_file_map)
    ph_files = {
        "ampal16l8a-a5004-3.2n": 260,
        "ampal16l8a-a5004-4.8s": 260,
        "pal20l8a-a5004-2.6m": 324,
        "ampal16r6a-a5004-1.6d": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("ikaria.zip", bundle_contents, func_map))

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
    func_map['palette'] = helpers.existing_files_helper(palette_common_file_map)
    ph_files = {
        "ampal16l8a-a5004-3.2n": 260,
        "ampal16l8a-a5004-4.8s": 260,
        "pal20l8a-a5004-2.6m": 324,
        "ampal16r6a-a5004-1.6d": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("ikarijp.zip", bundle_contents, func_map))

    # IKARI
    func_map = {}
    func_map['maincpu'] = helpers.name_file_helper("IkariWarriors.0.z80", "1.4p")
    func_map['sub'] = helpers.name_file_helper("IkariWarriors.1.z80", "2.8p")
    func_map['audiocpu'] = helpers.name_file_helper("IkariWarriors.2.z80", "3.7k")
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['us_common'] = helpers.existing_files_helper(us_common_file_map)
    func_map['palette'] = helpers.common_rename_helper(palette_common_file_map, {
        "2.2j": "a6002-2.2l",
        "1.1h": "a6002-1.1k",
        "3.1j": "a6002-3.1l"
    })
    out_files.append(utils.build_snk_rom("ikari.zip", bundle_contents, func_map))

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
    func_map['palette'] = helpers.existing_files_helper(palette_common_file_map)
    ph_files = {
        "ampal16l8a-a5004-3.2n": 260,
        "ampal16l8a-a5004-4.8s": 260,
        "pal20l8a-a5004-2.6m": 324,
        "ampal16r6a-a5004-1.6d": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("ikarinc.zip", bundle_contents, func_map))

    return out_files

def _handle_guerilla(bundle_contents):
    '''Extract Guerilla Wars'''
    out_files = []

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

    # GWAR Palette Common
    func_map = {}
    pal_filenames = [
        '2.9v',
        '3.9w',
        '1.9u'
    ]
    func_map['pal'] = utils.simple_palette_helper('GuerillaWar.pal', pal_filenames)
    logger.info("Processing GWAR palette common files...")
    pal_common_file_map = helpers.process_rom_files(bundle_contents, func_map)

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
    func_map['pal'] = helpers.existing_files_helper(pal_common_file_map)
    ph_files = {
        'l.1x': 0x1000,
        'l.1w': 0x1000
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("gwar.zip", bundle_contents, func_map))

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
    func_map['pal'] = helpers.common_rename_helper(pal_common_file_map, {
        "3.9w": "1.1k",
        "1.9u": "2.1l",
        "2.9v": "3.2l"
    })
    ph_files = {
        'l.1x': 0x1000,
        'l.1w': 0x1000,
        'horizon.8j': 0x400,
        'vertical.8k': 0x400
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("gwara.zip", bundle_contents, func_map))

    # GWARAB
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.tx", "gv5.3a")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.b.0.z80", "gv3 ver 1.4p")
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
    func_map['pal'] = helpers.common_rename_helper(pal_common_file_map, {
        "3.9w": "1.1k",
        "1.9u": "2.1l",
        "2.9v": "3.2l"
    })
    ph_files = {
        'l.1x': 0x1000,
        'l.1w': 0x1000,
        'horizon.8j': 0x400,
        'vertical.8k': 0x400
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("gwarab.zip", bundle_contents, func_map))

    # GWARJ
    func_map = {}
    func_map['tx'] = helpers.name_file_helper("GuerillaWar.j.tx", "gw5.8p")
    func_map['maincpu'] = helpers.name_file_helper("GuerillaWar.j.0.z80", "1.2g")
    func_map['audio'] = helpers.existing_files_helper(audio_common_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    func_map['pal'] = helpers.existing_files_helper(pal_common_file_map)
    ph_files = {
        'l.1x': 0x1000,
        'l.1w': 0x1000
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    out_files.append(utils.build_snk_rom("gwarj.zip", bundle_contents, func_map))

    return out_files

def _handle_psycho(bundle_contents):
    '''Extract Psycho Soldier'''
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
    ph_files = {
        'horizon.8j': 0x400,
        'vertical.8k': 0x400
    }
    func_map['ph'] = helpers.placeholder_helper(ph_files)
    pal_filenames = [
        "psc3.1l",
        "psc1.1k",
        "psc2.2k"
    ]
    func_map['pal'] = utils.simple_palette_helper('PsychoSoldier.pal', pal_filenames)
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
    out_files.append(utils.build_snk_rom("psychos.zip", bundle_contents, func_map))

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
    func_map['adpcm'] = helpers.equal_split_helper('PsychoSoldier.j.adpcm', adpcm_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    out_files.append(utils.build_snk_rom("psychosj.zip", bundle_contents, func_map))

    return out_files

def _handle_aso(bundle_contents):
    '''Extract Armored Scrum Object'''
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
    pals_filenames = [
        "mb7122h.13f",
        "mb7122h.12f",
        "mb7122h.14f"
    ]
    func_map['pal'] = utils.palette_rebuild_helper(pals_filenames, 'ASOArmoredScrumObject.pal')
    ph_files = {
        'pal16l8a-1.bin': 260,
        'pal16l8a-2.bin': 260,
        'pal16r6a.15b': 260
    }
    func_map['ph'] = helpers.placeholder_helper(ph_files)
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
    out_files.append(utils.build_snk_rom("aso.zip", bundle_contents, func_map))

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
    out_files.append(utils.build_snk_rom("alphamis.zip", bundle_contents, func_map))

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
    out_files.append(utils.build_snk_rom("arian.zip", bundle_contents, func_map))

    return out_files

def _handle_athena(bundle_contents):
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
    pals_filenames = [
        "2.1b",
        "3.2c",
        "1.1c"
    ]
    func_map['pal'] = utils.palette_rebuild_helper(pals_filenames, 'Athena.pal')
    out_files.append(utils.build_snk_rom("athena.zip", bundle_contents, func_map))

    return out_files

def _handle_tnk3(bundle_contents):
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
    pals_filenames = [
        "1.5g",
        "2.5f",
        "0.5h"
    ]
    func_map['pal'] = utils.palette_rebuild_helper(pals_filenames, 'TNKIII.pal')
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
    out_files.append(utils.build_snk_rom("tnk3.zip", bundle_contents, func_map))

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
    out_files.append(utils.build_snk_rom("tnk3j.zip", bundle_contents, func_map))

    return out_files
