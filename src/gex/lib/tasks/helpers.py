'''Convenience wrappers for task implementation'''
import io
import os
import zipfile
from gex.lib.utils.blob import transforms

STEAM_APP_ROOT = r"C:\Program Files (x86)\Steam\steamapps\common"
def gen_steam_app_default_folder(app_folder, library_root=STEAM_APP_ROOT):
    '''Convenience function to get a Steam App folder'''
    return os.path.join(library_root, app_folder)

def build_rom(in_files, func_map):
    '''Convenience function to run both process_rom_files and build_zip together'''
    file_map = process_rom_files(in_files, func_map)
    return build_zip(file_map)

def process_rom_files(in_files, func_map):
    '''Look at a list of content files and run a set of transform functions on them'''
    file_map = {}
    for func in func_map.values():
        file_map.update(func(in_files))
    return file_map

def create_combined_file_map(*file_maps):
    '''Create a combined file map from 2 or more existing maps'''
    new_map = {}
    for file_map in file_maps:
        new_map.update(file_map)
    return new_map

def build_zip(file_map):
    '''Build a zip file from a dictionary of paths to contents'''
    new_contents = io.BytesIO()
    with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
        for name, data in file_map.items():
            new_archive.writestr(name, data)
    return new_contents.getvalue()

def existing_files_helper(file_map):
    '''Func map helper to reuse a file map'''
    def existing_files(*_):
        return file_map
    return existing_files

def equal_split_helper(in_file_ref, filenames):
    '''Func map helper for transforms.equal_split'''
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.equal_split(contents, num_chunks = len(filenames))
        return dict(zip(filenames, chunks))
    return split

def custom_split_helper(in_file_ref, name_size_map):
    '''Func map helper for transforms.custom_split'''
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.custom_split(contents, list(name_size_map.values()))
        return dict(zip(name_size_map.keys(), chunks))
    return split

def deinterleave_helper(in_file_name, filenames, num_ways, word_size):
    '''Func map helper for deinterleaving a file'''
    def deinterleave(in_files):
        contents = in_files[in_file_name]
        chunks = transforms.deinterleave(contents, num_ways=num_ways, word_size=word_size)
        return dict(zip(filenames, chunks))
    return deinterleave

def name_file_helper(in_file_ref, filename):
    '''Func map helper for renaming a file'''
    def rename_from(in_files):
        return {filename: in_files[in_file_ref]}
    return rename_from

def splice_out_helper(start, length=None, end=None):
    '''Func map helper for transforms.splice_out'''
    def splice_func(contents):
        return transforms.splice_out(contents, start, length, end)
    return splice_func

def slice_helper(start=0, length=None, end=None):
    '''Func map helper for slicing a blob'''
    if length is None and end is None:
        raise Exception("Splice out needs a length or end value, but received neither.")
    elif length is not None and end is not None:
        raise Exception("Splice out needs a length or end value, but received both.")
    elif end is None:
        end = start + length
    def slice_func(contents):
        return contents[start:end]
    return slice_func

def placeholder_helper(file_map):
    '''Func map helper for making empty placeholder files'''
    def create_placeholders(_):
        out_files = {}
        for filename, size in file_map.items():
            out_files[filename] = bytes(size*b'\0')
        return out_files
    return create_placeholders

def common_picker_helper(common_file_map, src_name, dst_name=None):
    '''Func map helper for picking/renaming a single file from an existing common map'''
    def pick(_):
        out_files = {}

        content = common_file_map.get(src_name)
        filename = dst_name if not None else src_name

        out_files[filename] = content

        return out_files
    return pick

def common_rename_helper(common_file_map, rename_map):
    '''Func map helper for picking/renaming a single file from an existing common map'''
    def pick(_):
        out_files = {}

        for src_name, dst_name in rename_map.items():
            out_files[dst_name] = common_file_map.get(src_name)

        return out_files
    return pick
