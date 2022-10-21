# Roadmap

## Future / Other Tools
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
- Teenage Mutant Ninja Turtles: The Cowabunga Collection (August 30th, 2022)
  Assets are jammed into one file, but that file appears to be encrypted or compressed. Notes in #17.
  https://github.com/Masquerade64/Cowabunga
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
  


## Not Yet Owned / Future Investigation
- Neo Geo Pocket Color Selection Vol. 1
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

## Upcoming Releases
- Atari 50th: Anniversary Collection (Winter 2022)

## Unlikely
- Williams Arcade Classics (PC CD-ROM, 1995)
  Initial research shows that this is likely not ROM based.

## Not Complete ROMs (may add partial extraction later)
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

## Not ROMs
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

