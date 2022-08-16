## Street Fighter 30th Anniversary Collection

This is reverse-engineered based on:
- The Japanese shell scripts in https://web.archive.org/web/20220213232038/http://blog.livedoor.jp/scrap_a/archives/22823395.html
- Valad Amoleo's https://github.com/ValadAmoleo/sf30ac-extractor/

Beyond the usual QSound dl-1425.bin and decryption keys, some of the CRC matches appear to be modified VROMs. The extraction is correct - 90%+ of the ROM matches - but details appear to be changed.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                                         | **MAME Ver.**     | **FB Neo**     | **Filename**     | **CRC**     | **Notes**  
---------------------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------  
 **Street Fighter**                               | MAME 0.246    | Y          | sf.zip           | Bad         | 
 **Street Fighter 2**                             | MAME 0.78     | N          | sf2ub.zip        | Bad         | (2) (3)
 **Street Fighter Alpha**                         | MAME 0.139    | N          | sfau.zip         | Bad         | (1)
 **Street Fighter Alpha 2**                       | MAME 0.139    | N          | sfa2u.zip        | Bad         | (1) (3)
 **Street Fighter Alpha 3**                       | MAME 0.139    | N          | sfa3u.zip        | Bad         | (1)
 **Street Fighter 3**                             | MAME 0.246    | Y          | sfiiina.zip      | OK          |
 **Street Fighter 3: 2nd Impact**                 | MAME 0.246    | Y          | sfiii2n.zip      | OK          |
 **Street Fighter 3: 3rd Strike**                 | MAME 0.246    | Y          | sfiii3nr1.zip    | OK          |
 **Street Fighter 2 Championship Edition**        | MAME 0.78     | N          | sf2ce.zip        | Bad         | (2) (3)
 **Street Fighter 2 Hyper Fighting**              | MAME 0.78     | N          | sf2t.zip         | Bad         | (2) (3)
 **Super Street Fighter 2**                       | MAME 0.139    | N          | ssf2u.zip        | Bad         | (1) (3)
 **Super Street Fighter 2 Turbo**                 | MAME 0.139    | N          | ssf2tu.zip       | Bad         | (1) (3)

1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require.
2. These ROMs require an older version MAME. They test fine in MAME 0.78 (Mame 2003 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require.
3. These are using an older naming convention to allow recognition by the targeted MAME version.