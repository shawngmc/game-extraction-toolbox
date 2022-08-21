import io
import zipfile
from gex.lib.utils.blob import transforms

def build_rom(in_files, func_map):
    new_data = dict()
    for func in func_map.values():
        new_data.update(func(in_files))

    # Build the new zip file
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in new_data.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()

def equal_split_helper(in_file_ref, filenames):
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.equal_split(contents, num_chunks = len(filenames))
        return dict(zip(filenames, chunks))
    return split

def custom_split_helper(in_file_ref, name_size_map):
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.custom_split(contents, list(name_size_map.values()))
        return dict(zip(name_size_map.keys(), chunks))
    return split

def name_file_helper(in_file_ref, filename):
    def rename_from(in_files):
        return {filename: in_files[in_file_ref]}
    return rename_from

def placeholder_helper(file_map):
    def create_placeholders(contents):
        out_files = {}
        for filename, size in file_map.items():
            out_files[filename] = bytes(size*b'\0')
        return out_files  
    return create_placeholders
