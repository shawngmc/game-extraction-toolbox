'''Containes the BaseTask class, the base class for tasks'''

import copy
import json
import logging
import os
from gex.lib.utils.blob import hash as hash_helper
from gex.lib.archive import zip as zip_lib

logger = logging.getLogger('gextoolbox')

class BaseTask:
    '''Base class for rom extraction tasks'''
    _task_name = None
    _title = None
    _details_markdown = None
    _default_input_folder = None
    _input_folder_desc = None
    _out_file_list = []
    _out_file_notes = {}
    _prop_info = {}
    _props = {}
    _metadata = None

    def __init__(self):
        for prop_key, prop_value in self._prop_info.items():
            self._props[prop_key] = prop_value['default']

    def read_task_metadata(self):
        '''Read the JSON-based metadata for a task'''
        basetask_path = os.path.dirname(__file__)
        metadata_path = os.path.join(basetask_path, 'impl', self._task_name, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding="UTF-8") as metadata_file:
                self._metadata = json.load(metadata_file)
        if self._metadata is None:
            logger.warning(f"Could not find metadata.json for {self._task_name}")

    # Reading data files
    # - Multiple mapping types
    #   - One-to-one: Sometimes, one file is one game
    #   - One-to-many: Sometimes, one input file is multiple games
    #   - Many-to-one: Sometimes, we need multiple input files for one game
    #   - Many-to-many: Sometimes, both are true: for examplen read these 5 ROM types, get multiple variants of the same game out of these files
    # - Files can be very large - some games, for example, have single files above 8 GB!
    # - Some are straight copies, some are unpacking complex formats
    # - Disk IO is expensive, but... it could be worse
    # There's no one size fits all.

    def read_all_datafiles(self, in_dir):
        '''Read all data files as defined in the metadata - mostly useful for smaller collections with many-to-many relationships'''
        # We read all files at once generally because there are a few cases where we cross-read them to fill out missing files
        in_files = {}
        for file_ref, file_metadata in self._metadata['in']['files'].items():
            data_file = self.read_datafile(in_dir, file_metadata)
            in_files[file_ref] = data_file
        return in_files

    def read_datafile(self, in_dir, file_metadata):
        '''Read a specific data file as defined in the metadata, including CRC/Size check/version identification'''
        rel_path = file_metadata.get('rel_path') or []
        data_path = os.path.join(in_dir, *rel_path, file_metadata['filename'])
        if os.path.exists(data_path):
            # consider switching this to mmap bytearray/readablefile memory-mapped file hybrids to improve memory usage
            with open(data_path, 'rb') as data_file:
                contents = data_file.read()

            size = len(contents)
            crc = hash_helper.get_crc(contents)
            sha = hash_helper.get_sha1(contents)
            logging.debug(f"Read {data_path} with size {size}, crc {crc} and sha {sha}")

            versions = file_metadata.get("versions") or []
            file_ver_tag = None
            for version_tag, version_meta in versions.items():
                # Check size first if we have it
                if 'size' in version_meta:
                    if version_meta['size'] != size:
                        continue

                if 'sha' in version_meta:
                    if hex(int(version_meta['sha'], base=16)) == sha:
                        file_ver_tag = version_tag
                        break
                    else:
                        continue
                
                if 'crc' in version_meta:
                    if hex(int(version_meta['crc'], base=16)) == crc:
                        file_ver_tag = version_tag
                        break
                    else:
                        continue


            if file_ver_tag:
                logging.debug(f"Identified {data_path} as version {file_ver_tag}")
            else:
                logging.warning(f"Could not identify version of {data_path}!")

            return {
                "name": os.path.basename(data_path),
                "fullpath": data_path,
                "contents": contents,
                "version": file_ver_tag
            }
        else:
            logging.warning(f"Could not find file at {data_path}!")
            return None

    def verify_out_file(self, file_name, contents):
        '''Verify an output file using the method specified in the metadata'''
        # Find out_file entry
        out_file = next((x for x in self._metadata['out']['files'] if x['filename'] == file_name), None)
        if out_file is None:
            logger.info(f"Could not find entry to verify {file_name}")
            return None

        if out_file['status'] == 'partial' or out_file['status'] == 'no-rom':
            logger.info(f"Verification not available for partial ROM {file_name}")
            return None

        # Get verify object
        verify_obj = out_file.get('verify')
        if verify_obj is None:
            logger.info(f"Verification data not available for ROM {file_name}")
            return None

        # Check verify type
        if verify_obj['type'] == 'crc':
            crc = hash_helper.get_crc(contents)[2:].upper().rjust(8, "0")
            if len(contents) != verify_obj['size']:
                logger.info(f"Could NOT verify {file_name}: File size doesn't match!")
                return False
            elif crc != verify_obj['crc']:
                logger.info(f"Could NOT verify {file_name}: CRC doesn't match!")
                return False
            else:
                logger.info(f"Verified {file_name}.")
                return True
        elif verify_obj['type'] == 'zip':
            zip_metas = zip_lib.get_metadata(contents)
            # Ensure the file name lists are the same
            real_filenames = set(zip_metas.keys())
            expected_filenames = set(verify_obj['entries'].keys())
            if real_filenames != expected_filenames:
                logger.info(f"Could NOT verify {file_name}: File lists don't match!")
                return False
            # Compare file size/CRC
            for inner_filename, zip_meta in zip_metas.items():
                verify_entry = verify_obj['entries'][inner_filename]
                if zip_meta['crc'] != verify_entry['crc'] or zip_meta['size'] != verify_entry['size'] :
                    logger.info(f"Could NOT verify {file_name}: {inner_filename} should be {verify_entry['crc']} at {verify_entry['size']} bytes, found {zip_meta['crc']} at {zip_meta['size']}")
                    return False
            logger.info(f"Verified {file_name}.")
            return True
        else:
            logger.info(f"Unknown verify type: {verify_obj['type']}")
            return None

    def set_props(self, in_props):
        '''Set any additional props for this task'''
        for value in in_props:
            print(value)
            if '=' in value:
                key, value = value.split('=')
            else:
                key = value
            self._props[key] = value

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": copy.deepcopy(self._out_file_list),
            "notes": copy.deepcopy(self._out_file_notes)
        }

    def get_prop_info(self):
        '''Return a list of available props'''
        return copy.deepcopy(self._prop_info)

    def get_task_name(self):
        '''Get the task name, a short string for referring to the task'''
        return self._task_name

    def get_details_markdown(self):
        '''Get markdown for the details/help docs for this task'''
        return self._details_markdown

    def get_title(self):
        '''Get the nicely formatted name of this task'''
        return self._title

    def get_default_input_folder(self):
        '''Get the default input folder for this task'''
        return self._default_input_folder

    def get_input_folder_description(self):
        '''Get a short description of what the input folder should refer to'''
        return self._input_folder_desc

    def find_handler_func(self, package_name):
        '''Utility function to look for a sub-package handler in a task'''
        if f'_handle_{package_name}' in dir(self):
            return getattr(self, f'_handle_{package_name}')
        return None

    def execute(self, in_dir, out_dir):
        '''Main implementation call for the extraction task'''
