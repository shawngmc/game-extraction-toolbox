import sys
import zlib
import logging, sys

def extract(bytes):
    magic_string = bytes[0:4].decode("utf-8")
    if magic_string != "KPKA":
        raise Exception("Not a valid KPKA archive!")
    else:
        files = {}
        logging.debug("KPKA detected!")
        logging.debug(f'Archive Size: {len(bytes)}')
        version = int.from_bytes(bytes[4:8], sys.byteorder)
        logging.debug(f'Version: {version}')
        total_files = int.from_bytes(bytes[8:12], sys.byteorder)
        logging.debug(f'Number of files: {total_files}')
        dummy_val = int.from_bytes(bytes[12:16], sys.byteorder)

        curr_pos = 16
        for x in range(0, total_files):
            logging.debug(f'  file: {x}')
            name_crc_l = int.from_bytes(bytes[curr_pos:curr_pos+4], sys.byteorder)
            logging.debug(f'    name_crc_l: {name_crc_l}')
            name_crc_u = int.from_bytes(bytes[curr_pos+4:curr_pos+8], sys.byteorder)
            logging.debug(f'    name_crc_u: {name_crc_u}')
            offset = int.from_bytes(bytes[curr_pos+8:curr_pos+16], sys.byteorder)
            logging.debug(f'    offset: {offset}')
            zsize = int.from_bytes(bytes[curr_pos+16:curr_pos+24], sys.byteorder)
            logging.debug(f'    zsize: {zsize}')
            size = int.from_bytes(bytes[curr_pos+24:curr_pos+32], sys.byteorder)
            logging.debug(f'    size: {size}')
            flag = int.from_bytes(bytes[curr_pos+32:curr_pos+40], sys.byteorder)
            logging.debug(f'    flag: {flag}')
            dummy_2 = int.from_bytes(bytes[curr_pos+40:curr_pos+44], sys.byteorder)
            logging.debug(f'    dummy_2: {dummy_2}')
            dummy_3 = int.from_bytes(bytes[curr_pos+44:curr_pos+48], sys.byteorder)
            logging.debug(f'    dummy_3: {dummy_3}')

            # Handle the flag
            if flag == 0 or flag == 1024:
                contents = bytes[offset:offset+size]
            elif flag == 1:
                contents = bytes[offset:offset+zsize]
                contents = zlib.decompress(contents, wbits = -15)
                logging.debug(f'    decompressed size: {len(contents)} bytes')
            elif flag == 2:
                logging.debug("zstd NYI!")
                contents = bytes[offset:offset+zsize]
            else:
                if zsize != size:
                    logging.debug(f'Compression flag {flag} NYI!')
                    logging.debug(f'    zsize: {zsize}')
                    logging.debug(f'    size: {size}')
                contents = bytes[offset:offset+zsize]

            # Don't hash on offset, dupe offsets have been observed
            files[x] = {
                "contents": contents,
                "offset": offset,
                "entry": x,
                "size": size
            }
            curr_pos = curr_pos + 48

        return files
