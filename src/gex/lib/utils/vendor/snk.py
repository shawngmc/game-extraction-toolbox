'''
Utility functions for SNK games
'''

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


# def deoptimize_sprites(contents):
#     '''Deoptimizes sprites from the merged game releases'''
#     if isinstance(contents, bytes):
#         contents = bytearray(contents)
        
# # This is doing a lot of bitwise ORs (|), bitwise ANDs (&) and shifts (<<)
# # Ultimately, I THINK this is a bit-based reordering, but it's hard to mentally parse
# # for dstData, the individual sections don't interfere with each other due to the shifts

#     # We know the first half of the operation is reversing the order of every 4 byte chunk
#     # Ref: https://i486.mods.jp/ichild/sample-page/android_neogeo, 2013/04/25 postscript C-ROM rule can be specified
#     for i in range(0, len(contents), 4):
#         tmp = contents[i:i+4]
#         tmp.reverse()
#         contents[i:i+4] = tmp
        
#     # The problem is that there is definitely a bit transformation
#     # This bit transformation is before the split and deinterleave

#     # For example, bstars2:
#     # - Reverse 4 bits
#     # - Transform???
#     # - Cut in half
#     # - Deinterleave


        

# #             let dstData;
# #             dstData = buf[i+(y*8)+0] <<  0 |
# #                       buf[i+(y*8)+1] <<  8 |
# #                       buf[i+(y*8)+2] << 16 |
# #                       buf[i+(y*8)+3] << 24;
# #             for (let x = 0; x < 8; x++) {
# #                 tmp[0x43 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
# #                 tmp[0x41 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
# #                 tmp[0x42 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
# #                 tmp[0x40 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
# #             }

# #             dstData = buf[i+(y*8)+4] <<  0 |
# #                       buf[i+(y*8)+5] <<  8 |
# #                       buf[i+(y*8)+6] << 16 |
# #                       buf[i+(y*8)+7] << 24;
# #             for (let x = 0; x < 8; x++) {
# #                 tmp[0x03 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
# #                 tmp[0x01 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
# #                 tmp[0x02 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
# #                 tmp[0x00 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
# #             }
# #         }
#         # contents[i:i+0x80] = tmp
# #     }
#     return contents