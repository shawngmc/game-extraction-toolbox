'''Convenience functions for hashing a binary blob'''
import hashlib
import zlib

def get_crc(content):
    '''Get the common CRC32 hash for a blob'''
    return hex(zlib.crc32(content) & 0xffffffff)

def get_md5(content):
    '''Get the MD5 sum for a blob'''
    return hashlib.md5(content).hexdigest()

def get_sha1(content):
    '''Get the SHA-1 hash for a blob'''
    return hashlib.sha1(content).hexdigest()
