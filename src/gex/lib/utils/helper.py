
def cleanpath(path_str):
    if path_str.startswith("\""):
        path_str = path_str[1:]
    if path_str.endswith("\""):
        path_str = path_str[:-1]
    return path_str