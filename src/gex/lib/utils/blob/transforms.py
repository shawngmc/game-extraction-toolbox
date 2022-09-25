'''Common operations for blobs (binary contents) and arrays of blobs'''
import itertools
from typing import Callable
from bitarray import bitarray


def cut(contents: bytes, start: int, length: int=None, end: int=None) -> bytearray:
    '''Select a chunk out of a blob'''
    if length is None and end is None:
        raise Exception(
            "Splice out needs a length or end value, but received neither.")
    elif length is not None and end is not None:
        raise Exception(
            "Splice out needs a length or end value, but received both.")
    elif end is None:
        end = start + length

    return bytearray(contents[start:end])

def merge(chunks: list[bytes]) -> bytearray:
    '''Merge an array of blobs into a single blob'''
    new_content = bytearray()
    for chunk in chunks:
        new_content += chunk
    return new_content

def pad(contents: bytes, new_length: int, pad_byte=b'\0') -> bytearray:
    '''Pad a blob to a specific size'''
    new_content = bytearray()
    new_content.extend(contents)
    pad_size = new_length - len(contents)
    new_content.extend(bytearray(pad_byte * pad_size))
    return new_content

def custom_split(contents: bytes, chunk_sizes: list[int]) -> list[bytearray]:
    '''Split a blob into an array of blobs with specified sizes'''
    if len(contents) != sum(chunk_sizes):
        raise Exception(
            f'Custom split chunk_sizes {sum(chunk_sizes)} != input len {len(contents)}')

    num_chunks = len(chunk_sizes)
    start_offset = 0
    temp_chunks = []
    for i in range(0, num_chunks):
        temp_chunks.append(
            bytearray(contents[start_offset:start_offset+chunk_sizes[i]]))
        start_offset = start_offset + chunk_sizes[i]
    return temp_chunks


def equal_split(contents: bytes, num_chunks: int=None, chunk_size: int=None) -> list[bytearray]:
    '''Split a blob in an array of blobs with equal sizes'''
    if num_chunks is None and chunk_size is None:
        raise Exception("Equal split num_chunks or chunk_Size required")

    if num_chunks is not None and chunk_size is not None:
        if num_chunks * chunk_size != len(contents):
            raise Exception(
                "Equal split num_chunks * chunk_size != content length.")
    elif num_chunks is None:
        num_chunks = len(contents)//chunk_size
    else:
        chunk_size = len(contents)//num_chunks

    start_offset = 0
    temp_chunks = []
    for _ in range(0, num_chunks):
        temp_chunks.append(
            bytearray(contents[start_offset:start_offset+chunk_size]))
        start_offset = start_offset + chunk_size
    return temp_chunks


def interleave(chunks: list[bytes], word_size: int) -> bytearray:
    '''Interleave an array of blobs together into a single blob, word_size bytes at a time'''
    if len(chunks) < 2:
        raise Exception("Interleave requires at least 2 chunks to interleave.")

    chunk_length = len(chunks[0])
    for chunk in chunks:
        if len(chunk) != chunk_length:
            raise Exception("Interleave requires chunks of the same size.")

    combined_length = len(chunks) * chunk_length

    interleave_group_length = len(chunks) * word_size
    num_interleave_groups = combined_length//interleave_group_length
    new_contents = bytearray()
    for i in range(0, num_interleave_groups):
        offset = i * word_size
        for chunk in chunks:
            new_contents += chunk[offset:offset+word_size]
    return new_contents


def deinterleave(contents: bytes, num_ways: int, word_size: int) -> list[bytearray]:
    '''Deinterleave a blob into an array of num_ways blobs, word_size bytes at a time'''
    interleave_group_length = num_ways * word_size
    temp_chunks = []
    for j in range(0, num_ways):
        # Make a compress flag array of the combined group length.
        # This 1s only for the appropriate bytes for this chunk.
        flag_arr = [0] * interleave_group_length
        flag_arr[j*word_size:(j+1)*word_size] = [1 for val in flag_arr[j *
                                                                       word_size:(j+1)*word_size]]

        # Use compress() to select bytes based on the flag array repeated via cycle()
        temp_chunks.append(bytearray(itertools.compress(
            contents, itertools.cycle(flag_arr))))
    return temp_chunks

def deinterleave_nibble(contents: bytes, num_ways: int, bit_prefix: bitarray=bitarray('0000')) -> list[bytearray]:
    '''Deinterleave a blob into an array of num_ways blobs, 4 bits at a time; must be an even num_ways'''
    interleave_group_length = int(num_ways * .5)
    num_interleave_groups = len(contents) // interleave_group_length
    temp_bit_chunks = []
    for j in range(0, num_ways):
        temp_bit_chunks.append(bitarray())
    curr_bits = bitarray()
    for i in range(0, num_interleave_groups):
        curr_bytes = contents[i*interleave_group_length:(i+1)*interleave_group_length]
        curr_bits.clear()
        curr_bits.frombytes(curr_bytes)

        for j in range(0, num_ways):
            temp_bit_chunks[j].extend(bit_prefix + curr_bits[j*4:(j+1)*4])

    return [bytearray(temp_bit_chunk.tobytes()) for temp_bit_chunk in temp_bit_chunks]

def deinterleave_all(chunks: list[bytes], num_ways: int, word_size: int) -> list[bytes]:
    '''Convenience wrapper for deinterleave() to handle multiple input blobs at once'''
    # Note: A list comprehension like the following would be more pythonic here, but...
    # It's actually harder to read AND oddly slightly less performant (typically .1-.2s at the most)
    # It's not clear why it's slower, but not worth using the list comprehension.
    # Even 2 separated list comprehensions isn't faster...
    # return [d for chunk in chunks for d in deinterleave(chunk, num_ways, word_size)]
    temp_chunks = []
    for chunk in chunks:
        temp_chunks.extend(deinterleave(chunk, num_ways, word_size))
    return temp_chunks

def transform_all(chunks: list[bytes], transform_function: Callable,
    *function_args, **function_kwargs) -> list[bytes]:
    '''Apply an existing transformation function to all objects in chunks'''
    temp_chunks = []
    for chunk in chunks:
        temp_chunks.extend(transform_function(chunk, *function_args, **function_kwargs))
    return temp_chunks

def truncate(contents: bytes, max_length: int) -> bytes:
    '''Remove all content from a blob after max_length bytes'''
    return contents[0:max_length]


def splice_out(contents: bytes, start: int, length: int=None, end: int=None) -> bytearray:
    '''Remove an inner section of a blob'''
    if length is None and end is None:
        raise Exception(
            "Splice out needs a length or end value, but received neither.")
    elif length is not None and end is not None:
        raise Exception(
            "Splice out needs a length or end value, but received both.")
    elif end is None:
        end = start + length

    return bytearray(contents[0:start] + contents[end:len(contents)])


def swap_endian(contents: bytes) -> list[bytearray]:
    '''Swap the a blob from little endian to big or vice versa'''
    new_contents = bytearray(len(contents))
    new_contents[0::2] = contents[1::2]
    new_contents[1::2] = contents[0::2]
    return new_contents


def swap_endian_all(chunks: list[bytes]) -> list[bytearray]:
    '''Convenience wrapper for swap_endian() to handle multiple input blobs at once'''
    temp_chunks = []
    for chunk in chunks:
        temp_chunks.append(swap_endian(chunk))
    return temp_chunks


def bit_shuffle(contents: bytes, word_size_bytes: int, bit_order: list[int]) -> bytearray:
    '''Reshuffle bits in a blob using the specified order'''
    # This is a SLOW operation no matter what.
    # Given an example from SFA1:
    # - Bitwise math: ~17.5s
    # - Native Shuffle, bit map as we go: ~12.1s
    # - Native Shuffle, bit map as we go, but use += instead of extend: ~12.0s
    # - Native Shuffle, outer loop via chunker generator, bit map as we go, but use += instead of extend: ~12.8s
    # - Native Shuffle, bit map append as we go, but use += instead of extend: ~13.8s
    # - Native Shuffle, dump all in bitarray and change in place: ~12.5s
    # - Native Shuffle, dump all in bitarray, use itertools generator, use += instead of extend: ~11.2s
    # - Native Shuffle, dump all in bitarray, use itertools generator, use += and explicit tobytes instead of extend: ~11.2s
    # - Native Shuffle, dump all in bitarray, use itertools generator, don't clean updated_word,use += and explicit tobytes instead of extend: ~10.8s
    # - Full numpy process: ~19.0s
    # - Numpy Shuffle, assuming already numpy array: ~19.0s
    # - Numpy Shuffle, without pack/unpack: ~18.9s
    # - Numpy Shuffle ONLY replacing bitarray: ~37.0s
    # - Numpy Shuffle array: ~30.0s and it still isn't modifying in place
    # Also, things that don't seem to work:
    # - more_itertools.grouper gets int arrays instead of byte arrays
    # Other ideas:
    # - Use a memory view?

    # print(f"before: {hash_helper.get_crc(contents)}")
    # shuffle_start = time.perf_counter()
    def chunker(iterable, size, fillvalue=None):
        args = [iter(iterable)] * size
        return itertools.zip_longest(*args, fillvalue=fillvalue)
    word_size_bits = word_size_bytes*8
    bit_contents = bitarray()
    bit_contents.frombytes(contents)
    new_content = bytearray()
    updated_word = bitarray(word_size_bits*'0')
    for shuffle_word in chunker(bit_contents, word_size_bits):
        # Perform shuffle
        for idx, next_bit in enumerate(bit_order):
            updated_word[idx] = shuffle_word[next_bit]
        # Append to output
        new_content += updated_word.tobytes()
    return new_content


def split_bit_shuffle(contents: bytes, word_size_bytes: int, bit_order: list[int], num_ways: int) -> list[bytearray]:
    '''Reshuffle bits in a blob using the specified order into an array of blobs'''
    new_chunks = []
    for curr_way in range(0, num_ways):
        new_chunks.append(bytearray())

    num_shuffles = len(contents)//word_size_bytes
    shuffle_word = bitarray()
    updated_word = bitarray(word_size_bytes*8*'0')
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word.clear()
        shuffle_word.frombytes(contents[offset:offset+word_size_bytes])

        updated_word.setall(0)
        j = 0
        for next_bit in bit_order:
            updated_word[j] = shuffle_word[next_bit]
            j = j + 1

        offset = 0
        split_shuffle_length = word_size_bytes*8//num_ways
        for curr_way in range(0, num_ways):
            end = offset+split_shuffle_length
            new_chunks[curr_way] += updated_word[offset:end]
            offset = end

    return new_chunks


def byte_shuffle(contents: bytes, word_size_bytes: int, byte_order: list[int]) -> bytearray:
    '''Reshuffle bytes in a blob using the specified order'''
    new_content = bytearray()
    num_shuffles = len(contents)//word_size_bytes
    updated_word = bytearray(word_size_bytes)
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word = bytearray(contents[offset:offset+word_size_bytes])

        updated_word.clear()
        for idx, next_byte in enumerate(byte_order):
            updated_word[idx] = shuffle_word[next_byte]

        new_content += updated_word
    return new_content
