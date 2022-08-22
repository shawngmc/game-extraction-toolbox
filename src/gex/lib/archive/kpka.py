'''Module to handle KPKA archive (Capcom RE Engine)'''
import sys
import zlib
import logging

def extract(bytes_obj):
    '''Extract a KPKA archive (Capcom RE Engine)'''
    magic_string = bytes_obj[0:4].decode("utf-8")
    if magic_string != "KPKA":
        raise Exception("Not a valid KPKA archive!")
    else:
        files = {}
        logging.debug("KPKA detected!")
        logging.debug(f'Archive Size: {len(bytes_obj)}')
        version = int.from_bytes(bytes_obj[4:8], sys.byteorder)
        logging.debug(f'Version: {version}')
        total_files = int.from_bytes(bytes_obj[8:12], sys.byteorder)
        logging.debug(f'Number of files: {total_files}')
        _ = int.from_bytes(bytes_obj[12:16], sys.byteorder)

        curr_pos = 16
        for curr_file in range(0, total_files):
            logging.debug(f'  file: {curr_file}')
            name_crc_l = int.from_bytes(bytes_obj[curr_pos:curr_pos+4], sys.byteorder)
            logging.debug(f'    name_crc_l: {name_crc_l}')
            name_crc_u = int.from_bytes(bytes_obj[curr_pos+4:curr_pos+8], sys.byteorder)
            logging.debug(f'    name_crc_u: {name_crc_u}')
            offset = int.from_bytes(bytes_obj[curr_pos+8:curr_pos+16], sys.byteorder)
            logging.debug(f'    offset: {offset}')
            zsize = int.from_bytes(bytes_obj[curr_pos+16:curr_pos+24], sys.byteorder)
            logging.debug(f'    zsize: {zsize}')
            size = int.from_bytes(bytes_obj[curr_pos+24:curr_pos+32], sys.byteorder)
            logging.debug(f'    size: {size}')
            flag = int.from_bytes(bytes_obj[curr_pos+32:curr_pos+40], sys.byteorder)
            logging.debug(f'    flag: {flag}')
            dummy_2 = int.from_bytes(bytes_obj[curr_pos+40:curr_pos+44], sys.byteorder)
            logging.debug(f'    dummy_2: {dummy_2}')
            dummy_3 = int.from_bytes(bytes_obj[curr_pos+44:curr_pos+48], sys.byteorder)
            logging.debug(f'    dummy_3: {dummy_3}')

            # Handle the flag
            if flag == 0 or flag == 1024:
                contents = bytes_obj[offset:offset+size]
            elif flag == 1:
                contents = bytes_obj[offset:offset+zsize]
                contents = zlib.decompress(contents, wbits = -15)
                logging.debug(f'    decompressed size: {len(contents)} bytes')
            elif flag == 2:
                logging.debug("zstd NYI!")
                contents = bytes_obj[offset:offset+zsize]
            else:
                if zsize != size:
                    logging.debug(f'Compression flag {flag} NYI!')
                    logging.debug(f'    zsize: {zsize}')
                    logging.debug(f'    size: {size}')
                contents = bytes_obj[offset:offset+zsize]

            # Don't hash on offset, dupe offsets have been observed
            files[curr_file] = {
                "contents": contents,
                "offset": offset,
                "entry": curr_file,
                "size": size
            }
            curr_pos = curr_pos + 48

        return files
