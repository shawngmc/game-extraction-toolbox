import copy

    # Example Layout
    # _DDRAGON_TILE_LAYOUT = {
    #     'width': 16,
    #     'height': 16,
    #     'total': [1,2],
    #     'planes': 4,
    #     'planeoffset': [[1,2,0], [1,2,4], 0, 4],
    #     'xoffset': [3, 2, 1, 0, 16*8+3, 16*8+2, 16*8+1, 16*8+0,
    #         32*8+3, 32*8+2, 32*8+1, 32*8+0, 48*8+3, 48*8+2, 48*8+1, 48*8+0],
    #     'yoffset': [0*8, 1*8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8,
    #         8*8, 9*8, 10*8, 11*8, 12*8, 13*8, 14*8, 15*8],
    #     'charincrement': 64*8
    # }

def reencode_gfx(contents, layout):
    # This appears to be rebuilding GFX roms from sprites.
    mod_layout = copy.deepcopy(layout)
    num_planes = mod_layout['planes']
    dest = bytearray(len(contents) * num_planes // 8)

    if (isinstance(mod_layout['total'], list)):
        [num, den] = mod_layout['total']
        temp_layout = copy.deepcopy(mod_layout)
        temp_layout['total'] = len(dest) * 8 // mod_layout['charincrement'] * num // den

        def map_plane_offset(x):
            if isinstance(x, list):
                [num, den, *add] = x
                add = add[0] if add else 0
                return len(dest) * 8 * num // den + add
            else:
                return x
        temp_layout['planeoffset'] = list(map(map_plane_offset, mod_layout['planeoffset']))
        mod_layout = temp_layout

    i = 0
    for c in range(0, mod_layout['total']):
        charoffset = mod_layout['charincrement'] * c
        for y in range(0, mod_layout['height']):
            yoffset = charoffset + mod_layout['yoffset'][y]
            for x in range(0, mod_layout['width']):
                xoffset = yoffset + mod_layout['xoffset'][x]
                for p in range(0, num_planes):
                    offset = xoffset + mod_layout['planeoffset'][p]
                    dest[offset >> 3] = dest[offset >> 3] | ((contents[i] >> num_planes-1-p) & 1) << (~offset & 7)
                i += 1

    return dest
