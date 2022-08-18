
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

