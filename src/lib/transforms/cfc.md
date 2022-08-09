## Capcom Fighting Collection

This is reverse-engineered based on the CBEYB work from https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                             | **MAME Ver.**     | **FB Neo**     | **ENG Filename**     | **ENG CRC**     | **JP Filename**     | **JP CRC**     | **Notes**  
---------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------------|------------|-----------  
 **Darkstalkers: The Night Warriors** | MAME 0.139    | N          | dstlku.zip       | Bad         | vampj.zip        | Bad        | (1)
 **Night Warriors:Darkstalkers' Revenge** | MAME 0.139    | N          | nwarru.zip       | Bad         | vhuntjr2.zip     | Bad        | (1)


1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require


