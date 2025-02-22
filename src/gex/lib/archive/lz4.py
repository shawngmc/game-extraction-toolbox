'''Module to handle LZ4 compression in pure python'''
import logging
from io import BytesIO

logger = logging.getLogger('gextoolbox')

def extract(bytes_obj):
    '''Extract a LZ4 file'''
    # Based on https://raw.githubusercontent.com/SE2Dev/PyCoD/refs/heads/master/_lz4.py
    
    class CorruptError(Exception):
        pass

    def uncompress(src, offset=4):
        """uncompress a block of lz4 data.

        :param bytes src: lz4 compressed data (LZ4 Blocks)
        :param int offset: offset that the uncompressed data starts at
                            (Used to implicitly read the uncompressed data size)
        :returns: uncompressed data
        :rtype: bytearray

        .. seealso:: http://cyan4973.github.io/lz4/lz4_Block_format.html
        """
        src = BytesIO(src)
        if offset > 0:
            src.read(offset)

        # if we have the original size, we could pre-allocate the buffer with
        # bytearray(original_size), but then we would have to use indexing
        # instad of .append() and .extend()
        dst = bytearray()
        min_match_len = 4

        def get_length(src, length):
            """get the length of a lz4 variable length integer."""
            if length != 0x0f:
                return length

            while True:
                read_buf = src.read(1)
                if len(read_buf) != 1:
                    raise CorruptError("EOF at length read")
                len_part = read_buf[0]

                length += len_part

                if len_part != 0xff:
                    break

            return length

        while True:
            # decode a block
            read_buf = src.read(1)
            if not read_buf:
                raise CorruptError("EOF at reading literal-len")
            token = read_buf[0]

            literal_len = get_length(src, (token >> 4) & 0x0f)

            # copy the literal to the output buffer
            read_buf = src.read(literal_len)

            if len(read_buf) != literal_len:
                raise CorruptError("not literal data")
            dst.extend(read_buf)

            read_buf = src.read(2)
            if not read_buf:
                if token & 0x0f != 0:
                    raise CorruptError(
                        "EOF, but match-len > 0: %u" % (token % 0x0f, ))
                break

            if len(read_buf) != 2:
                raise CorruptError("premature EOF")

            offset = read_buf[0] | (read_buf[1] << 8)

            if offset == 0:
                raise CorruptError("offset can't be 0")

            match_len = get_length(src, (token >> 0) & 0x0f)
            match_len += min_match_len

            # append the sliding window of the previous literals
            for _ in range(match_len):
                dst.append(dst[-offset])

        return dst



    return uncompress(bytes_obj)





