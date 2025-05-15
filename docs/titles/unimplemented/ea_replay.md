# EA Replay
Looking at B.O.B.

Header
42 49 47 46 BIGF header				BIGF		Y
4E 39 A4 00 Archive size, little endian		10762574 	Y
00 00 00 0E Number of files, big endian		14		Y
00 00 01 62 Header size, big endian		354 bytes	Y

First entry
00 00 01 80 File offset				384 bytes	Y
00 0B 78 45 File size				751685 bytes	Y
62 6F 62 2E 73 6D 63 00 Null-term name string	bob.smc�	Y

The BIG archive appears to be extracting properly - multiple extractors show the same results, a hand extraction looks the same, the metadata lines up and extracting netcore/netcoreadhocboot.viv yields similar results.

This strongly implies that there is a step after the BIG extraction that would transform it into a valid ROM. The resulting file from the BIG is smaller than the real ROM, so it is likely compressed and encrypted still.

bob.dtb
This is likely a Data Array script - see https://tcrf.net/Rock_Band_(PlayStation_2)