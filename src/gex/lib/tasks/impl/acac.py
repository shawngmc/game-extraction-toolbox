'''Implementation of acac: Arcade Classics Anniversary Collection'''
import logging
import lzma
import os
from gex.lib.utils.blob import hash as hash_helper
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

# Implementation notes:
# - This one is a very imprecise process. While it initally looks like there's one internal LZMA blob per title,
#   this doesn't appear to actually 



class ACACTask(BaseTask):
    '''Implements acac: Arcade Classics Anniversary Collection'''
    _task_name = "acac"
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
            "notes": []
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
            "notes": []
        },
        {
            "name": "Haunted Castle (Version M)",
            "filename": "hcastle.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Haunted Castle (Version E)",
            "filename": "hcastlee.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Haunted Castle (Version K)",
            "filename": "hcastlek.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Akuma-Jou Dracula (Version N)",
            "filename": "akumajoun.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Nemesis (World?)",
            "filename": "nemesisuk.zip",
            "notes": []
        },
        {
            "name": "Nemesis",
            "filename": "nemesis.zip",
            "notes": []
        },
        # {
        #     "name": "salamand",
        #     "filename": "salamand.zip",
        #     'status': 'partial',
        #     "notes": [1],
        #     "in": {
        #         "start": 0x4165D0,
        #         "length": 4415040
        #     },
        # },
        # { # Investigate!
        #     "name": "scramble",
        #     "filename": "scramble.zip",
        #     'status': 'no-rom',
        #     "notes": [1]
        # },
        # {
        #     "name": "thunderx",
        #     "filename": "thunderx.zip",
        #     'status': 'partial',
        #     "notes": [1],
        #     "in": {
        #         "start": 0x4D13D0,
        #         "length": 1900800
        #     },
        # },
        # {
        #     "name": "twinbee",
        #     "filename": "twinbee.zip",
        #     'status': 'partial',
        #     "notes": [1],
        #     "in": {
        #         "start": 0x2F2DE0,
        #         "length": 541184
        #     },
        # },
        # {
        #     "name": "vulcan",
        #     "filename": "vulcan.zip",
        #     'status': 'partial',
        #     "notes": [1],
        #     "in": {
        #         "start": 0x37C280,
        #         "length": 3080192
        #     },
        # }
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
            src_contents_decomp = self.lzma_multi_decomp(src_contents, out_dir)

        with open(os.path.join(out_dir, 'merged_decomp_blob'), "wb") as out_file:
            out_file.write(src_contents_decomp)


        out_files = []
        out_files.extend(self._handle_nemesis(src_contents))
        out_files.extend(self._handle_hcastle(src_contents))
        out_files.extend(self._handle_ajax(src_contents))

        if out_files:
            for out_file_entry in out_files:
                out_path = os.path.join(out_dir, out_file_entry['filename'])
                with open(out_path, "wb") as out_file:
                    logger.info(f"Writing {out_file_entry['filename']}...")
                    out_file.write(out_file_entry['contents'])
        # for game in self._game_info_map:
        #     if game.get('status') == "no-rom":
        #         logger.info(f"Skipping {game['name']} as there is no ROM to extract...")
        #         continue

        #     is_partial = game.get('status') == "partial"
        #     if not self._props.get('include-partials') and is_partial:
        #         logger.info(f"Skipping {game['name']} as this tool cannot extract a working copy...")
        #         continue

        #     logger.info(f"Extracting {game['name']}...")

        #     # Get the specified decompression section
        #     contents = transforms.cut(src_contents, game['in']['start'], length=game['in']['length'])
        #     lzd = lzma.LZMADecompressor()
        #     contents = lzd.decompress(contents)

        #     output_files = []
        #     if 'handler' in game:
        #         handler_func = getattr(self, game['handler'])
        #         output_files.extend(handler_func(contents, game))
        #     else:
        #         logger.warning(f"No handler defined for {game['name']}; dumping contents")
        #         output_files.extend(self._handle_copyorig(contents, game))

        #     for output_file in output_files:
        #         filename = f"partial_{output_file['filename']}" if is_partial else output_file['filename']
        #         logger.info(f"Saving {filename}...")
        #         with open(os.path.join(out_dir, filename), "wb") as out_file:
        #             out_file.write(output_file['contents'])

        logger.info("Processing complete.")

    def _handle_copyorig(self, contents, game):
        return [{'filename': game['filename'], 'contents': helpers.build_zip({ "decompressed_blob": contents })}]

    def _handle_generic_copy(self, contents, game):
        zip_files = {}
        for work_file in game.get('out') or []:
            zip_files[work_file['filename']] = transforms.cut(contents, work_file['start'], length=work_file['length'])
        return [{'filename': game['filename'], 'contents': helpers.build_zip(zip_files)}]

    def _handle_ajax(self, contents):
        contents = transforms.cut(contents, 0x11B610, length=3473920)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []
        
        # AJAX Common
        func_map = {}
        def k_roms(contents):
            out_chunks = {}
            out_chunks["770c13.n22"] = transforms.cut(contents, 0x090000, length = 0x40000)
            out_chunks["770c12.k22"] = transforms.cut(contents, 0x0D0000, length = 0x40000)
            out_chunks["770c09.n4"] = transforms.cut(contents, 0x110000, length = 0x80000)
            out_chunks["770c08.k4"] = transforms.cut(contents, 0x190000, length = 0x80000)
            out_chunks["770c06.f4"] = transforms.cut(contents, 0x210000, length = 0x40000)
            out_chunks["770c07.h4"] = transforms.cut(contents, 0x250000, length = 0x40000)
            out_chunks["770c10"] = transforms.cut(contents, 0x290000, length = 0x40000)
            out_chunks["770c11"] = transforms.cut(contents, 0x2D0000, length = 0x80000)
            out_chunks["63s241.j11"] = transforms.cut(contents, 0x350000, length = 0x200)
            return out_chunks
        func_map['k_roms'] = k_roms
        common_file_map = helpers.process_rom_files(contents, func_map)

        # AJAXJ
        func_map = {}
        def ajaxj_maincpu(contents):
            out_chunks = {}
            out_chunks["770_l01.n11"] = transforms.cut(contents, 0x000000, length = 0x10000)
            out_chunks["770_l02.n12"] = transforms.cut(contents, 0x020000, length = 0x10000)
            out_chunks["770_l05.i16"] = transforms.cut(contents, 0x030000, length = 0x8000)
            out_chunks["770_f04.g16"] = transforms.cut(contents, 0x038000, length = 0x10000)
            out_chunks["770_f03.f16"] = transforms.cut(contents, 0x048000, length = 0x8000)
            return out_chunks
        func_map['maincpu'] = ajaxj_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'ajaxj.zip', 'contents': helpers.build_rom(contents, func_map)})

        # Typhoon
        func_map = {}
        def typhoon_maincpu(contents):
            out_chunks = {}
            out_chunks["770_k01.n11"] = transforms.cut(contents, 0x050000, length = 0x10000)
            out_chunks["770_k02.n12"] = transforms.cut(contents, 0x060000, length = 0x10000)
            out_chunks["770_k05.i16"] = transforms.cut(contents, 0x070000, length = 0x8000)
            out_chunks["770_f04.g16"] = transforms.cut(contents, 0x038000, length = 0x10000)
            out_chunks["770_h03.f16"] = transforms.cut(contents, 0x048000, length = 0x8000)
            return out_chunks
        func_map['maincpu'] = typhoon_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'typhoon.zip', 'contents': helpers.build_rom(contents, func_map)})
        
        return out_files

    def _handle_nemesis(self, contents):
        contents = transforms.cut(contents, 0x2F2DE0, length=541168)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []

        # Nemesis Common
        func_map = {}
        # k005289
        def k_rom(contents):
            filenames = [
                "400-a01.fse",
                "400-a02.fse"
            ]
            contents = transforms.cut(contents, 0x84000, length = 0x200)
            chunks = transforms.equal_split(contents, len(filenames))
            return dict(zip(filenames, chunks))
        func_map['k005289'] = k_rom
        common_file_map = helpers.process_rom_files(contents, func_map)

        # Nemesis
        func_map = {}
        def nemesis_maincpu(contents):
            filenames = [
                "456-d01.12a",
                "456-d05.12c",
                "456-d02.13a",
                "456-d06.13c",
                "456-d03.14a",
                "456-d07.14c",
                "456-d04.15a",
                "456-d08.15c",
            ]
            contents = transforms.cut(contents, 0x40000, length = 0x40000)
            chunks = transforms.equal_split(contents, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = nemesis_maincpu
        def nemesis_audiocpu(contents):
            contents = transforms.cut(contents, 0x80000, length = 0x4000)
            return {'456-d09.9c': contents}
        func_map['audiocpu'] = nemesis_audiocpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'nemesis.zip', 'contents': helpers.build_rom(contents, func_map)})

        # Nemesis UK/World?
        func_map = {}
        def nemesisuk_maincpu(contents):
            filenames = [
                "456-e01.12a",
                "456-e05.12c",
                "456-e02.13a",
                "456-e06.13c",
                "456-e03.14a",
                "456-e07.14c",
                "456-e04.15a",
                "456-e08.15c",
            ]
            contents = transforms.cut(contents, 0x00000, length = 0x40000)
            chunks = transforms.equal_split(contents, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = nemesisuk_maincpu
        def nemesisuk_audiocpu(contents):
            contents = transforms.cut(contents, 0x80000, length = 0x4000)
            return {'456-b09.9c': contents}
        func_map['audiocpu'] = nemesisuk_audiocpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'nemesisuk.zip', 'contents': helpers.build_rom(contents, func_map)})

        return out_files


    def _handle_hcastle(self, contents):
        contents = transforms.cut(contents, 0x2F2DE0, length=541168)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []

        # HCastle Common
        func_map = {}
        def k_roms(contents):
            out_chunks = {}
            out_chunks["768c07.e17"] = transforms.cut(contents, 0x0A8000, length = 0x80000)
            out_chunks["768c09.g21"] = transforms.cut(contents, 0x128000, length = 0x80000)
            out_chunks["768c08.g19"] = transforms.cut(contents, 0x1A8000, length = 0x80000)
            out_chunks["768c04.j5"] = transforms.cut(contents, 0x228000, length = 0x80000)
            out_chunks["768c05.j6"] = transforms.cut(contents, 0x2A8000, length = 0x80000)
            return out_chunks
        func_map['k_roms'] = k_roms
        def proms(contents):
            out_chunks = {}
            out_chunks["768c13.j21"] = transforms.cut(contents, 0x328000, length = 0x100)
            out_chunks["768c11.i4"] = out_chunks["768c13.j21"]
            out_chunks["768c14.j22"] = transforms.cut(contents, 0x328100, length = 0x100)
            out_chunks["768c10.i3"] = out_chunks["768c14.j22"]
            out_chunks["768b12.d20"] = transforms.cut(contents, 0x328400, length = 0x100)
            return out_chunks
        func_map['proms'] = proms
        def proms(contents):
            out_chunks = {}
            out_chunks["768e01.e4"] = transforms.cut(contents, 0x0A0000, length = 0x8000)
            return out_chunks
        func_map['proms'] = proms
        common_file_map = helpers.process_rom_files(contents, func_map)

        # HCASTLE
        func_map = {}
        def hcastle_maincpu(contents):
            out_chunks = {}
            out_chunks["m03.k12"] = transforms.cut(contents, 0x078000, length = 0x8000)
            out_chunks["b06.k8"] = transforms.cut(contents, 0x080000, length = 0x20000)
            return out_chunks
        func_map['maincpu'] = hcastle_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'hcastle.zip', 'contents': helpers.build_rom(contents, func_map)})

        # HCASTLEE
        func_map = {}
        def hcastlee_maincpu(contents):
            out_chunks = {}
            out_chunks["768e03.k12"] = transforms.cut(contents, 0x028000, length = 0x8000)
            out_chunks["768e06.k8"] = transforms.cut(contents, 0x030000, length = 0x20000)
            return out_chunks
        func_map['maincpu'] = hcastlee_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'hcastlee.zip', 'contents': helpers.build_rom(contents, func_map)})

        # HCASTLEK
        func_map = {}
        def hcastlek_maincpu(contents):
            out_chunks = {}
            out_chunks["768k03.k12"] = transforms.cut(contents, 0x050000, length = 0x8000)
            out_chunks["768g06.k8"] = transforms.cut(contents, 0x058000, length = 0x20000)
            return out_chunks
        func_map['maincpu'] = hcastlek_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'hcastlek.zip', 'contents': helpers.build_rom(contents, func_map)})

        # akumajoun
        func_map = {}
        def akumajoun_maincpu(contents):
            out_chunks = {}
            out_chunks["768n03.k12"] = transforms.cut(contents, 0x000000, length = 0x8000)
            out_chunks["768j06.k8"] = transforms.cut(contents, 0x008000, length = 0x20000)
            return out_chunks
        func_map['maincpu'] = akumajoun_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'akumajoun.zip', 'contents': helpers.build_rom(contents, func_map)})

        return out_files

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


    def lzma_multi_decomp(self, in_data, out_dir):
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
                    curr_chunk = lzd.decompress(target)
                    with open(os.path.join(out_dir, f'decompressed_blob_{offset}'), "wb") as out_file:
                        out_file.write(curr_chunk)
                    out_data += curr_chunk
                    after_len = len(lzd.unused_data)
                    consumed_bytes = before_len - after_len
                    offset += consumed_bytes
                    print(f'offset {offset}: magic {magic_bytes}, consumed {consumed_bytes} bytes')
                except lzma.LZMAError:
                    print(f'offset {offset}: magic {magic_bytes}, invalid')
                    offset += 1
        return out_data
