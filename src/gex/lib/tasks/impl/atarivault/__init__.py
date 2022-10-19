'''Implementation of atarivault: Atari Vault'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.atarivault import arcade

logger = logging.getLogger('gextoolbox')

class AtariVaultTask(BaseTask):
    '''Implements atarivault: Atari Vault'''
    _task_name = "atarivault"
    _title = "Atari Vault"
    _details_markdown = '''
ROM files are in the installation folder, but arcade ROMS need rebuilt and only work in MAME 2003.
Some arcade ROMs based on https://gist.githubusercontent.com/cxx/6d1d44ce4a6107ed80e0a6c8c5b887c4/raw/d3cae583024f44c06d69a55d867066084838c2f7/avault2mame.js
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Atari Vault")
    _input_folder_desc = "Atari Vault install folder"
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

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        if self._props.get('include-2600'):
            self.extract_console_set(in_dir, out_dir, '2600')
        if self._props.get('include-5200'):
            self.extract_console_set(in_dir, out_dir, '5200')
        if self._props.get('include-prototype'):
            self.extract_console_set(in_dir, out_dir, 'prototype')
        if self._props.get('include-mnetwork'):
            self.extract_console_set(in_dir, out_dir, 'mnetwork')
        if self._props.get('include-arcade'):
            include_partials = self._props.get('include-arcade-partials')
            arcade.extract(in_dir, out_dir, self, include_partials)

        logger.info("Processing complete.")

    
    def extract_console_set(self, in_dir, out_dir, game_set):
        '''Extract Atari Console ROMs'''
            
        for file_metadata in self._metadata['in']['files'].values():
            resolved_file = self.read_datafile(in_dir, file_metadata)
            if 'copy_to' in file_metadata:
                out_file_entries = [x for x in self._metadata['out']['files'] if x['game'] == file_metadata['copy_to'] and x['set'] == game_set]
                # Set isn't used in verification. Make 2600/5200/Arcade rom names unique, but keep the set match here
                if len(out_file_entries) == 1:
                    out_file_entry = out_file_entries[0]
                    logger.info(f"Copying {out_file_entry['game']}...")
                    filename = out_file_entry['filename']
                    _ = self.verify_out_file(filename, resolved_file['contents'])
                    out_path = os.path.join(out_dir, filename)
                    with open(out_path, "wb") as out_file:
                        out_file.write(resolved_file['contents'])

