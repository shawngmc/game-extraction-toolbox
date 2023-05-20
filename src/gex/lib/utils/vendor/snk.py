'''
Utility functions and common rebuilds for SNK games
'''

from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

def sfix_reorder(contents):
    '''Reorders an SFIX rom file'''
    if isinstance(contents, bytes):
        contents = bytearray(contents)

    for i in range(0, len(contents), 32):
        tmp = bytearray(32)
        for j in range(0, 8):
            tmp[j+16] = contents[i+4*j+0]
            tmp[j+24] = contents[i+4*j+1]
            tmp[j+ 0] = contents[i+4*j+2]
            tmp[j+ 8] = contents[i+4*j+3]
        contents[i:i+32] = tmp
    return contents


# Based on JS: function deoptimize_sprites(buf)
# from: https://gist.github.com/cxx/81b9f45eb5b3cb87b4f3783ccdf8894f by cxx
# which is based on: http://i486.mods.jp/ichild/?page_id=62 by Imaha486
def deoptimize_sprites(contents):
    '''Deoptimizes sprites from the merged game releases'''
    if isinstance(contents, bytes):
        contents = bytearray(contents)

    for i in range(0, len(contents), 0x80):
        tmp = bytearray(0x80)
        for y in range(0, 0x10):
            dst_data = contents[i+(y*8)+0] <<  0 | contents[i+(y*8)+1] <<  8 | contents[i+(y*8)+2] << 16 | contents[i+(y*8)+3] << 24
            for x in range(0, 8):
                tmp[0x43 | y << 2] |= (dst_data >> x*4+3 & 1) << 7-x
                tmp[0x41 | y << 2] |= (dst_data >> x*4+2 & 1) << 7-x
                tmp[0x42 | y << 2] |= (dst_data >> x*4+1 & 1) << 7-x
                tmp[0x40 | y << 2] |= (dst_data >> x*4+0 & 1) << 7-x

            dst_data = contents[i+(y*8)+4] <<  0 | contents[i+(y*8)+5] <<  8 | contents[i+(y*8)+6] << 16 | contents[i+(y*8)+7] << 24
            for x in range(0, 8):
                tmp[0x03 | y << 2] |= (dst_data >> x*4+3 & 1) << 7-x
                tmp[0x01 | y << 2] |= (dst_data >> x*4+2 & 1) << 7-x
                tmp[0x02 | y << 2] |= (dst_data >> x*4+1 & 1) << 7-x
                tmp[0x00 | y << 2] |= (dst_data >> x*4+0 & 1) << 7-x
        for r in range(0, 0x80):
            contents[i+r] = tmp[r]
    return contents


def handle_bstars2(bundle_contents):
    func_map = {}
    def bstars2_maincpu(in_files):
        contents = in_files['bstars2_game_m68k']

        chunks = transforms.equal_split(contents, num_chunks=2)

        return {"041-p1.p1": chunks[0]}
    func_map['maincpu'] = bstars2_maincpu
    adpcm_file_map = {
        '041-v1.v1': 0x100000,
        '041-v2.v2': 0x100000,
        '041-v3.v3': 0x80000
    }
    func_map['adpcm'] = helpers.custom_split_helper('bstars2_adpcm', adpcm_file_map)
    func_map['zoom'] = helpers.name_file_helper("bstars2_zoom_table", "000-lo.lo")

    # Audio CPU seems to officially duplicate the data?
    def bstars2_audiocpu(in_files):
        contents = in_files['bstars2_game_z80']

        return {"041-m1.m1": transforms.merge([contents, contents])}
    func_map['audiocpu'] = bstars2_audiocpu

    def bstars2_sprites(in_files):
        contents = in_files['bstars2_tiles']
        deoptimized = deoptimize_sprites(contents)
        filenames = [
            "041-c1.c1",
            "041-c2.c2",
            "041-c3.c3",
            "041-c4.c4",
        ]
        chunks = transforms.equal_split(deoptimized, len(filenames) // 2)
        chunks = transforms.deinterleave_all(chunks, 2, 1)
        return dict(zip(filenames, chunks))
    func_map['sprites'] = bstars2_sprites

    def bstars2_fixed(in_files):
        contents = in_files['bstars2_game_sfix']

        return {"041-s1.s1": sfix_reorder(contents)}
    func_map['fixed'] = bstars2_fixed

    return helpers.build_rom(bundle_contents, func_map)

def handle_twinspri(bundle_contents):
    func_map = {}
    def twinspri_maincpu(in_files):
        contents = in_files['twinspri_game_m68k']

        chunks = transforms.equal_split(contents, num_chunks=2)

        return {"224-p1.p1": chunks[0]}
    func_map['maincpu'] = twinspri_maincpu
    adpcm_file_map = {
        '224-v1.v1': 0x400000,
        '224-v2.v2': 0x200000,
    }
    func_map['adpcm'] = helpers.custom_split_helper('twinspri_adpcm', adpcm_file_map)
    func_map['zoom'] = helpers.name_file_helper("twinspri_zoom_table", "000-lo.lo")
    func_map['audiocpu'] = helpers.name_file_helper("twinspri_game_z80", "224-m1.m1")

    def twinspri_sprites(in_files):
        contents = in_files['twinspri_tiles']
        deoptimized = deoptimize_sprites(contents)
        filenames = [
            "224-c1.c1",
            "224-c2.c2",
            "224-c3.c3",
            "224-c4.c4",
        ]
        chunks = transforms.custom_split(deoptimized, [0x800000, 0x200000])
        chunks = transforms.deinterleave_all(chunks, 2, 1)
        return dict(zip(filenames, chunks))
    func_map['sprites'] = twinspri_sprites

    def twinspri_fixed(in_files):
        contents = in_files['twinspri_game_sfix']
        return {"224-s1.s1": sfix_reorder(contents)}
    func_map['fixed'] = twinspri_fixed

    return helpers.build_rom(bundle_contents, func_map)
