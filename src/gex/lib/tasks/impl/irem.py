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

    _game_info_list = [
        {
            "game": "Air Duel",
            "in_name": "airduel",
            "mame_name": "airduel",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Battle Chopper",
            "in_name": "bchopper",
            "mame_name": "bchopper",
            "status": "NYI",
            "notes": [1]
        },
        {
            "game": "Battle Master",
            "in_name": "bmaster",
            "mame_name": "bmaster",
            "status": "NYI",
            "notes": []
        },
        # {
        #     "game": "",
        #     "in_name": "cosmccop",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "dbreed72",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "gunforc2",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "gunforce",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "hharry",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "imgfight",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "inthunt",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "kungfum",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "loht",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "mrheli",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "mysticri",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "nspirit",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "rtypeleo",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "ssoldier",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "uccops",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "uccopsj",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # },
        # {
        #     "game": "",
        #     "in_name": "vigilant",
        #     "mame_name": "",
        #     "status": "NYI",
        #     "notes": []
        # }
    ]

    _out_file_notes = {
        "1": "This game requires MAME 2010 due to an older input file structure/variant. They are also missing an MCU rom, but play OK."
    }


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

        for game in self._game_info_list:
            logger.info(f"Extracting {game['game']}...")
            in_files = self._read_irem_game(game['in_name'], in_dir)
            handler_func = self.find_handler_func(game['in_name'])
            contents = handler_func(in_files)

            out_filename = f"{game['mame_name']}.zip"
            logger.info(f"Saving {game['game']} as {out_filename}...")
            with open(os.path.join(out_dir, out_filename), "wb") as out_file:
                out_file.write(contents)



    def _handle_airduel(self, in_files):
        func_map = {}

        # maincpu
        maincpu_filenames = [
            'ad-c-l0.bin',
            'ad-c-l3.bin',
            'ad-c-h0.bin',
            'ad-c-h3.bin'
        ]
        def maincpu(in_files):
            contents = in_files['CPU.BIN']
            contents = transforms.cut(contents, 0, length=0x80000)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks = transforms.transform_all(chunks, transforms.equal_split, 2)
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # GFX1 - Sprites
        gfx1_filenames = [
            'ad-00.bin',
            'ad-10.bin',
            'ad-20.bin',
            'ad-30.bin'
        ]
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            gfx1_filenames
        )

        # GFX2
        gfx2_filenames = [
            'ad-a0.bin',
            'ad-a1.bin',
            'ad-a2.bin',
            'ad-a3.bin'
        ]
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            gfx2_filenames
        )

        # GFX3
        gfx3_filenames = [
            'ad-b0.bin',
            'ad-b1.bin',
            'ad-b2.bin',
            'ad-b3.bin'
        ]
        func_map['gfx3'] = helpers.equal_split_helper(
            'GFX3.BIN',
            gfx3_filenames
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
            'c-l0-b.rom',
            'c-l1-b.rom',
            'c-l3-b.rom',
            'c-h0-b.rom',
            'c-h1-b.rom',
            'c-h3-b.rom'
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
        gfx1_filenames = [
            'c-00-a.rom',
            'c-01-b.rom',
            'c-10-a.rom',
            'c-11-b.rom',
            'c-20-a.rom',
            'c-21-b.rom',
            'c-30-a.rom',
            'c-31-b.rom'
        ]
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            gfx1_filenames
        )

        # GFX2
        gfx2_filenames = [
            'b-a0-b.rom',
            'b-a1-b.rom',
            'b-a2-b.rom',
            'b-a3-b.rom'
        ]
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            gfx2_filenames
        )

        # GFX3
        gfx3_filenames = [
            'b-b0-.rom',
            'b-b1-.rom',
            'b-b2-.rom',
            'b-b3-.rom'
        ]
        func_map['gfx3'] = helpers.equal_split_helper(
            'GFX3.BIN',
            gfx3_filenames
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
            'bm_d-l0-b.5f',
            'bm_d-l1-b.5j',
            'bm_d-h0-b.5m',
            'bm_d-h1-b.5l'
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
            'bm_d-sl0.rom',
            'bm_d-sh0.rom'
        ]
        def soundcpu(in_files):
            contents = in_files['CPU2.BIN']
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            return dict(zip(soundcpu_filenames, chunks))
        func_map['soundcpu'] = soundcpu

        # GFX1 - Sprites
        gfx1_filenames = [
            'bm_c0.rom', 'bm_c1.rom',
                     'bm_c2.rom', 'bm_c3.rom'
        ]
        func_map['gfx1'] = helpers.equal_split_helper(
            'GFX1.BIN',
            gfx1_filenames
        )

        # GFX2
        gfx2_filenames = [
            'bm_000.rom',
            'bm_010.rom',
            'bm_020.rom',
            'bm_030.rom'
        ]
        func_map['gfx2'] = helpers.equal_split_helper(
            'GFX2.BIN',
            gfx2_filenames
        )

        # Samples
        func_map['sound'] = helpers.name_file_helper(
            'SOUND.BIN',
            'bm_da.rom'
        )

        return helpers.build_rom(in_files, func_map)

    def _handle_cosmccop(self, in_files):
        print("NYI")
        return []

    def _handle_dbreed72(self, in_files):
        print("NYI")
        return []

    def _handle_gunforc2(self, in_files):
        print("NYI")
        return []

    def _handle_gunforce(self, in_files):
        print("NYI")
        return []

    def _handle_hharry(self, in_files):
        print("NYI")
        return []

    def _handle_imgfight(self, in_files):
        print("NYI")
        return []

    def _handle_inthunt(self, in_files):
        print("NYI")
        return []

    def _handle_kungfum(self, in_files):
        print("NYI")
        return []

    def _handle_loht(self, in_files):
        print("NYI")
        return []

    def _handle_mrheli(self, in_files):
        print("NYI")
        return []

    def _handle_mysticri(self, in_files):
        print("NYI")
        return []

    def _handle_nspirit(self, in_files):
        print("NYI")
        return []

    def _handle_rtypeleo(self, in_files):
        print("NYI")
        return []

    def _handle_ssoldier(self, in_files):
        print("NYI")
        return []

    def _handle_uccops(self, in_files):
        print("NYI")
        return []

    def _handle_uccopsj(self, in_files):
        print("NYI")
        return []

    def _handle_vigilant(self, in_files):
        print("NYI")
        return []
