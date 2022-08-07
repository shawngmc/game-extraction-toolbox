import traceback
import sys
import zlib
import logging, sys
import os

def extract(bytes):
    magic_string = bytes[0:3].decode("utf-8")
    if magic_string != "ARC":
        raise Exception("Not a valid ARC archive!")
    else:
        files = {}
        logging.debug("ARC detected!")
        logging.debug(f'Archive Size: {len(bytes)}')
        version = int.from_bytes(bytes[4:6], byteorder='little')
        logging.debug(f'Version: {version}')
        total_files = int.from_bytes(bytes[6:8], byteorder='little')
        logging.debug(f'Number of files: {total_files}')

        curr_pos = 0x8
        for x in range(0, total_files):
            logging.debug(f'  file: {x}')
            path = str(bytes[curr_pos:curr_pos+0x40], 'utf-8').rstrip('\x00')
            logging.debug(f'    path: {path}')
            type = int.from_bytes(bytes[curr_pos+0x40:curr_pos+0x44], byteorder='little')
            logging.debug(f'    type: {type}')
            zsize = int.from_bytes(bytes[curr_pos+0x44:curr_pos+0x48], byteorder='little')
            logging.debug(f'    zsize: {zsize}')
            size = int.from_bytes(bytes[curr_pos+0x48:curr_pos+0x4b], byteorder='little')
            logging.debug(f'    size: {size}')
            offset = int.from_bytes(bytes[curr_pos+0x4c:curr_pos+0x50], byteorder='little')
            logging.debug(f'    offset: {offset}')

            contents = bytes[offset:offset+zsize]
            contents = zlib.decompress(contents, wbits = 0)
            logging.debug(f'    decompressed size: {len(contents)} bytes')

            files[x] = {
                "contents": contents,
                "offset": offset,
                "entry": x,
                "size": size,
                "path": path
            }
            curr_pos = curr_pos + 0x50

        return files




