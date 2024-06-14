# Roadmap

## Future / Other Tools
- Mega Man Battle Network Collection Vol 1 + 2
  
- Retro Classix by Data East
  In title\title_Data\StreamingAssets folder
- Brave Battle Saga - The Legend of The Magic Warrior
- Activision Anthology Remix PC
  https://forums.atariage.com/topic/336118-how-to-extract-roms-from-the-activision-anthology-for-pc-and-a-request-for-info-on-the-included-roms/
- Sega Mega Drive & Genesis Classics
  Compressed ROMS: https://github.com/farmerbb/RED-Project/wiki/Sega-Mega-Drive-&-Genesis-Classics

### Uses BPList/Mbundle
- Samuari Shodown Collection
  https://github.com/ValadAmoleo/sf30ac-extractor

### Uses .PSB.M/.BIN File Container?
- Contra Anniversary Collection
  https://github.com/farmerbb/RED-Project/wiki/Contra-Anniversary-Collection
  Key is in executable at 0x272AF0, 13 bytes
- Castlevania Advance Collection
  https://github.com/farmerbb/RED-Project/wiki/Castlevania-Advance-Collection - needs audio fix
  Key is in executable at 0x224FA4, 13 bytes
- Castlevania Anniversary Collection
  https://github.com/farmerbb/RED-Project/wiki/Castlevania-Anniversary-Collection
  Key is in executable at 0x251CF0, 13 bytes
- Namco Museum Archives (Vol 1 and Vol 2)
  https://github.com/farmerbb/RED-Project/wiki/Namco-Museum-Archives
  Key is in executable at 0x1DC894, 13 bytes   (in both!)

### Uses dotemu2mame.js
- Raiden Legacy
  https://github.com/farmerbb/RED-Project/wiki/Raiden-Legacy

## Owned / Under Investigation
- Capcom Arcade Stadium 1
  Current versions have an odd archive format (unlike the CAS1_Old ZIP version).
  PLACEHOLDER ADDED. See #18.
- Capcom Arcade Stadium 2
  Current versions have an odd archive format (unlike the CAS1_Old ZIP version).
  PLACEHOLDER ADDED. See #18.
- Mega Man Zero / ZX Collection
- Mega Man X Legacy Collection 2
- Mega Man Legacy Collection 
- Arcade Collection Anniversary Classics
  Mostly working, but 2 titles remain...
- Psiyko Shooter Collector's Bundle https://store.steampowered.com/bundle/18805/PSIKYO_SHOOTER_Collectors_Bundle/
- PSP: EA Replay
  \PSP_GAME\USRDIR\data\roms.viv is an EA BIG4 archive that can be extracted via QuickBMS
  It has sensible ROM filenames, but the files are too small and not in an expected format.
  They don't appear to have REFPACK, zlib or gzip headers, nor use RAW DEFLATE.
- The King of Fighters 97 Global Match
  Possibly KOF 97? http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=kof97
  In data/rom/:
  - exact matches
    m1.bin is cslot1:audiocpu 232-m1.m1
    s1.bin and s2.bin are identical, and are cslot1:fixed 232-s1.s1
    sp_4j.bin is japan-mv1b:mainbios japan-j3.bin
    p1.bin is cslot1:maincpu roms - concatenated 232-p1.p1 and 232-p2.sp2
    v1.bin is cslot1:ymsnd:adpcma - concatenated 232-v1.v1, 232-v2.v2, 232-v3.v3
  - suspected
    c1.bin appears to be the cslot1:sprite roms, interleaved as expected
  - only in kof97gm
    sp_4s.bin is likely a mainbios, but not a known one
  - not in kof97gm
    spritegen:zoomy	000-lo.lo
    fixedbios sfix.sfix
    audiobios sm1.sm1
- Vasara Collection
  Partial roms exist in VasaraCollection_Data/StreamingData/VSR1.dat and VSR2.dat, but there's some missing, and the other files are UnityFS
  VSR1.dat
  0x00000000	0x001FFFFF	2MB	data.u34
  0x00200000	0x002FFFFF	1MB	NULL
  0x00300000	0x003FFFFF	1MB	deinterleave(1b) -> prg-l.u30, prg-h.u31
  0x00400000	0x01FFFFFF	16MB	???
  0x02000000	0x023FFFFF	4MB	NULL
  Missing 36 MB of contents with 16MB of unidentified stuff?
- Retro SNES Collection Vol. 1 (Jim Power, Legend, Iron Commando, Dorke and Ymp)
- S-Tribute (Metal Black S-Tribute, Puzzle Bobble 2x/3 and Bust-a-Move 2/3 S-Tribute)
  - These appear to have a bin-cue file pair for each title
  - However, these are not mountable - are they encrypted?
  


## Not Yet Owned / Future Investigation
- Neo Geo Pocket Color Selection Vol. 1
  This looks like NeoGeo Pocket emulation
- ColecoVision Flashback
  https://github.com/ZetTheLegendaryHero/Colecovision-Flashback-40-Game-Pack-ROM-Extractor
- 8-bit Adventure Anthology: Volume I	(Shadowgate, The Uninvited, Deja Vu)
  https://gitlab.com/vaiski/romextract/-/blob/master/supported.csv
- R-Type Dimensions EX
- CAVE: Mushihimesama
  Recommended in #15.
- CAVE: DoDonPachi Resurrection
  Recommended in #15.
- CAVE: Deathsmiles
  Recommended in #15.
- CAVE: Deathsmiles I + II
  Recommended in #15.
- Darius Cozmic Collection Arcade
- Taito Legends 1 and 2
- Saturn Cotton Collection
  https://gbatemp.net/threads/saturn-emulation-using-cotton-guardian-force-testing-and-debug.600756/
- Williams Arcade Classics (PC CD-ROM, 1995)
  Initial research shows that this is likely not ROM based.
- Andro Dunos II
  Likely a all-new build, as this is a new game
- SNK VS. CAPCOM: THE MATCH OF THE MILLENNIUM
  This looks like NeoGeo Pocket emulation
- NEOGEO POCKET COLOR SELECTION Vol.2
  This looks like NeoGeo Pocket emulation
- Umihara Kawase
  Slowdown is gone, so it might be a port
- Super Kick Off
  Has a bunch of diff 8/16-bit platforms
- Videopac Collection 1
  10 Magnavox Odyssey 2 games?
- Actua Sports (Actua Tennis, Actua Ice Hockey, Actua Ice Hockey 2, Actua Golf, Actua Soccer 2)
  All PS1 games?
- Todd's Adventures in Slime World (Lynx/Mega Drive)
- Buggy (PS1)
- N2O
- Summer Games (Atari 2600/CPC/Master System/Spectrum)
- California Games II (SNES?)
- Blue Lightning (Lynx)
- Checkered Flag (Lynx)
- Zarlor Mercenary (Lynx)
- Electrocop (Lynx)
- Gates of Zendocon (Lynx)
- Elland: The Crystal Wars (GBA)


## Incomplete ROMs (may add partial extraction later)
- Mortal Kombat Kollection
  Audio ROMs were replaced with a different audio solution.
- Dungeons & Dragons: Chronicles of Mystara
  Maincpu and Gfx ROMs are there, but audio is completely reworked.

### .SR Releases
The SR archives can be extracted via QuickBMS script: https://forum.xentax.com/viewtopic.php?t=13718
However, these seem to always use rebuilt audio, and some of the games have been rebuilt as native ELF executables.
- PSP: Capcom Classics Collection: Remixed
- PS2: Midway Arcade Treasures Vol. 1
- PS2: Midway Arcade Treasures Vol. 2

## Will Not Cover
### Not ROMs

- Phoenix Wright Ace Attorney Trilogy
  Appears to be a Unity port
- Mortal Kombat 1+2+3 (GOG)
  DOS Version
- Mortal Kombat Trilogy (GOG)
  Windows Version
- Earthworm Jim 1 and 2 (Steam, GOG)
  DOS Version
- Disney's Hercules
  https://www.gog.com/en/game/disneys_hercules
  Native PC Game
- Turok: Dinosaur Hunter
  Rebuilt on KeX Engine (https://www.nightdivestudios.com/kex/)
- Turok 2: Seeds of Evil
  Rebuilt on KeX Engine (https://www.nightdivestudios.com/kex/)
- The King of Fighters '98 Ultimate Match
  Rebuilt by CodeMasters
- The King of Fighters 2002 Unlimited Match
  Rebuilt by CodeMasters

### Encrypted
- Atari 50th: Anniversary Collection (Winter 2022)
  https://store.steampowered.com/app/1919470/Atari_50_The_Anniversary_Celebration/
  Digital Eclipse release that is encrypted
  Recommend looking at: https://github.com/Masquerade64/Cowabunga
- Teenage Mutant Ninja Turtles: The Cowabunga Collection (August 30th, 2022) (#17 in GitHub project)
  https://store.steampowered.com/app/1659600/Teenage_Mutant_Ninja_Turtles_The_Cowabunga_Collection/
  Digital Eclipse release that is encrypted
  Recommend looking at: https://github.com/Masquerade64/Cowabunga
