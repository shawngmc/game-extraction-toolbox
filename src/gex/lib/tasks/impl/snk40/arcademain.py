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
    }
]

def extract(bundle_contents):
    out_files = []
    contents = bundle_contents['main']
    out_files.extend(_handle_prehisle(contents))
    out_files.extend(_handle_streetsm(contents))
    out_files.extend(_handle_ikari3(contents))
    out_files.extend(_handle_vanguard(contents))
    out_files.extend(_handle_pow(contents))
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