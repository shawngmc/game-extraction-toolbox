import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "Beast Busters",
        "system": "Arcade",
        "filename": "bbusters.zip",
        "notes": [3]
    },
    {
        "game": "Beast Busters",
        "system": "Arcade",
        "filename": "bbustersj.zip",
        "notes": [3]
    },
    {
        "game": "Beast Busters",
        "system": "Arcade",
        "filename": "bbustersu.zip",
        "notes": [3]
    },
    {
        "game": "Search and Rescue",
        "system": "Arcade",
        "filename": "searchar.zip",
        "notes": []
    },
    {
        "game": "Search and Rescue",
        "system": "Arcade",
        "filename": "searcharj.zip",
        "notes": []
    },
    {
        "game": "Search and Rescue",
        "system": "Arcade",
        "filename": "searcharu.zip",
        "notes": []
    }
]

def extract(bundle_contents):
    out_files = []
    contents = bundle_contents['dlc']
    out_files.extend(_handle_bbusters(contents))
    out_files.extend(_handle_searchar(contents))

    return out_files

def _gfx_split_swap(in_file_ref, filenames):
    '''Func map helper for transforms.equal_split'''
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.equal_split(contents, num_chunks = len(filenames))
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(filenames, chunks))
    return split
    
def _handle_bbusters(mbundle_entries):
    # bbusters commons
    func_map = {}
    out_files = []
    func_map['gfx1'] = helpers.name_file_helper('bbusters.gfx1', 'bb-10.l9')
    gfx2_filenames = [
        "bb-f11.m16",
        "bb-f12.m13",
        "bb-f13.m12",
        "bb-f14.m11"
    ]
    func_map['gfx2'] = _gfx_split_swap('bbusters.gfx2', gfx2_filenames)
    gfx3_filenames = [
        "bb-f21.l10",
        "bb-f22.l12",
        "bb-f23.l13",
        "bb-f24.l15"
    ]
    func_map['gfx3'] = _gfx_split_swap('bbusters.gfx3', gfx3_filenames)
    func_map['gfx4'] = helpers.name_file_helper('bbusters.gfx4', 'bb-back1.m4')
    func_map['gfx5'] = helpers.name_file_helper('bbusters.gfx5', 'bb-back2.m6')
    func_map['scale_table1'] = helpers.name_file_helper('bbusters.scale_table', 'bb-6.e7')
    func_map['scale_table2'] = helpers.name_file_helper('bbusters.scale_table', 'bb-7.h7')
    func_map['scale_table3'] = helpers.name_file_helper('bbusters.scale_table', 'bb-8.a14')
    func_map['scale_table4'] = helpers.name_file_helper('bbusters.scale_table', 'bb-9.c14')
    func_map['audiocpu'] = helpers.name_file_helper('bbusters.audiocpu', 'bb-1.e6')
    func_map['ymsnd'] = helpers.name_file_helper('bbusters.ymsnd', 'bb-pcma.l5')

    logger.info("Processing bbusters common files...")
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

    # bbusters
    func_map = {}
    maincpu_filenames = [
        "bb-3.k10",
        "bb-5.k12",
        "bb-2.k8",
        "bb-4.k11"
    ]
    def bbusters_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, num_chunks = 2)

            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
            chunks = new_chunks

            return dict(zip(filenames, chunks))
        return maincpu
    func_map['maincpu'] = bbusters_maincpu('bbusters.maincpu', maincpu_filenames)
    func_map['ymsnd.deltat'] = helpers.name_file_helper('bbusters.ymsnd.deltat', 'bb-pcmb.l3')
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "bbusters.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # bbustersj
    func_map = {}
    maincpu_filenames = [
        "bb3_ver2_j3.k10",
        "bb5_ver2_j3.k12",
        "bb-2.k8",
        "bb-4.k11"
    ]
    func_map['maincpu'] = bbusters_maincpu('bbustersj.maincpu', maincpu_filenames)
    func_map['ymsnd.deltat'] = helpers.name_file_helper('bbusters.ymsnd.deltat', 'bb-pcmb.l3')
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "bbustersj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # bbustersu
    func_map = {}
    maincpu_filenames = [
        "bb-ver3-u3.k10",
        "bb-ver3-u5.k12",
        "bb-2.k8",
        "bb-4.k11"
    ]
    func_map['maincpu'] = bbusters_maincpu('bbustersu.maincpu', maincpu_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "bbustersu.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files

def _handle_searchar(mbundle_entries):
    # searchar common
    func_map = {}
    out_files = []
    func_map['soundcpu'] = helpers.name_file_helper('searchar.soundcpu', 'bh.5')
    gfx1_filenames = [
        "bh.7",
        "bh.8"
    ]
    func_map['gfx1'] = helpers.equal_split_helper("searchar.gfx1", gfx1_filenames)
    gfx2_filenames = [
        "bh.c1",
        "bh.c3",
        "bh.c5",
        "bh.c2",
        "bh.c4",
        "bh.c6"
    ]
    def searchar_gfx2(in_file_name, filenames):
        def gfx2(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.equal_split(contents, 7)
            del chunks[3] # Middle element is junk
            return dict(zip(filenames, chunks))
        return gfx2
    func_map['gfx2'] = searchar_gfx2("searchar.gfx2", gfx2_filenames)
    func_map['upd'] = helpers.name_file_helper('searchar.upd', 'bh.v1')

    logger.info("Processing searchar common files...")
    common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

    # searchar
    func_map = {}
    maincpu_filenames = [
        "bhw.2",
        "bhw.3"
    ]
    def searchar_maincpu(in_file_name, filenames):
        def maincpu(in_files):
            contents = in_files[in_file_name]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(filenames, chunks))
        return maincpu
    func_map['maincpu'] = searchar_maincpu('searchar.maincpu', maincpu_filenames)
    user_filenames = [
        "bhw.1",
        "bhw.4"
    ]
    func_map['user1'] = searchar_maincpu('searchar.user1', user_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "searchar.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # searcharj
    func_map = {}
    maincpu_filenames = [
        "bh2ver3j.9c",
        "bh3ver3j.10c"
    ]
    func_map['maincpu'] = searchar_maincpu('searcharj.maincpu', maincpu_filenames)
    user_filenames = [
        "bhw.1",
        "bhw.4"
    ]
    func_map['user1'] = searchar_maincpu('searchar.user1', user_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "searcharj.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")

    # searcharu
    func_map = {}
    maincpu_filenames = [
        "bh.2",
        "bh.3"
    ]
    func_map['maincpu'] = searchar_maincpu('searcharu.maincpu', maincpu_filenames)
    user_filenames = [
        "bh.1",
        "bh.4"
    ]
    func_map['user1'] = searchar_maincpu('searcharu.user1', user_filenames)
    func_map['common'] = helpers.existing_files_helper(common_file_map)
    mame_name = "searcharu.zip"
    logger.info(f"Building {mame_name}...")
    out_files.append(
        {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
    )
    logger.info(f"Extracted {mame_name}.")
    return out_files