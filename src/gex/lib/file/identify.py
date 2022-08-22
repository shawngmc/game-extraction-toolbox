'''
Wrapper for python-magic that adds support for game extraction specific file types
'''
import magic

KPKA = "KPKA Archive, Capcom RE Engine"
IBIS = "IBIS Archive, Capcom ROM Releases"
ARC = "ARC Archive, Capcom MT Engine"

def enhanced_magic_from_path(in_file):
    '''Use libmagic and enhanced_look to id a file's contents'''
    magic_id = None
    try:
        magic_id = magic.from_file(in_file)
    except Exception as error:
        print(error)

    if magic_id != 'data' and magic_id is not None:
        return magic_id

    # Try to identify based on known file types magic bytes
    with open(in_file, 'rb') as file:
        content_start = file.read(2048)
        return enhanced_look(content_start)

def enhanced_magic_from_buffer(content_peek):
    '''Use libmagic and enhanced_look to id buffer content'''
    magic_id = None
    try:
        magic_id = magic.from_buffer(content_peek)
    except Exception as error:
        print(error)

    if magic_id != 'data' and magic_id is not None:
        return magic_id

    # Try to identify based on known file types magic bytes
    return enhanced_look(content_peek)

def enhanced_look(content_peek):
    '''Magic-like function that identifies uncommon relevant filetypes'''
    if content_peek[0:4] == b"KPKA":
        return KPKA
    if content_peek[0:4] == b"IBIS":
        return IBIS
    if content_peek[0:3] == b"ARC":
        return ARC
    return 'data'

_PK_HEADER = "PK".encode('utf-8')
def check_if_zip(contents):
    '''Simple ZIP file check that searches for a 'PK' ZIP header'''
    return contents[0:2] == _PK_HEADER
