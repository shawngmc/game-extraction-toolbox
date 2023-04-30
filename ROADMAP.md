# Roadmap

## Future / Other Tools  
- MacVenture Series: Shadowgate, The Uninvited, Deja Vu, Deja Vu II
  https://gitlab.com/vaiski/romextract/-/blob/master/supported.csv
- Retro Classix by Data East
  In title\title_Data\StreamingAssets folder
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
- City Connection (owns Jaleco IP)
  - S-Tribute (Metal Black S-Tribute, Puzzle Bobble 2x/3 and Bust-a-Move 2/3 S-Tribute)
    - These appear to have a bin-cue file pair for each title
    - However, these are not mountable - are they encrypted?
  - Psiyko Shooter Collector's Bundle https://store.steampowered.com/bundle/18805/PSIKYO_SHOOTER_Collectors_Bundle/
    - STRIKERS 1945
    - STRIKERS 1945 II
    - STRIKERS 1945 III
    - GUNBIRD
    - GUNBIRD 2
    - GUNBARICH
    - Samurai Aces
    - TENGAI
    - Samurai Aces III: Sengoku Cannon
    - SOL DIVIDE -SWORD OF DARKNESS-
    - Dragon Blaze
    - Zero Gunner 2-
- R-Type Dimensions EX
- Capcom Arcade Stadium 1
  Current versions have an odd archive format (unlike the CAS1_Old ZIP version).
  PLACEHOLDER ADDED. See #18.
- Capcom Arcade Stadium 2
  Current versions have an odd archive format (unlike the CAS1_Old ZIP version).
  PLACEHOLDER ADDED. See #18.
- Mega Man Zero / ZX Collection
- Mega Man X Legacy Collection 2
- Mega Man Legacy Collection 2
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
- Piko Interactive Releases
  - Jim Power (SNES)
  - Legend (SNES)
  - Iron Commando (SNES)
  - Dorke and Ymp (SNES)
  - Brave Battle Saga - The Legend of The Magic Warrior (Genesis)
- CAVE (Recommended in #15)
  - Mushihimesama
  - DoDonPachi Resurrection
  - Deathsmiles
  


## Not Yet OwneD / Future Investigation
- Darius Cozmic Collection Arcade
- CAVE (Recommended in #15)
  - Deathsmiles I + II
- SNK Neo Geo Pocket Color Releases
  - Neo Geo Pocket Color Selection Vol. 1
  - SNK VS. CAPCOM: THE MATCH OF THE MILLENNIUM
  - NEOGEO POCKET COLOR SELECTION Vol.2
- ColecoVision Flashback
  https://github.com/ZetTheLegendaryHero/Colecovision-Flashback-40-Game-Pack-ROM-Extractor
- Taito Legends 1 and 2
- Saturn Cotton Collection
  https://gbatemp.net/threads/saturn-emulation-using-cotton-guardian-force-testing-and-debug.600756/
- Williams Arcade Classics (PC CD-ROM, 1995)
  Initial research shows that this is likely not ROM based.
- Andro Dunos II
  Likely a all-new build, as this is a new game
- Umihara Kawase
  Slowdown is gone, so it might be a port
- F-117A Stealth Fighter (NES)
- Piko Releases
  - Super Hunchback (GB)
  - Street Racer (SNES and DOS)
  - First Samurai (SNES)
  - Second Samurai (SNES)
  - 40 Winks (PS1)
  - Tunnel B1 (PS1 and DOS)
  - Radical Rex (SNES)
  - Dragon View (SNES)
  - Noah's Ark (NES)
  - Super 3D Noah's Ark (SNES and DOS)
  - Gourmet Warriors (SNES)
  - Water Margin - The Tale of Clouds and Wind (Genesis)
  - 8-Eyes (NES)
  - The Gadget Twins (Genesis)
  - Power Punch II (NES)
  - Switchblade (Genesis)
  - Tinhead (SNES)
  - Impossimole (TG16)
  - Viper (PS1)
  - Motor Mash (PS1)
  - Canon - Legend of the New Gods (Genesis)
  - Zero Tolerance (Genesis)
  - Blender Bros (GBA)
  - LIKELY NOT ROMS
    - Attack of the Mutant Penguins (They made a Jaguar version, but port is likely DOS)
    - Brutal Sports - Football (Likely DOS or Amiga, but could be Jaguar)
    - Head Over Heels (Likely Amiga, but could be Atari ST or Jaguar)
    - Soccer Kid (there are tons of verions)
    - Super Hero League of Hoboken (DOS)
    - Spellcasting Collection (DOS)
    - The Immortal (a few versions)
- Console Classics/Pixel Games UK PS1 re-releases
  - Actua Tennis
  - Actua Ice Hockey
  - Actua Ice Hockey 2
  - Actua Golf
  - Actua Golf 3
  - Actua Soccer 2
  - Buggy (there are TWO)
  - Mass Destruction (PS1)
  - Superstar Dance Club (PS1)
  - TNN Motorsports Hardcore TR (PS1)
  - Motorhead (PS1)
  - Re-Loaded (PS1)
  - N2O
  - Super Kick Off
    Has a bunch of diff 8/16-bit platforms
  - Videopac Collection 1
    10 Magnavox Odyssey 2 games?
  - Gates of Zendocon (Lynx)
  - Zarlor Mercenary (Lynx)
  - Todd's Adventures in Slime World (Lynx/Mega Drive)
  - Summer Games (Atari 2600/CPC/Master System/Spectrum)
  - California Games (Lynx?)
  - California Games II (SNES?)
  - Blue Lightning (Lynx)
  - Checkered Flag (Lynx)
  - Electrocop (Lynx)
  - Elland: The Crystal Wars (GBA)



### .SR Releases
The SR archives can be extracted via QuickBMS script: https://forum.xentax.com/viewtopic.php?t=13718
However, these seem to always use rebuilt audio, and some of the games have been rebuilt as native ELF executables.
- PSP: Capcom Classics Collection: Remixed
- PS2: Midway Arcade Treasures Vol. 1
- PS2: Midway Arcade Treasures Vol. 2

## Limbo
These titles require a major breakthrough.

**Title**                                           | **Reason**               | **Notes**
----------------------------------------------------|--------------------------|--------------------------
Dariusburst Chronicle Saviours                      | Does not appear ROM-based | based on Darius Another Chronicle EX Arcade?
Dungeons & Dragons: Chronicles of Mystara           | Audio Reworked           | Maincpu and Gfx ROMs are there, but audio is completely reworked
Mortal Kombat Kollection                            | Audio Reworked           | Audio ROMs were replaced with a different audio solution.

## Will Not Cover

**Title**                                           | **Reason**               | **Notes**
----------------------------------------------------|--------------------------|--------------------------
Phoenix Wright Ace Attorney Trilogy                 | Not ROM-based            | Appears to be a Unity Port
Mortal Kombat 1+2+3 (GOG)                           | Not ROM-based            | Appears to be the old DOS version
Mortal Kombat Trilogy (GOG)                         | Not ROM-based            | Appears to be the old Windows version
Turok: Dinosaur Hunter                              | Not ROM-based            | Rebuilt on KeX Engine (https://www.nightdivestudios.com/kex/)
Turok 2: Seeds of Evil                              | Not ROM-based            | Rebuilt on KeX Engine (https://www.nightdivestudios.com/kex/)
Disney's Hercules (GOG)                             | Not ROM-based            | Appears to be the old Windows version
Earthworm Jim 1 (Steam, GOG)                        | Not ROM-based            | Appears to be the old DOS version
Earthworm Jim 2 (Steam, GOG)                        | Not ROM-based            | Appears to be the old DOS version
Atari 50th: Anniversary Collection                  | Encrypted                | Recommend looking at: https://github.com/Masquerade64/Cowabunga
Teenage Mutant Ninja Turtles: The Cowabunga Collection | Encrypted                | Recommend looking at: https://github.com/Masquerade64/Cowabunga
Raiden V: Directors Cut                             | Modern Sequel            | This is an XOne/PS4/Switch/Steam title, there's no ROM.
Teenage Mutant Ninja Turtles: Shredder's Revenge    | Modern Sequel            | This is an XOne/PS4/Switch/Steam title, there's no ROM.

## Below need re-verified
### Not ROMs

- The King of Fighters '98 Ultimate Match
  Rebuilt by CodeMasters
- The King of Fighters 2002 Unlimited Match
  Rebuilt by CodeMasters
