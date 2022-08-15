## Street Fighter 30th Anniversary Collection

This is reverse-engineered based on:
- The Japanese shell scripts in https://web.archive.org/web/20220213232038/http://blog.livedoor.jp/scrap_a/archives/22823395.html
- Valad Amoleo's https://github.com/ValadAmoleo/sf30ac-extractor/

Beyond the usual QSound dl-1425.bin and decryption keys, some of the CRC matches appear to be modified VROMs. The extraction is correct - 90%+ of the ROM matches - but details appear to be changed.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                                         | **MAME Ver.**     | **FB Neo**     | **Filename**     | **CRC**     | **Notes**  
---------------------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------  
 **Street Fighter 2**                             | MAME 0.139    | N          | sf2.zip          | Bad         | (1)
 **Street Fighter Alpha**                         | MAME 0.139    | N          | sfau.zip         | Bad         | (1)
 **Street Fighter Alpha 2**                       | MAME 0.139    | N          | sfa2u.zip        | Bad         | (1) (2)
 **Street Fighter Alpha 3**                       | MAME 0.139    | N          | sfa3u.zip        | Bad         | (1)
 **Street Fighter**                               | NYI           | NYI        | NYI              | NYI         | NYI
 **Street Fighter 3**                             | NYI           | NYI        | NYI              | NYI         | NYI
 **Street Fighter 3: 2nd Impact**                 | NYI           | NYI        | NYI              | NYI         | NYI
 **Street Fighter 3: 3rd Strike**                 | NYI           | NYI        | NYI              | NYI         | NYI
 **Street Fighter 2 Championship Edition**        | NYI           | NYI        | NYI              | NYI         | NYI
 **Street Fighter 2 Hyper Fighting**              | NYI           | NYI        | NYI              | NYI         | NYI 
 **Super Street Fighter 2**                       | NYI           | NYI        | NYI              | NYI         | NYI
 **Super Street Fighter 2 Turbo**                 | NYI           | NYI        | NYI              | NYI         | NYI

1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require.
2. These are using an older naming convention to allow recognition by MAME 0.139.