'''
Utility functions for SNK games
'''

# from gex.lib.utils.blob import transforms

def sfix_reorder(contents):
    '''Reorders an SFIX rom file'''
    for i in range(0, len(contents), 32):
        tmp = bytearray(32)
        for j in range(0, 8):
            tmp[j+16] = contents[i+4*j+0]
            tmp[j+24] = contents[i+4*j+1]
            tmp[j+ 0] = contents[i+4*j+2]
            tmp[j+ 8] = contents[i+4*j+3]
        contents[i:i+32] = tmp
    return contents
