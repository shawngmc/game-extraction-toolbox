import magic

KPKA = "KPKA Archive, Capcom RE Engine"
IBIS = "IBIS Archive, Capcom ROM Releases"
ARC = "ARC Archive, Capcom MT Engine"

def enhanced_magic_from_path(in_file):
    magic_id = None
    try:
        magic_id = magic.from_file(in_file)
    except Exception as e:
        print(repr(e))

    if magic_id != 'data' and magic_id != None:
        return magic_id
    
    # Try to identify based on known file types magic bytes
    with open(in_file, 'rb') as file:
        content_start = file.read(2048)
        return enhanced_look(content_start)

def enhanced_magic_from_buffer(content_peek):
    magic_id = None
    try:
        magic_id = magic.from_buffer(content_peek)
    except Exception as e:
        print(repr(e))

    if magic_id != 'data' and magic_id != None:
        return magic_id
    
    # Try to identify based on known file types magic bytes
    return enhanced_look(content_peek)

def enhanced_look(content_peek):
    if content_peek[0:4] == b"KPKA":
        return KPKA
    if content_peek[0:4] == b"IBIS":
        return IBIS
    if content_peek[0:3] == b"ARC":
        return ARC
        
    return 'data'
            