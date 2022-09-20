'''Utility Functions specifically for SNK40'''
import logging
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

def build_snk_rom(mame_name, bundle_contents, func_map):
    '''Helper to compact the logging output and build call'''
    logger.info(f"Building {mame_name}...")
    out_file = {'filename': mame_name, 'contents': helpers.build_rom(bundle_contents, func_map)}
    logger.info(f"Extracted {mame_name}.")
    return out_file

def simple_palette_helper(in_file_ref, pal_filenames):
    '''Rebuild RGB Palette ROMs'''
    def palette(in_files):
        in_data = in_files[in_file_ref]
        pal_contents = transforms.deinterleave_nibble(in_data, 4)
        del pal_contents[2] # Remove the spacing entry
        return dict(zip(pal_filenames, pal_contents))
    return palette

def palette_rebuild_helper(file_metas, in_file_name):
    '''Helper to use generate_snk_palette_file to bit reorder a shuffled palette'''
    def palette(in_files):
        contents = in_files[in_file_name]
        return generate_snk_palette_file(file_metas, contents)
    return palette

def generate_snk_palette_file(filenames, contents):
    '''Given a set of CRC/SHA/size, generate a set nibble-based palette file via reordering'''

    # Apply the shuffle
    bit_shuffle_order = [1, 2, 12, 13, 4, 5, 6, 0, 8, 9, 10, 11, 7, 3, 14, 15]
    shuffled_contents = transforms.bit_shuffle(contents, 2, bit_shuffle_order)

    # Deinterleave the result
    pal_contents = transforms.deinterleave_nibble(shuffled_contents, 4)
    del pal_contents[2] # Remove the spacing entry

    return dict(zip(filenames, pal_contents))


# This is the original function used to search for the Palette reorder pattern
# As it was discovered that the shuffle order is always the same, we can do this MUCH faster.
# Keeping this function for posterity/future use
# def search_snk_palette_file(file_metas, in_data):
#     '''Given a set of CRC/SHA/size, generate a set nibble-based palette file via reordering'''

#     # move to a bit array
#     in_data_bits = bitarray()
#     in_data_bits.frombytes(in_data)

#     # get rid of 3rd nibbles
#     for i in range(len(in_data_bits), 0, -16):
#         del in_data_bits[i-8:i-4]

#     bit_order_pool = list(range(0,12))

#     out_files = {}

#     # Try each permutation (11800 permutations!)
#     for count, curr_permutation in enumerate(itertools.permutations(bit_order_pool, 4)):

#         # Build the output file
#         out_bitarray = bitarray()
#         for set_offset in range(0, len(in_data_bits), 12):
#             out_bitarray.extend(bitarray('0000'))
#             for src_bit in curr_permutation:
#                 out_bitarray.append(in_data_bits[set_offset + src_bit])

#         # Get the CRC
#         out_bytes = out_bitarray.tobytes()
#         crc = hash_helper.get_crc(out_bytes)

#         for file_meta in file_metas:
#             if (crc == file_meta['crc']):
#                 print(f"CRC HIT at {count} with {str(list(curr_permutation))}!")
#                 sha = hash_helper.get_sha1(out_bytes)
#                 if (sha == file_meta['sha']):
#                     print(f"SHA HIT at {count} with {str(list(curr_permutation))}!")
#                     out_files[file_meta['filename']] = out_bytes

#         if len(file_metas) == len(out_files):
#             break

#     return out_files
