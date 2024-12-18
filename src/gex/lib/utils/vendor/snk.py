'''
Utility functions for SNK games
'''

# from gex.lib.utils.blob import transforms

def sfix_reorder(contents):
    '''Reorders an SFIX rom file'''
    for i in range(0, len(contents), 32):
        tmp = bytearray(32)
        for j in range(0, 8):
            tmp[j+16] = contents[i+4*j+0]
            tmp[j+24] = contents[i+4*j+1]
            tmp[j+ 0] = contents[i+4*j+2]
            tmp[j+ 8] = contents[i+4*j+3]
        contents[i:i+32] = tmp
    return contents

# Based on "ack" post https://www.arcade-projects.com/threads/samurai-shodown-v-perfect-on-real-hardware.13565/page-2
def unswizzle(data: bytes):
    odd = bytearray()
    even = bytearray()

    tile = bytearray(128)
    offset = bytearray(8)
    planes = bytearray(4)

    index = 0
    while index + 128 <= len(data):
        tile = data[index:index+128]
        index += 128

        for block in range(4):
            if block == 0:
                x_offset, y_offset = 4, 0
            elif block == 1:
                x_offset, y_offset = 4, 8
            elif block == 2:
                x_offset, y_offset = 0, 0
            else:
                x_offset, y_offset = 0, 8

            for row in range(8):
                planes = bytearray([0, 0, 0, 0])
                offset = tile[x_offset + (y_offset * 8) + (row * 8): x_offset + (y_offset * 8) + (row * 8) + 8]

                for i in range(3, -1, -1):
                    offset_data = offset[i]
                    planes[0] = (planes[0] << 1) | ((offset_data >> 4) & 0x1)
                    planes[0] = (planes[0] << 1) | ((offset_data >> 0) & 0x1)
                    planes[1] = (planes[1] << 1) | ((offset_data >> 5) & 0x1)
                    planes[1] = (planes[1] << 1) | ((offset_data >> 1) & 0x1)
                    planes[2] = (planes[2] << 1) | ((offset_data >> 6) & 0x1)
                    planes[2] = (planes[2] << 1) | ((offset_data >> 2) & 0x1)
                    planes[3] = (planes[3] << 1) | ((offset_data >> 7) & 0x1)
                    planes[3] = (planes[3] << 1) | ((offset_data >> 3) & 0x1)

                odd.extend(planes[0:2])
                even.extend(planes[2:4])
    return odd, even