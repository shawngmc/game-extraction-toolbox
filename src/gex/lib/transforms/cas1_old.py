import traceback
import glob
import zipfile
import logging
import os
import io

from gex.lib.archive import kpka
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

# Standard processing:
# - Assume each zip in the KPKA is a game
# - Assume that the zip has a subfolder with the intended 'mame name' of the game

title = "Capcom Arcade Stadium 1 (OLD)"
description = "Capcom Arcade Stadium 1 as downloaded from depot using old manifests"
default_folder = "C:\Program Files (x86)\Steam\steamapps\content"
in_dir_desc = "SteamApps Content Folder"

pkg_name_map = {
    "1515951": "1943",
    "1556690": "Ghosts 'n Goblins",
    "1556700": "Vulgus",
    "1556701": "Pirate Ship Higemaru",
    "1556702": "1942",
    "1556703": "Commando",
    "1556704": "Section Z",
    "1556705": "Tatakai no Banka",
    "1556706": "Legendary Wings",
    "1556707": "Bionic Commando",
    "1556708": "Forgotton Worlds / Lost World",
    "1556709": "Ghouls 'n Ghosts (and 3 Wonders)",
    "1556710": "Strider",
    "1556711": "Dynasty Wars",
    "1556712": "Final Fight",
    "1556713": "1941 Counter Attack",
    "1556714": "Senjou no Ookami II",
    "1556715": "Mega Twins",
    "1556716": "Carrier Air Wing",
    "1556717": "Street Fighter II",
    "1556718": "Captain Commando",
    "1556719": "Varth Operation Thunderstorm",
    "1556720": "Warriors of Fate",
    "1556721": "Street Fighter II Hyper Fighting",
    "1556722": "Super Street Fighter II Turbo",
    "1556723": "Powered Gear: Strategic Variant Armor Equipment",
    "1556724": "Cyberbots: Fullmetal Madness",
    "1556725": "19XX: The War Against Destiny",
    "1556726": "Battle Circuit",
    "1556727": "Giga Wing",
    "1556728": "1944: The Loop Master",
    "1556729": "Progear"
}

def debug_print_kpka_contents(kpka_contents):
    for key, entry in kpka_contents.items():
        logger.debug(f'{key}: offset {entry["offset"]}, size {entry["size"]}')
        logger.debug(f'    {entry["contents"][0:30]}')

def debug_print_zip_contents(zip_bytes):
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as old_archive:
        zip_entries = list(old_archive.infolist())
        for file_entry in zip_entries:
            logger.debug(f'{file_entry.filename}')

def twiddle_zip(zip_bytes, remove_list = [], rename_dict = {}, lowercase_all = False):
    new_contents = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as old_archive:
        zip_entries = list(old_archive.infolist())
        with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            for file_entry in zip_entries:
                # Skip files to remove
                if not file_entry.filename in remove_list:
                    with old_archive.open(file_entry) as file_read_obj:
                        file_data = file_read_obj.read()
                        filename = file_entry.filename
                        # If a file needs renamed, do so
                        if filename in rename_dict.keys():
                            filename = rename_dict.get(filename)
                        # If filenames should be made lowercase, do so
                        if lowercase_all:
                            filename = filename.lower()
                        # add to new archive
                        new_archive.writestr(filename, file_data)
    return new_contents.getvalue()

def merged_rom_handler(zip_contents, func_map):
    new_data = dict()
    with zipfile.ZipFile(io.BytesIO(zip_contents), "r") as old_archive:
        zip_entries = list(old_archive.infolist())
        def getType(zip_entry):
            return zip_entry.filename.split('.')[1]
        for file_entry in zip_entries:
            # read in the entry - we need the body either way
            with old_archive.open(file_entry) as file_read_obj:
                file_data = file_read_obj.read()
                type_name = getType(file_entry)
                type_func = func_map.get(type_name)
                if type_func != None:
                    new_data.update(type_func(file_data))
    # Build the new zip file
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in new_data.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()

def weird_subzip_handler(kpka_contents, target_offset, subzip_filename):
    # Used for 3wonders in ghouls jp and 1941 in 1941j
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == target_offset:
                contents = file_entry['contents']
                subzip_contents = None
                with zipfile.ZipFile(io.BytesIO(contents), "r") as old_archive:
                    zip_entries = list(old_archive.infolist())
                    for file_entry in zip_entries:
                        if file_entry.filename == subzip_filename:
                            with old_archive.open(file_entry) as file_read_obj:
                                subzip_contents = file_read_obj.read()
                # If extra rom was found, save it off AND remove it from the main zip to allow processing
                if subzip_contents != None:
                    subzip_fixed = standard_kpka_contents_processing({'0': {'contents': subzip_contents}})[0]
                    out_files.append(subzip_fixed)
                    contents = twiddle_zip(contents, remove_list = [subzip_filename])
                other_zip = standard_kpka_contents_processing({'0': {'contents': contents}})[0]
                out_files.append(other_zip)
            else:
                other_zip = standard_kpka_contents_processing({'0': file_entry})[0]
                out_files.append(other_zip)
    return out_files

def handle_package_1515951(kpka_contents):
    out_files = []
    # Start with standard processing
    out_files = standard_kpka_contents_processing(kpka_contents)
    # Remove 1943j as it's just too broken
    out_files = list(filter(lambda i: i['filename'] != "1943j.zip", out_files))
    return out_files

def handle_package_1556690(kpka_contents):
    out_files = []
    # Start with standard processing
    out_files = standard_kpka_contents_processing(kpka_contents)
    for out_file in out_files:
        if out_file['filename'] == 'makaimurg.zip':
            out_file['contents'] = twiddle_zip(out_file['contents'], remove_list = ['gg1.bin'])
    return out_files

def handle_package_1556708(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352:
                contents = twiddle_zip(file_entry['contents'], lowercase_all=True)
                out_files.append({'filename': 'lostwrld.zip', 'contents': contents})
            else:
                # This is ok for standard processing
                ffightj_zip = standard_kpka_contents_processing({'0': file_entry})[0]
                out_files.append(ffightj_zip)
    return out_files

def handle_package_1556709(kpka_contents):
    return weird_subzip_handler(kpka_contents, 352, "3wondersu.zip")

def handle_package_1556710(kpka_contents):
    out_files = []
    # Start with standard processing
    out_files = standard_kpka_contents_processing(kpka_contents)
    for out_file in out_files:
        if out_file['filename'] == 'striderjr2.zip':
            out_file['filename'] = 'striderjr.zip'
        elif out_file['filename'] == 'striderua.zip':
            out_file['contents'] = twiddle_zip(out_file['contents'], remove_list = ['st24b2.1a'])
    return out_files

def handle_package_1556711(kpka_contents):
    out_files = []
    # Start with standard processing
    out_files = standard_kpka_contents_processing(kpka_contents)
    for out_file in out_files:
        if out_file['filename'] == 'dynwarj.zip':
            out_file['contents'] = twiddle_zip(out_file['contents'], remove_list = ['TK_14.BIN'])
    return out_files

def handle_package_1556712(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 1497211:
                contents = twiddle_zip(file_entry['contents'], lowercase_all=True)
                out_files.append({'filename': 'ffightu.zip', 'contents': contents})
            else:
                # This is ok for standard processing
                ffightj_zip = standard_kpka_contents_processing({'0': file_entry})[0]
                out_files.append(ffightj_zip)
    return out_files

def handle_package_1556713(kpka_contents):
    return weird_subzip_handler(kpka_contents, 352, "1941.zip")

def handle_package_1556714(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            # This is merjs; rename it
            out_files.append({'filename': 'mercsj.zip', 'contents': file_entry['contents']})
    return out_files

def handle_package_1556715(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 1511592:
                out_files.append({'filename': 'mtwins.zip', 'contents': file_entry['contents']})
            else:
                other_zip = standard_kpka_contents_processing({'0': file_entry})[0]
                out_files.append(other_zip)
    return out_files

def handle_package_1556716(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 1538278:
                out_files.append({'filename': 'cawingu.zip', 'contents': file_entry['contents']})
            else:
                other_zip = standard_kpka_contents_processing({'0': file_entry})[0]
                out_files.append(other_zip)
    return out_files

def handle_package_1556717(kpka_contents):
    out_files = standard_kpka_contents_processing(kpka_contents)
    for out_file in out_files:
        if out_file['filename'] == 'sf2ul.zip':
            out_file['filename'] = 'sf2um.zip'
            rename_dict = {
                "sf2_05(m1).bin": "sf2-1m.3a",
                "sf2_06(m5).bin": "sf2-5m.4a",
                "sf2_07(m3).bin": "sf2-3m.5a",
                "sf2_08(m7).bin": "sf2-7m.6a",
                "sf2_14(m2).bin": "sf2-2m.3c",
                "sf2_15(m6).bin": "sf2-6m.4c",
                "sf2_16(m4).bin": "sf2-4m.5c",
                "sf2_17(m8).bin": "sf2-8m.6c",
                "sf2_24(m9).bin": "sf2-9m.3d",
                "sf2_25(m13).bin": "sf2-13m.4d",
                "sf2_26(m11).bin": "sf2-11m.5d",
                "sf2_27(m15).bin": "sf2-15m.6d",
                "sf2_28m.bin": "sf-2u_28m.9e",
                "sf2_30m.bin": "sf-2u_30m.11e",
                "sf2_31m.bin": "sf-2u_31m.12e",
                "sf2_35m.bin": "sf-2u_35m.9f",
                "sf2_38m.bin": "sf-2u_38m.12f",
                "sf2j_29b.bin": "sf-2u_29m.10e",
                "sf2j_36b.bin": "sf-2u_36m.10f",
                "sf2u_09.bin": "sf2_09.12a",
                "sf2u_18.bin": "sf2_18.11c",
                "sf2u_19.bin": "sf2_19.12c",
                "sf2u_37m.bin": "sf-2u_37m.11f",
            }
            out_file['contents'] = twiddle_zip(out_file['contents'], rename_dict=rename_dict, lowercase_all=True)
    return out_files
    
def handle_package_1556718(kpka_contents):
    out_files = []
    # Start with standard processing
    out_files = standard_kpka_contents_processing(kpka_contents)
    # For each resulting zip, remove the optional and bad CRC files
    for out_file in out_files:
        out_file['contents'] = twiddle_zip(out_file['contents'], rename_dict={'c632b.ic1': 'c632.ic1'})
    return out_files

def handle_package_1556722(kpka_contents):
    out_files = []
    def gfx(contents):
        chunks = transforms.custom_split(contents, [8388608, 4194304, 4194304])
        chunks = transforms.deinterleave_all(chunks, num_ways=4, word_size=2)
        filenames = [
            'sfx.13m',
            'sfx.15m',
            'sfx.17m',
            'sfx.19m',
            'sfx.14m',
            'sfx.16m',
            'sfx.18m',
            'sfx.20m',
            'sfx.21m',
            'sfx.23m',
            'sfx.25m',
            'sfx.27m'
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x48000, length=0x8000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        chunks = transforms.equal_split(contents, num_chunks=2)
        filenames = [
            'sfx.01',
            'sfx.02'
        ]
        return dict(zip(filenames, chunks))
    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'sfx.11m',
            'sfx.12m'
        ]
        return dict(zip(filenames, chunks))

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #ssf2xj
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x380000, length=0x3FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=7)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "sfxj.03d", 
                        "sfxj.04a", 
                        "sfxj.05", 
                        "sfxj.06b", 
                        "sfxj.07a", 
                        "sfxj.08", 
                        "sfx.09"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'ssf2xj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #ssf2tu
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x380000, length=0x3FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=7)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "sfxu.03e", 
                        "sfxu.04a", 
                        "sfxu.05", 
                        "sfxu.06b", 
                        "sfxu.07a", 
                        "sfxu.08", 
                        "sfxu.09"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'ssf2tu.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556724(kpka_contents):
    out_files = []
    def gfx(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.deinterleave_all(chunks, num_ways=4, word_size=2)
        filenames = [   
            "cyb.13m", 
            "cyb.15m", 
            "cyb.17m", 
            "cyb.19m", 
            "cyb.14m", 
            "cyb.16m", 
            "cyb.18m", 
            "cyb.20m"
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x48000, length=0x8000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        chunks = transforms.equal_split(contents, num_chunks=2)

        return {
            'cyb.01': chunks[0],
            'cyb.02': chunks[1]
        }

    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)

        return {
            'cyb.11m': chunks[0],
            'cyb.12m': chunks[1]
        }

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #cybotsj
                func_map = {}

                def maincpu(contents):
                    chunks = transforms.equal_split(contents, num_chunks=8)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "cybj.03", 
                        "cybj.04", 
                        "cyb.05", 
                        "cyb.06", 
                        "cyb.07", 
                        "cyb.08", 
                        "cyb.09", 
                        "cyb.10"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'cybotsj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #cybotsu
                func_map = {}

                def maincpu(contents):
                    chunks = transforms.equal_split(contents, num_chunks=8)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "cybu.03", 
                        "cybu.04", 
                        "cyb.05", 
                        "cyb.06", 
                        "cyb.07", 
                        "cyb.08", 
                        "cyb.09", 
                        "cyb.10"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'cybotsu.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556725(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #19xxj
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x280000, length=0x180000)
                    chunks = transforms.equal_split(contents, num_chunks=5)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [    
                        '19xj.03a',
                        '19xj.04a',
                        '19xj.05a',
                        '19xj.06a',
                        '19xj.07a'
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu

                def gfx(contents):
                    contents = transforms.splice_out(contents, 0x200000, length=0x600000)
                    chunks = transforms.equal_split(contents, num_chunks=5)
                    chunks = transforms.deinterleave_all(chunks, num_ways=4, word_size=2)
                    filenames = [    
                        '19x-69.4j',
                        '19x-59.4d',
                        '19x-79.4m',
                        '19x-89.4p',
                        '19x-73.8j',
                        '19x-63.8d',
                        '19x-83.8m',
                        '19x-93.8p',
                        '19x-74.9j',
                        '19x-64.9d',
                        '19x-84.9m',
                        '19x-94.9p',
                        '19x-75.10j',
                        '19x-65.10d',
                        '19x-85.10m',
                        '19x-95.10p',
                        '19x-76.11j',
                        '19x-66.11d',
                        '19x-86.11m',
                        '19x-96.11p'
                    ]

                    return dict(zip(filenames, chunks))
                func_map['gfx'] = gfx

                def audiocpu(contents):
                    contents = transforms.splice_out(contents, 0x28000, length=0x28000)
                    contents = transforms.splice_out(contents, 0x8000, length=0x8000)
                    return {
                        '19x-01.1a': contents
                    }
                func_map['audiocpu'] = audiocpu

                def qsound(contents):
                    chunks = transforms.equal_split(contents, num_chunks=8)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "19x-51.6a", 
                        "19x-52.7a", 
                        "19x-53.8a", 
                        "19x-54.9a", 
                        "19x-55.10a", 
                        "19x-56.11a", 
                        "19x-57.12a", 
                        "19x-58.13a"
                    ]

                    return dict(zip(filenames, chunks))
                func_map['qsound'] = qsound

                out_files.append({'filename': '19xxj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #19xx
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x280000, length=0x180000)
                    chunks = transforms.equal_split(contents, num_chunks=5)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [    
                        '19xu.03',
                        '19xu.04',
                        '19xu.05',
                        '19xu.06',
                        '19x.07',
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                
                def gfx(contents):
                    contents = transforms.splice_out(contents, 0x200000, length=0x600000)
                    chunks = transforms.custom_split(contents, [2097152, 8388608])
                    chunks = transforms.deinterleave_all(chunks, num_ways=4, word_size=2)
                    filenames = [    
                        "19x.13m", 
                        "19x.15m", 
                        "19x.17m", 
                        "19x.19m", 
                        "19x.14m", 
                        "19x.16m", 
                        "19x.18m", 
                        "19x.20m", 
                    ]
                    return dict(zip(filenames, chunks))
                func_map['gfx'] = gfx
                
                def audiocpu(contents):
                    contents = transforms.splice_out(contents, 0x28000, length=0x28000)
                    contents = transforms.splice_out(contents, 0x8000, length=0x8000)
                    return {
                        '19x.01': contents
                    }
                func_map['audiocpu'] = audiocpu

                def qsound(contents):
                    chunks = transforms.equal_split(contents, num_chunks=2)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "19x.11m",   
                        "19x.12m"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['qsound'] = qsound
                out_files.append({'filename': '19xx.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556726(kpka_contents):
    out_files = []

    def gfx(contents):
        chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
        filenames = [
            'btc.13m',
            'btc.15m',
            'btc.17m',
            'btc.19m'
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x48000, length=0x8000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        chunks = transforms.equal_split(contents, num_chunks=2)
        filenames = [
            'btc.01',
            'btc.02'
        ]
        return dict(zip(filenames, chunks))
    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'btc.11m',
            'btc.12m'
        ]
        return dict(zip(filenames, chunks))

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #batcirj
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x380000, length=0x3FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=7)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "btcj.03", 
                        "btcj.04", 
                        "btcj.05", 
                        "btcj.06", 
                        "btc.07", 
                        "btc.08", 
                        "btc.09"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'batcirj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #batcir
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x380000, length=0x3FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=7)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "btce.03", 
                        "btce.04", 
                        "btce.05", 
                        "btce.06", 
                        "btc.07", 
                        "btc.08", 
                        "btc.09"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'batcir.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556727(kpka_contents):
    out_files = []

    def gfx(contents):
        chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
        filenames = [
            'ggw.13m',
            'ggw.15m',
            'ggw.17m',
            'ggw.19m'
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x28000, length=0x28000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        return {'ggw.01': contents}
    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'ggw.11m',
            'ggw.12m'
        ]
        return dict(zip(filenames, chunks))

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #gigawingj
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x180000, length=0x27FFFF)
                    chunks = transforms.equal_split(contents, num_chunks=3)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "ggwj.03a",
                        "ggwj.04a",
                        "ggwj.05a",
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'gigawingj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #gigawing
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x180000, length=0x27FFFF)
                    chunks = transforms.equal_split(contents, num_chunks=3)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "ggwu.03",
                        "ggwu.04",
                        "ggw.05",
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'gigawing.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556728(kpka_contents):
    out_files = []

    def gfx(contents):
        chunks = transforms.custom_split(contents, [16777216, 4194304])
        chunks = transforms.deinterleave_all(chunks, num_ways=4, word_size=2)
        filenames = [    
            "nff.13m", 
            "nff.15m", 
            "nff.17m", 
            "nff.19m", 
            "nff.14m", 
            "nff.16m", 
            "nff.18m", 
            "nff.20m", 
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x28000, length=0x28000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        return {'nff.01': contents}
    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'nff.11m',
            'nff.12m'
        ]
        return dict(zip(filenames, chunks))

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #1944j
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x180000, length=0x27FFFF)
                    chunks = transforms.equal_split(contents, num_chunks=3)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "nffj.03",
                        "nffj.04",
                        "nffj.05",
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': '1944j.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #1944
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x180000, length=0x27FFFF)
                    chunks = transforms.equal_split(contents, num_chunks=3)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "nffu.03",
                        "nff.04",
                        "nffu.05",
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': '1944.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def handle_package_1556729(kpka_contents):
    out_files = []

    def gfx(contents):
        chunks = transforms.deinterleave(contents, num_ways=8, word_size=1)
        filenames = [    
            "pga-simm.01c",
            "pga-simm.01d",
            "pga-simm.01a",
            "pga-simm.01b",
            "pga-simm.03c",
            "pga-simm.03d",
            "pga-simm.03a",
            "pga-simm.03b"
        ]
        return dict(zip(filenames, chunks))

    def audiocpu(contents):
        contents = transforms.splice_out(contents, 0x28000, length=0x28000)
        contents = transforms.splice_out(contents, 0x8000, length=0x8000)
        return {'pga.01': contents}
    def qsound(contents):
        chunks = transforms.equal_split(contents, num_chunks=4)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            "pga-simm.05a",
            "pga-simm.05b",
            "pga-simm.06a",
            "pga-simm.06b"
        ]
        return dict(zip(filenames, chunks))

    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2].decode("utf-8") == "PK"):
            if file_entry['offset'] == 352: #progearj
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x100000, length=0x2FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=2)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "pgaj.03",
                        "pgaj.04"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'progearj.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
            else: #progear
                func_map = {}

                def maincpu(contents):
                    contents = transforms.splice_out(contents, 0x100000, length=0x2FFFFF)
                    chunks = transforms.equal_split(contents, num_chunks=2)
                    chunks = transforms.swap_endian_all(chunks)
                    filenames = [   
                        "pgau.03",
                        "pgau.04"
                    ]
                    return dict(zip(filenames, chunks))
                func_map['maincpu'] = maincpu
                func_map['gfx'] = gfx
                func_map['audiocpu'] = audiocpu
                func_map['qsound'] = qsound
                out_files.append({'filename': 'progear.zip', 'contents': merged_rom_handler(file_entry['contents'], func_map)})
    return out_files

def find_files(in_path):
    return glob.glob(os.path.join(in_path, "**", "*.pak"), recursive=True)

def rebuild_mame_subfolder_zip(contents):
    # open old zipfile
    with zipfile.ZipFile(io.BytesIO(contents), "r") as old_archive:
        zip_entries = list(old_archive.infolist())
        
        def getPrefix(zip_entry):
            return zip_entry.filename.split('/')[0]

        def getName(zip_entry):
            return zip_entry.filename.split('/')[1]

        # first, check the zip entries for a subfolder to reuse the name of
        try:
            index = zip_entries[0].filename.index('/')
        except Exception as e:
            logger.warning(e)
            logger.warning(zip_entries[0])
            raise Exception(f'not a mame subfolder zip - no slash in first zip entry')

        prefix = getPrefix(zip_entries[0])
        for file_entry in zip_entries:
            if getPrefix(file_entry) != prefix:
                raise Exception(f'not a mame subfolder zip - {getPrefix(file_entry)} != {prefix}')

        new_contents = io.BytesIO()
        with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            for file_entry in zip_entries:
                with old_archive.open(file_entry) as file_read_obj:
                    file_data = file_read_obj.read()
 
                    # add to new archive
                    new_archive.writestr(getName(file_entry), file_data)
        
        ret_obj = dict()
        ret_obj['filename'] = f'{prefix}.zip'
        ret_obj['contents'] = new_contents.getvalue()
        return ret_obj

def standard_kpka_contents_processing(kpka_contents):
    out_files = []
    for file_entry in kpka_contents.values():
        if (file_entry['contents'][0:2] == "PK".encode('utf-8')):
            rebuilt = rebuild_mame_subfolder_zip(file_entry['contents'])
            out_files.append(rebuilt)
    return out_files

def main(steam_dir, out_path):
    pak_files = find_files(steam_dir)
    for file in pak_files:
        id = None
        if os.path.basename(file) == "re_chunk_000.pak":
            id = "1515951"
        else:
            id = file[-11:-4]

        if id in pkg_name_map:
            logger.info(f"Extracting {file}: {pkg_name_map[id]}") 
            try:
                with open(file, "rb") as curr_file:
                    file_content = bytearray(curr_file.read())
                    kpka_contents = kpka.extract(file_content)
                    output_files = []

                    special_func = globals().get(f'handle_package_{id}')
                    if special_func:
                        # Reflectively call the appropriate function to process the file
                        output_files = special_func(kpka_contents)
                    else:
                        output_files = standard_kpka_contents_processing(kpka_contents)
                        
                    for output_file in output_files:
                        with open(os.path.join(out_path, output_file['filename']), "wb") as out_file:
                            out_file.write(output_file['contents'])
            except Exception as e:
                traceback.print_exc()
                logger.warning(f'Error while processing {file}!') 
        else:
            logger.info(f'Skipping {file} as it contains no known ROMS!') 

    logger.info("""
        Processing complete. 
        TODOs:
         - Figure out fixes for the 'incomplete' games
           - Source for dl-1425.bin
           - How do we find/reproduce the enc keys
    """)
