'''
Utility functions for Capcom games

IBIS vs. JACK
It's unclear what the difference between IBIS and JACK headers really is
For example, all CBEUB games and all CFC games EXCEPT RedEarth ENG uses IBIS as the header
However
  - RedEarth JP uses a 'JACK' header
  - All CFC default save states use a 'jacksave' header
'''

from gex.lib.utils.blob import transforms

# Perform the following:
# - Get the chunk to process
# - Perform the bit shuffle
# - Split in into 1MB chunks
# - Interleave each pair of 1MB chunks together
# - Merge all the chunks back together
# - Deinterleave the chunks 4-ways
# - If a final split is defined, perform that split on each deinterleaved chunk
def gfx_cps2(filenames, data_select_func = lambda x: x, split = None):
    '''
    Handles a commonly-needed CPS2 GFX processing task

    Perform the following:
    - Get the chunk to process
    - Perform the bit shuffle
    - Split in into 1MB chunks
    - Interleave each pair of 1MB chunks together
    - Merge all the chunks back together
    - Deinterleave the chunks 4-ways
    - If a final split is defined, perform that split on each deinterleaved chunks
    '''
    def gfx(in_data):
        contents = data_select_func(in_data)

        contents = common_gfx_deshuffle(contents)

        # Split it
        chunks = transforms.equal_split(contents, num_chunks=len(contents)//(1024*1024))

        # Interleave each pair of chunks
        new_chunks = []
        for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
            new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
        chunks = new_chunks

        # Merge the chunks back together
        contents = transforms.merge(chunks)

        # Deinterleave the chunks into our files
        new_chunks = []
        chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)
        if split is not None:
            for chunk in chunks:
                new_chunks.extend(transforms.custom_split(chunk, split))
            chunks = new_chunks
        return dict(zip(filenames, chunks))
    return gfx

def audiocpu_cps2(start, filenames):
    '''Handles a commonly-needed CPS2 Audio CPU processing task'''
    def audiocpu(contents):
        chunks = []
        chunks.append(contents[start:start+0x8000] + contents[start+0x10000:start+0x28000])
        chunks.append(contents[start+0x28000:start+0x48000])
        return dict(zip(filenames, chunks))
    return audiocpu

def qsound_cps2(start, length, filenames, num_chunks=2):
    '''Handles a commonly-needed CPS2 QSound data ROM processing task'''
    def qsound(contents):
        contents = contents[start:start+length]
        chunks = transforms.equal_split(contents, num_chunks=num_chunks)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(filenames, chunks))
    return qsound

def maincpu_cps2(start, length, num_chunks, filenames):
    '''Handles a commonly-needed CPS2 Main CPU processing task'''
    def maincpu(contents):
        contents = contents[start:start+length]
        chunks = transforms.equal_split(contents, num_chunks=num_chunks)
        return dict(zip(filenames, chunks))
    return maincpu

_deshuffle_bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18,
                       30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]

def common_gfx_deshuffle(contents):
    '''
    Handles a commonly-needed CPS2 deshuffling task
    This is equivalent to the following bit shuffle, 
    but ends up being about 30% faster on this SLOW operation:

    def decode_cps1_gfx(data):
        buf = bytearray(data)
        for i in range(0, len(buf), 4):
            dwval = 0
            src = buf[i] + (buf[i + 1] << 8) + (buf[i + 2] << 16) + (buf[i + 3] << 24)

            for j in range(8):
                n = src >> (j * 4) & 0x0f
                if (n & 0x01):
                    dwval |= 1 << (     7 - j)
                if (n & 0x02):
                    dwval |= 1 << ( 8 + 7 - j)
                if (n & 0x04):
                    dwval |= 1 << (16 + 7 - j)
                if (n & 0x08):
                    dwval |= 1 << (24 + 7 - j)

            buf[i + 0] = (dwval)       & 0xff
            buf[i + 1] = (dwval >>  8) & 0xff
            buf[i + 2] = (dwval >> 16) & 0xff
            buf[i + 3] = (dwval >> 24) & 0xff
        return buf
    '''
    return transforms.bit_shuffle(contents, word_size_bytes=4, bit_order=_deshuffle_bit_order)
