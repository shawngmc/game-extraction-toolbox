'''
Magic-bytes handler for game extraction specific file types
'''

# Internally tracking these in https://docs.google.com/spreadsheets/d/1eMI9EIzopg1J9UZsMFOx5lLSMPsf7EYxovLM5VFoUjU/edit#gid=0

magic_types = {
    "KPKA": {
        "description": "KPKA Archive, Capcom RE Engine",
        "magic_bytes": b"KPKA"
    },
    "IBIS": {
        "description": "IBIS Archive, Capcom ROM Releases",
        "magic_bytes": b"IBIS"
    },
    "ARC": {
        "description": "ARC Archive, Capcom MT Framework",
        "magic_bytes": b"ARC"
    },
    "M2": {
        "description": "M2 Archive, M2 (Developer/Publisher)",
        "magic_bytes": b"mdf"
    },
    "PKZIP": {
        "description": "PK Zip Archive",
        "magic_bytes": "PK".encode('utf-8')
    }
}



def custom_magic_from_path(in_file):
    '''Use custom magic to id a file's contents'''
    # Try to identify based on known file types magic bytes
    with open(in_file, 'rb') as file:
        content_start = file.read(2048)
        return enhanced_look(content_start)

def custom_magic_from_buffer(content_peek):
    '''Use custom magic to id buffer content'''
    # Try to identify based on known file types magic bytes
    return enhanced_look(content_peek)

def enhanced_look(content_peek):
    '''Magic-like function that identifies uncommon relevant filetypes'''
    for short_name, magic_type in magic_types.items():
        if content_peek[0:len(magic_type['magic_bytes']) == magic_type['magic_bytes']]:
            return magic_type['description']
    return 'data'

_PK_HEADER = "PK".encode('utf-8')
def check_if_zip(contents):
    '''Simple ZIP file check that searches for a 'PK' ZIP header'''
    return contents[0:2] == _PK_HEADER
