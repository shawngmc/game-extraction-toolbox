
import os


def cleanpath(path_str):
    if path_str.startswith("\""):
        path_str = path_str[1:]
    if path_str.endswith("\""):
        path_str = path_str[:-1]
    return path_str

def preparepath(out_path):
    if not os.path.exists(out_path):
        try:
            os.makedirs(out_path)
        except Exception as x:
            raise Exception("Cannot create output folder.")
    else:
        if not os.access(out_path, os.W_OK):
            raise Exception("Cannot write to output folder.")

def task_module_print_header(name, transform_module):
    print(f'{name}: {transform_module.title}')
    if len(transform_module.description) > 0:
        print(f'  {transform_module.description}')
    print(f'  Expected input dir: {transform_module.in_dir_desc} (ex. {transform_module.default_folder})')
