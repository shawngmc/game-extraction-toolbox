## Capcom Fighting Collection

This is reverse-engineered based on the CBEYB work from https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                                         | **MAME Ver.**     | **FB Neo**     | **ENG Filename**     | **ENG CRC**     | **JP Filename**     | **JP CRC**     | **Notes**  
---------------------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------------|------------|-----------  
 **Darkstalkers: The Night Warriors**             | MAME 0.139    | N          | dstlku.zip       | Bad         | vampj.zip        | Bad        | (1)
 **Night Warriors:Darkstalkers' Revenge**         | MAME 0.139    | N          | nwarru.zip       | Bad         | vhuntjr2.zip     | Bad        | (1)
 **Vampire Savior: The Lord of Vampire**          | MAME 0.139    | N          | vsavj.zip        | Bad         | vsavu.zip        | Bad        | (1)
 **Vampire Hunter 2: Darkstalkers Revenge**       | MAME 0.139    | N          | N/A              | N/A         | vhunt2,zip       | Bad        | (1)
 **Vampire Savior 2: The Lord of Vampire**        | MAME 0.139    | N          | N/A              | N/A         | vsav2.zip        | Bad        | (1)
 **Cyberbots: Fullmetal Madness**                 | MAME 0.139    | N          | cybotsj.zip      | Bad         | cybotsu.zip      | Bad        | (1)
 **Super Puzzle Fighter II Turbo**                | MAME 0.139    | N          | spf2xj.zip       | Bad         | spf2tu.zip       | Bad        | (1) (3)
 **Super Gem Fighter Mini Mix**                   | MAME 0.139    | N          | pfghtj.zip       | Bad         | sgemf.zip        | Bad        | (1)
 **Hyper Street Fighter II: Anniversary Edition** | MAME 0.139    | N          | hsf2j.zip        | Bad         | hsf2.zip         | Bad        | (1) (4)
 **Red Earth**                                    | N/A           | N/A        | redearth         | N/A         | warzard          | N/A        | (2)


1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require
2. This CPS3 game cannot yet be extracted.
3. The US version of does not have a valid MAME release.
4. The JP version of is using an older internal file naming convention.