'''Module to handle KPKA archive (Capcom RE Engine)'''
import sys
import zlib
import logging

logger = logging.getLogger('gextoolbox')

def extract(bytes_obj):
    '''Extract a KPKA archive (Capcom RE Engine)'''
    magic_string = bytes_obj[0:4].decode("utf-8")
    if magic_string != "KPKA":
        raise Exception("Not a valid KPKA archive!")
    else:
        files = {}
        logger.debug("KPKA detected!")
        version = int.from_bytes(bytes_obj[4:8], sys.byteorder)
        total_files = int.from_bytes(bytes_obj[8:12], sys.byteorder)
        _ = int.from_bytes(bytes_obj[12:16], sys.byteorder)
        logger.debug(f'Archive Size: {len(bytes_obj)}')
        logger.debug(f'Version: {version}')
        logger.debug(f'Number of files: {total_files}')

        curr_pos = 16
        for curr_file in range(0, total_files):
            name_crc_l = int.from_bytes(bytes_obj[curr_pos:curr_pos+4], sys.byteorder)
            name_crc_u = int.from_bytes(bytes_obj[curr_pos+4:curr_pos+8], sys.byteorder)
            offset = int.from_bytes(bytes_obj[curr_pos+8:curr_pos+16], sys.byteorder)
            zsize = int.from_bytes(bytes_obj[curr_pos+16:curr_pos+24], sys.byteorder)
            size = int.from_bytes(bytes_obj[curr_pos+24:curr_pos+32], sys.byteorder)
            flag = int.from_bytes(bytes_obj[curr_pos+32:curr_pos+40], sys.byteorder)
            dummy_2 = int.from_bytes(bytes_obj[curr_pos+40:curr_pos+44], sys.byteorder)
            dummy_3 = int.from_bytes(bytes_obj[curr_pos+44:curr_pos+48], sys.byteorder)

            logger.debug(f'  file: {curr_file}')
            logger.debug(f'    name_crc_l: {name_crc_l}')
            logger.debug(f'    name_crc_u: {name_crc_u}')
            logger.debug(f'    offset: {offset}')
            logger.debug(f'    zsize: {zsize}')
            logger.debug(f'    size: {size}')
            logger.debug(f'    flag: {flag}')
            logger.debug(f'    dummy_2: {dummy_2}')
            logger.debug(f'    dummy_3: {dummy_3}')

            # Handle the flag
            if flag == 0 or flag == 1024:
                contents = bytes_obj[offset:offset+size]
            elif flag == 1:
                contents = bytes_obj[offset:offset+zsize]
                contents = zlib.decompress(contents, wbits = -15)
                logger.debug(f'    decompressed size: {len(contents)} bytes')
            elif flag == 2:
                logger.debug("zstd NYI!")
                contents = bytes_obj[offset:offset+zsize]
            else:
                if zsize != size:
                    logger.debug(f'Compression flag {flag} NYI!')
                    logger.debug(f'    zsize: {zsize}')
                    logger.debug(f'    size: {size}')
                contents = bytes_obj[offset:offset+zsize]

            # Don't hash on offset, dupe offsets have been observed
            files[curr_file] = {
                "contents": contents,
                "offset": offset,
                "entry": curr_file,
                "size": size,
                "flag": flag
            }
            curr_pos = curr_pos + 48

        return files
