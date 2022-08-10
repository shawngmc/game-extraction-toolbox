## Capcom Beat 'Em Up Bundle

The notes I found were at https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                             | **MAME Ver.**     | **FB Neo**     | **ENG Filename**     | **ENG CRC**     | **JP Filename**     | **JP CRC**     | **Notes**  
---------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------------|------------|-----------  
 **Final Fight**                      | MAME 0.246    | Y          | ffight.zip       | Bad         | ffightj.zip     | Bad        | (2)
 **King of Dragons**                  | MAME 0.246    | Y          | kod.zip          | Bad         | kodf.zip        | Bad        | (2)
 **Captain Commando**                 | See (3)       | Y          | captcomm.zip     | Bad         | captcommj.zip   | Bad        | (2) (3)
 **Knights of the Round**             | MAME 0.246    | Y          | knights.zip      | Bad         | knightsj.zip    | Bad        | (2)
 **Warriors of Fate**                 | None          | N          | wof.zip          | Bad         | wofj.zip        | Bad        | (2) (4)
 **Powered Gear**                     | MAME 0.139    | N          | pgear.zip        | OK          | armwar.zip      | OK         | (1)
 **Battle Circuit**                   | MAME 0.139    | N          | batcir.zip       | OK          | batcirj.zip     | OK         | (1)


1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require
2. These ROMs play fine, even in the current MAME, despite the bad CRCs. The bad CRCs are small ancillary files that aren't strictly required or included, but stubbed out to pass checks. 
3. The JP version of this ROM is fine in modern MAME 0.246; the English version needs 0.139
4. The Audio CPU ROM for this is not present in the expected format. Further investigation required.

