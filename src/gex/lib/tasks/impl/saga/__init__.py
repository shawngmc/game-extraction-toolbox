'''Implmentation of saga: Collection of SaGa Final Fantasy Legend'''
import logging
import os
import UnityPy
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class SagaTask(BaseTask):
    '''Implments saga: Collection of SaGa Final Fantasy Legend'''
    _task_name = "saga"
    _title = "Collection of SaGa Final Fantasy Legend"
    _details_markdown = '''
These are extracted from the Unity asset bundle files.
See https://github.com/farmerbb/RED-Project/issues/39 for more info.
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("Sa・Ga COLLECTION")
    _input_folder_desc = "Collection of SaGa Steam folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        # for each output file entry
        for out_file_entry in self._metadata['out']['files']:
            pkg_name = out_file_entry['extract']['in_file']
            # Check the status of it
            if out_file_entry['status'] == 'no-rom':
                logger.info(f"Skipping {pkg_name} - cannot extract...")
            else:
                logger.info(f"Extracting {pkg_name}...")

                # read the matching input file
                in_file_entry = self._metadata['in']['files'][pkg_name]
                loaded_file = self.read_datafile(in_dir, in_file_entry)

                # load the archive
                unity_bundle = UnityPy.load(loaded_file['contents'])

                # Get the rom asset entry
                rom_asset = unity_bundle.container.get(out_file_entry['extract']['archive_path'])
                rom_data = rom_asset.read().script

                if rom_asset is None:
                    logger.warning("Could not find rom asset in archive.")
                else:
                    _ = self.verify_out_file(out_file_entry['filename'], rom_data)

                    with open(os.path.join(out_dir, out_file_entry['filename']), "wb") as out_file:
                        out_file.write(rom_data)
        logger.info("Processing complete.")

