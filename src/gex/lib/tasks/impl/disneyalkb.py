'''Implementation of disneyalkb: Disney Aladdin / Lion King Bundle (and DLC)'''
import glob
import logging
import os
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class DisneyClassicsTask(BaseTask):
    '''Implements disneyalkb: Disney Aladdin / Lion King Bundle (and DLC)'''
    _task_name = "disneyalkb"
    _title = "Disney Aladdin / Lion King Bundle (and DLC)"
    _details_markdown = '''
Based on https://github.com/farmerbb/RED-Project/wiki/Disney-Classic-Games:-Aladdin-and-The-Lion-King

 **Game**                                         | **System**     |  **Filename**           
---------------------------------------------|---------------|------------------ 
 **Aladdin**                                 | Game Boy      | Aladdin.gb
 **Jungle Book**                             | Game Boy      | JungleBook.gb
 **Lion King**                               | Game Boy      | LionKing.gb
 **Aladdin (4F7A Patch)**                    | Genesis       | Aladdin.4F7A.PATCHED.md
 **Aladdin (9CB2 Patch)**                    | Genesis       | Aladdin.9CB2.PATCHED.md
 **Aladdin (CES Patch)**                     | Genesis       | Aladdin.CES.PATCHED.md
 **Aladdin Remix**                           | Genesis       | Aladdin-Remix.md
 **Jungle Book**                             | Genesis       | JungleBook.md
 **Jungle Book**                             | Genesis       | JUNGLEBOOK.PATCHED.md
 **Lion King**                               | Genesis       | LionKing.0D3D.PATCHED.md
 **Jungle Book**                             | NES           | JungleBook.nes
 **Aladdin**                                 | SNES          | Aladdin.sfc
 **Jungle Book**                             | SNES          | JungleBook.sfc
 **Jungle Book Music**                       | SNES          | JungleBookMusicROM.sfc
 **Lion King**                               | SNES          | LionKing.919A.PATCHED.sfc
 **Lion King**                               | SNES          | LionKing.DE6E.PATCHED.sfc

    '''
    _default_input_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Disney Classic Games Aladdin and the Lion King"
    _input_folder_desc = "Disney Classics Steam folder"
    _short_description = ""

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
        