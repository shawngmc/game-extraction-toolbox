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

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        zamngp_file = self.read_all_datafiles(in_dir).get("zamngp")
        exe_data = zamngp_file['contents']
        file_ver = zamngp_file['version']
        if file_ver is not None:
            logger.info(f"Found {file_ver}...")

        for game in self._metadata['out']['files']:
            game_data = None
            game_header = bytes.fromhex(game['extract']['header_bytes'])
            target_size = game['extract']['length']

            if file_ver is not None:
                logger.info(f"Pulling {game['game']} from known offset...")
                version_info = game['extract']['versions'][file_ver]
                start = int(version_info['start'], 16)
                game_data = exe_data[start:start+target_size]
            else:
                logger.info(f"Finding {game['game']}...")

                # Try check_offsets
                logger.info(f"Finding {game['game']} via known offsets...")
                for version_info in game['extract']['versions'].values():
                    check_offset = int(version_info['start'], 16)
                    check_header = exe_data[check_offset:check_offset+10]
                    if check_header == game_header:
                        logger.info(f"Found header at {hex(check_offset)}!")
                        game_data = exe_data[check_offset:check_offset+target_size]
                        crc = hash_helper.get_crc(game_data)[2:].upper().rjust(8, "0")
                        if crc == game['verify']['crc']:
                            logger.info(f"Found crc match at {hex(check_offset)}!")
                            break
                        else:
                            logger.info(f"False header match at {hex(check_offset)}!")
                            game_data = None

                # Do the manual search
                if not game_data:
                    logger.info(f"Finding {game['game']} via full search - please wait...")
                    for offset in range(0, len(exe_data) - target_size):
                        check_header = exe_data[offset:offset+10]
                        if check_header == game_header:
                            logger.info(f"Found header at {hex(offset)}!")
                            game_data = exe_data[offset:offset+target_size]
                            crc = hash_helper.get_crc(game_data)[2:].upper().rjust(8, "0")
                            if crc == game['verify']['crc']:
                                logger.info(f"Found crc match at {hex(offset)}!")
                                break
                            else:
                                logger.info(f"False header match at {hex(offset)}!")
                                game_data = None

            if game_data:
                _ = self.verify_out_file(game['filename'], game_data)
                logger.info(f"Saving {game['filename']}...")
                with open(os.path.join(out_dir, game['filename']), "wb") as out_file:
                    out_file.write(game_data)
            else:
                logger.warning(f"Game {game['game']} not found!")

        logger.info("Processing complete.")
