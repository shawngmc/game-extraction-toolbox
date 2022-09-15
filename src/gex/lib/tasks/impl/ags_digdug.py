'''Implementation of ags_digdug: Arcade Game Series Dig Dug'''
import logging
import os
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSDigDugTask(BaseTask):
    '''Implements ags_digdug: Arcade Game Series Dig Dug'''
    _task_name = "ags_digdug"
    _title = "Arcade Game Series Dig Dug"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("DIG DUG")
    _input_folder_desc = "Arcade Game Series Dig Dug folder"
    _short_description = ""

    _game_info_map = {
        "name": "Dig Dug",
        "src_path": r"DIG DUG_Data\Plugins\Release_0.dll",
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
        "filename": "digdug.zip"
    }

    _out_file_notes = {
        "1": "This extraction requires MAME 2003/0.78."
    }

    def __init__(self):
        super().__init__()
        self._out_file_list = map(lambda x: {
            'filename': x['filename'],
            'game': f"{x['name']}",
            'system': "Arcade",
            "notes": [1]},
            self._game_info_map)
        self._out_file_notes = {}

    def execute(self, in_dir, out_dir):
        with open(os.path.join(in_dir, self._game_info_map['src_path']), 'rb') as dll_file:
            contents = dll_file.read()

            zip_files = {}

            for file in self._game_info_map['files']:
                if file['start'] == 'placeholder':
                    file_content = bytearray(b'0' * file['length'])
                else:
                    file_content = transforms.cut(contents, file['start'], length=file['length'])

                zip_files[file['filename']] = file_content

            logger.info(f"Saving {self._game_info_map['filename']}...")
            with open(os.path.join(out_dir, self._game_info_map['filename']), "wb") as out_file:
                out_file.write(helpers.build_zip(zip_files))

        logger.info("Processing complete.")
