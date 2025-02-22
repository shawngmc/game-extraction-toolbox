'''Module to handle LZMA compression with error tolerance'''
import lzma
import logging

logger = logging.getLogger('gextoolbox')

def extract(bytes_obj):
    '''Extract a LZMA file with error tolerance'''
    # Based on https://stackoverflow.com/questions/66271285/python-lzma-corrupt-data-error-when-trying-to-decompress
    # This will try to trim off extra data
    def decompress_lzma(data):
        results = []
        while True:
            decomp = lzma.LZMADecompressor(lzma.FORMAT_AUTO, None, None)
            try:
                res = decomp.decompress(data)
            except lzma.LZMAError:
                if results:
                    break  # Leftover data is not a valid LZMA/XZ stream; ignore it.
                else:
                    raise  # Error on the first iteration; bail out.
            results.append(res)
            data = decomp.unused_data
            if not data:
                break
            if not decomp.eof:
                raise lzma.LZMAError("Compressed data ended before the end-of-stream marker was reached")
        return b"".join(results)
    byt = bytes(bytes_obj)
    length = len(bytes_obj)
    stay = True
    while stay:
        stay = False
        try:
            decompress_lzma(byt[0:length])
        except lzma.LZMAError:
            length -= 1
            stay = True

    return decompress_lzma(byt[0:length])