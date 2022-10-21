'''Module to handle ZIP archive (additional utility)'''
import io
import zipfile
import logging

logger = logging.getLogger('gextoolbox')

def extract(bytes_obj):
    '''Extract a ZIP archive into a list'''
    files = {}
    with zipfile.ZipFile(io.BytesIO(bytes_obj), "r") as archive:
        zip_entries = list(archive.infolist())
        for file_entry in zip_entries:
            with archive.open(file_entry) as file_read_obj:
                contents = file_read_obj.read()
                files[file_entry.filename] = {
                    "contents": contents,
                    "entry": file_entry.filename,
                    "size": file_entry.file_size
                }
    return files

def get_metadata(bytes_obj):
    '''Get a list of file entries usable for verifying the contents'''
    files = {}
    with zipfile.ZipFile(io.BytesIO(bytes_obj), "r") as archive:
        zip_entries = list(archive.infolist())
        for file_entry in zip_entries:
            files[file_entry.filename] = {
                "filename": file_entry.filename,
                "size": file_entry.file_size,
                "crc": hex(file_entry.CRC)[2:].upper().rjust(8, "0")
            }
    return files
