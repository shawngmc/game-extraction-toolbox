'''Implementation of mkak: Mortal Kombat Arcade Kollection'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class BubsyTask(BaseTask):
    '''Implements mkak: Mortal Kombat Arcade Kollection'''
    _task_name = "mkak"
    _title = "Mortal Kombat Arcade Kollection"
    _details_markdown = '''
    None of these games currently are playable, as it appears the Audio ROMs are replaced with a different audio format.

    It might be possible to convert the Audio to Ogg via instructions at:
    https://borderlands.fandom.com/wiki/Extracting_PC_resources
    Turning those into a functional (let alone CRC matching) ROM is a difficult task.
    See GH issue #25 for the most recent notes.

    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Mortal Kombat Arcade Kollection")
    _input_folder_desc = "Mortal Kombat Arcade Kollection Steam Folder"

    _out_file_list = [
        {
            "game": "Mortal Kombat",
            "system": "Arcade",
            "filename": "mkla4.zip",
            "status": "partial",
            "notes": [1]
        },
        {
            "game": "Mortal Kombat 2",
            "system": "Arcade",
            "filename": "mk2.zip",
            "status": "partial",
            "notes": [1]
        },
        {
            "game": "Ultimate Mortal Kombat 3",
            "system": "Arcade",
            "filename": "umk3.zip",
            "status": "partial",
            "notes": [1]
        }
    ]
    _out_file_notes = {
        "1": "This ROM is missing the Audio ROM files. MKAK appears to replace it with a different audio solution."
    }
    _game_info_map = {
    }

    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }
    def _find_files(self, base_path):
        new_paths = []
        for filename in self._game_info_map:
            new_path = os.path.join(base_path, filename)
            if os.path.exists(new_path):
                new_paths.append(new_path)
            else:
                logging.warning(f"Could not find {filename} in {base_path}")
        return new_paths

    def execute(self, in_dir, out_dir):
        if self._props.get('include-partials'):
            out_files = []
            out_files += self._handle_mk1(in_dir)
            out_files += self._handle_mk2(in_dir)
            out_files += self._handle_umk3(in_dir)

            for out_file in out_files:
                with open(os.path.join(out_dir, out_file['filename']), "wb") as write_file:
                    write_file.write(out_file['contents'])

            logger.info("Processing complete.")
        else:
            logger.error("mkak is not fully implemented - the audio ROMs are missing and have been replaced!")
            logger.error("To help investigate/pull partial contents, add --prop 'include-partials=True' to extract the game and graphics ROMs.")

    def _handle_mk1(self, in_dir):
        file_path = r"BINARIES\WIN32\DATA\MK1"
        in_filenames = [
            "MK1.BIN",
            "MK1AUDIO.BIN",
            "MK1COMP.BIN",
            "MK1IMAGE.BIN"
        ]

        in_files = {}
        for in_filename in in_filenames:
            with open(os.path.join(in_dir, file_path, in_filename), 'rb') as in_file:
                in_files[in_filename] = in_file.read()

        zip_files = {}

        # MAINCPU
        contents = in_files['MK1.BIN']
        chunks = transforms.deinterleave(contents, 2, 1)
        zip_files['l4_mortal_kombat_game_rom_u-105.u105'] = chunks[0]
        zip_files['l4_mortal_kombat_game_rom_u-89.u89'] = chunks[1]

        # GFX
        contents = in_files['MK1IMAGE.BIN']
        chunks = transforms.equal_split(contents, 12)
        gfx_filenames = [
            "l1_mortal_kombat_game_rom_u-111.u111",
            "l1_mortal_kombat_game_rom_u-112.u112",
            "l1_mortal_kombat_game_rom_u-113.u113",
            "l1_mortal_kombat_game_rom_u-114.u114",
            "l1_mortal_kombat_game_rom_u-95.u95",
            "l1_mortal_kombat_game_rom_u-96.u96",
            "l1_mortal_kombat_game_rom_u-97.u97",
            "l1_mortal_kombat_game_rom_u-98.u98",
            "l1_mortal_kombat_game_rom_u-106.u106",
            "l1_mortal_kombat_game_rom_u-107.u107",
            "l1_mortal_kombat_game_rom_u-108.u108",
            "l1_mortal_kombat_game_rom_u-109.u109"
        ]
        zip_files.update(dict(zip(gfx_filenames, chunks)))

        return [{'filename': "partial_mkla4.zip", 'contents': helpers.build_zip(zip_files)}]

    def _handle_mk2(self, in_dir):
        file_path = r"BINARIES\WIN32\DATA\MK2"
        in_filenames = [
            "MK2.BIN",
            "MK2AUDIO.BIN",
            "MK2COMP.BIN",
            "MK2IMAGE.BIN"
        ]

        zip_files = {}
        for in_filename in in_filenames:
            with open(os.path.join(in_dir, file_path, in_filename), 'rb') as in_file:
                zip_files[in_filename] = in_file.read()


        return [{'filename': "partial_mk2.zip", 'contents': helpers.build_zip(zip_files)}]

    def _handle_umk3(self, in_dir):
        file_path = r"BINARIES\WIN32\DATA\UMK3"
        in_filenames = [
            "UMK3.BIN",
            "UMK3AUDIO.BIN",
            "MK4COMP.BIN",
            "UMK3IMAGE.BIN"
        ]

        zip_files = {}
        for in_filename in in_filenames:
            with open(os.path.join(in_dir, file_path, in_filename), 'rb') as in_file:
                zip_files[in_filename] = in_file.read()


        return [{'filename': "partial_umk3.zip", 'contents': helpers.build_zip(zip_files)}]
