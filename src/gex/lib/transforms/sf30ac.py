

# Extraction Script for Street Fighter 30th Anniversary Collection

import glob
import zipfile
import logging
import os
import io

from gex.lib.utils.blob import transforms
from gex.lib.utils.vendor import capcom
from gex.lib.contrib.bputil import BPListReader

logger = logging.getLogger('gextoolbox')

title = "Street Fighter 30th Anniversary Collection"
description = ""
default_folder = "C:\Program Files (x86)\Steam\steamapps\common\Street Fighter 30th Anniversary Collection"
in_dir_desc = "SF30AC Steam folder"

pkg_name_map = {
    'bundleStreetFighter.mbundle': 'sf',
    'bundleStreetFighterAlpha.mbundle': 'sfa',
    'bundleStreetFighterAlpha2.mbundle': 'sfa2',
    'bundleStreetFighterAlpha3.mbundle': 'sfa3',
    'bundleStreetFighterII.mbundle': 'sf2',
    'bundleStreetFighterIII.mbundle': 'sf3',
    'bundleStreetFighterIII_2ndImpact.mbundle': 'sf3_2i',
    'bundleStreetFighterIII_3rdStrike.mbundle': 'sf3_3s',
    'bundleStreetFighterII_CE.mbundle': 'sf2ce',
    'bundleStreetFighterII_HF.mbundle': 'sf2hf',
    'bundleSuperStreetFighterII.mbundle': 'ssf2',
    'bundleSuperStreetFighterIITurbo.mbundle': 'ssf2t'
}

def write_temp_file(contents, path):
    with open(path, 'wb') as out_file:
        out_file.write(contents)

def find_files(base_path):
    bundle_path = os.path.join(base_path, "Bundle", '*.mbundle') 
    archive_list = glob.glob(bundle_path)
    return archive_list

def build_zip_file(entries):
    # Build the new zip file
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in entries.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()

def build_rom(in_files, func_map):
    new_data = dict()
    for func in func_map.values():
        new_data.update(func(in_files))
    return build_zip_file(new_data)

def save_in_files(in_files):
    out_files = []
    for key, value in in_files.items():
        out_files.append({'filename': key, 'contents': value})
    return out_files

def process_simm_common(simm_id, simm_prefix, simm_size_bytes):
    def process_simm(in_files):
        contents = in_files[simm_id]
        num_chunks = len(contents)//simm_size_bytes
        filenames = list(map(lambda x:f'{simm_prefix}-{simm_id}.{x}', range(0,num_chunks)))
        chunks = transforms.equal_split(contents, chunk_size = simm_size_bytes)
        return dict(zip(filenames, chunks))
    return process_simm

def name_file(in_file_ref, filename):
    def rename_from(in_files):
        return {filename: in_files[in_file_ref]}
    return rename_from

def deshuffle_gfx_common(filenames, num_interim_split, final_split = None):
    def gfx(in_files):
        contents = in_files['vrom']
        
        # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
        contents = capcom.common_gfx_deshuffle(contents)

        # Split into even chunks
        chunks = transforms.equal_split(contents, num_chunks=num_interim_split)

        # Interleave each pair of chunks
        new_chunks = []
        for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
            new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
        chunks = new_chunks

        # Merge the chunks back together
        contents = transforms.merge(chunks)

        # Deinterleave the chunks into our 4 files
        chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)

        # Do final split if provided
        if final_split:
            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(transforms.custom_split(oldchunk, final_split))
            chunks = new_chunks

        return dict(zip(filenames, chunks))
    return gfx

def cps1_gfx_deinterleave(contents, num_ways=4, word_size=2):
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

    interleave_group_length = num_ways * word_size
    num_interleave_groups = len(contents)//interleave_group_length
    temp_chunks = [bytearray() for i in range(num_ways)]
    for i in range(0, num_interleave_groups):
        offset = i * interleave_group_length
        interleave_group = contents[offset:offset+interleave_group_length]
        interleave_group = decode_cps1_gfx(interleave_group)
        interleave_offset = 0
        for j in range(0, num_ways):
            interleave_end = interleave_offset + word_size
            temp_chunks[j].extend(interleave_group[interleave_offset:interleave_end])
            interleave_offset = interleave_end
    return temp_chunks

def placeholder_generator(file_map):
    def create_placeholders(contents):
        out_files = {}
        for filename, size in file_map.items():
            out_files[filename] = bytes(size*b'\0')
        return out_files  
    return create_placeholders

def equal_split_helper(in_file_ref, filenames):
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.equal_split(contents, num_chunks = len(filenames))
        return dict(zip(filenames, chunks))
    return split

################################################################################
# START Street Fighter                                                         #
################################################################################

    # sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".bplanes.rom", ["sf-39.2k", "sf-38.1k", "sf-41.4k", "sf-40.3k"], 128 * 1024))
    # sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".mplanes.rom", ["sf-25.1d", "sf-28.1e", "sf-30.1g", "sf-34.1h", "sf-26.2d", "sf-29.2e", "sf-31.2g", "sf-35.2h"], 128 * 1024))
    # sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".sprites.rom", ["sf-15.1m", "sf-16.2m", "sf-11.1k", "sf-12.2k", "sf-07.1h", "sf-08.2h", "sf-03.1f", "sf-17.3m", "sf-18.4m", "sf-13.3k", "sf-14.4k", "sf-09.3h", "sf-10.4h","sf-05.3f"], 128 * 1024))
    # sf30th_sf.files.append(RenameGameFile(sf30th_sf.extracted_folder_name +".alpha.rom", "sf-27.4d"))
    # sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".maps.rom", ["sf-37.4h", "sf-36.3h", "sf-32.3g", "sf-33.4g"], 64 * 1024))
    # sf30th_sf.files.append(RenameGameFile(sf30th_sf.extracted_folder_name +".z80", "sf-02.7k"))
    # sf30th_sf.files.append(SplitGameFile(sf30th_sf.extracted_folder_name +".u.samples.rom", ["sfu-00.1h", "sf-01.1k"], 128 * 1024))
    # sf30th_sf.files.append(SplitGameFileEvenOdd(sf30th_sf.extracted_folder_name +".u.68k", [("sfd-19.2a", "sfd-22.2c"),("sfd-20.3a", "sfd-23.3c"),("sfd-21.4a", "sfd-24.4c")], 64 * 1024))

def handle_sf(mbundle_entries):
    # C:\Program Files (x86)\Steam\steamapps\common\Street Fighter 30th Anniversary Collection\Bundle\bundleStreetFighter.mbundle
    # StreetFighter.z80
    # StreetFighter.alpha.rom
    # StreetFighter.u.68k
    # StreetFighter.sprites.rom
    # StreetFighter.u.samples.rom
    # StreetFighter.maps.rom
    # StreetFighter.bplanes.rom
    # StreetFighter.mplanes.rom

    func_map = {}
    in_files = {}
    in_files['z80'] = mbundle_entries.get("StreetFighter.z80")
    in_files['alpha'] = mbundle_entries.get("StreetFighter.alpha.rom")
    in_files['68k'] = mbundle_entries.get("StreetFighter.u.68k")
    in_files['sprites'] = mbundle_entries.get("StreetFighter.sprites.rom")
    in_files['samples'] = mbundle_entries.get("StreetFighter.u.samples.rom")
    in_files['maps'] = mbundle_entries.get("StreetFighter.maps.rom")
    in_files['bplanes'] = mbundle_entries.get("StreetFighter.bplanes.rom")
    in_files['mplanes'] = mbundle_entries.get("StreetFighter.mplanes.rom")

    bplanes_filenames = [
        "sf-39.2k", 
        "sf-38.1k", 
        "sf-41.4k", 
        "sf-40.3k"
    ]
    func_map['bplanes'] = equal_split_helper('bplanes', bplanes_filenames)

    mplanes_filenames = [
        "sf-25.1d", 
        "sf-28.1e", 
        "sf-30.1g", 
        "sf-34.1h", 
        "sf-26.2d", 
        "sf-29.2e", 
        "sf-31.2g", 
        "sf-35.2h"
    ]
    func_map['mplanes'] = equal_split_helper('mplanes', mplanes_filenames)

    sprites_filenames = [
        "sf-15.1m", 
        "sf-16.2m", 
        "sf-11.1k", 
        "sf-12.2k", 
        "sf-07.1h", 
        "sf-08.2h", 
        "sf-03.1f", 
        "sf-17.3m", 
        "sf-18.4m", 
        "sf-13.3k", 
        "sf-14.4k", 
        "sf-09.3h", 
        "sf-10.4h",
        "sf-05.3f"
    ]
    func_map['sprites'] = equal_split_helper('sprites', sprites_filenames)

    func_map['alpha'] = name_file("alpha", "sf-27.4d")

    maps_filenames = [
        "sf-37.4h", 
        "sf-36.3h", 
        "sf-32.3g", 
        "sf-33.4g"
    ]
    func_map['maps'] = equal_split_helper('maps', maps_filenames)

    func_map['z80'] = name_file("z80", "sf-02.7k")

    samples_filenames = [
        "sfu-00.1h", 
        "sf-01.1k"
    ]
    func_map['samples'] = equal_split_helper('samples', samples_filenames)

    maincpu_filenames = [
        "sfd-19.2a", 
        "sfd-22.2c",
        "sfd-20.3a", 
        "sfd-23.3c",
        "sfd-21.4a", 
        "sfd-24.4c"  
    ] 
    def maincpu(in_files):
        contents = in_files['68k']
        chunks = transforms.equal_split(contents, num_chunks = 3)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
        chunks = new_chunks

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    ph_files = {
        'mb7114h.12k': 0x100,
        'mb7114h.11h': 0x100,
        'mb7114h.12j': 0x100,
        'mmi-7603.13h': 0x020,
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    out_files = []
    out_files.append({'filename': 'sf.zip', 'contents': build_rom(in_files, func_map)})
    return out_files

################################################################################
# END Street Fighter                                                           #
################################################################################


################################################################################
# START Street Fighter 2                                                       #
################################################################################

def handle_sf2(mbundle_entries):
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterII.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterII.z80')
    in_files['oki'] = mbundle_entries.get('StreetFighterII.oki')
    in_files['ub68k'] = mbundle_entries.get('StreetFighterII.ub.68k')

    # audiocpu
    audiocpu_filenames = [   
        "sf2_9.12a"
    ]
    def audiocpu(in_files):
        contents = in_files['z80']
        return dict(zip(audiocpu_filenames, [contents]))
    func_map['audiocpu'] = audiocpu

    # maincpu
    maincpu_filenames = [
        'sf2_30a.bin',
        'sf2u.37b',
        'sf2_31a.bin',
        'sf2_38a.bin',
        'sf2_28a.bin',
        'sf2_35a.bin',
        'sf2_29a.bin',
        'sf2_36a.bin'
    ]
    def maincpu(in_files):
        contents = in_files['ub68k']
        chunks = transforms.equal_split(contents, num_chunks = 4)
        
        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
        chunks = new_chunks

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    # gfx
    gfx_filenames = [
        "sf2_06.bin", 
        "sf2_08.bin", 
        "sf2_05.bin", 
        "sf2_07.bin",
        "sf2_15.bin", 
        "sf2_17.bin", 
        "sf2_14.bin", 
        "sf2_16.bin",
        "sf2_25.bin", 
        "sf2_27.bin", 
        "sf2_24.bin", 
        "sf2_26.bin"
    ]
    def gfx(in_files):
        contents = in_files['vrom']
        chunks = transforms.equal_split(contents, num_chunks=3)

        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(cps1_gfx_deinterleave(oldchunk, num_ways=4, word_size=2))
        chunks = new_chunks
        return dict(zip(gfx_filenames, chunks))
    func_map['gfx'] = gfx

    # oki
    oki_filenames = [   
        'sf2_18.11c',
        'sf2_19.12c'
    ]
    def oki(in_files):
        chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
        return dict(zip(oki_filenames, chunks))
    func_map['oki'] = oki


    ph_files = {
        'buf1': 0x117,
        'c632.ic1': 0x117,
        'ioa1': 0x117,
        'iob1.11d': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'stf29.1a': 0x117
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    return [{'filename': 'sf2ub.zip', 'contents': build_rom(in_files, func_map)}]

################################################################################
# END Street Fighter 2                                                         #
################################################################################


################################################################################
# START Street Fighter Alpha                                                   #
################################################################################

def handle_sfa(mbundle_entries):
    out_files = []
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterAlpha.z80')
    in_files['qs'] = mbundle_entries.get('StreetFighterAlpha.qs')
    in_files['nv'] = mbundle_entries.get('StreetFighterAlpha.nv')
    in_files['ub68k'] = mbundle_entries.get('StreetFighterAlpha.u.68k')
    in_files['ub68y'] = mbundle_entries.get('StreetFighterAlpha.u.68y')

    # maincpu
    maincpu_filenames = [
        'sfzu.03a',
        'sfz.04a',
        'sfz.05a',
        'sfz.06'
    ]
    def maincpu(in_files):
        contents = in_files['ub68k']
        contents = transforms.swap_endian(contents)
        chunks = transforms.equal_split(contents, num_chunks = 4)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    #vrom
    vrom_filenames = [
        "sfz.14m",
        "sfz.16m",
        "sfz.18m",
        "sfz.20m",
    ]
    func_map['vrom'] = deshuffle_gfx_common(vrom_filenames, 8)


    # z80
    z80_filenames = [   
        'sfz.01',
        'sfz.02'
    ]
    def z80(in_files):
        chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
        return dict(zip(z80_filenames, chunks))
    func_map['z80'] = z80


    # qsound
    qsound_filenames = [   
        'sfz.11m',
        'sfz.12m'
    ]
    def qsound(in_files):
        chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(qsound_filenames, chunks))
    func_map['qsound'] = qsound
    out_files.append({'filename': 'sfau.zip', 'contents': build_rom(in_files, func_map)})

    return out_files

################################################################################
# END Street Fighter Alpha                                                     #
################################################################################


################################################################################
# START Street Fighter Alpha 2                                                 #
################################################################################

def handle_sfa2(mbundle_entries):
    out_files = []
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha2.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterAlpha2.z80')
    in_files['qs'] = mbundle_entries.get('StreetFighterAlpha2.qs')
    in_files['u168k'] = mbundle_entries.get('StreetFighterAlpha2.u1.68k')

    maincpu_filenames = [
        "sz2u.03",
        "sz2u.04",
        "sz2u.05",
        "sz2u.06",
        "sz2u.07",
        "sz2u.08"
    ]
    def maincpu(in_files):
        contents = in_files['u168k']
        contents = transforms.swap_endian(contents)
        chunks = transforms.equal_split(contents, num_chunks = 6)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    vrom_filenames = [
        "sz2.13m",
        "sz2.14m",
        "sz2.15m",
        "sz2.16m",
        "sz2.17m",
        "sz2.18m",
        "sz2.19m",
        "sz2.20m"
    ]
    func_map['vrom'] = deshuffle_gfx_common(vrom_filenames, 20, final_split = [0x400000, 0x100000])

    # z80
    z80_filenames = [   
        'sz2.01a',
        'sz2.02a'
    ]
    def z80(in_files):
        chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
        return dict(zip(z80_filenames, chunks))
    func_map['z80'] = z80

    # qsound
    qsound_filenames = [   
        'sz2.11m',
        'sz2.12m'
    ]
    def qsound(in_files):
        chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(qsound_filenames, chunks))
    func_map['qsound'] = qsound

    out_files.append({'filename': 'sfa2u.zip', 'contents': build_rom(in_files, func_map)})

    return out_files

################################################################################
# END Street Fighter Alpha 2                                                   #
################################################################################


################################################################################
# START Street Fighter Alpha 3                                                 #
################################################################################

def handle_sfa3(mbundle_entries):
    out_files = []
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha3.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterAlpha3.z80')
    in_files['qs'] = mbundle_entries.get('StreetFighterAlpha3.qs')
    in_files['u168k'] = mbundle_entries.get('StreetFighterAlpha3.u.68k')

    maincpu_filenames = [
        "sz3u.03c",
        "sz3u.04c",
        "sz3.05c",
        "sz3.06c",
        "sz3.07c",
        "sz3.08c",
        "sz3.09c",
        "sz3.10b"
    ]
    def maincpu(in_files):
        contents = in_files['u168k']
        contents = transforms.swap_endian(contents)
        chunks = transforms.equal_split(contents, num_chunks = 8)

        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    vrom_filenames = [
        "sz3.13m",
        "sz3.14m",
        "sz3.15m",
        "sz3.16m",
        "sz3.17m",
        "sz3.18m",
        "sz3.19m",
        "sz3.20m"
    ]
    func_map['vrom'] = deshuffle_gfx_common(vrom_filenames, 32, final_split = [0x400000, 0x400000])

    # z80
    z80_filenames = [   
        'sz3.01',
        'sz3.02'
    ]
    def z80(in_files):
        chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
        return dict(zip(z80_filenames, chunks))
    func_map['z80'] = z80

    # qsound
    qsound_filenames = [   
        'sz3.11m',
        'sz3.12m'
    ]
    def qsound(in_files):
        chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(qsound_filenames, chunks))
    func_map['qsound'] = qsound

    out_files.append({'filename': 'sfa3u.zip', 'contents': build_rom(in_files, func_map)})

    return out_files

################################################################################
# END Street Fighter Alpha 3                                                   #
################################################################################


################################################################################
# START Street Fighter 3                                                       #
################################################################################

def sf3_common(mbundle_entries, in_bios_filename, in_simm_bank_files, simm_prefix, bios_filename, mame_name):
    out_files = []
    func_map = {}
    in_files = {}
    simm_size = 2*1024*1024
    for simm_bank_num, simm_filename in in_simm_bank_files.items():
        bank_name = f'simm{simm_bank_num}'
        in_files[bank_name] = mbundle_entries.get(simm_filename)
        func_map[bank_name] = process_simm_common(bank_name, simm_prefix, simm_size)

    in_files['bios'] = mbundle_entries.get(in_bios_filename)
    func_map['bios'] = name_file("bios", bios_filename)

    out_files.append({'filename': mame_name, 'contents': build_rom(in_files, func_map)})

    return out_files

def handle_sf3(mbundle_entries):
    in_prefix = "StreetFighterIII"
    in_simm_bank_nums = [1, 3, 4, 5]
    in_simm_files = dict(zip(in_simm_bank_nums, list(map(lambda x:f'{in_prefix}.s{x}', in_simm_bank_nums))))
    in_bios_file = f'{in_prefix}.bios'
    return sf3_common(mbundle_entries, in_bios_file, in_simm_files, 'sfiii', "sfiii_asia_nocd.29f400.u2", 'sfiiina.zip')

################################################################################
# END Street Fighter 3                                                         #
################################################################################


################################################################################
# START Street Fighter 3 2nd Impact                                            #
################################################################################

def handle_sf3_2i(mbundle_entries):
    in_prefix = "StreetFighterIII_2ndImpact"
    in_simm_bank_nums = list(range(1,6))
    in_simm_files = dict(zip(in_simm_bank_nums, list(map(lambda x:f'{in_prefix}.s{x}', in_simm_bank_nums))))
    in_bios_file = f'{in_prefix}.bios'
    return sf3_common(mbundle_entries, in_bios_file, in_simm_files, 'sfiii2', "sfiii2_asia_nocd.29f400.u2", 'sfiii2n.zip')

################################################################################
# END Street Fighter 3 2nd Impact                                              #
################################################################################


################################################################################
# START Street Fighter 3 3rd Strike                                            #
################################################################################

def handle_sf3_3s(mbundle_entries):
    in_prefix = "StreetFighterIII_3rdStrike"
    in_simm_files = {
        1: f'{in_prefix}.r1.s1',
        2: f'{in_prefix}.r1.s2',
        3: f'{in_prefix}.s3',
        4: f'{in_prefix}.s4',
        5: f'{in_prefix}.s5',
        6: f'{in_prefix}.s6'
    }
    in_bios_file = f'{in_prefix}.bios'
    return sf3_common(mbundle_entries, in_bios_file, in_simm_files, 'sfiii3', "sfiii3_japan_nocd.29f400.u2", 'sfiii3nr1.zip')

################################################################################
# END Street Fighter 3 3rd Strike                                              #
################################################################################


################################################################################
# START Street Fighter 2 Championship Edition                                  #
################################################################################

def handle_sf2ce(mbundle_entries):
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterII_CE.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterII_CE.z80')
    in_files['oki'] = mbundle_entries.get('StreetFighterII_CE.oki')
    in_files['68k'] = mbundle_entries.get('StreetFighterII_CE.ua.68k')

    # audiocpu
    audiocpu_filenames = [   
        "s92_09.bin"
    ]
    def audiocpu(in_files):
        contents = in_files['z80']
        return dict(zip(audiocpu_filenames, [contents]))
    func_map['audiocpu'] = audiocpu

    # maincpu
    maincpu_filenames = [
        "s92u-23a", 
        "sf2ce.22",
        "s92_21a.bin"
    ]
    def maincpu(in_files):
        contents = in_files['68k']
        chunks = transforms.equal_split(contents, num_chunks = 3)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    # gfx
    gfx_filenames = [
        "s92_01.bin",
        "s92_02.bin", 
        "s92_03.bin", 
        "s92_04.bin",
        "s92_05.bin", 
        "s92_06.bin", 
        "s92_07.bin", 
        "s92_08.bin",
        "s92_10.bin",
        "s92_11.bin", 
        "s92_12.bin", 
        "s92_13.bin"
    ]
    def gfx(in_files):
        contents = in_files['vrom']
        chunks = transforms.equal_split(contents, num_chunks=3)

        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(cps1_gfx_deinterleave(oldchunk, num_ways=4, word_size=2))
        chunks = new_chunks
        return dict(zip(gfx_filenames, chunks))
    func_map['gfx'] = gfx

    # oki
    oki_filenames = [   
        's92_18.bin',
        's92_19.bin'
    ]
    def oki(in_files):
        chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
        return dict(zip(oki_filenames, chunks))
    func_map['oki'] = oki


    ph_files = {
        'bprg1.11d': 0x117,
        'buf1': 0x117,
        'c632.ic1': 0x117,
        'ioa1': 0x117,
        'iob1.12d': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'ioc1.ic7': 0x104
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    return [{'filename': 'sf2ceua.zip', 'contents': build_rom(in_files, func_map)}]

################################################################################
# END Street Fighter 2 Championship Edition                                    #
################################################################################


################################################################################
# START Street Fighter 2 Hyper Fighting                                        #
################################################################################
    
def handle_sf2hf(mbundle_entries):
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('StreetFighterII_HF.u.vrom')
    in_files['z80'] = mbundle_entries.get('StreetFighterII_HF.z80')
    in_files['oki'] = mbundle_entries.get('StreetFighterII_HF.oki')
    in_files['68k'] = mbundle_entries.get('StreetFighterII_HF.u.68k')

    # audiocpu
    audiocpu_filenames = [   
        "s92_09.bin"
    ]
    def audiocpu(in_files):
        contents = in_files['z80']
        return dict(zip(audiocpu_filenames, [contents]))
    func_map['audiocpu'] = audiocpu

    # maincpu
    maincpu_filenames = [
        "sf2_23a",
        "sf2_22.bin",
        "sf2_21.bin"
    ]
    def maincpu(in_files):
        contents = in_files['68k']
        chunks = transforms.equal_split(contents, num_chunks = 3)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    # gfx
    gfx_filenames = [
        "s92_01.bin", 
        "s92_02.bin", 
        "s92_03.bin", 
        "s92_04.bin",
        "s92_05.bin", 
        "s92_06.bin", 
        "s92_07.bin", 
        "s92_08.bin",
        "s2t_10.bin", 
        "s2t_11.bin", 
        "s2t_12.bin", 
        "s2t_13.bin"
    ]
    def gfx(in_files):
        contents = in_files['vrom']
        chunks = transforms.equal_split(contents, num_chunks=3)

        new_chunks = []
        for oldchunk in chunks:
            new_chunks.extend(cps1_gfx_deinterleave(oldchunk, num_ways=4, word_size=2))
        chunks = new_chunks
        return dict(zip(gfx_filenames, chunks))
    func_map['gfx'] = gfx

    # oki
    oki_filenames = [   
        's92_18.bin',
        's92_19.bin'
    ]
    def oki(in_files):
        chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
        return dict(zip(oki_filenames, chunks))
    func_map['oki'] = oki


    ph_files = {
        'bprg1.11d': 0x117,
        'buf1': 0x117,
        'c632.ic1': 0x117,
        'ioa1': 0x117,
        'iob1.12d': 0x117,
        'prg1': 0x117,
        'rom1': 0x117,
        'sou1': 0x117,
        'ioc1.ic7': 0x104
    }
    func_map['placeholders'] = placeholder_generator(ph_files)

    return [{'filename': 'sf2t.zip', 'contents': build_rom(in_files, func_map)}]

################################################################################
# END Street Fighter 2 Hyper Fighting                                          #
################################################################################


################################################################################
# START Super Street Fighter 2                                                 #
################################################################################
    
def handle_ssf2(mbundle_entries):
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('SuperStreetFighterII.vrom')
    in_files['z80'] = mbundle_entries.get('SuperStreetFighterII.z80')
    in_files['qsound'] = mbundle_entries.get('SuperStreetFighterII.qs')
    in_files['68k'] = mbundle_entries.get('SuperStreetFighterII.u.68k')

    # audiocpu
    audiocpu_filenames = [   
        "ssf.01"
    ]
    def audiocpu(in_files):
        contents = in_files['z80']
        return dict(zip(audiocpu_filenames, [contents]))
    func_map['audiocpu'] = audiocpu

    # maincpu
    maincpu_filenames = [
        "ssfu.03a", 
        "ssfu.04a", 
        "ssfu.05", 
        "ssfu.06", 
        "ssfu.07"
    ]
    def maincpu(in_files):
        contents = in_files['68k']
        chunks = transforms.equal_split(contents, num_chunks = 5)
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    vrom_filenames = [
        "ssf.13m",
        "ssf.14m",
        "ssf.15m",
        "ssf.16m",
        "ssf.17m",
        "ssf.18m",
        "ssf.19m",
        "ssf.20m"
    ]
    func_map['vrom'] = deshuffle_gfx_common(vrom_filenames, 12, final_split = [0x200000, 0x100000])

    # qsound
    qsound_filenames = [   
        "ssf.q01", 
        "ssf.q02", 
        "ssf.q03", 
        "ssf.q04", 
        "ssf.q05", 
        "ssf.q06", 
        "ssf.q07", 
        "ssf.q08"
    ]
    def qsound(in_files):
        chunks = transforms.equal_split(in_files['qsound'], num_chunks=8)
        return dict(zip(qsound_filenames, chunks))
    func_map['qsound'] = qsound

    return [{'filename': 'ssf2u.zip', 'contents': build_rom(in_files, func_map)}]

################################################################################
# END Super Street Fighter 2                                                   #
################################################################################


################################################################################
# START Super Street Fighter 2 Turbo                                           #
################################################################################

def handle_ssf2t(mbundle_entries):
    func_map = {}
    in_files = {}
    in_files['vrom'] = mbundle_entries.get('SuperStreetFighterIITurbo.vrom')
    in_files['z80'] = mbundle_entries.get('SuperStreetFighterIITurbo.z80')
    in_files['qsound'] = mbundle_entries.get('SuperStreetFighterIITurbo.qs')
    in_files['68k'] = mbundle_entries.get('SuperStreetFighterIITurbo.u.68k')

    # audiocpu
    audiocpu_filenames = [   
        "sfx.01",   
        "sfx.02"
    ]
    def audiocpu(in_files):
        contents = in_files['z80']
        chunks = transforms.equal_split(contents, num_chunks = len(audiocpu_filenames))
        return dict(zip(audiocpu_filenames, chunks))
    func_map['audiocpu'] = audiocpu

    # maincpu
    maincpu_filenames = [
        "sfxu.03e", 
        "sfxu.04a", 
        "sfxu.05", 
        "sfxu.06b", 
        "sfxu.07a", 
        "sfxu.08", 
        "sfx.09"
    ]
    def maincpu(in_files):
        contents = in_files['68k']
        chunks = transforms.equal_split(contents, num_chunks = len(maincpu_filenames))
        chunks = transforms.swap_endian_all(chunks)
        return dict(zip(maincpu_filenames, chunks))
    func_map['maincpu'] = maincpu

    vrom_filenames = [
        "sfx.13m",
        "sfx.14m",
        "sfx.21m",
        "sfx.15m",
        "sfx.16m",
        "sfx.23m",
        "sfx.17m",
        "sfx.18m",
        "sfx.25m", 
        "sfx.19m",
        "sfx.20m",
        "sfx.27m"
    ]
    func_map['vrom'] = deshuffle_gfx_common(vrom_filenames, 16, final_split = [0x200000, 0x100000, 0x100000])

    # qsound
    qsound_filenames = [   
        "sfx.11m", 
        "sfx.12m",
    ]
    def qsound(in_files):
        chunks = transforms.equal_split(in_files['qsound'], num_chunks=2)
        return dict(zip(qsound_filenames, chunks))
    func_map['qsound'] = qsound

    return [{'filename': 'ssf2tu.zip', 'contents': build_rom(in_files, func_map)}]

################################################################################
# END Super Street Fighter 2 Turbo                                             #
################################################################################

def merged_rom_handler(merged_contents, func_map):
    new_data = dict()
    for func in func_map.values():
        new_data.update(func(bytearray(merged_contents)))

    # Build the new zip file
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in new_data.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()

def main(game_base_dir, out_path):
    bundle_files = find_files(game_base_dir)
    for file_path in bundle_files:
        with open(file_path, 'rb') as fp:
            file_name = os.path.basename(file_path)
            pkg_name = pkg_name_map.get(file_name)
            if pkg_name != None:
                logger.info(f'Reading files for {file_name}...')
                contents = fp.read()
                reader = BPListReader(contents)
                parsed = reader.parse()
                
                handler_func = globals().get(f'handle_{pkg_name}')

                if parsed != None and handler_func != None:
                    output_files = handler_func(parsed)
                        
                    for output_file in output_files:
                        with open(os.path.join(out_path, output_file['filename']), "wb") as out_file:
                            out_file.write(output_file['contents'])
                elif parsed == None:
                    logger.warning("Could not find merged rom data in mbundle.")
                elif handler_func == None:
                    logger.warning("Could not find matching handler function.")
            else:
                logger.info(f'Skipping {file_name} as it contains no known roms...')
    logger.info("""
        Processing complete. 
    """)
