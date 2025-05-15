'''Implementation of toaplan_truxton2: Truxton 2'''
import logging
import os
from gex.lib.utils.blob import hash as hash_helper

from gex.lib.archive import lzma
from gex.lib.utils.blob import transforms
from gex.lib.tasks import helpers

from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class ToaplanTruxton2Task(BaseTask):
    '''Implements of toaplan_truxton2: Truxton 2'''
    _task_name = "toaplan_truxton2"
    _title = "Truxton 2"
    _details_markdown = ''''''

    _default_input_folder = helpers.gen_steam_app_default_folder("Truxton 2")
    _input_folder_desc = "Truxton 2 Steam folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        # for each output file entry
        for out_file_entry in self._metadata['out']['files']:
            pkg_name = out_file_entry['in_file']
            # Check the status of it
            if out_file_entry['status'] == 'no-rom':
                logger.info(f"Skipping {pkg_name} - cannot extract...")
            else:
                logger.info(f"Extracting {pkg_name}...")

                # read the matching input file
                in_file_entry = self._metadata['in']['files'][pkg_name]
                loaded_file = self.read_datafile(in_dir, in_file_entry)

                # run the handler
                handler_func = self.find_handler_func(pkg_name)
                if loaded_file is not None and handler_func is not None:
                    output_contents = handler_func(loaded_file['contents'])

                    _ = self.verify_out_file(out_file_entry['filename'], output_contents)

                    with open(os.path.join(out_dir, out_file_entry['filename']), "wb") as out_file:
                        out_file.write(output_contents)
                elif handler_func is None:
                    logger.warning("Could not find matching handler function.")
        logger.info("Processing complete.")

    ################################################################################
    # Truxton 2                                                                    #
    ################################################################################

    def _handle_truxton2(self, merged_contents):
        func_map = {}

        rom_filenames = [
            "tp024_1.bin",
            "tp024_4.bin",
            "tp024_3.bin",
            "tp024_2.bin"
        ]

        def rom(contents):
            # Pull out the LZMA Section - this is approximate, but will be fixed by the safe decompress
            compressed_data = transforms.cut(contents, 0xF7680, 1225200)
            
            # Decompress the LZMA data
            decompressed_data = lzma.extract(compressed_data)

            # Pad the data
            decompressed_data = transforms.pad(decompressed_data, 3145728)

            # Chunk the data out
            chunks = transforms.custom_split(decompressed_data, [0x80000, 0x100000, 0x100000, 0x80000])

            # Endian swap first chunk
            chunks[0] = transforms.swap_endian(chunks[0])

            return dict(zip(rom_filenames, chunks))
        func_map['rom'] = rom

        return helpers.build_rom(merged_contents, func_map)
