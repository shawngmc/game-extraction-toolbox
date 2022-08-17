

import hashlib
import zlib


def get_crc(content):
    return hex(zlib.crc32(content) & 0xffffffff)

def get_md5(content):
    return hashlib.md5(content).hexdigest()

def get_sha1(content):
    return hashlib.sha1(content).hexdigest()