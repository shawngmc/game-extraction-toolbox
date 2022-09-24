'''Implementation of ddragontrilogy: Double Dragon Trilogy'''
import glob
import logging
import os
from gex.lib.utils.blob import transforms
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask
from gex.lib.utils import gfx_rebuilder

logger = logging.getLogger('gextoolbox')

class DoubleDragonTrilogyTask(BaseTask):
    '''Implements ddragontrilogy: Double Dragon Trilogy'''
    _task_name = "ddragontrilogy"
    _title = "Double Dragon Trilogy"
    _details_markdown = '''
Based on dotemu2mame.js: https://gist.github.com/cxx/81b9f45eb5b3cb87b4f3783ccdf8894f
'''
    _game_info_list = [
        {
            "game": "Double Dragon",
            "filename": "ddragon.zip",
            "notes": []
        },
        {
            "game": "Double Dragon 2: The Revenge",
            "filename": "ddragon2.zip",
            "notes": []
        },
        {
            "game": "Double Dragon 3: The Rosetta Stone",
            "filename": "dragon3.zip",
            "notes": [1]
        }
    ]
    _out_file_notes = {
        "1": "This ROM is missing the PROM file. A placeholder allows it to work for MAME, but this doesn't work for FB Neo."
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("Double Dragon Trilogy")
    _input_folder_desc = "Double Dragon Trilogy Steam folder"

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['game'],
            'status': "good",
            'system': "Arcade",
            "notes": x['notes']},
            self._game_info_list)

    def execute(self, in_dir, out_dir):
        all_ddragon_trio_files = self._read_all_files(in_dir)

        funcs = [
            self._ddragon,
            self._ddragon2,
            self._ddragon3
        ]

        for func in funcs:
            logger.info(f"Extracting {func.__name__[1:]}...")
            rom_package = func(all_ddragon_trio_files)
            with open(os.path.join(out_dir, rom_package['filename']), "wb") as out_file:
                out_file.write(rom_package['contents'])

        logger.info("Processing complete.")

    def _read_all_files(self, base_path):
        files_path = os.path.join(base_path, "resources", "game")
        file_paths = glob.glob(files_path +'/*.*')
        files = {}
        for file_path in file_paths:
            with open(file_path, 'rb') as file_obj:
                file_data = file_obj.read()
                files[os.path.basename(file_path)] = file_data
        return files

    def _dotemu_reencode_gfx_helper(self, in_file_name, filenames, layout):
        def encode(in_files):
            contents = in_files[in_file_name]
            contents = gfx_rebuilder.reencode_gfx(contents, layout)
            chunks = transforms.equal_split(contents, num_chunks=len(filenames))
            return dict(zip(filenames, chunks))
        return encode

    _DDRAGON_CHAR_LAYOUT = {
        'width': 8,
        'height': 8,
        'total': [1,1],
        'planes': 4,
        'planeoffset': [0, 2, 4, 6],
        'xoffset': [1, 0, 8*8+1, 8*8+0, 16*8+1, 16*8+0, 24*8+1, 24*8+0],
        'yoffset': [0*8, 1*8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8],
        'charincrement': 32*8
    }

    _DDRAGON_TILE_LAYOUT = {
        'width': 16,
        'height': 16,
        'total': [1,2],
        'planes': 4,
        'planeoffset': [[1,2,0], [1,2,4], 0, 4],
        'xoffset': [3, 2, 1, 0, 16*8+3, 16*8+2, 16*8+1, 16*8+0,
            32*8+3, 32*8+2, 32*8+1, 32*8+0, 48*8+3, 48*8+2, 48*8+1, 48*8+0],
        'yoffset': [0*8, 1*8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8,
            8*8, 9*8, 10*8, 11*8, 12*8, 13*8, 14*8, 15*8],
        'charincrement': 64*8
    }

    def _ddragon(self, in_files):
        func_map = {}

        # MainCPU
        maincpu_filenames = [
            '21j-1-5.26',
            '21j-2-3.25',
            '21j-3.24',
            '21j-4-1.23'
        ]
        func_map['maincpu'] = helpers.equal_split_helper(
            'ddragon_hd6309.bin',
            maincpu_filenames
        )

        # Sub
        func_map['sub'] = helpers.name_file_helper(
            'ddragon_hd63701.bin',
            '21jm-0.ic55'
        )

        # SoundCPU
        func_map['soundcpu'] = helpers.name_file_helper(
            'ddragon_m6809.bin',
            '21j-0-1'
        )

        # Gfx 1
        gfx1_filesnames = [
            '21j-5'
        ]
        func_map['gfx1'] = self._dotemu_reencode_gfx_helper(
            'ddragon_gfxdata1.bin',
            gfx1_filesnames,
            self._DDRAGON_CHAR_LAYOUT)

        # Gfx 2
        gfx2_filesnames = [
            '21j-a',
            '21j-b',
            '21j-c',
            '21j-d',
            '21j-e',
            '21j-f',
            '21j-g',
            '21j-h'
        ]
        func_map['gfx2'] = self._dotemu_reencode_gfx_helper(
            'ddragon_gfxdata2.bin',
            gfx2_filesnames,
            self._DDRAGON_TILE_LAYOUT
        )

        # Gfx 3
        gfx3_filesnames = [
            '21j-8',
            '21j-9',
            '21j-i',
            '21j-j'
        ]
        func_map['gfx3'] = self._dotemu_reencode_gfx_helper(
            'ddragon_gfxdata3.bin',
            gfx3_filesnames,
            self._DDRAGON_TILE_LAYOUT
        )

        # ADPCM
        adpcm_filenames = [
            '21j-6',
            '21j-7'
        ]
        func_map['adpcm'] = helpers.equal_split_helper('ddragon_adpcm.bin', adpcm_filenames)

        # PROMs
        prom_file_map = {
            '21j-k-0': 0x100,
            '21j-l-0': 0x200
        }
        func_map['prom'] = helpers.custom_split_helper('proms.bin', prom_file_map)

        return {'filename': 'ddragon.zip', 'contents': helpers.build_rom(in_files, func_map)}

    def _ddragon2(self, in_files):
        func_map = {}

        # MainCPU
        maincpu_filenames = [
            '26a9-04.bin',
            '26aa-03.bin',
            '26ab-0.bin',
            '26ac-0e.63'
        ]
        func_map['maincpu'] = helpers.equal_split_helper('ddragon2_hd6309.bin', maincpu_filenames)

        # Sub
        func_map['sub'] = helpers.name_file_helper(
            'ddragon2_z80sub.bin',
            '26ae-0.bin'
        )

        # SoundCPU
        func_map['soundcpu'] = helpers.name_file_helper(
            'ddragon2_z80sound.bin',
            '26ad-0.bin'
        )

        # Gfx 1
        gfx1_filesnames = [
            '26a8-0e.19'
        ]
        func_map['gfx1'] = self._dotemu_reencode_gfx_helper(
            'ddragon2_gfxdata1.bin',
            gfx1_filesnames,
            self._DDRAGON_CHAR_LAYOUT
        )

        # Gfx 2
        gfx2_filesnames = [
            '26j0-0.bin',
            '26j1-0.bin',
            '26af-0.bin',
            '26j2-0.bin',
            '26j3-0.bin',
            '26a10-0.bin'
        ]
        func_map['gfx2'] = self._dotemu_reencode_gfx_helper(
            'ddragon2_gfxdata2.bin',
            gfx2_filesnames,
            self._DDRAGON_TILE_LAYOUT
        )

        # Gfx 3
        gfx3_filesnames = [
            '26j4-0.bin',
            '26j5-0.bin'
        ]
        func_map['gfx3'] = self._dotemu_reencode_gfx_helper(
            'ddragon2_gfxdata3.bin',
            gfx3_filesnames,
            self._DDRAGON_TILE_LAYOUT
        )

        # OKI
        oki_filenames = [
            '26j6-0.bin',
            '26j7-0.bin'
        ]
        func_map['oki'] = helpers.equal_split_helper(
            'ddragon2_oki.bin',
            oki_filenames
        )

        # PROMs
        prom_file_map = {
            '21j-k-0': 0x100,
            'prom.16': 0x200
        }
        func_map['prom'] = helpers.custom_split_helper(
            'proms.bin',
            prom_file_map
        )

        return {'filename': 'ddragon2.zip', 'contents': helpers.build_rom(in_files, func_map)}


    _WWF_TILE_LAYOUT = {
        'width': 16,
        'height': 16,
        'total': [1,2],
        'planes': 4,
        'planeoffset': [8, 0, [1,2,8], [1,2,0]],
        'xoffset': [0, 1, 2, 3, 4, 5, 6, 7,
                  32*8+0, 32*8+1, 32*8+2, 32*8+3, 32*8+4, 32*8+5, 32*8+6, 32*8+7],
        'yoffset': [0*16, 1*16, 2*16, 3*16, 4*16, 5*16, 6*16, 7*16,
    	      16*8, 16*9, 16*10, 16*11, 16*12, 16*13, 16*14, 16*15],
        'charincrement': 64*8
    }

    _WWF_SPRITE_LAYOUT = {
        'width': 16,
        'height': 16,
        'total': [1,4],
        'planes': 4,
        'planeoffset': [[0,4], [1,4], [2,4], [3,4]],
        'xoffset': [0, 1, 2, 3, 4, 5, 6, 7,
                  16*8+0, 16*8+1, 16*8+2, 16*8+3, 16*8+4, 16*8+5, 16*8+6, 16*8+7],
        'yoffset': [0*8, 1*8, 2*8, 3*8, 4*8, 5*8, 6*8, 7*8,
    	      8*8, 9*8, 10*8, 11*8, 12*8, 13*8, 14*8, 15*8],
        'charincrement': 32*8
    }

    def _ddragon3(self, in_files):
        func_map = {}

        # CPU
        maincpu_filenames = [
            '30a15-0.ic79',
            '30a14-0.ic78'
        ]
        def maincpu(in_files):
            contents = in_files['ddragon3_m68k.bin']
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            chunks[0] = chunks[0][0:0x20000]
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        # AudioCPU
        func_map['audiocpu'] = helpers.name_file_helper('ddragon3_z80.bin', '30a13-0.ic43')

        # Gfx 1
        gfx1_filenames = [
            '30j-6.ic5',
            '30j-4.ic7',
            '30j-7.ic4',
            '30j-5.ic6'
        ]
        def gfx1(in_files):
            contents = in_files['ddragon3_gfxdata1.bin']
            contents = gfx_rebuilder.reencode_gfx(contents, self._WWF_TILE_LAYOUT)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            contents = transforms.merge(chunks)
            chunks = transforms.equal_split(contents, len(gfx1_filenames))
            return dict(zip(gfx1_filenames, chunks))
        func_map['gfx1'] = gfx1

        # Gfx 2
        gfx2_filenames = [
            '30j-3.ic9',
            '30a12-0.ic8',
            '30j-2.ic11',
            '30a11-0.ic10',
            '30j-1.ic13',
            '30a10-0.ic12',
            '30j-0.ic15',
            '30a9-0.ic14'
        ]
        def gfx2(in_files):
            contents = in_files['ddragon3_gfxdata2.bin']
            contents = gfx_rebuilder.reencode_gfx(contents, self._WWF_SPRITE_LAYOUT)
            chunks = transforms.custom_split(contents,
                [0x80000, 0x10000, 0x80000, 0x10000, 0x80000, 0x10000, 0x80000, 0x10000])
            return dict(zip(gfx2_filenames, chunks))
        func_map['gfx2'] = gfx2

        # OKI
        func_map['oki'] = helpers.name_file_helper('ddragon3_oki.bin', '30j-8.ic73')

        # PROMs
        def dummy_prom(_):
            return {'mb7114h.ic38': bytearray(0x100)}
        func_map['prom'] = dummy_prom

        return {'filename': 'ddragon3.zip', 'contents': helpers.build_rom(in_files, func_map)}
