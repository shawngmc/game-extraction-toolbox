'''INCOMPLETE Implementation of cas2: Capcom Arcade Stadium 2'''
import glob
import logging
import os

from gex.lib.archive import kpka
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

# TODO: Further research required

class CAS2Task(BaseTask):
    '''INCOMPLETE Implements cas2: Capcom Arcade Stadium 2'''
    _task_name = 'cas2'
    _title = "Capcom Arcade Stadium 2"
    _details_markdown = '''
## INCOMPLETE!

This script is a placeholder for full CAS2 extraction. See https://github.com/shawngmc/game-extraction-toolbox/issues/18 for latest details!

Currently, it extracts nothing; however, with a "--prop include-partials=True", it will extract all KPKA paks with the following naming convention:
[ARCHIVEID]_[SEQUENTIALNUM]_[SIZE].dat
These are not playable ROMs!

## Analysis
### KPKA
These appear to be KPKA archives, and it is reasonably certain that the extraction is correct, as most files have a 3-4 character allcaps header
indicating file type. Note that the file order can differ between KPKA files; the size and header bytes are best used for identification.
    '''
    _out_file_list = [
    ]

    _out_file_notes = {
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("Capcom Arcade 2nd Stadium")
    _input_folder_desc = "CAS 2 Folder"
    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }

    def _find_files(self, in_path):
        return glob.glob(os.path.join(in_path, "**", "*.pak"), recursive=True)

    def execute(self, in_dir, out_dir):
        if self._props.get('include-partials'):
            pak_files = self._find_files(in_dir)
            for file in pak_files:
                file_id = None
                filename = os.path.basename(file)
                if "patch" in filename:
                    logger.info(f"Skipping patch file {filename}")
                elif filename == "re_chunk_000.pak":
                    file_id = "0000000"
                else:
                    file_id = file[-11:-4]

                logger.info(f"Extracting {file}: {file_id}")
                try:
                    with open(file, "rb") as curr_file:
                        file_content = bytearray(curr_file.read())
                        kpka_contents = kpka.extract(file_content)
                        output_files = []

                        for kpka_contents in kpka_contents.values():
                            print(f"{kpka_contents['entry']}: {kpka_contents['size']}")
                            output_files.append({
                                'filename': f"{file_id}_{kpka_contents['entry']}"\
                                    f"_{kpka_contents['size']}.dat",
                                "contents": kpka_contents['contents']
                            })

                        for output_file in output_files:
                            out_path = os.path.join(out_dir, output_file['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(output_file['contents'])
                except OSError as error:
                    logger.warning(f'Error while processing {file}!')
                    logger.warning(error)
        else:
            logger.error("cas2 is not yet implemented!")
            logger.error("To help investigate, add --prop 'include-partials=True' to extract raw KPKA")

        logger.info("Processing complete.")
