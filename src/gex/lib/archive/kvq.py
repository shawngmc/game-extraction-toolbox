'''Module to handle KVQ files (Sega Smash Pack, Sega Puzzle Pack)'''

def extract(kvq_bytes, encode_string):
    '''Extract a sega pack kvq'''
    scramble = 6
    out_file = bytearray()
    for index, encoded_byte in enumerate(kvq_bytes[8:]):
        encode_string_character = encode_string[index % len(encode_string)]
        decoded_byte = ((encoded_byte ^ encode_string_character ^ 0x80) - scramble) & 0xFF
        out_file.append(decoded_byte)
        scramble += 3
    return out_file
