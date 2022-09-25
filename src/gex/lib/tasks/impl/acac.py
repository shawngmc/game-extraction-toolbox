'''Implementation of acac: Arcade Classics Anniversary Collection'''
import logging
import lzma
import os
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
            'status': 'playable',
            "notes": []
        },
        {
            "name": "Typhoon",
            "filename": "typhoon.zip",
            'status': 'playable',
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
            'status': 'good',
            "notes": []
        },
        {
            "name": "Nemesis",
            "filename": "nemesis.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Gradius 2",
            "filename": "gradius2.zip",
            'status': 'playable',
            "notes": []
        },
        {
            "name": "Vulcan Venture",
            "filename": "vulcan.zip",
            'status': 'playable',
            "notes": []
        },
        {
            "name": "Thunder Cross (J)",
            "filename": "thunderxj.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Thunder Cross (Set 1)",
            "filename": "thunderx.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Thunder Cross (Set 2)",
            "filename": "thunderxa.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Thunder Cross (Set 3)",
            "filename": "thunderxb.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Salamander",
            "filename": "salamand.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Salamander (J)",
            "filename": "salamandj.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Lifeforce",
            "filename": "lifefrce.zip",
            'status': 'good',
            "notes": []
        },
        {
            "name": "Lifeforce (J)",
            "filename": "lifefrcejzip",
            'status': 'playable',
            "notes": [2]
        },
        # TWINBEE - can find bits and pieces
        # SCRAMBLE - no sign of it
    ]

    _out_file_notes = {
        "1": "This game has a placeholder file and may be missing some sound samples.",
        "2": "This game has a bad dump, but is fully playable."
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
        out_files.extend(self._handle_vulcan(src_contents))
        out_files.extend(self._handle_thunderx(src_contents))
        out_files.extend(self._handle_salamand(src_contents))
        if self._props.get('include-partials'):
            out_files.extend(self._handle_twinbee(src_contents))

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
        contents = transforms.cut(contents, 0x11B610, length=1124930)
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
        def ajaxj_krom(contents):
            out_chunks = {}
            out_chunks["770c13.n22"] = transforms.cut(contents, 0x090000, length = 0x40000)
            out_chunks["770c12.k22"] = transforms.cut(contents, 0x0D0000, length = 0x40000)
            return out_chunks
        func_map['k_roms'] = ajaxj_krom
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
        func_map['k_roms'] = ajaxj_krom
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
        contents = transforms.cut(contents, 0x22E110, length=798376)
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
        def audiocpu(contents):
            out_chunks = {}
            out_chunks["768e01.e4"] = transforms.cut(contents, 0x0A0000, length = 0x8000)
            return out_chunks
        func_map['audiocpu'] = audiocpu
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

    def _handle_vulcan(self, contents):
        contents = transforms.cut(contents, 0x37C280, length=3080192)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []

        # 0x000000   0x040000     maincpu - gradius2
        # 0x040000   0x040000     maincpu - vulcan
        # 0x080000   0x040000     sub
        # 0x0C0000   0x008000     audiocpu
        # 0x0C8000   0x020000     k_rom
        # 0x0E8000   0x004000     fixed - gradius2
        # 0x0EB000   0x004000     fixed - vulcan
        # 0x0F0000   0x200000     gfx
        
        # 785_f02.7c MISSING 0x20000

        # VULCAN Common
        func_map = {}
        def audiocpu(contents):
            out_chunks = {}
            out_chunks["785_g03.10a"] = transforms.cut(contents, 0x0C0000, length = 0x8000)
            return out_chunks
        func_map['audiocpu'] = audiocpu
        def gfx(contents):
            filenames = [
                "785f15.p13",
                "785f17.p16",
                "785f16.p15",
                "785f18.p18"
            ]
            contents = transforms.cut(contents, 0x0F0000, length = 0x200000)
            chunks = transforms.equal_split(contents, 2)
            chunks = transforms.deinterleave_all(chunks, 2, 2)
            chunks = transforms.swap_endian_all(chunks)
            return dict(zip(filenames, chunks))
        func_map['gfx'] = gfx
        def sub(contents):
            filenames = [
                "785_p07.10n",
                "785_p06.8n",
                "785_p13.10s",
                "785_p12.8s",
            ]
            contents = transforms.cut(contents, 0x080000, length = 0x040000)
            chunks = transforms.equal_split(contents, 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['sub'] = sub
        def k_rom(contents):
            out_chunks = {}
            out_chunks["785_f01.5a"] = transforms.cut(contents, 0x0C8000, length = 0x20000)
            return out_chunks
        func_map['k_rom'] = k_rom
        ph_files = {
            "785_f02.7c": 0x20000
        }
        func_map['ph'] = helpers.placeholder_helper(ph_files)
        common_file_map = helpers.process_rom_files(contents, func_map)

        # GRADIUS2
        func_map = {}
        #maincpu
        def gradius2_maincpu(contents):
            filenames = [
                "785_x05.6n",
                "785_x04.4n",
                "785_x09.6r",
                "785_x08.4r",
            ]
            contents = transforms.cut(contents, 0x00000, length = 0x40000)
            chunks = transforms.equal_split(contents, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = gradius2_maincpu
        def fixed(contents):
            out_chunks = {}
            out_chunks["785_g14.d8"] = transforms.cut(contents, 0x0E8000, length = 0x4000)
            return out_chunks
        func_map['fixed'] = fixed
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'gradius2.zip', 'contents': helpers.build_rom(contents, func_map)})

        
        # VULCAN
        func_map = {}
        def vulcan_maincpu(contents):
            filenames = [
                "785_w05.6n",
                "785_w04.4n",
                "785_w09.6r",
                "785_w08.4r",
            ]
            contents = transforms.cut(contents, 0x40000, length = 0x40000)
            chunks = transforms.equal_split(contents, len(filenames) // 2)
            chunks = transforms.deinterleave_all(chunks, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = vulcan_maincpu
        def vulcan_fixed(contents):
            out_chunks = {}
            out_chunks["785_h14.d8"] = transforms.cut(contents, 0x0EC000, length = 0x4000)
            return out_chunks
        func_map['fixed'] = vulcan_fixed
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'vulcan.zip', 'contents': helpers.build_rom(contents, func_map)})

        return out_files



    def _handle_thunderx(self, contents):
        contents = transforms.cut(contents, 0x4D13D0, length=455549)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []

        # 0x000000 0x020000     maincpu - thunderxj
        # 0x020000 0x008000     audiocpu -thunderxj/xb/x
        # 0x028000 0x020000     maincpu - thunderxb
        # 0x048000 0x020000     maincpu - thunderx
        # 0x068000 0x050000     mystery junk data
        #    BK header kinda looks like maincpu, but no idea what it could match
        #    We have every thunderx variant MAME knows, and the other games for this driver are very different
        # 0x048000 0x020000     maincpu - thunderxa
        # 0x0C8000 0c008000     audiocpu -thunderxa
        # 0x0D0000 0x080000     tiles
        # 0x150000 0x080000     sprites
        # 0x1D0000 0x000100     prom

        # thunderx common
        func_map = {}
        def thunderx_common_proms(contents):
            out_chunks = {}
            out_chunks["873a08.f20"] = transforms.cut(contents, 0x1D0000, length = 0x100)
            return out_chunks
        func_map['proms'] = thunderx_common_proms
        def thunderx_common_sprites(contents):
            sets = [
                {
                    'filenames': [
                        "873c04a.f11",
                        "873c04c.f10"
                    ],
                    'start': 0x150000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c05a.f9",
                        "873c05c.f8"
                    ],
                    'start': 0x190000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c04b.e11",
                        "873c04d.e10"
                    ],
                    'start': 0x170000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c05b.e9",
                        "873c05d.e8"
                    ],
                    'start': 0x1B0000,
                    'length': 0x20000
                },

            ]
            out_tiles = {}
            for curr_set in sets:
                temp_contents = transforms.cut(contents, curr_set['start'], length = curr_set['length'])
                chunks = transforms.deinterleave(temp_contents, 2, 1)
                out_tiles.update(dict(zip(curr_set['filenames'], chunks)))
            return out_tiles
        func_map['sprites'] = thunderx_common_sprites
        
        def thunderx_common_tiles(contents):
            sets = [
                {
                    'filenames': [
                        "873c06a.f6",
                        "873c06c.f5"
                    ],
                    'start': 0x0D0000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c07a.f4",
                        "873c07c.f3"
                    ],
                    'start': 0x110000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c06b.e6",
                        "873c06d.e5",
                    ],
                    'start': 0x0F0000,
                    'length': 0x20000
                },
                {
                    'filenames': [
                        "873c07b.e4",
                        "873c07d.e3",
                    ],
                    'start': 0x130000,
                    'length': 0x20000
                },

            ]
            out_tiles = {}
            for curr_set in sets:
                temp_contents = transforms.cut(contents, curr_set['start'], length = curr_set['length'])
                chunks = transforms.deinterleave(temp_contents, 2, 1)
                out_tiles.update(dict(zip(curr_set['filenames'], chunks)))
            return out_tiles
        func_map['tiles'] = thunderx_common_tiles
        common_file_map = helpers.process_rom_files(contents, func_map)

        # thunderx common audio
        func_map = {}
        def thunderx_common_audiocpu(contents):
            contents = transforms.cut(contents, 0x20000, length = 0x8000)
            return {"873-f01.f8": contents}
        func_map['audiocpu'] = thunderx_common_audiocpu
        common_audio_file_map = helpers.process_rom_files(contents, func_map)

        # thunderxj
        func_map = {}
        def thunderxj_maincpu(contents):
            filenames = [
                "873-n02.k13",
                "873-n03.k15"
            ]
            contents = transforms.cut(contents, 0x00000, length = 0x20000)
            chunks = transforms.equal_split(contents, 2)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = thunderxj_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        func_map['audio'] = helpers.existing_files_helper(common_audio_file_map)
        out_files.append({'filename': 'thunderxj.zip', 'contents': helpers.build_rom(contents, func_map)})

        # thunderxb
        func_map = {}
        def thunderxb_maincpu(contents):
            filenames = [
                "873-02.k13",
                "873-03.k15"
            ]
            contents = transforms.cut(contents, 0x28000, length = 0x20000)
            chunks = transforms.equal_split(contents, 2)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = thunderxb_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        func_map['audio'] = helpers.existing_files_helper(common_audio_file_map)
        out_files.append({'filename': 'thunderxb.zip', 'contents': helpers.build_rom(contents, func_map)})

        # thunderx
        func_map = {}
        def thunderx_maincpu(contents):
            filenames = [
                "873-s02.k13",
                "873-s03.k15"
            ]
            contents = transforms.cut(contents, 0x48000, length = 0x20000)
            chunks = transforms.equal_split(contents, 2)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = thunderx_maincpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        func_map['audio'] = helpers.existing_files_helper(common_audio_file_map)
        out_files.append({'filename': 'thunderx.zip', 'contents': helpers.build_rom(contents, func_map)})

        # thunderxa
        func_map = {}
        def thunderxa_maincpu(contents):
            filenames = [
                "873-k02.k13",
                "873-k03.k15"
            ]
            contents = transforms.cut(contents, 0xA8000, length = 0x20000)
            chunks = transforms.equal_split(contents, 2)
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = thunderxa_maincpu
        def thunderxa_audiocpu(contents):
            contents = transforms.cut(contents, 0xC8000, length = 0x8000)
            return {"873-h01.f8": contents}
        func_map['audiocpu'] = thunderxa_audiocpu
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        out_files.append({'filename': 'thunderxa.zip', 'contents': helpers.build_rom(contents, func_map)})

        return out_files


    def _handle_salamand(self, contents):
        contents = transforms.cut(contents, 0x4165D0, length=752816)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)
        out_files = []

        #                                   salamand        salamandj       lifefrce        lifefrcej
        # 0x000000  0x20000     maincpu2                    X
        # 0x020000  0x40000     
        # 0x060000  0x08000     audiocpu    X               X
        # 0x068000  0x20000     krom        X               X               X               X
        # 0x088000  0x20000     maincpu2    X
        # 0x0A8000  0x40000     maincpu1    X               X               X
        # 0x0E8000  0x20000     maincpu2                                    X
        # 0x108000  0x40000     ???
        # 0x148000  0x08000     audiocpu                                    X
        # 0x150000  0x20000     ???
        # 0x170000  0x20000     maincpu2                                                    X
        # 0x170000  0x20000     maincpu1                                                    X
        # 0x1D0000  0x08000     audiocpu                                                    X
        # 0x1D8000  0x04000     vlm         X               X
        # 0x1DC000  0x04000     vlm                                         X               X

        # all common
        func_map = {}
        def krom(contents):
            out_chunks = {}
            out_chunks["587-c01.10a"] = transforms.cut(contents, 0x068000, length = 0x20000)
            return out_chunks
        func_map['krom'] = krom
        all_common_file_map = helpers.process_rom_files(contents, func_map)

        # salamand common
        func_map = {}
        def salamand_vlm(contents):
            out_chunks = {}
            out_chunks["587-d08.8g"] = transforms.cut(contents, 0x1D8000, length = 0x4000)
            return out_chunks
        func_map['vlm'] = salamand_vlm
        def salamand_audiocpu(contents):
            out_chunks = {}
            out_chunks["587-d09.11j"] = transforms.cut(contents, 0x060000, length = 0x8000)
            return out_chunks
        func_map['audiocpu'] = salamand_audiocpu
        salamand_common_file_map = helpers.process_rom_files(contents, func_map)

        # common maincpu1
        func_map = {}
        def common_maincpu1(contents):
            filenames = [
                "587-c03.17b",
                "587-c06.17c",
            ]
            contents = transforms.cut(contents, 0xA8000, length = 0x40000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu1'] = common_maincpu1
        common_maincpu1_file_map = helpers.process_rom_files(contents, func_map)

        # salamand
        func_map = {}
        def salamand_maincpu2(contents):
            filenames = [
                "587-d02.18b",
                "587-d05.18c",
            ]
            contents = transforms.cut(contents, 0x88000, length = 0x20000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu2'] = salamand_maincpu2
        func_map['all'] = helpers.existing_files_helper(all_common_file_map)
        func_map['salamand-common'] = helpers.existing_files_helper(salamand_common_file_map)
        func_map['common-maincpu1'] = helpers.existing_files_helper(common_maincpu1_file_map)
        out_files.append({'filename': 'salamand.zip', 'contents': helpers.build_rom(contents, func_map)})

        # salamandj
        func_map = {}
        def salamandj_maincpu2(contents):
            filenames = [
                "587-j02.18b",
                "587-j05.18c",
            ]
            contents = transforms.cut(contents, 0x00000, length = 0x20000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu2'] = salamandj_maincpu2
        func_map['all'] = helpers.existing_files_helper(all_common_file_map)
        func_map['salamand-common'] = helpers.existing_files_helper(salamand_common_file_map)
        func_map['common-maincpu1'] = helpers.existing_files_helper(common_maincpu1_file_map)
        out_files.append({'filename': 'salamandj.zip', 'contents': helpers.build_rom(contents, func_map)})

        # lifefrce
        func_map = {}
        def lifefrce_maincpu2(contents):
            filenames = [
                "587-k02.18b",
                "587-k05.18c",
            ]
            contents = transforms.cut(contents, 0xE8000, length = 0x20000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu2'] = lifefrce_maincpu2
        func_map['all'] = helpers.existing_files_helper(all_common_file_map)
        def lifefrce_vlm(contents):
            out_chunks = {}
            out_chunks["587-k08.8g"] = transforms.cut(contents, 0x1DC000, length = 0x4000)
            return out_chunks
        func_map['vlm'] = lifefrce_vlm
        def lifefrce_audiocpu(contents):
            out_chunks = {}
            out_chunks["587-k09.11j"] = transforms.cut(contents, 0x148000, length = 0x8000)
            return out_chunks
        func_map['audiocpu'] = lifefrce_audiocpu
        func_map['common-maincpu1'] = helpers.existing_files_helper(common_maincpu1_file_map)
        out_files.append({'filename': 'lifefrce.zip', 'contents': helpers.build_rom(contents, func_map)})

        # lifefrcej
        func_map = {}
        def lifefrcej_maincpu2(contents):
            filenames = [
                "587-n02.18b",
                "587-n05.18c",
            ]
            contents = transforms.cut(contents, 0x170000, length = 0x20000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu2'] = lifefrcej_maincpu2
        func_map['all'] = helpers.existing_files_helper(all_common_file_map)
        def lifefrcej_vlm(contents):
            out_chunks = {}
            out_chunks["587-n08.8g"] = transforms.cut(contents, 0x1DC000, length = 0x4000)
            return out_chunks
        func_map['vlm'] = lifefrcej_vlm
        def lifefrcej_audiocpu(contents):
            out_chunks = {}
            out_chunks["587-n09.11j"] = transforms.cut(contents, 0x1D0000, length = 0x8000)
            return out_chunks
        func_map['audiocpu'] = lifefrcej_audiocpu
        def lifefrcej_maincpu1(contents):
            filenames = [
                "587-n03.17b",
                "587-n06.17c",
            ]
            contents = transforms.cut(contents, 0x190000, length = 0x40000)
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu1'] = lifefrcej_maincpu1
        out_files.append({'filename': 'lifefrcej.zip', 'contents': helpers.build_rom(contents, func_map)})

        return out_files

    def _handle_twinbee(self, full_contents):
        out_files = []
        
        # Get FSE files Nemesis
        contents = transforms.cut(full_contents, 0x2F2DE0, length=541168)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)

        func_map = {}
        def k_rom(contents):
            filenames = [
                "400-a01.fse",
                "400-a02.fse"
            ]
            contents = transforms.cut(contents, 0x84000, length = 0x200)
            chunks = transforms.equal_split(contents, len(filenames))
            return dict(zip(filenames, chunks))
        func_map['k005289'] = k_rom
        fse_file_map = helpers.process_rom_files(contents, func_map)

        # Get the maincpu1
        contents = transforms.cut(full_contents, 0x5407E0, length=67191)
        lzd = lzma.LZMADecompressor()
        contents = lzd.decompress(contents)

        func_map = {}
        def maincpu1(contents):
            filenames = [
                "412-a05.17l",
                "412-a07.12l"
            ]
            chunks = transforms.deinterleave(contents, 2, 1)
            return dict(zip(filenames, chunks))
        func_map['maincpu1'] = maincpu1
        maincpu1_file_map = helpers.process_rom_files(contents, func_map)


        func_map = {}
        func_map['fse'] = helpers.existing_files_helper(fse_file_map)
        func_map['maincpu1'] = helpers.existing_files_helper(maincpu1_file_map)
        out_files.append({'filename': 'twinbee.zip', 'contents': helpers.build_rom(contents, func_map)})

        # # Bubble ROM
        # func_map = {}
        # def main(contents):
        #     contents = transforms.cut(contents, 0x00000, length = 0x40000)
        #     chunks = transforms.deinterleave(contents, 2, 1)
        #     return dict(zip(['twinbee.bin'], chunks))
        # func_map['main'] = main
        # out_files.append({'filename': 'twinbeeb.zip', 'contents': helpers.build_rom(contents, func_map)})


        return out_files
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
        # zip_files["twinbee.bin"] = transforms.cut(decomp_merged, 0x1358A2A, length=0x402F0)

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
                print(f'offset {hex(offset)}: skipping, invalid comp_type')
                offset += 1
            else:
                try:
                    target = in_data[offset:]
                    before_len = len(target)
                    magic_bytes = in_data[offset:offset+5]
                    lzd = lzma.LZMADecompressor()
                    curr_chunk = lzd.decompress(target)
                    after_len = len(lzd.unused_data)
                    consumed_bytes = before_len - after_len
                    print(f'offset {hex(offset)}: magic {magic_bytes}, consumed {consumed_bytes} bytes')
                    with open(os.path.join(out_dir, f'decompressed_blob_{hex(offset)}'), "wb") as out_file:
                        out_file.write(curr_chunk)
                    out_data += curr_chunk
                    offset += consumed_bytes
                except lzma.LZMAError:
                    print(f'offset {hex(offset)}: magic {magic_bytes}, invalid')
                    offset += 1
        return out_data
