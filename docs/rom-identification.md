# ROM Identification

When searching for ROMs in collections, it's helpful to know what you are looking for. As such, below are technical breakdowns that are useful for this.


## NES

## SNES
### Headers
#### Types
SNES ROM files can have two types of headers:
- An optional 512 byte copier header, for data propietary to the device that dumped it. Almost useless.
- The SNES ROM Header - containing Nintendo-required data including title. Required to emulate.
- An optional Extended developer header - a flag in the main header tells it to look at this. Not generally useful.

#### Finding the SNES Header
The SNES ROM header is valuable for detecting a ROM. However, this header is NOT at the start of the file; it varies based on the cartridge's memory mapper type and the presence of that optional header:

| Mapper  | w/o Copier Header | w/ Copier Header |
|---------|-------------------|------------------|
| LoROM   | $007FC0           | $0081C0          |
| HiROM   | $00FFC0           | $0101C0          |
| ExHiROM | $40FFC0           | $4101C0          |

#### SNES Header Format
| First address | Length | Contents                                                                               |
|---------------|--------|----------------------------------------------------------------------------------------|
| $FFC0         | 21     | Cartridge title (21 bytes uppercase ASCII. Unused bytes should be spaces.)             |
| $FFD5         | 1      | ROM speed and memory map mode (LoROM/HiROM/ExHiROM)                                    |
| $FFD6         | 1      | Chipset (Indicates if a cartridge contains extra RAM, a battery, and/or a coprocessor) |
| $FFD7         | 1      | ROM size: 1<                                                                           |
| $FFD8         | 1      | RAM size: 1<                                                                           |
| $FFD9         | 1      | Country (Implies NTSC/PAL)                                                             |
| $FFDA         | 1      | Developer ID                                                                           |
| $FFDB         | 1      | ROM version (0 = first)                                                                |
| $FFDC         | 2      | Checksum                                                                               |
| $FFDE         | 2      | Checksum compliment (Checksum ^ $FFFF)                                                 |
| $FFE0         | 32     | [[CPU vectors\|Interrupt vectors]]                                                     |

### Size
An SNES ROM file follows a set of rules:
- There is an optional 512 byte copier header
- ROM Data will consist of 32K or 64K banks
- The ROM does not need to be a power of two in size, but should be the sum of powers of 2.
- Example: a 3MB ROM might be: 2MB + 1MB + 512 or 2MB + 1MB

### Refs
- SNESDev Wiki
  - [ROM File Formats](https://snes.nesdev.org/wiki/ROM_file_formats)
  - [ROM Header](https://snes.nesdev.org/wiki/ROM_header)
  - [Memory Map](https://snes.nesdev.org/wiki/Memory_map)

## GBA Roms

### Refs
- [GBA Rom Format](http://problemkaputt.de/gbatek-gba-cartridge-header.htm)