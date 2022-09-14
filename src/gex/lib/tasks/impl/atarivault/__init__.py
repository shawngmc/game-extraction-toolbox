'''Implementation of atarivault: Atari Vault'''
import logging
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.atarivault import atari2600, atari5200, prototype2600, mnetwork, arcade

logger = logging.getLogger('gextoolbox')

class AtariVaultTask(BaseTask):
    '''Implements atarivault: Atari Vault'''
    _task_name = "atarivault"
    _title = "Atari Vault"
    _details_markdown = '''
ROM files are in the installation folder, but arcade ROMS need rebuilt and only work in MAME 2003.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Atari Vault")
    _input_folder_desc = "Atari Vault install folder"
    _short_description = ""
    _prop_info = {
        "include-2600": {
            "description": "Include Atari 2600 Games",
            "default": True,
            "type": "Boolean"
        },
        "include-5200": {
            "description": "Include Atari 5200 Games",
            "default": True,
            "type": "Boolean"
        },
        "include-mnetwork": {
            "description": "Include Atari MNetwork Games",
            "default": True,
            "type": "Boolean"
        },
        "include-prototype": {
            "description": "Include Atari Prototype Games",
            "default": True,
            "type": "Boolean"
        },
        "include-arcade": {
            "description": "Include Atari Arcade Games",
            "default": True,
            "type": "Boolean"
        },
        "include-arcade-partials": {
            "description": "Include Atari Arcade Games that cannot be converted to MAME",
            "default": False,
            "type": "Boolean"
        }
    }

    _out_file_list = []
    _out_file_list.extend(atari2600.get_game_list())
    _out_file_list.extend(atari5200.get_game_list())
    _out_file_list.extend(prototype2600.get_game_list())
    _out_file_list.extend(mnetwork.get_game_list())
    _out_file_list.extend(arcade.get_game_list())
    _out_file_list.append({
        'filename': "N/A",
        'game': "Pong",
        'system': "Arcade",
        "notes": [4]
        })

    _out_file_notes = {
        "1": "Arcade ROMs require MAME 2003.",
        "2": "This ROM has a CRC mismatch, but appears to work fine.",
        "3": "This Arcade ROM is currently non-functional - too small, etc.",
        "4": "There does not appear to be a ROM for this title",
    }

    def execute(self, in_dir, out_dir):
        # if self._props.get('include-2600'):
        #     atari2600.copy(in_dir, out_dir)
        # if self._props.get('include-5200'):
        #     atari5200.copy(in_dir, out_dir)
        # if self._props.get('include-prototype'):
        #     prototype2600.copy(in_dir, out_dir)
        # if self._props.get('include-mnetwork'):
        #     mnetwork.copy(in_dir, out_dir)
        if self._props.get('include-arcade'):
            arcade.extract(in_dir, out_dir)
        if self._props.get('include-arcade-partials'):
            arcade.extract_partials(in_dir, out_dir)

        logger.info("Processing complete.")
