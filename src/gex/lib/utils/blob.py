from bitarray import bitarray

def merge(chunks):
    new_content = bytearray()
    for chunk in chunks:
        new_content.extend(chunk)
    return new_content

def custom_split(contents, chunk_sizes):
    if len(contents) != sum(chunk_sizes):
        raise Exception("Custom split needs the chunk_sizes to equal the input size.")

    num_chunks = len(chunk_sizes)
    start_offset = 0
    temp_chunks = []
    for i in range(0, num_chunks):
        temp_chunks.append(bytearray(contents[start_offset:start_offset+chunk_sizes[i]]))
        start_offset = start_offset + chunk_sizes[i]
    return temp_chunks


def equal_split(contents, num_chunks = None, chunk_size = None):
    if num_chunks == None and chunk_size == None:
        raise Exception("Equal split needs a number of slices to end up with and/or a chunk size.")
    elif num_chunks != None and chunk_size != None:
        if num_chunks * chunk_size != len(contents):
            raise Exception("Equal split received a number of slices to end up with and a chunk size, but these don't add up to the content length.")
    elif num_chunks == None:
        num_chunks = len(contents)//chunk_size
    else:
        chunk_size = len(contents)//num_chunks

    start_offset = 0
    temp_chunks = []
    for i in range(0, num_chunks):
        temp_chunks.append(bytearray(contents[start_offset:start_offset+chunk_size]))
        start_offset = start_offset + chunk_size
    return temp_chunks

def interleave(chunks, word_size):
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
            new_contents.extend(chunk[offset:offset+word_size])
    return new_contents



def deinterleave(contents, num_ways, word_size):
    interleave_group_length = num_ways * word_size
    num_interleave_groups = len(contents)//interleave_group_length
    temp_chunks = [bytearray() for i in range(num_ways)]
    for i in range(0, num_interleave_groups):
        offset = i * interleave_group_length
        interleave_group = contents[offset:offset+interleave_group_length]
        interleave_offset = 0
        for j in range(0, num_ways):
            interleave_end = interleave_offset + word_size
            temp_chunks[j].extend(interleave_group[interleave_offset:interleave_end])
            interleave_offset = interleave_end
    return temp_chunks


def deinterleave_all(chunks, num_ways, word_size):
    temp_chunks = []
    for chunk in chunks:
        temp_chunks.extend(deinterleave(chunk, num_ways, word_size))
    return temp_chunks


def truncate(contents, max_length):
    return contents[0:max_length]


def splice_out(contents, start, length=None, end=None):
    if length == None and end == None:
        raise Exception("Splice out needs a length or end value, but received neither.")
    elif length != None and end != None:
        raise Exception("Splice out needs a length or end value, but received both.")
    elif end == None:
        end = start + length

    new_contents = bytearray()
    new_contents.extend(contents[0:start])
    new_contents.extend(contents[end:len(contents)])
    return new_contents


def swap_endian(contents):
    new_contents = bytearray(len(contents))
    new_contents[0::2] = contents[1::2]
    new_contents[1::2] = contents[0::2]
    return new_contents


def swap_endian_all(chunks):
    temp_chunks = []
    for chunk in chunks:
        temp_chunks.append(swap_endian(chunk))
    return temp_chunks

def bit_shuffle(contents, word_size_bytes, bit_order):
    new_content = bytearray()    
    num_shuffles = len(contents)//word_size_bytes
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word = bitarray()
        shuffle_word.frombytes(contents[offset:offset+word_size_bytes])

        updated_word = bitarray(word_size_bytes*8*'0')
        i = 0
        for next_bit in bit_order:
            updated_word[i] = shuffle_word[next_bit]
            i = i + 1

        new_content.extend(updated_word)
    return new_content

def split_bit_shuffle(contents, word_size_bytes, bit_order, num_ways):
    new_chunks = []
    for x in range(0, num_ways):
        new_chunks.append(bytearray())
   
    num_shuffles = len(contents)//word_size_bytes
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word = bitarray()
        shuffle_word.frombytes(contents[offset:offset+word_size_bytes])

        updated_word = bitarray(word_size_bytes*8*'0')
        j = 0
        for next_bit in bit_order:
            updated_word[j] = shuffle_word[next_bit]
            j = j + 1

        offset = 0
        split_shuffle_length = word_size_bytes*8//num_ways
        for x in range(0, num_ways):
            end = offset+split_shuffle_length
            new_chunks[x].extend(updated_word[offset:end])
            offset = end

    return new_chunks

def byte_shuffle(contents, word_size_bytes, byte_order):
    new_content = bytearray()    
    num_shuffles = len(contents)//word_size_bytes
    for i in range(0, num_shuffles):
        offset = i*word_size_bytes
        shuffle_word = bytearray(contents[offset:offset+word_size_bytes])

        updated_word = bytearray(word_size_bytes)
        i = 0
        for next_byte in byte_order:
            updated_word[i] = shuffle_word[next_byte]
            i = i + 1

        new_content.extend(updated_word)
    return new_content