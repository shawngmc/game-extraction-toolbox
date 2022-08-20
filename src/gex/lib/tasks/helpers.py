import zipfile
from gex.lib.utils.blob import transforms

def build_rom(self, in_files, func_map):
        new_data = dict()
        for func in func_map.values():
            new_data.update(func(in_files))
        
        # Build the new zip file
        new_contents = io.BytesIO()
        with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            for name, data in new_data.items():
                new_archive.writestr(name, data)
        return new_contents.getvalue()

def equal_split_helper(self, in_file_ref, filenames):
    def split(in_files):
        contents = in_files[in_file_ref]
        chunks = transforms.equal_split(contents, num_chunks = len(filenames))
        return dict(zip(filenames, chunks))
    return split

def name_file_helper(self, in_file_ref, filename):
    def rename_from(in_files):
        return {filename: in_files[in_file_ref]}
    return rename_from
        