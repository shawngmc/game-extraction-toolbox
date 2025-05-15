# 0.2.0
- Fixes
  - Remove external compiled dependencies 
    - Removed libmagic, which has binary components
    - Removed UnityPy, which has binary components... this does break SaGa extraction
- Added Collections
  - kof97_gm: The King of Fighters '97 Global Match - thanks @fliperama86
    - Requires Neo-Geo BIOS ROM
  - mvscc: Marvel vs. Capcom Fighting Collection - thanks @fliperama86
    - 5/7 games implemented
    - The Punisher and MVC2 not yet implemented
- Updated Collections
  - NeoGeo Classics by SNK (Humble Store)
    - Fixed issue with AoF2 zip identification
    - Added Basebasll Stars 2
- Known Issues
  - Collection of SaGa/Final Fantasy Legend
    - currently broken; needs reimplemented without UnityPy

# 0.1.7
 - Added Games/Collections
   - Breakers Collection (Thanks tydog98 and Feilakas)
   - MegaMan Battle Network Legacy Collection 1 (Thanks Bad-Acetabulum, RealRelativeEase, and Seb)
   - MegaMan Battle Network Legacy Collection 2 (Thanks Bad-Acetabulum, RealRelativeEase, and Seb)
 - Fixes
   - Requires Python 3.9+
   - Fixed bug when tracking verification errors

# 0.1.6
 - Added Games/Collections
   - NeoGeo Classics by SNK (Humble Store)
 - Fixes
   - Limit python-magic-bin dependency to Windows

# 0.1.5
 - Added Games/Collections
   - Sega Smash Pack 1 (Thanks zZeck)
   - Sega Smash Pack 2 (Thanks zZeck)

# 0.1.4
- Updated Collections:
  - Genesis and Mega Drive Collection
    - Fixed mislabeled Super Thunder Blade ROM
  - IREM Arcade Classics
    - Fix bug preventing details output
  - SNK 40th Anniversary Edition
    - Bermuda Triangle: Completed extraction on actual Bermuda Triangle (#37)
- Improvements:
  - Added input/output file verification to tasks (#36)
- Internal:
  - Made a few reusable tasks - 'CopyTask', 'ZipSpliceTask', 'SpliceTask'

# 0.1.3
- Improvements:
  - Fixed forgotten version number roll
  - Added badges to readme

# 0.1.2
- Added Games/Collections:
  - Psikyo Shooter Collector's Bundle (Partial Only)
  - IREM Arcade Classics
- Updated Collections:
  - Arcade Collection Anniversary Classics
    - hcastle/akumajoun: Partial -> Good
    - nemesis: Partial -> Good
    - vulcan/gradius2: Partial -> Good
    - thunderx: Partial -> Good
    - salamand/lifeforce: Partial -> Good
      - lifefrcej has a known bad dump, but runs fine
  - Atari Vault
    - Fixed a bug preventing this script from completing
  - Namco Arcade Game Series
    - Fixed partial support
  - SNK 40th Anniversary Collection
    - victroad: Playable -> Playable: Added missing PID ROM that is in chopperb (was placeholder)

# 0.1.1
- Added Games/Collections:
  - Wonder Boy The Dragon's Trap
- Updated Collections:
  - Arcade Collection Anniversary Classics
    - ajaxj/typhoon: No-ROM -> Good
    - hcastle/hcastlee/hcastlek/akumajoun: No-ROM -> Good
  - PAC MAN Museum Plus
    - pacland: Partial -> Good: properly ID'd as modified paclandj and found missing ROM
    - puckman: Partial -> Playable: Added placeholder for missing PROM
    - Fix entry in README
  - SNK 40th Anniversary Collection
    - bbusters/bbustersj/bbustersu: Playable -> Good: Added missing EEPROM
    - bermudata: Playable -> Playable: Removed unnecessary placeholders
    - legofair: Playable -> Playable: Added missing placeholders
    - psychosj: Broken -> Playable: Added missing Sound ROM
    - worldwar: Partial -> Playable: Added missing ADPCM ROM, removed unnecessary placeholders
- Improvements:
  - More consistent 'ROM Status' field (#29)
- Internal:
  - Started adding typing hints to util classes

# 0.1.0
- Added Games/Collections:
  - Atari Vault
  - Mortal Kombat Arcade Collection (No playable ROMs at this time)
  - Namco Arcade Game Series
  - Pac Man Museum Plus
  - Zombies Ate My Neighbor & Ghoul Patrol
- Updated Collections:
  - SNK 40th Anniversary Collection
    - Added partial (broken) ROM extraction support
    - Fixed most ROMs, including changes from lionel/BuildROM and some further decoding research
- Improvements:
  - Some tasks now support config flags via '--prop'; see task details for supported flags
  - Reworked tables using TextTable to make code cleaner and tables more reliable
  - Added placeholder partials for CAS1 and CAS2
  - Performance improvements, including major gains for deinterleave and bit shuffle operations
  - Fix a bug where some tasks aren't listed
- Internal:
  - Restructured some tasks to allow splitting/props
  - Added some support tool for Steam folders (eventually may add detection?)
  
# 0.0.22
- Added Games/Collections:
  - Disney Classics Collection: Aladdin and Lion King (w/ Jungle Book DLC)
  - SNK 40th Anniversary Collection
- Updated Collections:
  - Street Fighter 30th Anniversary Collection
    - Added International Release Support

# 0.0.21
- Added Games/Collections:
  - Blizzard Arcade Collection
  - Bubsy Two-Fur
  - Collection of SaGa/Final Fantasy Legend
  - Disney Afternoon Collection
  - Double Dragon Trilogy
  - Mega Man Legacy Collection 1
  - Mega Man X Legacy Collection 1
  - Sonic Adventure DX (Hidden Game Gear games)
- Improvements:
  - Moved 'postprocess steam' commands to more generic 'tasks' command
    This is one of the main purposes of this program, and not Steam specific - GOG, etc. should also be considered
  - Added default input folders for Tasks
  - Fixing tables in task details
- Internal:
  - Test configs for development should now work on any machine
  - Tasks are now slightly more defined using a class
  - First major lint/code style effort; nowhere near done, but much more idiomatic
  
# 0.0.20
- Added Games/Collections:
  - Sega Genesis and Mega Drive Collection
- Functional Improvements
  - ZIP files now actually compressed
  - More code reuse
  - Standardized logging config on all CLI commands (not all USE the logger yet)
  - Makes output folder if it doesn't exist

# 0.0.19
- Added Games/Collections:
  - Street Fighter 30th Anniversary Collection
- README improvements

# 0.0.18
- Repush

# 0.0.17
- Readd psutil, original bitarray ref

# 0.0.16
- Readd missing library

# 0.0.15
- Remove OBE libraries to fix install issues

# 0.0.14
- Fix postprocess steam extract command

# 0.0.13
- Added 'version' subcommand
- More build improvements
- Fix postprocess steam list command

# 0.0.12
- Re-enabled magic after fixing library conflict

# 0.0.7 - 0.0.11
- Packaging/Installer Fixes
- Magic file IDing temporarily disabled

# 0.0.6
- Added Games/Collections:
  - Capcom Beat 'em Up Bundle
  - Capcom Fighting Collection
- Added to library:
  - Generic IBIS CPS2 handling
- Cleanup

# 0.0.5
- Cleanup

# 0.0.3
- README fix

# 0.0.2
- Initial Release