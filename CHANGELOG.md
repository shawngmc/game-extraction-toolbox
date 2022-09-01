# 0.0.23
- Improvements:
  - Some tasks now support config flags via '--prop'; see task details for supported flags
  - Reworked tables using TextTable to make code cleaner and tables more reliable
- Internal:
  - Restructured some tasks to allow splitting/props

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