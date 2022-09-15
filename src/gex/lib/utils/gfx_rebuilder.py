'''Tools for Graphics ROMs, largely based on dotemu2mame.js and avault2mame.js by cxx on GitHub'''
import copy
from collections import namedtuple
import struct

# TODO: Make these functions easier to read/more pythonic

def reencode_gfx(contents, layout):
    '''
    Rebuild GFX roms from sprite/tile content.
    # Example Layout
    _DDRAGON_TILE_LAYOUT = {
        'width': 16,
        'height': 16,
        'total': [1,2],
        'planes': 4,
        'planeoffset': [[1,2,0], [1,2,4], 0, 4],
        'xoffset': [3, 2, 1, 0, 16*8+3, 16*8+2, 16*8+1, 16*8+0,
            32*8+3, 32*8+2, 32*8+1, 32*8+0, 48*8+3, 48*8+2, 48*8+1, 48*8+0],
        'yoffset': [0*8, 1*8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8,
            8*8, 9*8, 10*8, 11*8, 12*8, 13*8, 14*8, 15*8],
        'charincrement': 64*8
    }
'''
    mod_layout = copy.deepcopy(layout)
    num_planes = mod_layout['planes']
    dest = bytearray(len(contents) * num_planes // 8)

    if isinstance(mod_layout['total'], list):
        [num, den] = mod_layout['total']
        temp_layout = copy.deepcopy(mod_layout)
        temp_layout['total'] = len(dest) * 8 // mod_layout['charincrement'] * num // den

        def map_plane_offset(plane_offset):
            if isinstance(plane_offset, list):
                [num, den, *add] = plane_offset
                add = add[0] if add else 0
                return len(dest) * 8 * num // den + add
            else:
                return plane_offset
        temp_layout['planeoffset'] = list(map(map_plane_offset, mod_layout['planeoffset']))
        mod_layout = temp_layout

    i = 0
    for curr_char in range(0, mod_layout['total']):
        charoffset = mod_layout['charincrement'] * curr_char
        for curr_height in range(0, mod_layout['height']):
            yoffset = charoffset + mod_layout['yoffset'][curr_height]
            for curr_width in range(0, mod_layout['width']):
                xoffset = yoffset + mod_layout['xoffset'][curr_width]
                for curr_plane in range(0, num_planes):
                    offset = xoffset + mod_layout['planeoffset'][curr_plane]
                    dest[offset >> 3] = dest[offset >> 3] | ((contents[i] >> num_planes-1-curr_plane) & 1) << (~offset & 7)
                i += 1

    return dest

BitmapMeta = namedtuple('BitmapMeta', 'offset width height')
def reverse_bmp(contents):
    '''Given a .BMP bitmap, reverse it for gfx rom rebuilding'''
    bmp_meta = BitmapMeta._make(struct.unpack('<L4xLL', contents[10:26]))
    buf = bytearray()
    for row in range(0, bmp_meta.height):
        src_start = bmp_meta.offset + (bmp_meta.width * (bmp_meta.height - (1 + row)))
        buf += contents[src_start:src_start + bmp_meta.width]
    return buf