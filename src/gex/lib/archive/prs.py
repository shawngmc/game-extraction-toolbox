# SEGA PRS Decompression (LZS variant)
# From: https://forums.qhimm.com/index.php?topic=11225.0 (Micky)
# Credits:
# based on information/comparing output with
# Nemesis/http://www.romhacking.net/utils/671/
# puyotools/http://code.google.com/p/puyotools/
# fuzziqer software prs/http://www.fuzziqersoftware.com/projects.php

# TODO: This was quickly converted from python2, and can likely be optimized and made much more pythonic

import array

class DecompressPrs:
    def __init__(self, data):
        self.ibuf = array.array("B", data)
        self.obuf = array.array("B")

        self.iofs = 0
        self.bit = 0
        self.cmd = 0

    def _get_byte(self):
        val = self.ibuf[self.iofs]
        self.iofs += 1
        return val

    def _get_bit(self):
        if self.bit == 0:
            self.cmd = self._get_byte()
            self.bit = 8
        bit = self.cmd & 1
        self.cmd >>= 1
        self.bit -= 1
        return bit

    def decompress(self):
        while self.iofs < len(self.ibuf):
            cmd = self._get_bit()
            if cmd:
                self.obuf.append(self.ibuf[self.iofs])
                self.iofs += 1
            else:
                t = self._get_bit()
                if t:
                    a = self._get_byte()
                    b = self._get_byte()

                    offset = ((b << 8) | a) >> 3
                    amount = a & 7
                    if self.iofs < len(self.ibuf):
                        if amount == 0:
                            amount = self._get_byte() + 1
                        else:
                            amount += 2

                    start = len(self.obuf) - 0x2000 + offset
                else:
                    amount = 0
                    for _ in range(2):
                        amount <<= 1
                        amount |= self._get_bit()
                    offset = self._get_byte()
                    amount += 2

                    start = len(self.obuf) - 0x100 + offset
                for j in range(amount):
                    if start < 0:
                        self.obuf.append(0)
                    elif start < len(self.obuf):
                        self.obuf.append(self.obuf[start])
                    else:
                        self.obuf.append(0)
                    start += 1

        return self.obuf.tobytes()
