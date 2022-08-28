'''Implementation of snk40: SNK 40th Anniversary Collection'''
import glob
import logging
import os
from gex.lib.utils.blob import transforms
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class SNK40thAnniversaryCollectionTask(BaseTask):
    '''Implements snk40: SNK 40th Anniversary Collection'''
    _task_name = "snk40"
    _title = "SNK 40th Anniversary Collection"
    _details_markdown = '''
Based on https://gitlab.com/vaiski/romextract/-/blob/master/scripts/STEAM-865940.sh

 **Game**                                         | **System**     | **Filename**           | **Notes**           
---------------------------------------------|---------------|--------------------|-------------  
Alpha Mission                         | NES        | ASO.nes              |            
Alpha Mission                         | NES        | ASO_jp.nes           |            
Athena                                | NES        | Athena.nes           |            
Athena                                | NES        | Athena_jp.nes        |            
Crystalis                             | NES        | Crystalis.nes        |            
Crystalis                             | NES        | Crystalis_jp.nes     |            
Guerrilla War                         | NES        | GuerrillaWar.nes     |            
Guerrilla War                         | NES        | GuerrillaWar_jp.nes  |            
Ikari Warriors                        | NES        | Ikari.nes            |            
Ikari Warriors                        | NES        | Ikari_jp.nes         |            
Ikari II: Victory Road                | NES        | Ikari2.nes           |            
Ikari II: Victory Road                | NES        | Ikari2_jp.nes        |            
Ikari III: The Rescue                 | NES        | Ikari3.nes           |            
Ikari III: The Rescue                 | NES        | Ikari3_jp.nes        |            
P.O.W                                 | NES        | POW.nes              |            
P.O.W                                 | NES        | POW_jp.nes           |            
Beast Busters                         | Arcade     | bbusters.zip         | (3)           
Beast Busters                         | Arcade     | bbustersj.zip        | (3)           
Beast Busters                         | Arcade     | bbustersu.zip        | (3)           
Search and Rescue                     | Arcade     | searchar.zip         |            
Search and Rescue                     | Arcade     | searcharj.zip        |            
Search and Rescue                     | Arcade     | searcharu.zip        |            
Iron Tank                             | Arcade     | IronTank.nes         |            
Iron Tank                             | Arcade     | IronTank_jp.nes      |            
Prehistoric Isle                      | Arcade     | gensitou.zip         |            
Prehistoric Isle                      | Arcade     | prehisle.zip         |            
Prehistoric Isle                      | Arcade     | prehisleu.zip        |            
Street Smart                          | Arcade     | streetsm.zip         |            
Street Smart                          | Arcade     | streetsm1.zip        |            
Street Smart                          | Arcade     | streetsmj.zip        |            
Street Smart                          | Arcade     | streetsmw.zip        |            
Ikari III: The Rescue                 | Arcade     | ikari3.zip           |            
Ikari III: The Rescue                 | Arcade     | ikari3j.zip          |            
Ikari III: The Rescue                 | Arcade     | ikari3k.zip          |            
Ikari III: The Rescue                 | Arcade     | ikari3u.zip          |            
P.O.W                                 | Arcade     | pow.zip              |            
P.O.W                                 | Arcade     | powj.zip             |            
Vanguard                              | Arcade     | vanguard.zip         |            
Vanguard                              | Arcade     | vanguardc.zip        |            
Vanguard                              | Arcade     | vanguardj.zip        |            
Chopper I                             | Arcade     | chopperb.zip         |            
Chopper I                             | Arcade     | legofair.zip         | (3)           
Fantasy                               | Arcade     | fantasyj.zip         |            
Fantasy                               | Arcade     | fantasyu.zip         |            
Time Soldiers                         | Arcade     | btlfield.zip         | (3)           
Time Soldiers                         | Arcade     | timesold.zip         | (3)           
Munch Mobile (Joyful Road)            | Arcade     | joyfulr.zip          |            
Munch Mobile (Joyful Road)            | Arcade     | mnchmobl.zip         |            
Sasuke vs. Commander                  | Arcade     | sasuke.zip           |            
Ozma Wars                             | Arcade     | ozmawars.zip         | (2)  
Paddle Mania                          | Arcade     | paddlema.zip         | (2)  
ASO ArmoredScrumObject                | Arcade     | N/A                  | (1)  
Guerilla War                          | Arcade     | N/A                  | (1)  
Psycho Soldier                        | Arcade     | N/A                  | (1)    
TNKIII                                | Arcade     | N/A                  | (1)    
Ikari I                               | Arcade     | N/A                  | (1)    
Ikari 2 Victory Road                  | Arcade     | N/A                  | (1)    
Bermuda Triangle / World Wars         | Arcade     | N/A                  | (1)     
MarvinsMaze                           | Arcade     | N/A                  | (1)    
Athena                                | Arcade     | N/A                  | (1)    

(1) This is not extracted as there are missing files, such as Missing PROMs.
(2) This is playable, but is a bad dump or has a bad CRC.
(3) This requires MAME 0.139 to play.

    '''
    _default_input_folder = r"C:\Program Files (x86)\Amazon Games\Library\SNK 40th Anniversary Collection"
    _input_folder_desc = "SNK 40th install folder"
    _short_description = ""

    def execute(self, in_dir, out_dir):
        bundle_files = self._find_files(in_dir)
        for file_path in bundle_files:
            with open(file_path, 'rb') as in_file:
                file_name = os.path.basename(file_path)
                pkg_name = self._pkg_name_map.get(file_name)
                if pkg_name is not None:
                    logger.info(f'Reading files for {file_name}...')
                    contents = in_file.read()
                    reader = BPListReader(contents)
                    parsed = reader.parse()

                    handler_func = self.find_handler_func(pkg_name)
                    if parsed is not None and handler_func is not None:
                        output_files = handler_func(parsed)
                        for out_file_entry in output_files:
                            out_path = os.path.join(out_dir, out_file_entry['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(out_file_entry['contents'])
                    elif parsed is None:
                        logger.warning("Could not find merged rom data in mbundle.")
                    elif handler_func is None:
                        logger.warning("Could not find matching handler function.")
                else:
                    logger.info(f'Skipping {file_name} as it contains no known roms...')
        logger.info("Processing complete.")

    _pkg_name_map = {
        'bundleMain.mbundle': 'main',
        'bundleDLC1.mbundle': 'dlc',
        'bundlePatch1.mbundle': 'patch'
    }

    def _find_files(self, base_path):
        bundle_path = os.path.join(base_path, "Bundle", '*.mbundle')
        archive_list = glob.glob(bundle_path)
        return archive_list

    def _handle_main(self, mbundle_entries):
        out_files = []
        for key, value in mbundle_entries.items():
            if key.endswith(".nes"):
                logger.info(f"Extracting {key}...")
                out_files.append({'filename': key, 'contents': value})

        out_files.extend(self._handle_prehisle(mbundle_entries))
        out_files.extend(self._handle_streetsm(mbundle_entries))
        out_files.extend(self._handle_ikari3(mbundle_entries))
        out_files.extend(self._handle_vanguard(mbundle_entries))
        out_files.extend(self._handle_pow(mbundle_entries))

        return out_files

    def _handle_prehisle(self, mbundle_entries):
        # PREHISLE Common
        func_map = {}
        out_files = []
        func_map['z80'] = helpers.name_file_helper("PrehistoricIsleIn1930.z80", "gt1.1")
        func_map['tx'] = helpers.name_file_helper("PrehistoricIsleIn1930.w.alpha.rom", "gt15.b15")
        func_map['bgrom'] = helpers.name_file_helper("PrehistoricIsleIn1930.bg.rom", "pi8914.b14")
        func_map['fgrom'] = helpers.name_file_helper("PrehistoricIsleIn1930.fg.rom", "pi8916.h16")
        sprite_file_map = {
            "pi8910.k14": 524288,
            "gt5.5": 131072
        }
        func_map['sprites'] = helpers.custom_split_helper(
            "PrehistoricIsleIn1930.sprites.rom", sprite_file_map)
        func_map['bgmap'] = helpers.name_file_helper("PrehistoricIsleIn1930.bg.map", "gt11.11")
        func_map['samples'] = helpers.name_file_helper("PrehistoricIsleIn1930.samples", "gt4.4")
        logger.info("Processing PREHISLE common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        def prehisle_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return maincpu

        # GENSITOU / PREHISLEJ
        func_map = {}
        maincpu_filenames = [
            "gt-j2.2h",
            "gt-j3.3h"
        ]
        func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.j.68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "gensitou.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # PREHISLEU
        func_map = {}
        maincpu_filenames = [
            "gt-u2.2h",
            "gt-u3.3h"
        ]
        func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.u.68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "prehisleu.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # PREHISLE
        func_map = {}
        maincpu_filenames = [
            "gt-e2.2h",
            "gt-e3.3h"
        ]
        func_map['maincpu'] = prehisle_maincpu('PrehistoricIsleIn1930.w.68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "prehisle.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_streetsm(self, mbundle_entries):
        # STREETS Common
        func_map = {}
        out_files = []
        func_map['soundcpu'] = helpers.name_file_helper("streetsm.soundcpu", "s2-5.16c")
        func_map['upd'] = helpers.name_file_helper("streetsm.upd", "s2-6.18d")
        def streets_gfx2(in_file_name, filenames):
            def gfx2(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, 7)
                del chunks[3] # Middle element is junk
                return dict(zip(filenames, chunks))
            return gfx2
        gfx2_filenames = [
            "stsmart.900",
            "stsmart.902",
            "stsmart.904",
            "stsmart.901",
            "stsmart.903",
            "stsmart.905",
        ]
        func_map['gfx2'] = streets_gfx2('streetsm.gfx2', gfx2_filenames)

        logger.info("Processing STREETS common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # STREETS1 GFX Common
        func_map = {}
        gfx1_filenames = [
            "s2-7.15l",
            "s2-8.15m"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('streetsm1.gfx1', gfx1_filenames)
        logger.info("Processing STREETS1 GFX common files...")
        gfx1_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        def streets_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return maincpu

        # STREETSM
        func_map = {}
        maincpu_filenames = [
            "s2-1ver2.14h",
            "s2-2ver2.14k"
        ]
        func_map['maincpu'] = streets_maincpu('streetsm.maincpu', maincpu_filenames)
        gfx1_filenames = [
            "s2-9.25l",
            "s2-10.25m"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('streetsm.gfx1', gfx1_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "streetsm.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # STREETSM1
        func_map = {}
        maincpu_filenames = [
            "s2-1ver1.9c",
            "s2-2ver1.10c"
        ]
        func_map['maincpu'] = streets_maincpu('streetsm1.maincpu', maincpu_filenames)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "streetsm1.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # STREETSMJ
        func_map = {}
        maincpu_filenames = [
            "s2v1j_01.bin",
            "s2v1j_02.bin"
        ]
        func_map['maincpu'] = streets_maincpu('streetsmj.maincpu', maincpu_filenames)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "streetsmj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # STREETSMW
        func_map = {}
        maincpu_filenames = [
            "s-smart1.bin",
            "s-smart2.bin"
        ]
        func_map['maincpu'] = streets_maincpu('streetsmw.maincpu', maincpu_filenames)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "streetsmw.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_ikari3(self, mbundle_entries):
        # IKARI3 Common
        func_map = {}
        out_files = []
        func_map['upd'] = helpers.name_file_helper("ikari3.upd", "ik3-6.18e")
        user_filenames = [
	        "ik3-1.c8",
	        "ik3-4.c12"
        ]
        func_map['user'] = helpers.deinterleave_helper('ikari3.user1',
            user_filenames, num_ways=2, word_size=1)

        logger.info("Processing IKARI3 common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # IKARI3 GFX1 Common
        func_map = {}
        gfx1_filenames = [
	        "ik3-7.16l",
	        "ik3-8.16m"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('ikari3.gfx1', gfx1_filenames)
        logger.info("Processing IKARI3 GFX1 common files...")
        gfx1_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # IKARI3 GFX2 Common
        func_map = {}
        gfx2_filenames = [
	        "ik3-23.bin",
	        "ik3-13.bin",
	        "ik3-22.bin",
	        "ik3-12.bin",
	        "ik3-21.bin",
	        "ik3-11.bin",
	        "ik3-20.bin",
	        "ik3-10.bin",
	        "ik3-19.bin",
	        "ik3-9.bin",
	        "ik3-14.bin",
	        "ik3-24.bin",
	        "ik3-15.bin",
	        "ik3-25.bin",
	        "ik3-16.bin",
	        "ik3-26.bin",
	        "ik3-17.bin",
	        "ik3-27.bin",
	        "ik3-18.bin",
	        "ik3-28.bin"
        ]
        def ikari3_gfx2_common(in_file_name, filenames):
            def gfx2(in_files):
                contents = in_files[in_file_name]
                contents = transforms.splice_out(contents, start = 1310720, end = 2097152)
                chunks = transforms.equal_split(contents, 10)
                chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return gfx2
        func_map['gfx2'] = ikari3_gfx2_common('ikari3.gfx2', gfx2_filenames)
        logger.info("Processing IKARI3 GFX2 common files...")
        gfx2_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # IKARI3
        func_map = {}
        maincpu_filenames = [
            "ik3-2-ver1.c10",
            "ik3-3-ver1.c9"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('ikari3.maincpu',
            maincpu_filenames, num_ways=2, word_size=1)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
        func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ikari3.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # IKARI3J
        func_map = {}
        maincpu_filenames = [
            "ik3-2-j.c10",
            "ik3-3-j.c9"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('ikari3j.maincpu',
            maincpu_filenames, num_ways=2, word_size=1)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
        func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ikari3j.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # IKARI3K
        func_map = {}
        maincpu_filenames = [
            "ik3-2k.c10",
            "ik3-3k.c9"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('ikari3k.maincpu',
            maincpu_filenames, num_ways=2, word_size=1)
        gfx1_filenames = [
            "ik3-7k.16l",
            "ik3-8k.16m"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('ikari3k.gfx1', gfx1_filenames)
        gfx2_filenames = [
	        "ikari-880d_t53.d2",
            "ikari-880c_t54.c2",
            "ik12.d1",
            "ik11.c1",
            "ikari-880d_t52.b2",
            "ikari-880c_t51.a2",
            "ik10.b1",
            "ik9.a1",
        ]
        def ikari3k_gfx2(in_file_name, filenames):
            def gfx2(in_files):
                contents = in_files[in_file_name]
                contents = transforms.splice_out(contents, start = 1310720, end = 2097152)
                chunks = transforms.custom_split(contents,
                    [1024*1024, 1024*256, 1024*1024, 1024*256])
                chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return gfx2
        func_map['gfx2'] = ikari3k_gfx2('ikari3.gfx2', gfx2_filenames)
        func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.16d")
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ikari3k.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # IKARI3U
        func_map = {}
        maincpu_filenames = [
            "ik3-2.c10",
            "ik3-3.c9"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('ikari3u.maincpu',
            maincpu_filenames, num_ways=2, word_size=1)
        func_map['gfx1'] = helpers.existing_files_helper(gfx1_file_map)
        func_map['gfx2'] = helpers.existing_files_helper(gfx2_file_map)
        func_map['soundcpu'] = helpers.name_file_helper("ikari3.soundcpu", "ik3-5.15d")
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ikari3u.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_vanguard(self, mbundle_entries):
        # VANGUARD Common
        func_map = {}
        out_files = []

        gfx1_filenames = [
	        "sk5_ic50.bin",
	        "sk5_ic51.bin"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('vanguard.gfx1', gfx1_filenames)

        prom_filenames = [
	        "sk5_ic7.bin",
	        "sk5_ic6.bin"
        ]
        func_map['prom'] = helpers.equal_split_helper('vanguard.proms', prom_filenames)

        snk6502_filenames = [
	        "sk4_ic51.bin",
	        "sk4_ic52.bin"
        ]
        func_map['snk6502'] = helpers.equal_split_helper('vanguard.snk6502', snk6502_filenames)

        speech_file_names = [
            "sk6_ic07.bin",
            "sk6_ic08.bin",
            "sk6_ic11.bin"
        ]
        def vanguard_speech(in_file_name, filenames):
            def speech(in_files):
                contents = in_files[in_file_name]
                contents = contents[16384:]
                chunks = transforms.equal_split(contents, len(filenames))
                return dict(zip(filenames, chunks))
            return speech
        func_map['speech'] = vanguard_speech("vanguard.speech", speech_file_names)
        logger.info("Processing VANGUARD common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # VANGUARD
        func_map = {}
        maincpu_filenames = [
	        "sk4_ic07.bin",
	        "sk4_ic08.bin",
	        "sk4_ic09.bin",
	        "sk4_ic10.bin",
	        "sk4_ic13.bin",
	        "sk4_ic14.bin",
	        "sk4_ic15.bin",
	        "sk4_ic16.bin"
        ]
        func_map['maincpu'] = helpers.equal_split_helper('vanguard.maincpu', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "vanguard.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # VANGUARDC
        func_map = {}
        maincpu_filenames = [
	        "sk4_ic07.bin",
	        "sk4_ic08.bin",
	        "sk4_ic09.bin",
	        "4",
	        "5",
	        "sk4_ic14.bin",
	        "sk4_ic15.bin",
	        "8"
        ]
        func_map['maincpu'] = helpers.equal_split_helper('vanguardc.maincpu', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "vanguardc.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # VANGUARDJ
        func_map = {}
        maincpu_filenames = [
	        "sk4_ic07.bin",
	        "sk4_ic08.bin",
	        "sk4_ic09.bin",
	        "vgj4ic10.bin",
	        "vgj5ic13.bin",
	        "sk4_ic14.bin",
	        "sk4_ic15.bin",
	        "sk4_ic16.bin"
        ]
        func_map['maincpu'] = helpers.equal_split_helper('vanguardj.maincpu', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "vanguardj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_pow(self, mbundle_entries):
        # POW Common
        func_map = {}
        out_files = []

        gfx1_filenames = [
            "dg9.l25",
            "dg10.m25"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('pow.gfx1', gfx1_filenames)

        func_map['soundcpu'] = helpers.name_file_helper('pow.soundcpu', 'dg8.e25')
        func_map['upd'] = helpers.name_file_helper('pow.upd', 'dg7.d20')
        func_map['plds'] = helpers.name_file_helper('pow.plds', 'pal20l10.a6')

        gfx2_file_names = [
            "snk88011a.1a",
            "snk88015a.2a",
            "snk88012a.1b",
            "snk88016a.2b",
            "snk88013a.1c",
            "snk88017a.2c",
            "snk88014a.1d",
            "snk88018a.2d",
            "snk88019a.3a",
            "snk88023a.4a",
            "snk88020a.3b",
            "snk88024a.4b",
            "snk88021a.3c",
            "snk88025a.4c",
            "snk88022a.3d",
            "snk88026a.4d"
        ]
        def pow_gfx2_common(in_file_name, filenames):
            def gfx2(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, 8)
                chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return gfx2
        func_map['gfx2'] = pow_gfx2_common('pow.gfx2', gfx2_file_names)
        logger.info("Processing POW common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # POW
        func_map = {}
        maincpu_filenames = [
            "dg1ver1.j14",
            "dg2ver1.l14"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('pow.maincpu', maincpu_filenames, 2, 1)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "pow.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # POWJ
        func_map = {}
        maincpu_filenames = [
            "1-2",
            "2-2"
        ]
        func_map['maincpu'] = helpers.deinterleave_helper('powj.maincpu', maincpu_filenames, 2, 1)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "powj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _gfx_split_swap(self, in_file_ref, filenames):
        '''Func map helper for transforms.equal_split'''
        def split(in_files):
            contents = in_files[in_file_ref]
            chunks = transforms.equal_split(contents, num_chunks = len(filenames))
            chunks = transforms.swap_endian_all(chunks)
            return dict(zip(filenames, chunks))
        return split

    def _handle_dlc(self, mbundle_entries):
        out_files = []

        out_files.extend(self._handle_bbusters(mbundle_entries))
        out_files.extend(self._handle_searchar(mbundle_entries))

        return out_files

    def _handle_bbusters(self, mbundle_entries):
        # bbusters commons
        func_map = {}
        out_files = []
        func_map['gfx1'] = helpers.name_file_helper('bbusters.gfx1', 'bb-10.l9')
        gfx2_filenames = [
            "bb-f11.m16",
            "bb-f12.m13",
            "bb-f13.m12",
            "bb-f14.m11"
        ]
        func_map['gfx2'] = self._gfx_split_swap('bbusters.gfx2', gfx2_filenames)
        gfx3_filenames = [
            "bb-f21.l10",
            "bb-f22.l12",
            "bb-f23.l13",
            "bb-f24.l15"
        ]
        func_map['gfx3'] = self._gfx_split_swap('bbusters.gfx3', gfx3_filenames)
        func_map['gfx4'] = helpers.name_file_helper('bbusters.gfx4', 'bb-back1.m4')
        func_map['gfx5'] = helpers.name_file_helper('bbusters.gfx5', 'bb-back2.m6')
        func_map['scale_table1'] = helpers.name_file_helper('bbusters.scale_table', 'bb-6.e7')
        func_map['scale_table2'] = helpers.name_file_helper('bbusters.scale_table', 'bb-7.h7')
        func_map['scale_table3'] = helpers.name_file_helper('bbusters.scale_table', 'bb-8.a14')
        func_map['scale_table4'] = helpers.name_file_helper('bbusters.scale_table', 'bb-9.c14')
        func_map['audiocpu'] = helpers.name_file_helper('bbusters.audiocpu', 'bb-1.e6')
        func_map['ymsnd'] = helpers.name_file_helper('bbusters.ymsnd', 'bb-pcma.l5')

        logger.info("Processing bbusters common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # bbusters
        func_map = {}
        maincpu_filenames = [
            "bb-3.k10",
            "bb-5.k12",
            "bb-2.k8",
            "bb-4.k11"
        ]
        def bbusters_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 2)

                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
                chunks = new_chunks

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = bbusters_maincpu('bbusters.maincpu', maincpu_filenames)
        func_map['ymsnd.deltat'] = helpers.name_file_helper('bbusters.ymsnd.deltat', 'bb-pcmb.l3')
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "bbusters.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # bbustersj
        func_map = {}
        maincpu_filenames = [
            "bb3_ver2_j3.k10",
            "bb5_ver2_j3.k12",
            "bb-2.k8",
            "bb-4.k11"
        ]
        func_map['maincpu'] = bbusters_maincpu('bbustersj.maincpu', maincpu_filenames)
        func_map['ymsnd.deltat'] = helpers.name_file_helper('bbusters.ymsnd.deltat', 'bb-pcmb.l3')
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "bbustersj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # bbustersu
        func_map = {}
        maincpu_filenames = [
            "bb-ver3-u3.k10",
            "bb-ver3-u5.k12",
            "bb-2.k8",
            "bb-4.k11"
        ]
        func_map['maincpu'] = bbusters_maincpu('bbustersu.maincpu', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "bbustersu.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_searchar(self, mbundle_entries):
        # searchar common
        func_map = {}
        out_files = []
        func_map['soundcpu'] = helpers.name_file_helper('searchar.soundcpu', 'bh.5')
        gfx1_filenames = [
            "bh.7",
            "bh.8"
        ]
        func_map['gfx1'] = helpers.equal_split_helper("searchar.gfx1", gfx1_filenames)
        gfx2_filenames = [
            "bh.c1",
            "bh.c3",
            "bh.c5",
            "bh.c2",
            "bh.c4",
            "bh.c6"
        ]
        def searchar_gfx2(in_file_name, filenames):
            def gfx2(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, 7)
                del chunks[3] # Middle element is junk
                return dict(zip(filenames, chunks))
            return gfx2
        func_map['gfx2'] = searchar_gfx2("searchar.gfx2", gfx2_filenames)
        func_map['upd'] = helpers.name_file_helper('searchar.upd', 'bh.v1')

        logger.info("Processing searchar common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # searchar
        func_map = {}
        maincpu_filenames = [
            "bhw.2",
            "bhw.3"
        ]
        def searchar_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = searchar_maincpu('searchar.maincpu', maincpu_filenames)
        user_filenames = [
            "bhw.1",
            "bhw.4"
        ]
        func_map['user1'] = searchar_maincpu('searchar.user1', user_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "searchar.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # searcharj
        func_map = {}
        maincpu_filenames = [
            "bh2ver3j.9c",
            "bh3ver3j.10c"
        ]
        func_map['maincpu'] = searchar_maincpu('searcharj.maincpu', maincpu_filenames)
        user_filenames = [
            "bhw.1",
            "bhw.4"
        ]
        func_map['user1'] = searchar_maincpu('searchar.user1', user_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "searcharj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # searcharu
        func_map = {}
        maincpu_filenames = [
            "bh.2",
            "bh.3"
        ]
        func_map['maincpu'] = searchar_maincpu('searcharu.maincpu', maincpu_filenames)
        user_filenames = [
            "bh.1",
            "bh.4"
        ]
        func_map['user1'] = searchar_maincpu('searcharu.user1', user_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "searcharu.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")
        return out_files

    def _handle_patch(self, mbundle_entries):
        out_files = []
        out_files.extend(self._handle_chopper(mbundle_entries))
        out_files.extend(self._handle_fantasy(mbundle_entries))
        out_files.extend(self._handle_timesoldiers(mbundle_entries))
        out_files.extend(self._handle_munchmobile(mbundle_entries))
        out_files.extend(self._handle_sasuke(mbundle_entries))
        out_files.extend(self._handle_ozmawars(mbundle_entries))
        out_files.extend(self._handle_paddlemania(mbundle_entries))
        return out_files

    def _handle_chopper(self, mbundle_entries):
        out_files = []

        # CHOPPERB
        func_map = {}
        func_map['maincpu'] = helpers.name_file_helper("chopper.maincpu", "kk1.8g")
        func_map['sub'] = helpers.name_file_helper("chopper.sub", "kk4.6g")
        prom_file_names = [
	        "1.9w",
	        "3.9u",
	        "2.9v"
        ]
        func_map['prom'] = helpers.equal_split_helper("chopper.proms", prom_file_names)
        func_map['audiocpu'] = helpers.name_file_helper("chopper.audiocpu", "kk3.3d")
        func_map['tx'] = helpers.name_file_helper("chopper.tx_tiles", "kk5.8p")
        bg_file_names = [
	        "kk10.8y",
	        "kk11.8z",
	        "kk12.8ab",
	        "kk13.8ac"
        ]
        func_map['bg'] = helpers.equal_split_helper("chopper.bg_tiles", bg_file_names)
        sp16_file_names = [
	        "kk9.3k",
	        "kk8.3l",
	        "kk7.3n",
	        "kk6.3p"
        ]
        func_map['sp16'] = helpers.equal_split_helper("chopper.sp16_tiles", sp16_file_names)
        sp32_file_names = [
	        "kk18.3ab",
	        "kk19.2ad",
	        "kk20.3y",
	        "kk21.3aa",
	        "kk14.3v",
	        "kk15.3x",
	        "kk16.3s",
	        "kk17.3t"
        ]
        func_map['sp32'] = helpers.equal_split_helper("chopper.sp32_tiles", sp32_file_names)
        func_map['ym2'] = helpers.name_file_helper("chopper.ym2", "kk2.3j")
        func_map['plds'] = helpers.name_file_helper("chopper.plds", "p-a1.2c")
        mame_name = "chopperb.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # LEGOFAIR
        func_map = {}
        func_map['maincpu'] = helpers.name_file_helper("legofair.maincpu", "kk1.4m")
        func_map['sub'] = helpers.name_file_helper("legofair.sub", "kk4.8m")
        prom_file_names = [
	        "1.1k",
	        "2.1l",
	        "3.2k"
        ]
        func_map['prom'] = helpers.equal_split_helper("chopper.proms", prom_file_names)
        func_map['audiocpu'] = helpers.name_file_helper("chopper.audiocpu", "kk3.6j")
        func_map['tx'] = helpers.name_file_helper("chopper.tx_tiles", "kk5.3a")
        bg_file_names = [
	        "kk10.1a",
	        "kk11.1b",
	        "kk12.1d",
	        "kk13.1e"
        ]
        func_map['bg'] = helpers.equal_split_helper("chopper.bg_tiles", bg_file_names)
        sp16_file_names = [
	        "kk9.3g",
	        "kk8.3e",
	        "kk7.3d",
	        "kk6.3b"
        ]
        func_map['sp16'] = helpers.equal_split_helper("chopper.sp16_tiles", sp16_file_names)
        sp32_file_names = [
	        "kk18.8m",
	        "kk19.8n",
	        "kk20.8p",
	        "kk21.8s",
	        "kk14.7p",
	        "kk15.7s",
	        "kk16.8j",
	        "kk17.8k"
        ]
        func_map['sp32'] = helpers.equal_split_helper("chopper.sp32_tiles", sp32_file_names)
        func_map['ym2'] = helpers.name_file_helper("chopper.ym2", "kk2.5b")
        func_map['plds'] = helpers.name_file_helper("chopper.plds", "p-a1.8b")
        mame_name = "legofair.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_fantasy(self, mbundle_entries):
        out_files = []
        # COMMON
        func_map = {}
        gfx1_file_names = [
	        "fs10ic50.bin",
	        "fs11ic51.bin"
        ]
        func_map['gfx1'] = helpers.equal_split_helper("fantasyu.gfx1", gfx1_file_names)
        snk6502_file_names = [
	        "fs_b_51.bin",
	        "fs_a_52.bin",
	        "fs_c_53.bin"
        ]
        func_map['snk6502'] = helpers.equal_split_helper("fantasyu.snk6502", snk6502_file_names)
        speech_file_names = [
	        "fs_d_7.bin",
	        "fs_e_8.bin",
	        "fs_f_11.bin"
        ]
        func_map['speech'] = helpers.equal_split_helper("fantasyu.speech", speech_file_names)
        logger.info("Processing fantasy common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # FANTASYJ
        func_map = {}
        prom_file_names = [
	        "prom-8.bpr",
	        "prom-7.bpr"
        ]
        func_map['prom'] = helpers.equal_split_helper("fantasyj.proms", prom_file_names)
        maincpu_file_names = [
	        "fs5jic12.bin",
	        "fs1jic7.bin",
	        "fs2jic8.bin",
	        "fs3jic9.bin",
	        "fs4jic10.bin",
	        "fs6jic14.bin",
	        "fs7jic15.bin",
	        "fs8jic16.bin",
	        "fs9jic17.bin"
        ]
        func_map['maincpu'] = helpers.equal_split_helper("fantasyj.maincpu", maincpu_file_names)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "fantasyj.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # FANTASYU
        func_map = {}
        prom_file_names = [
	        "fantasy.ic7",
	        "fantasy.ic6"
        ]
        func_map['prom'] = helpers.equal_split_helper("fantasyu.proms", prom_file_names)
        maincpu_file_names = [
	        "ic12.cpu",
	        "ic07.cpu",
	        "ic08.cpu",
	        "ic09.cpu",
	        "ic10.cpu",
	        "ic14.cpu",
	        "ic15.cpu",
	        "ic16.cpu",
	        "ic17.cpu"
        ]
        func_map['maincpu'] = helpers.equal_split_helper("fantasyu.maincpu", maincpu_file_names)

        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "fantasyu.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_timesoldiers(self, mbundle_entries):
        out_files = []

        # Common
        func_map = {}
        z80_file_names = [
            "bf.7",
            "bf.8",
            "bf.9"
        ]
        func_map['z80'] = helpers.equal_split_helper("TimeSoldiers.z80", z80_file_names)
        gfx2_file_names = [
            "bf.10",
            "bf.14",
            "bf.18",
            "bf.11",
            "bf.15",
            "bf.19",
            "bf.12",
            "bf.16",
            "bf.20",
            "bf.13",
            "bf.17",
            "bf.21"
        ]
        def timesold_gfx2(in_file_name, filenames):
            def process(in_files):
                contents = in_files[in_file_name]
                contents = transforms.splice_out(contents, start=15*131072, length=131072)
                contents = transforms.splice_out(contents, start=11*131072, length=131072)
                contents = transforms.splice_out(contents, start=7*131072, length=131072)
                contents = transforms.splice_out(contents, start=3*131072, length=131072)
                chunks = transforms.equal_split(contents, len(filenames))
                return dict(zip(filenames, chunks))
            return process
        func_map['gfx2'] = timesold_gfx2("TimeSoldiers.gfx2.rom", gfx2_file_names)

        logger.info("Processing timesold common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)


        def timesold_maincpu_common(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, 2)
                chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return maincpu

        # TIMESOLD
        func_map = {}
        maincpu_file_names = [
            "bf.3",
            "bf.4",
            "bf.1",
            "bf.2"
        ]
        func_map['maincpu'] = timesold_maincpu_common("TimeSoldiers.3.68k", maincpu_file_names)
        gfx1_file_names = [
            "bf.6",
            "bf.5"
        ]
        func_map['gfx1'] = helpers.deinterleave_helper("TimeSoldiers.u.gfx1.rom",
            gfx1_file_names, num_ways=2, word_size=1)
        func_map['common'] = helpers.existing_files_helper(common_file_map)

        mame_name = "timesold.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # BTLFIELD
        func_map = {}
        maincpu_file_names = [
            "bfv1_03.bin",
            "bfv1_04.bin",
            "bf.1",
            "bf.2"
        ]
        func_map['maincpu'] = timesold_maincpu_common("TimeSoldiers.j.68k", maincpu_file_names)
        gfx1_file_names = [
            "bfv1_06.bin",
            "bfv1_05.bin"
        ]
        func_map['gfx1'] = helpers.deinterleave_helper("TimeSoldiers.j.gfx1.rom",
            gfx1_file_names, num_ways=2, word_size=1)
        func_map['common'] = helpers.existing_files_helper(common_file_map)

        mame_name = "btlfield.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_munchmobile(self, mbundle_entries):
        out_files = []

        # Common
        func_map = {}
        func_map['audiocpu'] = helpers.name_file_helper("joyfulr.audiocpu", "mu.2j")
        func_map['proms'] = helpers.name_file_helper("joyfulr.proms", "a2001.clr")
        gfx1_file_names = [
            "s1.10a",
            "s2.10b"
        ]
        func_map['gfx1'] = helpers.equal_split_helper("joyfulr.gfx1", gfx1_file_names)
        gfx2_file_names = [
            "b1.2c",
            "b2.2b"
        ]
        func_map['gfx2'] = helpers.equal_split_helper("joyfulr.gfx2", gfx2_file_names)
        func_map['gfx4'] = helpers.name_file_helper("joyfulr.gfx4", "h")

        logger.info("Processing joyfulr common files...")
        common_file_map = helpers.process_rom_files(mbundle_entries, func_map)

        # JOYFULR
        func_map = {}
        maincpu_file_names = [
            "m1j.10e",
            "m2j.10d"
        ]
        func_map['maincpu'] = helpers.equal_split_helper("joyfulr.maincpu", maincpu_file_names)
        gfx3_file_names = [
            "f1j.1g",
            "f2j.3g",
            "f3j.5g"
        ]
        func_map['gfx3'] = helpers.equal_split_helper("joyfulr.gfx3", gfx3_file_names)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "joyfulr.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # MNCHMOBL
        func_map = {}
        maincpu_file_names = [
            "m1.10e",
            "m2.10d"
        ]
        func_map['maincpu'] = helpers.equal_split_helper("mnchmobl.maincpu", maincpu_file_names)
        gfx3_file_names = [
            "f1.1g",
            "f2.3g",
            "f3.5g"
        ]
        func_map['gfx3'] = helpers.equal_split_helper("mnchmobl.gfx3", gfx3_file_names)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "mnchmobl.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_sasuke(self, mbundle_entries):
        out_files = []

        func_map = {}
        maincpu_file_names = [
            "sc1",
            "sc2",
            "sc3",
            "sc4",
            "sc5",
            "sc6",
            "sc7",
            "sc8",
            "sc9",
            "sc10"
        ]
        func_map['maincpu'] = helpers.equal_split_helper('sasuke.maincpu', maincpu_file_names)
        gfx1_file_names = [
            "mcs_c",
            "mcs_d"
        ]
        func_map['gfx1'] = helpers.equal_split_helper('sasuke.gfx1', gfx1_file_names)
        func_map['proms'] = helpers.name_file_helper("sasuke.proms", "sasuke.clr")
        func_map['snk6502'] = helpers.name_file_helper("sasuke.snk6502", "sc11")

        mame_name = "sasuke.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_ozmawars(self, mbundle_entries):
        out_files = []

        func_map = {}
        maincpu_file_names = [
            "mw01",
            "mw02",
            "mw03",
            "mw04",
            "mw05",
            "mw06"
        ]
        def ozmawars_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                contents = transforms.splice_out(contents, start = 8192, end = 16384)
                chunks = transforms.equal_split(contents, len(filenames))
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['gfx2'] = ozmawars_maincpu("ozmawars.maincpu", maincpu_file_names)
        prom_file_names = [
            "01.1",
            "02.2"
        ]
        func_map['prom'] = helpers.equal_split_helper('moonbase.proms', prom_file_names)
        mame_name = "ozmawars.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files

    def _handle_paddlemania(self, mbundle_entries):
        func_map = {}

        prom_file_map = {
            "padlem.a": 0x100,
            "padlem.b": 0x100,
            "padlem.c": 0x100,
	        "padlem.17j": 0x400,
	        "padlem.16j": 0x400
        }
        func_map['prom'] = helpers.custom_split_helper('PaddleMania.proms.rom', prom_file_map)
        func_map['audiocpu'] = helpers.name_file_helper('PaddleMania.z80', 'padlem.18c')
        func_map['color_prom'] = helpers.name_file_helper('PaddleMania.clut.rom', 'padlem.18n')
        maincpu_file_names = [
	        "padlem.6g",
	        "padlem.3g",
	        "padlem.6h",
	        "padlem.3h"
        ]
        def padlem_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, len(filenames) // 2)
                chunks = transforms.deinterleave_all(chunks, num_ways=2, word_size=1)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = padlem_maincpu('PaddleMania.1.68k', maincpu_file_names)
        gfx1_file_names = [
            "padlem.9m",
	        "padlem.16m",
	        "padlem.9n",
	        "padlem.16n",
	        "padlem.6m",
	        "padlem.13m",
	        "padlem.6n",
	        "padlem.13n"
        ]
        func_map['gfx1'] = padlem_maincpu('PaddleMania.gfx1.rom', gfx1_file_names)
        mame_name = "paddlema.zip"
        logger.info(f"Building {mame_name}...")
        out_files = []
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(mbundle_entries, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        return out_files
