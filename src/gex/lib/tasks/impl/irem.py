'''Implments irem: Irem Arcade Hits'''
from io import BytesIO
import logging
import os
from zipfile import ZipFile
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class IremTask(BaseTask):
    '''Implments irem: Irem Arcade Hits'''
    _task_name = "irem"
    _title = "Irem Arcade Hits"
    _details_markdown = '''
Uses Windows version from https://www.gamefools.com/pc-games/irem-arcade-hits.html
Based on dotemu2mame.js: https://gist.github.com/cxx/81b9f45eb5b3cb87b4f3783ccdf8894f
    '''
    _default_input_folder = r"C:\Program Files (x86)\GameFools\Irem Arcade Hits"
    _input_folder_desc = "Irem Arcade Hits install folder"

    _game_info_map = {
        "airduel": {
            "name": "Air Duel",
            "status": "playable"
        },
        "bchopper": {
            "name": "Battle Chopper",
            "status": "NYI"
        },
        "bmaster": {
            "name": "Battle Master",
            "status": "playable"
        },
        "cosmccop": {
            "name": "Cosmic Cop",
            "status": "playable"
        },
        "dbreed72": {
            "name": "Dragon Breed",
            "status": "playable",
            "mame_name": 'dbreedm72'
        },
        "gunforce": {
            "name": "Gunforce",
            "status": "NYI"
        },
        "gunforc2": {
            "name": "Gunforce 2",
            "status": "NYI"
        },
        "hharry": {
            "name": "Hammerin' Harry",
            "status": "NYI"
        },
        "imgfight": {
            "name": "Image Fight",
            "status": "NYI"
        },
        "inthunt": {
            "name": "In the Hunt",
            "status": "NYI"
        },
        "kungfum": {
            "name": "Kung-Fu Master", # ("b-6f-.bin" is missing)
            "status": "NYI"
        },
        "loht": {
            "name": "Legend of Hero Tonma",
            "status": "NYI"
        },
        "mrheli": {
            "name": "Mr. HELI no Daibouken",
            "status": "NYI"
        },
        "mysticri": {
            "name": "Mystic Riders",
            "status": "NYI"
        },
        "nspirit": {
            "name": "Ninja Spirit", # ("proms" and "plds" ROMs are missing)
            "status": "NYI"
        },
        "rtypeleo": {
            "name": "R-Type Leo",
            "status": "NYI"
        },
        "ssoldier": {
            "name": "Superior Soldiers",
            "status": "NYI"
        },
        "uccops": {
            "name": "Undercover Cops",
            "status": "NYI"
        },
        "uccopsj": {
            "name": "Undercover Cops (J)",
            "status": "NYI"
        },
        "vigilant": {
            "name": "Vigilante", # ("plds" ROMs are missing)
            "status": "NYI"
        }
    }

    _out_file_notes = {
        "1": "This game requires MAME 2010 due to an older input file structure/variant. Some are also missing an MCU or PIDS rom, but play OK."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda in_name, game: {
            'filename': f"{game['mame_name'] if 'mame_name' in game else in_name}.zip",
            'game': f"{game['name']}",
            'system': "Arcade",
            "status": game['status'],
            "notes": [1]},
            self._game_info_map.items())

    def _read_irem_game(self, name, in_dir):
        '''Handle the zip-in-zip packaging format'''
        file_name = f"arcade_{name}.zip"
        file_path = os.path.join(in_dir, "gamefiles", "Games", "roms", file_name)
        with ZipFile(file_path, 'r') as outer_zip:
            inner_zip_bytes = outer_zip.read(file_name)

        inner_zip_file = BytesIO(inner_zip_bytes)
        out_files = {}
        with ZipFile(inner_zip_file, 'r') as inner_zip:
            for filename in inner_zip.namelist():
                out_files[filename] = inner_zip.read(filename)

        return out_files

    def execute(self, in_dir, out_dir):
        '''Main implementation call for the extraction task'''
        logger.info("Processing complete.")

        for in_name, game in self._game_info_map.items():
            logger.info(f"Extracting {game['name']}...")
            in_files = self._read_irem_game(in_name, in_dir)
            handler_func = self.find_handler_func(in_name)
            contents = handler_func(in_files)
            if contents:
                filename = f"{game['mame_name'] if 'mame_name' in game else in_name}.zip"
                logger.info(f"Saving {game['name']} as {filename}...")
                with open(os.path.join(out_dir, filename), "wb") as out_file:
                    out_file.write(contents)



    def _handle_airduel(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'ad-c-l0.bin', 'ad-c-l3.bin', 'ad-c-h0.bin', 'ad-c-h3.bin'
        ]
        def maincpu(in_files):
            contents = in_files['CPU.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.equal_split, 2)
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # GFX1 - Sprites
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['ad-00.bin', 'ad-10.bin', 'ad-20.bin', 'ad-30.bin']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['ad-a0.bin', 'ad-a1.bin', 'ad-a2.bin', 'ad-a3.bin']
        )

        # GFX3
        func_map['gfx3'] = helpers.equal_split_helper(
            'GFX3.BIN',
            ['ad-b0.bin', 'ad-b1.bin', 'ad-b2.bin', 'ad-b3.bin']
        )

        # Samples
        func_map['samples'] = helpers.name_file_helper(
            'SAMPLES.BIN',
            'ad-v0.bin'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_bchopper(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'c-l0-b.rom', 'c-l1-b.rom', 'c-l3-b.rom',
            'c-h0-b.rom', 'c-h1-b.rom', 'c-h3-b.rom'
        ]
        def maincpu(in_files):
            contents = in_files['CPU.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.equal_split, 4)
            del chunks[6]
            del chunks[2]
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # GFX1 - Sprites
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['c-00-a.rom', 'c-01-b.rom', 'c-10-a.rom', 'c-11-b.rom',
             'c-20-a.rom', 'c-21-b.rom', 'c-30-a.rom', 'c-31-b.rom']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['b-a0-b.rom', 'b-a1-b.rom', 'b-a2-b.rom', 'b-a3-b.rom']
        )

        # GFX3
        func_map['gfx3'] = helpers.equal_split_helper(
            'GFX3.BIN',
            ['b-b0-.rom', 'b-b1-.rom', 'b-b2-.rom', 'b-b3-.rom']
        )

        # Samples
        func_map['samples'] = helpers.name_file_helper(
            'SAMPLES.BIN',
            'c-v0-b.rom'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_bmaster(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'bm_d-l0-b.5f', 'bm_d-l1-b.5j', 'bm_d-h0-b.5m', 'bm_d-h1-b.5l'
        ]
        def maincpu(in_files):
            contents = in_files['CPU1.BIN']
            contents = transforms.cut(contents, 0, length=0xa0000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.custom_split, [0x40000, 0x10000])
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # soundcpu
        soundcpu_filenames = [
            'bm_d-sl0.rom', 'bm_d-sh0.rom'
        ]
        def soundcpu(in_files):
            contents = in_files['CPU2.BIN']
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(soundcpu_filenames, chunks))
        func_map['soundcpu'] = soundcpu

        # GFX1 - Sprites
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['bm_c0.rom', 'bm_c1.rom', 'bm_c2.rom', 'bm_c3.rom']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['bm_000.rom', 'bm_010.rom', 'bm_020.rom', 'bm_030.rom']
        )

        # Samples
        func_map['sound'] = helpers.name_file_helper(
            'SOUND.BIN',
            'bm_da.rom'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_cosmccop(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'cc-d-l0b.bin', 'cc-d-h0b.bin'
        ]
        def maincpu(in_files):
            contents = in_files['CPU1.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # soundcpu
        func_map['soundcpu'] = helpers.name_file_helper(
            'CPU2.BIN',
            'cc-d-sp.bin'
        )

        # GFX1 - Sprites
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['cc-c-00.bin', 'cc-c-10.bin', 'cc-c-20.bin', 'cc-c-30.bin']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['cc-d-g00.bin', 'cc-d-g10.bin', 'cc-d-g20.bin', 'cc-d-g30.bin']
        )

        # Samples
        func_map['samples'] = helpers.name_file_helper(
            'SAMPLES.BIN',
            'cc-c-v0.bin'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_dbreed72(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'db_c-l3.rom', 'db_c-l0.rom', 'db_c-h3.rom', 'db_c-h0.rom'
        ]
        def maincpu(in_files):
            contents = in_files['CPU.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.custom_split, [0x20000, 0x10000, 0x10000])
            del chunks[4]
            del chunks[1]
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu


        # GFX1 - Sprites
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['db_k800m.00', 'db_k801m.10', 'db_k802m.20', 'db_k803m.30']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['db_k804m.a0', 'db_k805m.a1', 'db_k806m.a2', 'db_k807m.a3']
        )

        # GFX3
        func_map['gfx3'] = helpers.equal_split_helper(
            'GFX3.BIN',
            ['db_k804m.b0', 'db_k805m.b1', 'db_k806m.b2', 'db_k807m.b3']
        )

        # Samples
        func_map['samples'] = helpers.name_file_helper(
            'SAMPLES.BIN',
            'db_c-v0.rom'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_gunforce(self, in_files):
        func_map = {}
        
        # maincpu
        maincpu_filenames = [
            'gf_l0-c.5f', 'gf_l1-c.5j', 'gf_h0-c.5m', 'gf_h1-c.5l'
        ]
        def maincpu(in_files):
            contents = in_files['CPU1.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.equal_split, 2)
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # soundcpu
        soundcpu_filenames = [
            'gf_sl0.rom', 'gf_sh0.rom'
        ]
        def soundcpu(in_files):
            contents = in_files['CPU2.BIN']
            contents = transforms.cut(contents, 0, length=0x20000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(soundcpu_filenames, chunks))
        func_map['soundcpu'] = soundcpu

        # GFX1
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            ['gf_c0.rom', 'gf_c1.rom', 'gf_c2.rom', 'gf_c3.rom']
        )

        # GFX2
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            ['gf_000.rom', 'gf_010.rom', 'gf_020.rom', 'gf_030.rom']
        )

        # Sound
        func_map['sound'] = helpers.name_file_helper(
            'SOUND.BIN',
            'gf-da.rom'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_gunforc2(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_hharry(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_imgfight(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_inthunt(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_kungfum(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_loht(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_mrheli(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_mysticri(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_nspirit(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_rtypeleo(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_ssoldier(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_uccops(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_uccopsj(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)

    def _handle_vigilant(self, in_files):
        func_map = {}
        print("NYI")
        return helpers.build_rom(in_files, func_map)
