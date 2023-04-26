'''Convenience functions for comparing two files/archives'''
from enum import Enum
import logging
import os
from gex.lib.utils.blob import hash as hash_helper
from gex.lib.archive import zip as zip_lib

logger = logging.getLogger('gextoolbox')

class VerifyErrors(Enum):
    MISSING_FILE = 1
    EXTRA_FILE = 2
    SIZE_MISMATCH = 3
    CHECKSUM_MISMATCH = 4
    VERSION_MISMATCH = 5

def verify_via_metadata(contents, verify_metadata):
    '''Wrapper to apply any verify test; returns errors, than any verification notes (such as matched version)'''
    if verify_metadata['type'] == "zip":
        return verify_zip(contents, verify_metadata['entries']), None
    elif verify_metadata['type'] == "sha":
        return verify_sha(contents, verify_metadata['sha'], verify_metadata['size']), None
    elif verify_metadata['type'] == "crc":
        return verify_crc(contents, verify_metadata['crc'], verify_metadata['size']), None
    elif verify_metadata['type'] == "versions":
        return verify_versions(contents, verify_metadata['versions'])


def verify_versions(contents, versions):
    all_version_errors = {}
    for version_name, version_verify_metadata in versions.items():
        all_version_errors[version_name] = verify_via_metadata(contents, version_verify_metadata)

    closest_version = min(all_version_errors, key=all_version_errors.get)
    version_errors = all_version_errors[closest_version]
    return version_errors, closest_version 


def verify_zip(zip_data, known_entries):
    errors = []

    zip_metas = zip_lib.get_metadata(zip_data)

    # Ensure the file name lists are the same
    real_filenames = set(zip_metas.keys())
    expected_filenames = set(known_entries.keys())
    if real_filenames != expected_filenames:
        missing_files = expected_filenames.difference(real_filenames)
        for missing_file in missing_files:
            errors.append({VerifyErrors.MISSING_FILE, missing_file})
        extra_files = real_filenames.difference(expected_filenames)
        for extra_file in extra_files:
            errors.append({VerifyErrors.EXTRA_FILE, extra_file})

    # Compare each file size/CRC
    check_files = real_filenames.intersection(expected_filenames)
    for inner_filename in check_files:
        zip_meta = zip_metas.get(inner_filename)
        verify_entry = known_entries[inner_filename]
        if zip_meta['crc'] != verify_entry['crc']:
            errors.append((VerifyErrors.CHECKSUM_MISMATCH, {zip_meta['crc'], verify_entry['crc'], "CRC", inner_filename}))
        if zip_meta['size'] != verify_entry['size']:
            errors.append((VerifyErrors.SIZE_MISMATCH, {zip_meta['size'], verify_entry['size'], inner_filename}))
            
    return errors

def verify_crc(contents, known_crc, known_size):
    size = len(contents)
    crc = hash_helper.get_crc(contents)
    known_crc = hex(int(known_crc, base=16))
    errors = []
    if known_size != size:
        errors.append((VerifyErrors.SIZE_MISMATCH, {size, known_size}))

    if known_crc != crc:
        errors.append((VerifyErrors.CHECKSUM_MISMATCH, {crc, known_crc, "CRC"}))

    return errors

def verify_sha(contents, known_sha, known_size):
    size = len(contents)
    sha = hash_helper.get_sha1(contents)
    errors = []
    if known_size != size:
        errors.append((VerifyErrors.SIZE_MISMATCH, {size, known_size}))

    if known_sha != sha:
        errors.append((VerifyErrors.CHECKSUM_MISMATCH, {sha, known_sha, "SHA-1"}))

    return errors

def print_errors(errors, ref):
    logger.info(f"Verification of {ref} failed!")
    for error in errors:
        message = ""
        type = error[0]
        data = error[1]
        if type is VerifyErrors.MISSING_FILE:
            message = f"File {data[0]} is missing!"
        elif type is VerifyErrors.EXTRA_FILE:
            message = f"File {data[0]} is extraneous!"
        elif type is VerifyErrors.SIZE_MISMATCH:
            if len(data) == 2:
                message = f"Expected size {data[0]}, found {data[1]}!"
            elif len(data) == 3:
                message = f"Expected size {data[0]} for {data[2]}, found {data[1]}!"
        elif type is VerifyErrors.CHECKSUM_MISMATCH:
            if len(data) == 3:
                message = f"Expected {data[2]} {data[0]}, found {data[1]}!"
            elif len(data) == 4:
                message = f"Expected {data[2]} {data[0]} for {data[3]}, found {data[1]}!"
        logger.info(f"- {message}")


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
