'''Implementation of sadxgg: Sonic Adventure DX - Game Gear'''
import logging
import os

from gex.lib.tasks.basetask import BaseTask
from gex.lib.archive.prs import DecompressPrs

logger = logging.getLogger('gextoolbox')

class SonicAdventureDXGameGearTask(BaseTask):
    '''Implements sadxgg: Sonic Adventure DX - Game Gear'''
    _task_name = "sadxgg"
    _title = "Sonic Adventure DX - Game Gear"
    _details_markdown = '''
Largely based on:
Romextract.sh - https://gitlab.com/vaiski/romextract/tree/master

However, this doesn't use an external PRS tool and is intended to target Sonic Adventure DX from Steam.
PRS Code from: https://forums.qhimm.com/index.php?topic=11225.0

 **Game**                                                    | **Region**        | **Filename**  
--------------------------------------------------------|---------------|----------------------------   
 **G-Sonic - Sonic Blast**                                   | World             | G-Sonic - Sonic Blast (World).gg  
 **Sonic Labyrinth**                                         | World             | Sonic Labyrinth (World).gg  
 **Dr. Robotnik's Mean Bean Machine**                        | USA,Europe        | Dr. Robotnik's Mean Bean Machine (USA,Europe).gg  
 **Sonic Drift 2**                                           | Japan,USA         | Sonic Drift 2 (Japan,USA).gg  
 **Tails no Skypatrol**                                      | Japan             | Tails no Skypatrol (Japan).gg  
 **Sonic The Hedgehog 2**                                    | World             | Sonic The Hedgehog 2 (World).gg  
 **Sonic Chaos**                                             | USA,Europe        | Sonic Chaos (USA,Europe).gg  
 **Sonic Drift**                                             | Japan             | Sonic Drift (Japan).gg  
 **Sonic The Hedgehog (Rev 1)**                              | World             | Sonic The Hedgehog (Rev 1) (World).gg  
 **Sonic & Tails**                                           | Japan             | Sonic & Tails (Japan).gg  
 **Sonic & Tails 2**                                         | Japan             | Sonic & Tails 2 (Japan).gg  
 **Sonic Spinball**                                          | USA,Europe        | Sonic Spinball (USA,Europe).gg  
 **Sonic The Hedgehog - Triple Trouble**                     | USA,Europe        | Sonic The Hedgehog - Triple Trouble (USA,Europe).gg  
 **Tails Adventures**                                        | World             | Tails Adventures (World).gg  
    '''
    _default_input_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Sonic Adventure DX"
    _input_folder_desc = "Sonic Adventure DX Steam folder"
    _short_description = ""


    def execute(self, in_dir, out_dir):
        bundle_files = self._find_files(in_dir)
        for file_path in bundle_files:
            file_name = os.path.basename(file_path)
            game_info = self._game_info_map.get(file_name)
            if game_info:
                logger.info(f"Extracting {file_path}: {game_info['name']}")
                with open(file_path, 'rb') as in_file:
                    in_data = in_file.read()
                    prs = DecompressPrs(in_data)
                    rom_data = prs.decompress()
                    filename = f"{game_info['name']} ({game_info['region']}).gg"
                    with open(os.path.join(out_dir, filename), "wb") as out_file:
                        out_file.write(rom_data)
            else:
                logger.info(f'Skipping {file_path} as it contains no known ROMS!')

        logger.info("Processing complete.")

    def _find_files(self, base_path):
        new_paths = []
        for filename in self._game_info_map:
            new_path = os.path.join(base_path, 'system', filename)
            if os.path.exists(new_path):
                new_paths.append(new_path)
            else:
                logging.warning(f"Could not find {filename} in {base_path}")
        return new_paths

    _game_info_map = {
        "g-sonic.prs": {
            'name': "G-Sonic - Sonic Blast",
            'region': "World"
        },
        "labylin.prs": {
            'name': "Sonic Labyrinth",
            'region': "World"
        },
        "mbmachin.prs": {
            'name': "Dr. Robotnik's Mean Bean Machine",
            'region': "USA,Europe"
        },
        "s-drift2.prs": {
            'name': "Sonic Drift 2",
            'region': "Japan,USA"
        },
        "skypat.prs": {
            'name': "Tails no Skypatrol",
            'region': "Japan"
        },
        "sonic2.prs": {
            'name': "Sonic The Hedgehog 2",
            'region': "World"
        },
        "sonic-ch.prs": {
            'name': "Sonic Chaos",
            'region': "USA,Europe"
        },
        "sonicdri.prs": {
            'name': "Sonic Drift",
            'region': "Japan"
        },
        "sonic.prs": {
            'name': "Sonic The Hedgehog (Rev 1)",
            'region': "World"
        },
        "sonictai.prs": {
            'name': "Sonic & Tails",
            'region': "Japan"
        },
        "sonic_tt.prs": {
            'name': "Sonic & Tails 2",
            'region': "Japan"
        },
        "spinball.prs": {
            'name': "Sonic Spinball",
            'region': "USA,Europe"
        },
        "s-tail2.prs": {
            'name': "Sonic The Hedgehog - Triple Trouble",
            'region': "USA,Europe"
        },
        "tailsadv.prs": {
            'name': "Tails Adventures",
            'region': "World"
        }
    }
