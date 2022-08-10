from gex.lib.utils import blob

# IBIS vs. JACK
# It's unclear what the difference between IBIS and JACK headers really is
# For example, all CBEUB games and all CFC games EXCEPT RedEarth ENG uses IBIS as the header
# However
#   - RedEarth JP uses a 'JACK' header
#   - All CFC default save states use a 'jacksave' header


def gfx_cps2(start, length, filenames, split = None):
    def gfx(contents):    # Cut out the section
        contents = contents[start:start+length]

        # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
        bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18, 30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]
        contents = blob.bit_shuffle(contents, word_size_bytes=4, bit_order=bit_order)

        # Split it
        chunks = blob.equal_split(contents, num_chunks=length//(1024*1024))

        # Interleave each pair of chunks
        new_chunks = []
        for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
            new_chunks.append(blob.interleave([oddchunk, evenchunk], word_size=8))
        chunks = new_chunks

        # Merge the chunks back together
        contents = blob.merge(chunks)

        # Deinterleave the chunks into our files
        new_chunks = []
        chunks = blob.deinterleave(contents, num_ways = 4, word_size=2)
        if split != None:
            for chunk in chunks:
                new_chunks.extend(blob.custom_split(chunk, split))
            chunks = new_chunks
        return dict(zip(filenames, chunks))
    return gfx

def audiocpu_cps2(start, filenames):
    def audiocpu(contents):
        chunks = []
        chunks.append(contents[start:start+0x8000] + contents[start+0x10000:start+0x28000])
        chunks.append(contents[start+0x28000:start+0x48000])
        return dict(zip(filenames, chunks))
    return audiocpu
    
def qsound_cps2(start, length, filenames, num_chunks=2):
    def qsound(contents):
        contents = contents[start:start+length]
        chunks = blob.equal_split(contents, num_chunks=num_chunks)
        chunks = blob.swap_endian_all(chunks)
        return dict(zip(filenames, chunks))
    return qsound

def maincpu_cps2(start, length, num_chunks, filenames):
    def maincpu(contents):
        contents = contents[start:start+length]
        chunks = blob.equal_split(contents, num_chunks=num_chunks)
        return dict(zip(filenames, chunks))
    return maincpu




