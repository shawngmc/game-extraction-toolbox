import copy

def reencode_gfx(contents, layout):
    # This appears to be rebuilding GFX roms from sprites.
    modLayout = copy.deepcopy(layout)
    numPlanes = modLayout['planes']
    dest = bytearray(len(contents) * numPlanes // 8)

    if (isinstance(modLayout['total'], list)):
        [num, den] = modLayout['total']
        tempLayout = copy.deepcopy(modLayout)
        tempLayout['total'] = len(dest) * 8 // modLayout['charincrement'] * num // den

        def map_plane_offset(x):
            if isinstance(x, list):
                [num, den, *add] = x
                add = add[0] if add else 0
                return len(dest) * 8 * num // den + add
            else:
                return x
        tempLayout['planeoffset'] = list(map(map_plane_offset, modLayout['planeoffset']))
        modLayout = tempLayout

    i = 0
    for c in range(0, modLayout['total']):
        charoffset = modLayout['charincrement'] * c
        for y in range(0, modLayout['height']):
            yoffset = charoffset + modLayout['yoffset'][y]
            for x in range(0, modLayout['width']):
                xoffset = yoffset + modLayout['xoffset'][x]
                for p in range(0, numPlanes):
                    offset = xoffset + modLayout['planeoffset'][p]
                    dest[offset >> 3] = dest[offset >> 3] | ((contents[i] >> numPlanes-1-p) & 1) << (~offset & 7)
                i += 1

    return dest