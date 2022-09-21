'''Implementation of acac: Arcade Classics Anniversary Collection'''
import logging
import lzma
import os
from gex.lib.utils.blob import hash as hash_helper
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class ACACTask(BaseTask):
    '''Implements acac: Arcade Classics Anniversary Collection'''
    _task_name = "ags"
    _title = "Arcade Classics Anniversary Collection"
    _details_markdown = ''''''
    _default_input_folder = helpers.gen_steam_app_default_folder("Arcade Classics Anniversary Collection")
    _input_folder_desc = "Arcade Classics Anniversary Collection install folder"
    _short_description = ""

    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }

    _game_info_map = [
        {
            "name": "AJAX (J)",
            "filename": "ajaxj.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x11B610,
                "length": 3473920
            },
            "out": [
                {"filename": "770_l01.n11", "start": 0x000000, "length": 0x10000},
                {"filename": "770_l02.n12", "start": 0x020000, "length": 0x10000},
                {"filename": "770_l05.i16", "start": 0x030000, "length": 0x8000},
                {"filename": "770_f04.g16", "start": 0x038000, "length": 0x10000},
                {"filename": "770_f03.f16", "start": 0x048000, "length": 0x8000},
                {"filename": "770c13.n22", "start": 0x090000, "length": 0x40000},
                {"filename": "770c12.k22", "start": 0x0D0000, "length": 0x40000},
                {"filename": "770c09.n4", "start": 0x110000, "length": 0x80000},
                {"filename": "770c08.k4", "start": 0x190000, "length": 0x80000},
                {"filename": "770c06.f4", "start": 0x210000, "length": 0x40000},
                {"filename": "770c07.h4", "start": 0x250000, "length": 0x40000},
                {"filename": "770c10", "start": 0x290000, "length": 0x40000},
                {"filename": "770c11", "start": 0x2D0000, "length": 0x80000},
                {"filename": "63s241.j11", "start": 0x350000, "length": 0x200},
            ],
        },
        {
            "name": "AJAX",
            "filename": "ajax.zip",
            'status': 'no-rom',
            "notes": [2],
        },
        {
            "name": "Typhoon",
            "filename": "typhoon.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x11B610,
                "length": 3473920
            },
            "out": [
                {"filename": "770_k01.n11", "start": 0x050000, "length": 0x10000},
                {"filename": "770_k02.n12", "start": 0x060000, "length": 0x10000},
                {"filename": "770_k05.i16", "start": 0x070000, "length": 0x8000},
                {"filename": "770_f04.g16", "start": 0x038000, "length": 0x10000},
                {"filename": "770_h03.f16", "start": 0x088000, "length": 0x8000},
                {"filename": "770c13.n22", "start": 0x090000, "length": 0x40000},
                {"filename": "770c12.k22", "start": 0x0D0000, "length": 0x40000},
                {"filename": "770c09.n4", "start": 0x110000, "length": 0x80000},
                {"filename": "770c08.k4", "start": 0x190000, "length": 0x80000},
                {"filename": "770c06.f4", "start": 0x210000, "length": 0x40000},
                {"filename": "770c07.h4", "start": 0x250000, "length": 0x40000},
                {"filename": "770c10", "start": 0x290000, "length": 0x40000},
                {"filename": "770c11", "start": 0x2D0000, "length": 0x80000},
                {"filename": "63s241.j11", "start": 0x350000, "length": 0x200},
            ],
        },
        {
            "name": "Haunted Castle (Version M)",
            "filename": "hcastle.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x22E110,
                "length": 3310848
            },
            "out": [
                {"filename": "m03.k12", "start": 0x078000, "length": 0x8000},
                {"filename": "b06.k8", "start": 0x080000, "length": 0x20000},
                {"filename": "768e01.e4", "start": 0x0A0000, "length": 0x8000},
                {"filename": "768c07.e17", "start": 0x0A8000, "length": 0x80000},
                {"filename": "768c09.g21", "start": 0x128000, "length": 0x80000},
                {"filename": "768c08.g19", "start": 0x1A8000, "length": 0x80000},
                {"filename": "768c04.j5", "start": 0x228000, "length": 0x80000},
                {"filename": "768c05.j6", "start": 0x2A8000, "length": 0x80000},
                {"filename": "768c13.j21", "start": 0x328000, "length": 0x100},
                {"filename": "768c11.i4", "start": 0x328000, "length": 0x100},
                {"filename": "768c14.j22", "start": 0x328100, "length": 0x100},
                {"filename": "768c10.i3", "start": 0x328100, "length": 0x100},
                {"filename": "768b12.d20", "start": 0x328400, "length": 0x100},
            ],
        },
        {
            "name": "Haunted Castle (Version E)",
            "filename": "hcastlee.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x22E110,
                "length": 3310848
            },
            "out": [
                {"filename": "768e03.k12", "start": 0x028000, "length": 0x8000},
                {"filename": "768e06.k8", "start": 0x030000, "length": 0x20000},
                {"filename": "768e01.e4", "start": 0x0A0000, "length": 0x8000},
                {"filename": "768c07.e17", "start": 0x0A8000, "length": 0x80000},
                {"filename": "768c09.g21", "start": 0x128000, "length": 0x80000},
                {"filename": "768c08.g19", "start": 0x1A8000, "length": 0x80000},
                {"filename": "768c04.j5", "start": 0x228000, "length": 0x80000},
                {"filename": "768c05.j6", "start": 0x2A8000, "length": 0x80000},
                {"filename": "768c13.j21", "start": 0x328000, "length": 0x100},
                {"filename": "768c11.i4", "start": 0x328000, "length": 0x100},
                {"filename": "768c14.j22", "start": 0x328100, "length": 0x100},
                {"filename": "768c10.i3", "start": 0x328100, "length": 0x100},
                {"filename": "768b12.d20", "start": 0x328400, "length": 0x100},
            ],
        },
        {
            "name": "Haunted Castle (Version K)",
            "filename": "hcastlek.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x22E110,
                "length": 3310848
            },
            "out": [
                {"filename": "768k03.k12", "start": 0x050000, "length": 0x8000},
                {"filename": "768g06.k8", "start": 0x058000, "length": 0x20000},
                {"filename": "768e01.e4", "start": 0x0A0000, "length": 0x8000},
                {"filename": "768c07.e17", "start": 0x0A8000, "length": 0x80000},
                {"filename": "768c09.g21", "start": 0x128000, "length": 0x80000},
                {"filename": "768c08.g19", "start": 0x1A8000, "length": 0x80000},
                {"filename": "768c04.j5", "start": 0x228000, "length": 0x80000},
                {"filename": "768c05.j6", "start": 0x2A8000, "length": 0x80000},
                {"filename": "768c13.j21", "start": 0x328000, "length": 0x100},
                {"filename": "768c11.i4", "start": 0x328000, "length": 0x100},
                {"filename": "768c14.j22", "start": 0x328100, "length": 0x100},
                {"filename": "768c10.i3", "start": 0x328100, "length": 0x100},
                {"filename": "768b12.d20", "start": 0x328400, "length": 0x100},
            ],
        },
        {
            "name": "Akuma-Jou Dracula (Version N)",
            "filename": "akumajoun.zip",
            'status': 'good',
            "notes": [],
            "in": {
                "start": 0x22E110,
                "length": 3310848
            },
            "out": [
                {"filename": "768n03.k12", "start": 0x000000, "length": 0x8000},
                {"filename": "768j06.k8", "start": 0x008000, "length": 0x20000},
                {"filename": "768e01.e4", "start": 0x0A0000, "length": 0x8000},
                {"filename": "768c07.e17", "start": 0x0A8000, "length": 0x80000},
                {"filename": "768c09.g21", "start": 0x128000, "length": 0x80000},
                {"filename": "768c08.g19", "start": 0x1A8000, "length": 0x80000},
                {"filename": "768c04.j5", "start": 0x228000, "length": 0x80000},
                {"filename": "768c05.j6", "start": 0x2A8000, "length": 0x80000},
                {"filename": "768c13.j21", "start": 0x328000, "length": 0x100},
                {"filename": "768c11.i4", "start": 0x328000, "length": 0x100},
                {"filename": "768c14.j22", "start": 0x328100, "length": 0x100},
                {"filename": "768c10.i3", "start": 0x328100, "length": 0x100},
                {"filename": "768b12.d20", "start": 0x328400, "length": 0x100},
            ],
        },
        {
            "name": "nemesis",
            "filename": "nemesis.zip",
            'status': 'partial',
            "notes": [1],
            "in": {
                "start": 0x22E110,
                "length": 74752
            },
        },
        {
            "name": "salamand",
            "filename": "salamand.zip",
            'status': 'partial',
            "notes": [1],
            "in": {
                "start": 0x4165D0,
                "length": 4415040
            },
        },
        # { # Investigate!
        #     "name": "scramble",
        #     "filename": "scramble.zip",
        #     'status': 'no-rom',
        #     "notes": [1]
        # },
        {
            "name": "thunderx",
            "filename": "thunderx.zip",
            'status': 'partial',
            "notes": [1],
            "in": {
                "start": 0x4D13D0,
                "length": 1900800
            },
        },
        {
            "name": "twinbee",
            "filename": "twinbee.zip",
            'status': 'partial',
            "notes": [1],
            "in": {
                "start": 0x2F2DE0,
                "length": 541184
            },
        },
        {
            "name": "vulcan",
            "filename": "vulcan.zip",
            'status': 'partial',
            "notes": [1],
            "in": {
                "start": 0x37C280,
                "length": 3080192
            },
        }
    ]

    _out_file_notes = {
        "1": "This game is not yet extractable; it might not be implemented as a usable ROM.",
        "2": "This variant does not appear to be present in this collection."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'system': "Arcade",
            "status": x['status'],
            "notes": x['notes']},
            self._game_info_map)

    def execute(self, in_dir, out_dir):
        src_file = os.path.join(in_dir, "AA_AC_ArcadeClassics.exe")
        with open(src_file, 'rb') as src_file:
            src_contents = src_file.read()
            src_contents_decomp = lzma_multi_decomp(src_contents)
            # src_decomp_hash = hash_helper.get_crc(src_contents_decomp)
            # if (src_decomp_hash == '0xb4f2f51b'):
            #     print(f"CRC MATCH {src_decomp_hash}")
            # else:
            #     print(f"CRC MISMATCH! OH NOOOOOOOOOOOOOO! {src_decomp_hash}")

        with open(os.path.join(out_dir, 'decompressed_blob'), "wb") as out_file:
            out_file.write(src_contents_decomp)

        for game in self._game_info_map:
            if game.get('status') == "no-rom":
                logger.info(f"Skipping {game['name']} as there is no ROM to extract...")
                continue

            is_partial = game.get('status') == "partial"
            if not self._props.get('include-partials') and is_partial:
                logger.info(f"Skipping {game['name']} as this tool cannot extract a working copy...")
                continue

            logger.info(f"Extracting {game['name']}...")
            zip_files = {}

            # Get the specified decompression section
            contents = transforms.cut(src_contents, game['in']['start'], length=game['in']['length'])

            if is_partial:
                zip_files["decompressed_blob"] = contents
            else:
                for work_file in game.get('out') or []:
                    zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])

            filename = f"partial_{game['filename']}" if  is_partial else game['filename']
            logger.info(f"Saving {filename}...")
            with open(os.path.join(out_dir, filename), "wb") as out_file:
                out_file.write(helpers.build_zip(zip_files))

        logger.info("Processing complete.")

# def _handle_twinbee(decomp_merged, out_dir):
#     zip_files = {}
    
    # There are two versions: ROM and Bubble System
    # Both are in the Arcade Archives: https://www.nintendo.com/store/products/arcade-archives-twinbee-switch/
    # Neither appears to have a full fileset in ACAC.

    # TWINBEE (ROM): http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=twinbee&search_id=1
    
    # filename = "twinbee.zip"
    # zip_files["400-a01.fse"] = transforms.cut(decomp_merged, 0x6FC700, length=0x100)
    # zip_files["400-a02.fse"] = transforms.cut(decomp_merged, 0x6FC800, length=0x100)
    # "400-a04.10l" NOT PRESENT
    # "400-a06.15l" NOT PRESENT
    # Checked for 10l and 15l interleave like 12l and 17l - no match!
    # "400-e03.5l" NOT PRESENT
    # temp = transforms.cut(decomp_merged, 0x1358AA6, length=0x40000)
    # temp = transforms.deinterleave(temp, 2, 1)
    # zip_files["412-a05.12l"] = temp[0]
    # zip_files["412-a07.17l"] = temp[1]

    # TWINBEEB (BUBSYS): http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=twinbeeb&search_id=1
    # zip_files["400-a01.fse"] = transforms.cut(decomp_merged, 0x6FC700, length=0x100)
    # zip_files["400-a02.fse"] = transforms.cut(decomp_merged, 0x6FC800, length=0x100)
    # "400-e03.5l" NOT PRESENT
    # "boot.bin" NOT PRESENT
    # "mcu" NOT PRESENT
    # zip_files["twinbee.bin""] = transforms.cut(decomp_merged, 0x1358A2A, length=0x402F0)

    # BUBSYS Base ROM: http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=bubsys&back_games=twinbeeb;&search_id=1
    # zip_files["400a1.2b"] = transforms.cut(decomp_merged, 0x6FC700, length=0x100)
    # zip_files["400a2.1b"] = transforms.cut(decomp_merged, 0x6FC800, length=0x100)
    # "400b03.8g" NOT PRESENT
    # "boot.bin" NOT PRESENT
    # "mcu" NOT PRESENT

    # logger.info(f"Saving {filename}...")
    # with open(os.path.join(out_dir, filename), "wb") as out_file:
    #     out_file.write(helpers.build_zip(zip_files))


def lzma_multi_decomp(in_data):
    out_data = b''

    offset = 0
    while True:
        offset = in_data.find(b']\x00\x00', offset)
        if offset == -1:
            print("out of input")
            break

        # Check LZMA header
        # 1 => 5d 00 00 01 00
        # 2 => 5d 00 00 10 00
        # 3 => 5d 00 00 08 00
        # 4 => 5d 00 00 10 00
        # 5 => 5d 00 00 20 00
        # 6 => 5d 00 00 40 00
        # 7 => 5d 00 00 80 00
        # 8 => 5d 00 00 00 01
        # 9 => 5d 00 00 00 02
        comp_mode = in_data[offset+3:offset+5]
        valid_modes = [
            b'\x01\x00',
            b'\x10\x00',
            b'\x08\x00',
            b'\x18\x00',
            b'\x20\x00',
            b'\x40\x00',
            b'\x80\x00',
            b'\x00\x01',
            b'\x00\x02'
        ]
        if comp_mode not in valid_modes:
            print(f'offset {offset}: skipping, invalid comp_type')
            offset += 1
        else:
            try:
                target = in_data[offset:]
                before_len = len(target)
                magic_bytes = in_data[offset:offset+5]
                lzd = lzma.LZMADecompressor()
                out_data += lzd.decompress(target)
                after_len = len(lzd.unused_data)
                consumed_bytes = before_len - after_len
                offset += consumed_bytes
                print(f'offset {offset}: magic {magic_bytes}, consumed {consumed_bytes} bytes')
            except lzma.LZMAError:
                print(f'offset {offset}: magic {magic_bytes}, invalid')
                offset += 1
    return out_data

# def lzma_multi_decomp(in_data):
#     out_data = b''
#     i = 1
#     while(in_data):
#         if i % 100 == 0:
#             print(f"pass: {i}   len: {len(in_data)}")
#         # Decompress this chunk
#         # print(len(in_data))
#         # print(in_data[0:10])
#         lzd = lzma.LZMADecompressor()
#         try:
#             out_data += lzd.decompress(in_data)
#             in_data = bytearray(lzd.unused_data)
#         except lzma.LZMAError:
#             in_data = in_data[1:]

#         # print(len(out_data))

#         # Prep the next chunk of data by stripping b'00's
#         while len(in_data) > 0 and in_data[0] != 0x5d:
#             # print('remove')
#             in_data = in_data[1:]
#         i += 1

#     return out_data
