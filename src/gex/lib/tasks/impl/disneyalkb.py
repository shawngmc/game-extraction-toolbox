'''Implementation of disneyalkb: Disney Aladdin / Lion King Bundle (and DLC)'''
import glob
import logging
import os
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class DisneyClassicsTask(BaseTask):
    '''Implements disneyalkb: Disney Aladdin / Lion King Bundle (and DLC)'''
    _task_name = "disneyalkb"
    _title = "Disney Aladdin / Lion King Bundle (and DLC)"
    _details_markdown = '''
Based on https://github.com/farmerbb/RED-Project/wiki/Disney-Classic-Games:-Aladdin-and-The-Lion-King
'''
    _out_file_list = [
        {
            "game": "Aladdin",
            "system": "Game Boy",
            "filename": "Aladdin.gb",
            'status': "good",
            "notes": []
        },
        {
            "game": "Jungle Book",
            "system": "Game Boy",
            "filename": "JungleBook.gb",
            'status': "good",
            "notes": []
        },
        {
            "game": "Lion King",
            "system": "Game Boy",
            "filename": "LionKing.gb",
            'status': "good",
            "notes": []
        },
        {
            "game": "Aladdin (4F7A Patch)",
            "system": "Genesis",
            "filename": "Aladdin.4F7A.PATCHED.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Aladdin (9CB2 Patch)",
            "system": "Genesis",
            "filename": "Aladdin.9CB2.PATCHED.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Aladdin (CES Patch)",
            "system": "Genesis",
            "filename": "Aladdin.CES.PATCHED.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Aladdin Remix",
            "system": "Genesis",
            "filename": "Aladdin-Remix.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Jungle Book",
            "system": "Genesis",
            "filename": "JungleBook.md",
            'status': "good",
            "notes": []
        },
        {
            "game": "Jungle Book (Patched)",
            "system": "Genesis",
            "filename": "JUNGLEBOOK.PATCHED.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Lion King (0D3D Patch)",
            "system": "Genesis",
            "filename": "LionKing.0D3D.PATCHED.md",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Jungle Book",
            "system": "NES",
            "filename": "JungleBook.sfc",
            'status': "good",
            "notes": []
        },
        {
            "game": "Aladdin",
            "system": "SNES",
            "filename": "Aladdin.sfc",
            'status': "good",
            "notes": []
        },
        {
            "game": "Jungle Book",
            "system": "SNES",
            "filename": "JungleBook.sfc",
            'status': "good",
            "notes": []
        },
        {
            "game": "Jungle Book Music",
            "system": "SNES",
            "filename": "JungleBookMusicROM.sfc",
            'status': "good",
            "notes": []
        },
        {
            "game": "Lion King (919A Patch)",
            "system": "SNES",
            "filename": "LionKing.919A.PATCHED.sfc",
            'status': "playable",
            "notes": []
        },
        {
            "game": "Lion King (DE6E Patch)",
            "system": "SNES",
            "filename": "LionKing.DE6E.PATCHED.sfc",
            'status': "playable",
            "notes": []
        }
    ]
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder(
        "Disney Classic Games Aladdin and the Lion King")
    _input_folder_desc = "Disney Classics Steam folder"

    def execute(self, in_dir, out_dir):
        bundle_files = self._find_files(in_dir)
        for file_path in bundle_files:
            with open(file_path, 'rb') as in_file:
                file_name = os.path.basename(file_path)
                pkg_name = self._pkg_name_map.get(file_name)
                if pkg_name is not None:
                    logger.info(f'Reading files for {file_name}...')
                    contents = in_file.read()
                    reader = BPListReader(contents)
                    parsed = reader.parse()

                    handler_func = self.find_handler_func(pkg_name)
                    if parsed is not None and handler_func is not None:
                        output_files = handler_func(parsed)
                        for out_file_entry in output_files:
                            out_path = os.path.join(out_dir, out_file_entry['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(out_file_entry['contents'])
                    elif parsed is None:
                        logger.warning("Could not find merged rom data in mbundle.")
                    elif handler_func is None:
                        logger.warning("Could not find matching handler function.")
                else:
                    logger.info(f'Skipping {file_name} as it contains no known roms...')
        logger.info("Processing complete.")

    _pkg_name_map = {
        'bundleAladdin.mbundle': 'aladdin',
        'bundleDLC1.mbundle': 'dlc',
        'bundleLionKing.mbundle': 'lionking',
        'bundleMain.mbundle': 'main',
    }

    def _find_files(self, base_path):
        bundle_path = os.path.join(base_path, "Bundle", '*.mbundle')
        archive_list = glob.glob(bundle_path)
        return archive_list

    def _handle_aladdin(self, mbundle_entries):
        files = {
            'Aladdin-Remix.bin',
            'Aladdin.4F7A.PATCHED.bin',
            'Aladdin.9CB2.PATCHED.bin',
            'Aladdin.CES.PATCHED.bin',
            'Aladdin.gb'
        }
        return self._bundle_handler(files, mbundle_entries)

    def _handle_dlc(self, mbundle_entries):
        files = {
            'JungleBook.gb',
            'JungleBook.md',
            'JungleBook.nes',
            'Aladdin.sfc',
            'JungleBook.sfc',
            'JungleBookMusicROM.sfc'
        }
        return self._bundle_handler(files, mbundle_entries)

    def _handle_lionking(self, mbundle_entries):
        files = {
            'LionKing.0D3D.PATCHED.bin',
            'LionKing.gb',
            'LionKing.919A.PATCHED.sfc',
            'LionKing.DE6E.PATCHED.sfc',
        }
        return self._bundle_handler(files, mbundle_entries)

    def _handle_main(self, mbundle_entries):
        files = {
            'JUNGLEBOOK.PATCHED.md',
        }
        return self._bundle_handler(files, mbundle_entries)

    def _bundle_handler(self, files, mbundle_entries):
        out_files = []
        for file in files:
            out_name = file.replace('.bin', '.md')
            logger.info(f'Extracting {out_name}...')
            out_files.append({'filename': out_name, 'contents': mbundle_entries[file]})
        return out_files
        