'''Implementation of acac: Arcade Classics Anniversary Collection'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class ACACTask(BaseTask):
    '''Implements acac: Arcade Classics Anniversary Collection'''
    _task_name = "ags"
    _title = "Arcade Classics Anniversary Collection"
    _details_markdown = ''''''
    _default_input_folder = helpers.gen_steam_app_default_folder("Arcade Classics Anniversary Collection")
    _input_folder_desc = "Arcade Classics Anniversary Collection install folder"
    _short_description = ""

    # _prop_info = {
    #     "include-partials": {
    #         "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
    #         "default": False,
    #         "type": "Boolean"
    #     }
    # }

    _game_info_map = [
        # {
        #     "name": "Ms. Pac-Man",
        #     "src_path": r"Ms. PAC-MAN\Ms. PAC-MAN_Data\Plugins\Release_2.dll",
        #     "files": [
        #         {
        #             "filename": "82s126.1m",
        #             "start": 0x1AE30,
        #             "length": 0x100
        #         }
        #     ],
        #     "filename": "mspacman.zip",
        #     'partial': True,
        #     "notes": []
        # },
        {
            "name": "ajax",
            "files": [
            ],
            "filename": "ajax.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "hcastle",
            "files": [],
            "filename": "hcastle.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "nemesis",
            "files": [],
            "filename": "nemesis.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "salamand.zip",
            "files": [1],
            "filename": "salamand",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "scramble",
            "files": [],
            "filename": "scramble.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "thunderx",
            "files": [1],
            "filename": "thunderx.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "twinbee",
            "files": [
                {
                    "filename": "",
                    "start": "",
                    "length": ""
                }],
            "filename": "twinbee.zip",
            'partial': True,
            "notes": [1]
        },
        {
            "name": "vulcan",
            "files": [],
            "filename": "vulcan.zip",
            'partial': True,
            "notes": [1]
        }
    ]

    _out_file_notes = {
        "1": "This game is not yet extractable; it might not be implemented as a usable ROM."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'system': "Arcade",
            "notes": x['notes']},
            self._game_info_map)

    def execute(self, in_dir, out_dir):
        for game in self._game_info_map:
            if not self._props.get('include-partials') and game.get('partial'):
                logger.info(f"Skipping {game['name']} as this tool cannot extract a working copy...")
                continue
            
            src_file = os.path.join(in_dir, "AA_AC_ArcadeClassics.exe")
            if not os.path.exists(src_file):
                logger.error(f"Cannot find {self._title} executable at {src_file}; exiting!")
                exit
            with open(src_file, 'rb') as dll_file:
                contents = dll_file.read()

                logger.info(f"Extracting {game['name']}...")
                zip_files = {}
                for file in game['files']:
                    if file['start'] == 'placeholder':
                        file_content = bytearray(b'0' * file['length'])
                    else:
                        file_content = transforms.cut(contents, file['start'], length=file['length'])

                    zip_files[file['filename']] = file_content

                logger.info(f"Saving {game['filename']}...")
                with open(os.path.join(out_dir, game['filename']), "wb") as out_file:
                    out_file.write(helpers.build_zip(zip_files))

        logger.info("Processing complete.")
