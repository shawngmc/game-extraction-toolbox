'''Implementation of zamn: Zombies Ate My Neighbors and Ghoul Patrol'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.utils.blob import hash as hash_helper

logger = logging.getLogger('gextoolbox')

class ZAMNTask(BaseTask):
    '''Implements zamn: Zombies Ate My Neighbors and Ghoul Patrol'''
    _task_name = "zamn"
    _title = "Zombies Ate My Neighbors and Ghoul Patrol"
    _details_markdown = '''
Based on: https://www.gog.com/forum/general/rom_based_gog_games_compatible_with_third_party_emulators_thread/post127

These ROMs are pulled out of the main executable. 
    '''
    _default_input_folder = r"C:\Program Files (x86)\GOG Galaxy\Games\Zombies Ate My Neighbour & Ghoul Patrol"
    _input_folder_desc = "ZAMN folder"

    _game_info_map = [
        {
            "name": "Zombies Ate My Neighbor",
            "length": 1024*1024,
            "check_offsets": [
                0x1b0974c, # Steam 1.0
                0x1b0bd4c, # Steam 1.1
                0x1b0654c, # GOG 1.0
                0x1b0894c, # GOG 1.1
            ],
            "header_bytes": "02 FE C2 10 E2 20 A2 00 00 9B",
            "crc": 0x7cfc0c7c,
            "filename": "ZombiesAteMyNeighbor.sfc"
        },
        {
            "name": "Ghoul Patrol",
            "length": 1024*1024,
            "check_offsets": [
                0x19a03c0, # Steam 1.0
                0x19a29c0, # Steam 1.1
                0x199d1c0, # GOG 1.0
                0x199f5c0, # GOG 1.1
            ],
            "header_bytes": "80 FE C2 10 E2 20 A2 00 00 9B",
            "crc": 0xea16b5a2,
            "filename": "GhoulPatrol.sfc"
        }
    ]
    _out_file_notes = {}

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'system': "SNES",
            'status': 'good',
            "notes": []},
            self._game_info_map)
        self._out_file_notes = {}

    def execute(self, in_dir, out_dir):
        exe_path = os.path.join(in_dir, "ZAMN_GP.exe")
        with open(exe_path, 'rb') as exe_file:
            exe_data = exe_file.read()

            for game in self._game_info_map:
                game_data = None
                game_header = bytes.fromhex(game['header_bytes'])
                logger.info(f"Finding {game['name']}...")

                # Try check_offsets
                logger.info(f"Finding {game['name']} via known offsets...")
                for check_offset in game['check_offsets']:
                    check_header = exe_data[check_offset:check_offset+10]
                    if check_header == game_header:
                        logger.info(f"Found header at {hex(check_offset)}!")
                        game_data = exe_data[check_offset:check_offset+game['length']]
                        crc = hash_helper.get_crc(game_data)
                        if crc == hex(game['crc']):
                            logger.info(f"Found crc match at {hex(check_offset)}!")
                            break
                        else:
                            logger.info(f"False header match at {hex(check_offset)}!")
                            game_data = None

                # Do the manual search
                if not game_data:
                    logger.info(f"Finding {game['name']} via full search - please wait...")
                    for offset in range(0, len(exe_data) - game['length']):
                        check_header = exe_data[offset:offset+10]
                        if check_header == game_header:
                            logger.info(f"Found header at {hex(offset)}!")
                            game_data = exe_data[offset:offset+game['length']]
                            crc = hash_helper.get_crc(game_data)
                            if crc == hex(game['crc']):
                                logger.info(f"Found crc match at {hex(offset)}!")
                                break
                            else:
                                logger.info(f"False header match at {hex(offset)}!")
                                game_data = None

                if game_data:
                    logger.info(f"Saving {game['filename']}...")
                    with open(os.path.join(out_dir, game['filename']), "wb") as out_file:
                        out_file.write(game_data)
                else:
                    logger.warning(f"Game {game['name']} not found!")

        logger.info("Processing complete.")
