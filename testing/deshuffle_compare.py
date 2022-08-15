import zlib
import os
import timeit
from gex.lib.contrib.bputil import BPListReader
from gex.lib.utils import blob
from bitarray import bitarray

sf30ac_root_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Street Fighter 30th Anniversary Collection\\"


filenames = [
    "sz3.13m",
    "sz3.14m",
    "sz3.15m",
    "sz3.16m",
    "sz3.17m",
    "sz3.18m",
    "sz3.19m",
    "sz3.20m"
]
num_interim_split = 32
final_split = [0x400000, 0x400000]

def deshuffle_gfx_common(contents):    
    # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
    bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18, 30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]
    contents = blob.bit_shuffle(contents, word_size_bytes=4, bit_order=bit_order)

    return contents



def deshuffle_gfx_common_v2(contents):
    # TODO: This is not giving the same results!
    big_endian = False
    word_size_bytes = 4
    bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18, 30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]
    new_content = bytearray()    
    shuffle_word = bitarray(word_size_bytes*8, endian = "big" if big_endian else "little")
    updated_word = bitarray(word_size_bytes*8, endian = "big" if big_endian else "little")
    num_shuffles = len(contents)//word_size_bytes
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word.frombytes(contents[offset:offset+word_size_bytes])

        updated_word.setall(0)
        i = 0
        for next_bit in bit_order:
            updated_word[i] = shuffle_word[next_bit]
            i = i + 1

        new_content.extend(updated_word)
    return new_content

def deshuffle_gfx_common_v3(contents):
    # TODO: This is not giving the same results!
    big_endian = False
    word_size_bytes = 4
    bit_order = [7, 3, 15, 11, 23, 19, 31, 27, 6, 2, 14, 10, 22, 18, 30, 26, 5, 1, 13, 9, 21, 17, 29, 25, 4, 0, 12, 8, 20, 16, 28, 24]
    new_content = bytearray(len(contents))    
    shuffle_word = bitarray(word_size_bytes*8, endian = "big" if big_endian else "little")
    updated_word = bitarray(word_size_bytes*8, endian = "big" if big_endian else "little")
    num_shuffles = len(contents)//word_size_bytes
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word.frombytes(contents[offset:offset+word_size_bytes])

        updated_word.setall(0)
        i = 0
        for next_bit in bit_order:
            updated_word[i] = shuffle_word[next_bit]
            i = i + 1

        new_content[offset:offset+word_size_bytes] = updated_word
    return new_content

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


# Read file
print("starting...")
sfa3_path = os.path.join(sf30ac_root_path, "Bundle", 'bundleStreetFighterAlpha3.mbundle')
with open(sfa3_path, 'rb') as bundle_file:
    contents = bundle_file.read()
    reader = BPListReader(contents)
    parsed = reader.parse()
    vrom_data = parsed['StreetFighterAlpha3.vrom']
    print("sfa3 vrom read...")

    num_runs = 1
    
    test_funcs = {
        # 'bitwise_op_v1': decode_cps1_gfx,
        'bitarray_op_v1': deshuffle_gfx_common,
        'bitarray_op_v2': deshuffle_gfx_common_v2
    }

    results = {}

    for name, test_func in test_funcs.items():
        print(f'Running {name} {num_runs} times...')
        curr_result = []
        total_run_time = timeit.timeit(stmt='curr_result.append(test_func(vrom_data))', setup='pass', number=num_runs, globals=globals())
        average_time = total_run_time // num_runs
        print(f'{name} function on average took {average_time} seconds.')
        results[name] = curr_result

    # Are results the same?
    print('Running equality check...')
    
    def get_crc(content):
        return hex(zlib.crc32(content) & 0xffffffff)

    crcs = {}
    for name, results in results.items():
        print(results[0][0::20])
        curr_crc = get_crc(results[0])
        consistent = True
        for i in range(0, len(results)):
            if get_crc(results[i]) != curr_crc:
                print (f'Inconsistent results for {name}!')
                consistent = False
        
        if consistent:
            print(f'{name} had common result CRC of {curr_crc}')


