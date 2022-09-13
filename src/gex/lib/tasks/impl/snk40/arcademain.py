'''Extraction code for Arcade ROMs from SNK40 Main Bundle'''
import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "gensitou.zip",
        "notes": []
    },
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "prehisle.zip",
        "notes": []
    },
    {
        "game": "Prehistoric Isle",
        "system": "Arcade",
        "filename": "prehisleu.zip",
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsm.zip",
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsm1.zip",
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsmj.zip",
        "notes": []
    },
    {
        "game": "Street Smart",
        "system": "Arcade",
        "filename": "streetsmw.zip",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3.zip",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3j.zip",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3k.zip",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "Arcade",
        "filename": "ikari3u.zip",
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "Arcade",
        "filename": "pow.zip",
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "Arcade",
        "filename": "powj.zip",
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguard.zip",
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguardc.zip",
        "notes": []
    },
    {
        "game": "Vanguard",
        "system": "Arcade",
        "filename": "vanguardj.zip",
        "notes": []
    },
    {
        "game": "Guerilla War",
        "system": "Arcade",
        "filename": "gwar.zip",
        "notes": [2]
    },
    {
        "game": "Guerilla War (A)",
        "system": "Arcade",
        "filename": "gwara.zip",
        "notes": [2]
    },
    {
        "game": "Guerilla War (B)",
        "system": "Arcade",
        "filename": "gwarb.zip",
        "notes": []
    },
    {
        "game": "Guevara (Guerilla War (J))",
        "system": "Arcade",
        "filename": "gwarj.zip",
        "notes": [2]
    },
    {
        "game": "Psycho Soldier",
        "system": "Arcade",
        "filename": "psychos.zip",
        "notes": [2]
    },
    {
        "game": "Psycho Soldier (J)",
        "system": "Arcade",
        "filename": "psychosj.zip",
        "notes": [2]
    },
    {
        "game": "Ikari I",
        "system": "Arcade",
        "filename": "ikari.zip",
        "notes": [2]
    },
    {
        "game": "Ikari I (US Alt.)",
        "system": "Arcade",
        "filename": "ikaria.zip",
        "notes": [2]
    },
    {
        "game": "Ikari I (J, No Continues)",
        "system": "Arcade",
        "filename": "ikarijp.zip",
        "notes": [2]
    },
    {
        "game": "Ikari I (No Continues)",
        "system": "Arcade",
        "filename": "ikarinc.zip",
        "notes": [2]
    },
    {
        "game": "Ikari 2 Victory Road",
        "system": "Arcade",
        "filename": "victroad.zip",
        "notes": [2]
    },
    {
        "game": "Dogou Souken (Ikari 2 Victory Road (J))",
        "system": "Arcade",
        "filename": "dogosoke.zip",
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
    out_files.extend(_handle_victoryroad(contents))
    out_files.extend(_handle_ikari(contents))
    out_files.extend(_handle_guerilla(contents))
    return out_files

def _handle_prehisle(mbundle_entries):
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
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

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
    mame_name = "gensitou.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # PREHISLEU
    func_map = {}
    maincpu_filenames = [
        "gt-u2.2h",
        "gt-u3.3h"
    ]
    func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.u.68k', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "prehisleu.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # PREHISLE
    func_map = {}
    maincpu_filenames = [
        "gt-e2.2h",
        "gt-e3.3h"
    ]
    func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.w.68k', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "prehisle.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files

def _handle_streetsm(mbundle_entries):
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
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

    # STREETS1 GFX Common
    func_map = {}
    gfx1_filenames = [
        "s2-7.15l",
        "s2-8.15m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('streetsm1.gfx1', gfx1_filenames)
    logger.info("Processing STREETS1 GFX common files...")
    gfx1_file_map = helpers.process_rom_files(mbundle_entries, func_map)

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
    mame_name = "streetsm.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # STREETSM1
    func_map = {}
    maincpu_filenames = [
        "s2-1ver1.9c",
        "s2-2ver1.10c"
    ]
    func_map['maincpu'] = streets_maincpu('streetsm1.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "streetsm1.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # STREETSMJ
    func_map = {}
    maincpu_filenames = [
        "s2v1j_01.bin",
        "s2v1j_02.bin"
    ]
    func_map['maincpu'] = streets_maincpu('streetsmj.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "streetsmj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # STREETSMW
    func_map = {}
    maincpu_filenames = [
        "s-smart1.bin",
        "s-smart2.bin"
    ]
    func_map['maincpu'] = streets_maincpu('streetsmw.maincpu', maincpu_filenames)
    func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "streetsmw.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files

def _handle_ikari3(mbundle_entries):
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
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

    # IKARI3 GFX1 Common
    func_map = {}
    gfx1_filenames = [
        "ik3-7.16l",
        "ik3-8.16m"
    ]
    func_map['gfx1'] = helpers.equal_split_helper('ikari3.gfx1', gfx1_filenames)
    logger.info("Processing IKARI3 GFX1 common files...")
    gfx1_file_map = helpers.process_rom_files(mbundle_entries, func_map)

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
    gfx2_file_map = helpers.process_rom_files(mbundle_entries, func_map)

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
    mame_name = "ikari3.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    mame_name = "ikari3j.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    mame_name = "ikari3k.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    mame_name = "ikari3u.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files

def _handle_vanguard(mbundle_entries):
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
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

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
    mame_name = "vanguard.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    mame_name = "vanguardc.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    mame_name = "vanguardj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files

def _handle_pow(mbundle_entries):
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
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

    # POW
    func_map = {}
    maincpu_filenames = [
        "dg1ver1.j14",
        "dg2ver1.l14"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('pow.maincpu', maincpu_filenames, 2, 1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "pow.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # POWJ
    func_map = {}
    maincpu_filenames = [
        "1-2",
        "2-2"
    ]
    func_map['maincpu'] = helpers.deinterleave_helper('powj.maincpu', maincpu_filenames, 2, 1)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "powj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files


def _pal_helper(in_file_ref, pal_filenames):
    '''Rebuild RGB Palette ROMs'''
    def palette(in_files):
        in_data = in_files[in_file_ref]
        pal_contents = transforms.deinterleave_nibble(in_data, 4)
        del pal_contents[2] # Remove the spacing entry
        return dict(zip(pal_filenames, pal_contents))
    return palette


def _handle_victoryroad(bundle_contents):
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
    func_map['pal'] = _pal_helper('VictoryRoad.j.pal', pal_filenames)
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
    ph_files = {
        "1.1d": 4096,
        "1.2d": 4096,
        "a5004-1.6d": 260,
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
    func_map['pal'] = _pal_helper('VictoryRoad.pal', pal_filenames)
    mame_name = "victroad.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    func_map['pal'] = _pal_helper('IkariWarriors.pal', pal_filenames)
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
    func_map['palette'] = helpers.existing_files_helper(palette_common_file_map)
    ph_files = {
        "ampal16l8a-a5004-3.2n": 260,
        "ampal16l8a-a5004-4.8s": 260,
        "pal20l8a-a5004-2.6m": 324,
        "ampal16r6a-a5004-1.6d": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
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
    func_map['palette'] = helpers.common_rename_helper(palette_common_file_map, {
        "2.2j": "a6002-2.2l",
        "1.1h": "a6002-1.1k",
        "3.1j": "a6002-3.1l"
    })
    ph_files = {
        "1.1d": 4096,
        "1.2d": 4096
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
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
    func_map['palette'] = helpers.existing_files_helper(palette_common_file_map)
    ph_files = {
        "ampal16l8a-a5004-3.2n": 260,
        "ampal16l8a-a5004-4.8s": 260,
        "pal20l8a-a5004-2.6m": 324,
        "ampal16r6a-a5004-1.6d": 260
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    mame_name = "ikarinc.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")


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
    func_map['pal'] = _pal_helper('GuerillaWar.pal', pal_filenames)
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
    func_map['pal'] = helpers.common_rename_helper(pal_common_file_map, {
        "3.9w": "1.1k",
        "1.9u": "2.1l",
        "2.9v": "3.2l"
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
    func_map['pal'] = helpers.existing_files_helper(pal_common_file_map)
    ph_files = {
        'l.1x': 0x1000,
        'l.1w': 0x1000
    }
    func_map['placeholders'] = helpers.placeholder_helper(ph_files)
    mame_name = "gwarj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

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
    func_map['pal'] = _pal_helper('PsychoSoldier.pal', pal_filenames)
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
