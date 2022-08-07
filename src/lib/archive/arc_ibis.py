import traceback
import sys
import zlib
import logging, sys
import os


# Example 1) Vampj in Capcom Fighting Collection
# - 64 byte header
#   - Magic 'IBIS' (4 bytes)
#   - ??? 60 bytes
# - maincpu (512K x8)
#   -0x00000040
#      vamj.03a
#      vamj.04b
#      vamj.05a
#      vamj.06a
#      vamj.07a
#      vamj.08a
#      vamj.09a
#      vamj.10a
#   -0x00400040
# - *** Unknown 24MB Section - likely GFX here
# - audiocpu (128K x2)
#   -0x01c00040
#      vam.01
#      vam.02
#   -0x01c48040
# - *** Unknown 8KB Section - all 0xFF
# - qsound - endian swap (2048K x2)
#   -0x01c50040
#     vam.11m
#     vam.12m
#   -0x02050040


# - Only 8.25MB of this file is ID'd
# - It's 33MB (33,882,176)
# - There's still more than enough for all the missing components (24MB > ~20MB)
# - It's possible there is also a maincpu_decrypted section

# NOT YET FOUND
# - qsound bios (8K x1)
#   dt-1425.bin
# - gfx - interleaved? bit/byte swapped? (4096K x4, 1024K x4 = 20MB)
#   vam.13m
#   vam.15m
#   vam.17m
#   vam.19m
#   vam.14m
#   vam.16m
#   vam.18m
#   vam.20m
# - key  (20B x1)
#   vampj.key


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def extract(bytes):
    magic_string = bytes[0:4].decode("utf-8")
    if magic_string != "IBIS":
        raise Exception("Not a valid IBIS archive!")
    else:
        files = {}
        logging.debug("IBIS detected!")
                
        # logging.debug(f'Archive Size: {len(bytes)}')
        # version = int.from_bytes(bytes[4:6], byteorder='little')
        # logging.debug(f'Version: {version}')
        # total_files = int.from_bytes(bytes[6:8], byteorder='little')
        # logging.debug(f'Number of files: {total_files}')

        curr_pos = 0x40
        # for x in range(0, total_files):
        #     logging.debug(f'  file: {x}')
        #     path = str(bytes[curr_pos:curr_pos+0x40], 'utf-8').rstrip('\x00')
        #     logging.debug(f'    path: {path}')
        #     type = int.from_bytes(bytes[curr_pos+0x40:curr_pos+0x44], byteorder='little')
        #     logging.debug(f'    type: {type}')
        #     zsize = int.from_bytes(bytes[curr_pos+0x44:curr_pos+0x48], byteorder='little')
        #     logging.debug(f'    zsize: {zsize}')
        #     size = int.from_bytes(bytes[curr_pos+0x48:curr_pos+0x4b], byteorder='little')
        #     logging.debug(f'    size: {size}')
        #     offset = int.from_bytes(bytes[curr_pos+0x4c:curr_pos+0x50], byteorder='little')
        #     logging.debug(f'    offset: {offset}')

        #     contents = bytes[offset:offset+zsize]
        #     contents = zlib.decompress(contents, wbits = 0)
        #     logging.debug(f'    decompressed size: {len(contents)} bytes')

        #     files[x] = {
        #         "contents": contents,
        #         "offset": offset,
        #         "entry": x,
        #         "size": size,
        #         "path": path
        #     }
        #     curr_pos = curr_pos + 0x50

        # return files
        return dict()




