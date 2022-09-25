'''Implementation of psikyo: Psikyo Shooter Collector's Bundle'''
import glob
import logging
import os
from gex.lib.utils.blob import transforms
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class PsikyoTask(BaseTask):
    '''Implements psikyo: Psikyo Shooter Collector's Bundle'''
    _task_name = "psikyo"
    _title = "Psikyo Shooter Collector's Bundle"
    _details_markdown = '''
'''
    _game_info_list = [
        {
            "game": "Dragon Blaze",
            "in": {
                "base_dir": "Dragon Blaze\\Data"
            },
            "filename": "dragnblz.zip",
            "status": "partial",
            "handler": "_handle_dragnblz",
            "notes": []
        },
        {
            "game": "Strikers 1945",
            "in": {
                "base_dir": "STRIKERS1945\\Data"
            },
            "filename": "s1945.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "Strikers 1945 II",
            "in": {
                "base_dir": "STRIKERS1945 Ⅱ\\Data"
            },
            "filename": "s1945ii.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "Strikers 1945 III",
            "in": {
                "base_dir": "STRIKERS1945 III\\Data"
            },
            "filename": "s1945iii.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "GUNBARICH",
            "in": {
                "base_dir": "GUNBARICH\\Data"
            },
            "filename": "gnbarich.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "GUNBIRD",
            "in": {
                "base_dir": "GUNBIRD\\Data"
            },
            "filename": "gunbird.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "GUNBIRD 2",
            "in": {
                "base_dir": "GUNBIRD2\\Data"
            },
            "filename": "gunbird2.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "SOL DIVIDE -SWORD OF DARKNESS-",
            "in": {
                "base_dir": "SOL DIVIDE -SWORD OF DARKNESS-\\Data"
            },
            "filename": "soldivid.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "ZERO GUNNER 2",
            "in": {
                "base_dir": "ZERO GUNNER 2-\\Data"
            },
            "filename": "zerogu2.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "TENGAI",
            "in": {
                "base_dir": "TENGAI\\Data"
            },
            "filename": "tengai.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "Samurai Aces",
            "in": {
                "base_dir": "Samurai Aces\\Data"
            },
            "filename": "samuraia.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        },
        {
            "game": "Samurai Aces III: Sengoku Cannon",
            "in": {
                "base_dir": "SENGOKU CANNON\\Data"
            },
            "filename": "sngkace.zip",
            "status": "partial",
            "handler": "_handle_copyorig",
            "notes": []
        }
    ]
    _out_file_notes = {}
    _default_input_folder = helpers.STEAM_APP_ROOT
    _input_folder_desc = "Steam library root"

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': x['game'],
            'status': x['status'],
            'system': "Arcade",
            "notes": x['notes']},
            self._game_info_list)

    def _read_all_files(self, base_path):
        file_paths = glob.glob(base_path + '\\**\\*.*', recursive=True)
        files = {}
        for file_path in file_paths:
            with open(file_path, 'rb') as file_obj:
                file_data = file_obj.read()
                files[os.path.basename(file_path)] = file_data
        return files

    def execute(self, in_dir, out_dir):
        output_files = []
        for game in self._game_info_list:
            if game.get('status') == 'partial' and not self._props.get('include-partials'):
                logger.info(f"Skipping {game['game']} as complete extraction isn't possible.")
                continue

            game_dir = os.path.join(in_dir, game['in']['base_dir'])
            if os.path.exists(game_dir):
                logger.info(f"Extracting {game['game']}...")

                # Load the files
                in_files = self._read_all_files(game_dir)
                # in_files = {}
                # for in_path_fragment in game['in']['files']:
                #     in_path = os.path.join(game_dir, in_path_fragment)
                #     with open(in_path, "rb") as curr_file:
                #         in_files[in_path_fragment] = curr_file.read()

                if 'handler' in game:
                    handler_func = getattr(self, game['handler'])
                    output_files.append(handler_func(in_files, game))
                else:
                    logger.warning(f"No handler defined for {game['game']}")

        for output_file in output_files:
            with open(os.path.join(out_dir, output_file['filename']), "wb") as out_file:
                out_file.write(output_file['contents'])

        logger.info("Processing complete.")


    def _handle_dragnblz(self, in_files, game_info):
        func_map = {}

        # Temporary working
        def raw_files(in_files): 
            return {f'orig/{k}':v for (k,v) in in_files.items()}
        func_map["raw"] = raw_files

        # maincpu - identical, but 426b missing at the end of each file
        def maincpu(in_files): 
            contents = in_files['SH922.BIN']
            contents = transforms.swap_endian(contents)
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=2)
            filenames = [
                "2prog_h.u21",
                "1prog_l.u22"
            ]
            return dict(zip(filenames, chunks))
        func_map['maincpu'] = maincpu

        # # gfx1_1
        # def gfx1_1(in_files): 
        #     contents = in_files['CGCMN.BIN']
        #     chunks = transforms.deinterleave(contents, num_ways=2, word_size=2)
        #     filenames = [
        #         "2prog_h.u21",
        #         "1prog_l.u22"
        #     ]
        #     return dict(zip(filenames, chunks))
        # func_map['gfx1_1'] = gfx1_1

        return {'filename': game_info['filename'], 'contents': helpers.build_rom(in_files, func_map)}

        
    def _handle_copyorig(self, in_files, game_info):
        func_map = {}

        # Temporary working
        def raw_files(in_files): 
            return {f'orig/{k}':v for (k,v) in in_files.items()}
        func_map["raw"] = raw_files

        return {'filename': game_info['filename'], 'contents': helpers.build_rom(in_files, func_map)}
