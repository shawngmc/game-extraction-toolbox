# Unimplemented Collections

This document covers technical writeups for collections that either are not yet implements, cannot be implemented, or will not for various reasons.

## Hamster Arcade Archives
### Windows Store
While there are tools to find the download URLs for the Windows Store packages, these are encrypted .eappx packages.

These are installed in C:\Program Files\WindowsApps\. This folder is hidden; however, revealing it and taking ownership in Windows Explorer/Powershell/etc. is still not enough for these titles. The executable - which appears to have all substantial game content - is protected via Windows Encrpyted File System. The file has a lock overlay on the icon, and any attempts to open/copy it yield 'Access is denied'.

[UWPDumper](https://github.com/Wunkolo/UWPDumper), however, allows us to bypass this.

1) Buy the appropriate app and install it.
2) Start the app.
3) Run UWPDumper, then find the HAMSTER process in the list.
   (There may be multiple; if one fails, reopen the list and choose another.)
4) It will hook into the process and pull all files into a special folder.

At this point, the executable is the only reasonably large file, and there's no clear data structure that looks like a ROM at this time. The other remaining concern is size; for example, Metal Slug 4's basic ROM, compressed in ZIP, is well over 50MB, but the executable is only 34MB. 


## EA Replay
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