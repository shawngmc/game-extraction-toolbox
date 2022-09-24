'''Implementation of ags: Namco Arcade Game Series'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSTask(BaseTask):
    '''Implements ags: Namco Arcade Game Series'''
    _task_name = "ags"
    _title = "Namco Arcade Game Series"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL.
    '''
    _default_input_folder = helpers.STEAM_APP_ROOT
    _input_folder_desc = "Steam library root"


    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }
    _game_info_map = [
        {
            "name": "Ms. Pac-Man",
            "src_path": r"Ms. PAC-MAN\Ms. PAC-MAN_Data\Plugins\Release_2.dll",
            "files": [
                {
                    "filename": "82s126.1m",
                    "start": 0x1AE30,
                    "length": 0x100
                },
                {
                    "filename": "82s123.7f",
                    "start": 0x1AF30,
                    "length": 0x20
                },
                {
                    "filename": "82s126.4a", # CRC Mismatch
                    "start": 0x1AF50,
                    "length": 0x100
                },
                {
                    "filename": "pacman.5ef",
                    "start": 0x1B050,
                    "length": 0x1000
                },
                {
                    "filename": "5e",
                    "start": 0x1D050,
                    "length": 0x1000
                },
                {
                    "filename": "boot1",
                    "start": 0x28C20,
                    "length": 0x1000
                },
                {
                    "filename": "boot2",
                    "start": 0x29C20,
                    "length": 0x1000
                },
                {
                    "filename": "boot3",
                    "start": 0x2AC20,
                    "length": 0x1000
                },
                {
                    "filename": "boot4",
                    "start": 0x2BC20,
                    "length": 0x1000
                },
                {
                    "filename": "boot5",
                    "start": 0x30C20,
                    "length": 0x1000
                },
                {
                    "filename": "boot6",
                    "start": 0x31C20,
                    "length": 0x1000
                },
                {
                    "filename": "82s126.3m",
                    "start": 'placeholder',
                    "length": 0x100
                }
            ],
            "filename": "mspacman.zip",
            'status': "partial",
            "notes": []
        },
        {
            "name": "Galaga",
            "src_path": r"GALAGA\GALAGA_Data\Plugins\Release_1.dll",
            "files": [
                {
                    "filename": "prom-1.1d",
                    "start": 0x56710,
                    "length": 0x100
                },
                {
                    "filename": "prom-5.5n",
                    "start": 0x56810,
                    "length": 0x20
                },
                {
                    "filename": "prom-3.1c",
                    "start": 0x56830,
                    "length": 0x100
                },
                {
                    "filename": "prom-4.2n",
                    "start": 0x56930,
                    "length": 0x100
                },
                {
                    "filename": "gg1_11.4d",
                    "start": 0x56A30,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_10.4f",
                    "start": 0x57A30,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_9.4l",
                    "start": 0x58A30,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_7b.2c",
                    "start": 0x64A00,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_5b.3f",
                    "start": 0x65A00,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_1b.3p",
                    "start": 0x66A00,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_2b.3m",
                    "start": 0x67A00,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_3.2m",
                    "start": 0x68A00,
                    "length": 0x1000
                },
                {
                    "filename": "gg1_4b.2l",
                    "start": 0x69A00,
                    "length": 0x1000
                },
                {
                    "filename": "prom-2.5c",
                    "start": 'placeholder',
                    "length": 0x100
                },
                {
                    "filename": "51xx.bin",
                    "start": 'placeholder',
                    "length": 0x400
                },
                {
                    "filename": "54xx.bin",
                    "start": 'placeholder',
                    "length": 0x400
                }
            ],
            'status': "playable",
            "filename": "galaga.zip",
            "notes": [1]
        },
            {
            "name": "Dig Dug",
            "src_path": r"DIG DUG\DIG DUG_Data\Plugins\Release_0.dll",
            "files": [
                {
                    "filename": "digdug.spr",
                    "start": 0x1D9F0,
                    "length": 0x100
                },
                {
                    "filename": "dd1.10b",
                    "start": 0x1DAF0,
                    "length": 0x1000
                },
                {
                    "filename": "digdug.5n",
                    "start": 0x1EAF0,
                    "length": 0x20
                },
                {
                    "filename": "digdug.1c",
                    "start": 0x1EB10,
                    "length": 0x100
                },
                {
                    "filename": "digdug.2n",
                    "start": 0x1EC10,
                    "length": 0x100
                },
                {
                    "filename": "136007.116",
                    "start": 0x1ED10,
                    "length": 0x1000
                },
                {
                    "filename": "dd1.14",
                    "start": 0x1FD10,
                    "length": 0x1000
                },
                {
                    "filename": "136007.118",
                    "start": 0x20D10,
                    "length": 0x1000
                },
                {
                    "filename": "136007.119",
                    "start": 0x21D10,
                    "length": 0x1000
                },
                {
                    "filename": "dd1.9",
                    "start": 0x22D10,
                    "length": 0x800
                },
                {
                    "filename": "dd1.11",
                    "start": 0x23510,
                    "length": 0x1000
                },
                {
                    "filename": "136007.107",
                    "start": 0x35420,
                    "length": 0x1000
                },
                {
                    "filename": "dd1.5b",
                    "start": 0x36420,
                    "length": 0x1000
                },
                {
                    "filename": "dd1.6b",
                    "start": 0x37420,
                    "length": 0x1000
                },
                {
                    "filename": "136007.101",
                    "start": 0x38420,
                    "length": 0x1000
                },
                {
                    "filename": "136007.102",
                    "start": 0x39420,
                    "length": 0x1000
                },
                {
                    "filename": "136007.103",
                    "start": 0x3A420,
                    "length": 0x1000
                },
                {
                    "filename": "dd1.4b",
                    "start": 0x3B420,
                    "length": 0x1000
                },
                {
                    "filename": "136007.109",
                    "start": 'placeholder',
                    "length": 0x100
                }
            ],
            'status': "playable",
            "filename": "digdug.zip",
            "notes": [2]
        },
            {
            "name": "Pac-Man",
            "src_path": r"PAC-MAN\PAC-MAN_Data\Plugins\Release_3.dll",
            "files": [
                {
                    "filename": "82s126.1m",
                    "start": 0x1AA30,
                    "length": 0x100
                },
                {
                    "filename": "82s123.7f",
                    "start": 0x1AB30,
                    "length": 0x20
                },
                {
                    "filename": "82s126.4a",
                    "start": 0x1AB50,
                    "length": 0x100
                },
                {
                    "filename": "pacman.5f",
                    "start": 0x1AC50,
                    "length": 0x1000
                },
                {
                    "filename": "pacman.5e",
                    "start": 0x1C050,
                    "length": 0x1000
                },
                {
                    "filename": "pacman.6e",
                    "start": 0x28020,
                    "length": 0x1000
                },
                {
                    "filename": "pacman.6f",
                    "start": 0x29020,
                    "length": 0x1000
                },
                {
                    "filename": "pacman.6h",
                    "start": 0x2A020,
                    "length": 0x1000
                },
                {
                    "filename": "pacman.6j",
                    "start": 0x2B020,
                    "length": 0x1000
                },
                {
                    "filename": "82s126.3m",
                    "start": 'placeholder',
                    "length": 0x100
                },
            ],
            'status': "good",
            "filename": "pacman.zip",
            "notes": []
        }
    ]

    _out_file_notes = {
        "1": "This extraction requires MAME 2017/1.39 due to the NAMCO base ROMs, which have placeholders.",
        "2": "This extraction requires MAME 2003/0.78 due to the NAMCO base ROMs."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'system': "Arcade",
            "status": x['status'],
            "notes": x['notes']},
            self._game_info_map)

    def execute(self, in_dir, out_dir):
        for game in self._game_info_map:
            is_partial = game.get('status') == 'partial'
            if not self._props.get('include-partials') and is_partial:
                logger.info(f"Skipping {game['name']} as this tool cannot extract a working copy...")
                continue

            src_file = os.path.join(in_dir, game['src_path'])
            if not os.path.exists(src_file):
                logger.info(f"Skipping {game['name']} as this tool cannot find it in the given Steam library folder...")
                continue

            logger.info(f"Extracting {game['name']}...")
            with open(src_file, 'rb') as dll_file:
                contents = dll_file.read()
                zip_files = {}
                for file in game['files']:
                    if file['start'] == 'placeholder':
                        file_content = bytearray(b'0' * file['length'])
                    else:
                        file_content = transforms.cut(contents, file['start'], length=file['length'])

                    zip_files[file['filename']] = file_content
                if is_partial:
                    zip_files['full_dump'] = contents

                logger.info(f"Saving {game['filename']}...")
                with open(os.path.join(out_dir, game['filename']), "wb") as out_file:
                    out_file.write(helpers.build_zip(zip_files))

        logger.info("Processing complete.")
