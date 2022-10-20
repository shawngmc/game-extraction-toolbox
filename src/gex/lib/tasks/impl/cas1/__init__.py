'''INCOMPLETE Implementation of cas1: Capcom Arcade Stadium 1'''
import glob
import logging
import os

from gex.lib.archive import kpka
from gex.lib.tasks import helpers
from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

# TODO: Further research required

class CAS1Task(BaseTask):
    '''INCOMPLETE Implements cas1: Capcom Arcade Stadium 1'''
    _task_name = 'cas1'
    _title = "Capcom Arcade Stadium 1"
    _details_markdown = '''
## INCOMPLETE!

This script is a placeholder for full CAS1 extraction. See https://github.com/shawngmc/game-extraction-toolbox/issues/18 for latest details!

Currently, it extracts nothing; however, with a "--prop include-partials=True", it will extract all KPKA paks with the following naming convention:
[ARCHIVEID]_[SEQUENTIALNUM]_[SIZE].dat
These are not playable ROMs!

## Analysis
### KPKA
These appear to be KPKA archives, and it is reasonably certain that the extraction is correct, as most files have a 3-4 character allcaps header
indicating file type. Note that the file order can differ between KPKA files; the size and header bytes are best used for identification.

### File Types
It's more effective to actually categorize the files.

#### ROM Data (New Only)
 - Has no header
 - Large (very similar to the extracted ZIP file sizes, but slightly smaller - perhaps diff compression)
 - 1-2 per PAK (typically 2, but only 1 if the game didn't have a US release)
 - Is this an encrypted version of the PKZIP file?

#### Very Small MMAC
 - MMAC Header
 - Always 26 bytes
 - 1-2 per PAK (does not necessarily match the number of ROM Data packages)

#### Moderate MMAC
 - MMAC Header
 - Typically a couple K in size

#### 'MAME' file
 - MAME header
 - Typically less than 1K
 - Some internal paths, some also mention DSW1/DSW2 - could these be DIP Switches?
 - Like a MAME engine config file for the ROM, to tell it MAME driver name, etc.?

#### SCN
 - SCN Header
 - Typically less than 1K
 - RE Engine Scene Description?
 - Has paths for other related files

#### PSB
 - '.psb' header
 - Always 331 bytes
 - CAS1 - all PSBs are the same
 - CAS2 - no per-pak PSB, 1 in the main archive
 - CAS1 and CAS2 a little different
   - 0x31-0x35 - 5 bytes
   - 0x3A-0x46 - 13 bytes
   - 0x6F-0x82 - 20 bytes
   - 38/331 bytes - about 11%

#### PKZIP (Old Depot Only)
 - 'PK' Header
 - Appears to be a standard ZIP file with the ROM

##### Diff vs. M2 PSB
In the example above, 1556708_1_331.dat appears to have ".psb" at the beginning; however, this doesn't match what we know about the PSB filetype.
 - If this was an uncompressed PSB file, we would expect the first three bytes to be "PSB"
 - If this were a compressed PSB file, we would expect the first three bytes to be a compression type indicator, like "mdf"
 - We have no current indication M2 (which makes the m2engage emulator and MArchive file format) worked on CAS
 - MArchiveBatchTool can't seem to do anything with the file.
 - The file is far shorter than most PSB files.
As such, 'PSB' is likely a coincidence or other dead end.
For CAS1, every '.psb' file is identical. CAS2 does not have these '.psb' files (at least in the per-DLC packages). 
However, there is a '.psb' file in the main package (look for the 331 byte file size/file 1888).
It is definitely different than the CAS1 PSB, but only about 30% of the file is changed. (0x30-0x47, 0x6F-0x81)

### Examples
#### Example 1 -  (1556708)
 - 1556708_0_1957557.dat - One of the ROM packages
 - 1556708_1_331.dat - has '.psb' at the beginning, but does not appear to be a valid M2 MArchive/PSB Archive
 - 1556708_2_1976307.dat - One of the ROM packages
 - 1556708_3_150.dat - Small MAME file describing ROM name?
 - 1556708_4_138.dat - Small file of null bytes
 - 1556708_5_667.dat - SCN file - Scene description?
 - 1556708_6_3828.dat - Moderate MMAC file listing ROM file names and possible keys?
 - 1556708_7_26.dat - Very small MMAC file

#### Example 2 - 1556700 (Vulgus)
| Old                | New                 | Info                                                            | 
|--------------------|---------------------|-----------------------------------------------------------------| 
| 1_346.dat          | 1_346.dat           | MAME file; both 346 bytes, identical, for 'vulgus', has DSWs    | 
| 6_134.dat          | 7_134.dat           | MAME file; both 134 bytes, identical, for 'vulgusj'             | 
| 4_26.dat           | 5_26.dat            | Very Small MMAC; Both 26 bytes, 1 byte diff (0x08)              | 
| 0_14.dat           | 0_26.dat            | Very Small MMAC; 14 vs 26 bytes                                 | 
| 5_655.dat          | 6_655.dat           | SCN file; Both 655 bytes, identical                             | 
| N/A                | 3_331.dat           | '.psb' file; only in new                                        | 
| 2_71436.dat        | 2_70421.dat         | PK vs ??? file, guessing via size and orig this is vulgusj      | 
| 3_71071.dat        | 4_70123.dat         | PK vs ??? file, guessing via size and orig this is vulgus       | 
    '''
    _out_file_list = [
    ]

    _out_file_notes = {
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("Capcom Arcade Stadium")
    _input_folder_desc = "CAS 1 Folder"
    _prop_info = {
        "include-partials": {
            "description": "Include the partial ROMs that are missing data; useful for mixing with other sources or investigation",
            "default": False,
            "type": "Boolean"
        }
    }

    def _find_files(self, in_path):
        return glob.glob(os.path.join(in_path, "**", "*.pak"), recursive=True)

    def execute(self, in_dir, out_dir):
        
        if self._props.get('include-partials'):
            pak_files = self._find_files(in_dir)
            for file in pak_files:
                file_id = None
                filename = os.path.basename(file)
                if "patch" in filename:
                    # logger.info(f"Skipping patch file {filename}")
                    file_id = "patch"
                elif filename == "re_chunk_000.pak":
                    file_id = "chunk"
                else:
                    file_id = file.split(".")[0].split("_")[-1]

                logger.info(f"Extracting {file}: {file_id}")
                try:
                    with open(file, "rb") as curr_file:
                        file_content = bytearray(curr_file.read())
                        kpka_contents = kpka.extract(file_content)
                        output_files = []

                        for kpka_contents in kpka_contents.values():
                            print(f"{kpka_contents['entry']}: {kpka_contents['size']}")
                            output_files.append({'filename': f"{file_id}_{kpka_contents['entry']}_{kpka_contents['size']}.dat", "contents": kpka_contents['contents']})

                        for output_file in output_files:
                            out_path = os.path.join(out_dir, output_file['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(output_file['contents'])
                except OSError as error:
                    logger.warning(f'Error while processing {file}!')
                    logger.warning(error)
        else:
            logger.error("CAS1 is not yet implemented; to help investigate, add --prop 'include-partials=True' to extract what we have so far!")

        logger.info("Processing complete.")
