'''Implementation of sf30ac: Street Fighter 30th Anniversary Collection'''
import glob
import logging
import os
from gex.lib.utils.blob import transforms
from gex.lib.utils.vendor import capcom
from gex.lib.contrib.bputil import BPListReader
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

# TODO: Split class into a few smaller classes
# TODO: Add extraction of incomplete roms

logger = logging.getLogger('gextoolbox')

class SF30ACTask(BaseTask):
    '''Implements sf30ac: Street Fighter 30th Anniversary Collection'''
    _task_name = "sf30ac"
    _title = "Street Fighter 30th Anniversary Collection"
    _details_markdown = '''
This is reverse-engineered based on:
- The Japanese shell scripts in https://web.archive.org/web/20220213232038/http://blog.livedoor.jp/scrap_a/archives/22823395.html
- Valad Amoleo's https://github.com/ValadAmoleo/sf30ac-extractor/

Beyond the usual QSound dl-1425.bin and decryption keys, some of the CRC matches appear to be modified VROMs. The extraction is correct - 90%+ of the ROM matches - but details appear to be changed.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below.

Note that this does NOT extract the Japanese ROMs as those are only included in SF30AC International Edition. As a US player, I can't get them - I've tried!
'''

    _out_file_list = [
        {
            "game": "Street Fighter 2 (U)",
            "system": "Arcade",
            "filename": "sf2ub.zip",
            "status": "playable",
            "notes": [2, 3]
        },
        {
            "game": "Street Fighter 2 Championship Edition (U)",
            "system": "Arcade",
            "filename": "sf2ceua.zip",
            "status": "playable",
            "notes": [2, 3]
        },
        {
            "game": "Street Fighter 2 Hyper Fighting (U)",
            "system": "Arcade",
            "filename": "sf2t.zip",
            "status": "playable",
            "notes": [2, 3]
        },
        {
            "game": "Super Street Fighter 2 (U)",
            "system": "Arcade",
            "filename": "ssf2u.zip",
            "status": "playable",
            "notes": [1, 3]
        },
        {
            "game": "Super Street Fighter 2 Turbo (U)",
            "system": "Arcade",
            "filename": "ssf2tu.zip",
            "status": "playable",
            "notes": [1, 3]
        },
        {
            "game": "Street Fighter (W)",
            "system": "Arcade",
            "filename": "sf.zip",
            "status": "playable",
            "notes": []
        },
        {
            "game": "Street Fighter (J)",
            "system": "Arcade",
            "filename": "sfj.zip",
            "status": "playable",
            "notes": [4]
        },
        {
            "game": "Street Fighter 3",
            "system": "Arcade",
            "filename": "sfiiina.zip",
            "status": "good",
            "notes": []
        },
        {
            "game": "Street Fighter 3: 2nd Impact",
            "system": "Arcade",
            "filename": "sfiii2n.zip",
            "status": "good",
            "notes": []
        },
        {
            "game": "Street Fighter 3: 3rd Strike",
            "system": "Arcade",
            "filename": "sfiii3nr1.zip",
            "status": "good",
            "notes": []
        },
        {
            "game": "Street Fighter 2 (JA)",
            "system": "Arcade",
            "filename": "sf2ja.zip",
            "status": "playable",
            "notes": [2, 3, 4]
        },
        {
            "game": "Street Fighter 2 (JL)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [2, 3, 4, 5]
        },
        {
            "game": "Street Fighter 2 Championship Edition (JB)",
            "system": "Arcade",
            "filename": "sf2cejb.zip",
            "status": "playable",
            "notes": [2, 3, 4]
        },
        {
            "game": "Street Fighter 2 Championship Edition (JC)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [2, 3, 4, 5]
        },
        {
            "game": "Street Fighter 2 Hyper Fighting (J)",
            "system": "Arcade",
            "filename": "sf2tj.zip",
            "status": "playable",
            "notes": [2, 3, 4]
        },
        {
            "game": "Street Fighter Alpha (U)",
            "system": "Arcade",
            "filename": "sfau.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Street Fighter Alpha (J)",
            "system": "Arcade",
            "filename": "sfzj.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Street Fighter Alpha (JR2)",
            "system": "Arcade",
            "filename": "sfzjr2.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Street Fighter Alpha 2 (U)",
            "system": "Arcade",
            "filename": "sfa2u.zip",
            "status": "playable",
            "notes": [1, 3]
        },
        {
            "game": "Street Fighter Alpha 2 (J)",
            "system": "Arcade",
            "filename": "sfz2j.zip",
            "status": "playable",
            "notes": [1, 3, 4]
        },
        {
            "game": "Street Fighter Alpha 2 (JR1)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [1, 3, 4, 5]
        },
        {
            "game": "Street Fighter Alpha 3 (J)",
            "system": "Arcade",
            "filename": "sfz3j.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Street Fighter Alpha 3 (JR2)",
            "system": "Arcade",
            "filename": "sfz3jr2.zip",
            "status": "playable",
            "notes": [1, 4]
        },
        {
            "game": "Street Fighter Alpha 3 (U)",
            "system": "Arcade",
            "filename": "sfa3u.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Super Street Fighter 2 (J)",
            "system": "Arcade",
            "filename": "ssf2.zip",
            "status": "playable",
            "notes": [1, 3, 4]
        },
        {
            "game": "Super Street Fighter 2 (JR1)",
            "system": "Arcade",
            "filename": "ssf2u.zip",
            "status": "playable",
            "notes": [1, 3, 4]
        },
        {
            "game": "Super Street Fighter 2 Turbo (J)",
            "system": "Arcade",
            "filename": "ssf2tu.zip",
            "status": "playable",
            "notes": [1, 3, 4]
        },
        {
            "game": "Super Street Fighter 2 Turbo (JR1)",
            "system": "Arcade",
            "filename": "N/A",
            "status": "no-rom",
            "notes": [1, 3, 4, 5]
        }
    ]
    _out_file_notes = {
        "1": "These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). "\
            "This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require.",
        "2": "These ROMs require an older version MAME. They test fine in MAME 0.78 (Mame 2003 in RetroArch). "\
            "This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require.",
        "3": "These are using an older naming convention to allow recognition by the targeted MAME version.",
        "4": "These ROMs are only present if your Street Fighter 30th Anniversary Collection says it is 'International'.",
        "5": "This ROM is not extracted as no known emulators can play it as is due to the missing key and being a newer post-MAME2010 split."
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("Street Fighter 30th Anniversary Collection")
    _input_folder_desc = "SF30AC Steam folder"

    _pkg_name_map = {
        'bundleStreetFighter.mbundle': 'sf',
        'bundleStreetFighterAlpha.mbundle': 'sfa',
        'bundleStreetFighterAlpha2.mbundle': 'sfa2',
        'bundleStreetFighterAlpha3.mbundle': 'sfa3',
        'bundleStreetFighterII.mbundle': 'sf2',
        'bundleStreetFighterIII.mbundle': 'sf3',
        'bundleStreetFighterIII_2ndImpact.mbundle': 'sf3_2i',
        'bundleStreetFighterIII_3rdStrike.mbundle': 'sf3_3s',
        'bundleStreetFighterII_CE.mbundle': 'sf2ce',
        'bundleStreetFighterII_HF.mbundle': 'sf2hf',
        'bundleSuperStreetFighterII.mbundle': 'ssf2',
        'bundleSuperStreetFighterIITurbo.mbundle': 'ssf2t'
    }
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

    def _find_files(self, base_path):
        bundle_path = os.path.join(base_path, "Bundle", '*.mbundle')
        archive_list = glob.glob(bundle_path)
        return archive_list

    def _process_simm_common(self, simm_id, simm_prefix, simm_size_bytes):
        def process_simm(in_files):
            contents = in_files[simm_id]
            num_chunks = len(contents)//simm_size_bytes
            filenames = list(map(lambda x:f'{simm_prefix}-{simm_id}.{x}', range(0,num_chunks)))
            chunks = transforms.equal_split(contents, chunk_size = simm_size_bytes)
            return dict(zip(filenames, chunks))
        return process_simm

    def _deshuffle_gfx_common(self, filenames, num_interim_split, final_split = None):
        def gfx(in_files):
            contents = in_files['vrom']

            # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
            contents = capcom.common_gfx_deshuffle(contents)

            # Split into even chunks
            chunks = transforms.equal_split(contents, num_chunks=num_interim_split)

            # Interleave each pair of chunks
            new_chunks = []
            for oddchunk,evenchunk in zip(chunks[0::2], chunks[1::2]):
                new_chunks.append(transforms.interleave([oddchunk, evenchunk], word_size=8))
            chunks = new_chunks

            # Merge the chunks back together
            contents = transforms.merge(chunks)

            # Deinterleave the chunks into our 4 files
            chunks = transforms.deinterleave(contents, num_ways = 4, word_size=2)

            # Do final split if provided
            if final_split:
                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(transforms.custom_split(oldchunk, final_split))
                chunks = new_chunks

            return dict(zip(filenames, chunks))
        return gfx

    def _cps2_gfx_deinterleave(self, contents, num_ways=4, word_size=2):
        interleave_group_length = num_ways * word_size
        num_interleave_groups = len(contents)//interleave_group_length
        contents = capcom.common_gfx_deshuffle(contents)
        temp_chunks = [bytearray() for i in range(num_ways)]
        for i in range(0, num_interleave_groups):
            offset = i * interleave_group_length
            interleave_group = contents[offset:offset+interleave_group_length]
            interleave_offset = 0
            for j in range(0, num_ways):
                interleave_end = interleave_offset + word_size
                temp_chunks[j] += interleave_group[interleave_offset:interleave_end]
                interleave_offset = interleave_end
        return temp_chunks

    ################################################################################
    # Street Fighter                                                               #
    ################################################################################

    def _handle_sf(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['z80'] = mbundle_entries.get("StreetFighter.z80")
        in_files['alpha'] = mbundle_entries.get("StreetFighter.alpha.rom")
        in_files['68k'] = mbundle_entries.get("StreetFighter.u.68k")
        in_files['sprites'] = mbundle_entries.get("StreetFighter.sprites.rom")
        in_files['samples'] = mbundle_entries.get("StreetFighter.u.samples.rom")
        in_files['maps'] = mbundle_entries.get("StreetFighter.maps.rom")
        in_files['bplanes'] = mbundle_entries.get("StreetFighter.bplanes.rom")
        in_files['mplanes'] = mbundle_entries.get("StreetFighter.mplanes.rom")

        in_files['j-samples'] = mbundle_entries.get("StreetFighter.j.samples.rom")
        in_files['j-68k'] = mbundle_entries.get("StreetFighter.j.68k")

        bplanes_filenames = [
            "sf-39.2k",
            "sf-38.1k",
            "sf-41.4k",
            "sf-40.3k"
        ]
        func_map['bplanes'] = helpers.equal_split_helper('bplanes', bplanes_filenames)

        mplanes_filenames = [
            "sf-25.1d",
            "sf-28.1e",
            "sf-30.1g",
            "sf-34.1h",
            "sf-26.2d",
            "sf-29.2e",
            "sf-31.2g",
            "sf-35.2h"
        ]
        func_map['mplanes'] = helpers.equal_split_helper('mplanes', mplanes_filenames)

        sprites_filenames = [
            "sf-15.1m",
            "sf-16.2m",
            "sf-11.1k",
            "sf-12.2k",
            "sf-07.1h",
            "sf-08.2h",
            "sf-03.1f",
            "sf-17.3m",
            "sf-18.4m",
            "sf-13.3k",
            "sf-14.4k",
            "sf-09.3h",
            "sf-10.4h",
            "sf-05.3f"
        ]
        func_map['sprites'] = helpers.equal_split_helper('sprites', sprites_filenames)

        func_map['alpha'] = helpers.name_file_helper("alpha", "sf-27.4d")

        maps_filenames = [
            "sf-37.4h",
            "sf-36.3h",
            "sf-32.3g",
            "sf-33.4g"
        ]
        func_map['maps'] = helpers.equal_split_helper('maps', maps_filenames)

        func_map['z80'] = helpers.name_file_helper("z80", "sf-02.7k")

        logger.info("Processing SF common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        samples_filenames = [
            "sfu-00.1h",
            "sf-01.1k"
        ]
        func_map['samples'] = helpers.equal_split_helper('samples', samples_filenames)
        maincpu_filenames = [
            "sfd-19.2a",
            "sfd-22.2c",
            "sfd-20.3a",
            "sfd-23.3c",
            "sfd-21.4a",
            "sfd-24.4c"
        ]
        def sf_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 3)

                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
                chunks = new_chunks

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sf_maincpu('68k', maincpu_filenames)
        ph_files = {
            'mb7114h.12k': 0x100,
            'mb7114h.11h': 0x100,
            'mb7114h.12j': 0x100,
            'mmi-7603.13h': 0x020,
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sf.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # See if the J ROM is present
        if in_files['j-68k'] is not None and in_files['j-samples'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map['maincpu'] = sf_maincpu('j-68k', maincpu_filenames)
            samples_filenames_j = [
                "sf-00.1h",
                "sf-01.1k"
            ]
            func_map['samples'] = helpers.equal_split_helper('j-samples', samples_filenames_j)
            ph_files_j = {
                'mb7114h.12j': 0x100,
                'sfb00.bin': 0x100,
                'sfb05.bin': 0x100,
                'mmi-7603.13h': 0x020,
                'sf_s.id8751h-8.14f': 0x1000
            }
            func_map['placeholders'] = helpers.placeholder_helper(ph_files_j)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name = "sfj.zip"
            logger.info(f"Building {mame_name}...")
            out_files.append(
                {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name}.")
        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files

    ################################################################################
    #  Street Fighter 2                                                            #
    ################################################################################

    def _handle_sf2(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterII.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterII.z80')
        in_files['oki'] = mbundle_entries.get('StreetFighterII.oki')
        in_files['ub68k'] = mbundle_entries.get('StreetFighterII.ub.68k')
        in_files['ja-68k'] = mbundle_entries.get('StreetFighterII.ja.68k')
        in_files['jl-68k'] = mbundle_entries.get('StreetFighterII.jl.68k')

        # audiocpu
        audiocpu_filenames = [
            "sf2_9.12a"
        ]
        def audiocpu(in_files):
            contents = in_files['z80']
            return dict(zip(audiocpu_filenames, [contents]))
        func_map['audiocpu'] = audiocpu

        # gfx
        gfx_filenames = [
            "sf2_06.bin",
            "sf2_08.bin",
            "sf2_05.bin",
            "sf2_07.bin",
            "sf2_15.bin",
            "sf2_17.bin",
            "sf2_14.bin",
            "sf2_16.bin",
            "sf2_25.bin",
            "sf2_27.bin",
            "sf2_24.bin",
            "sf2_26.bin"
        ]
        def gfx(in_files):
            contents = in_files['vrom']
            chunks = transforms.equal_split(contents, num_chunks=3)

            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(self._cps2_gfx_deinterleave(oldchunk, num_ways=4, word_size=2))
            chunks = new_chunks
            return dict(zip(gfx_filenames, chunks))
        func_map['gfx'] = gfx

        # oki
        oki_filenames = [
            'sf2_18.11c',
            'sf2_19.12c'
        ]
        def oki(in_files):
            chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
            return dict(zip(oki_filenames, chunks))
        func_map['oki'] = oki

        ph_files = {
            'buf1': 0x117,
            'c632.ic1': 0x117,
            'ioa1': 0x117,
            'iob1.11d': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'stf29.1a': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        logger.info("Processing SF2 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        # maincpu
        maincpu_filenames = [
            'sf2_30a.bin',
            'sf2u.37b',
            'sf2_31a.bin',
            'sf2_38a.bin',
            'sf2_28a.bin',
            'sf2_35a.bin',
            'sf2_29a.bin',
            'sf2_36a.bin'
        ]
        def sf2_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 4)

                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(transforms.deinterleave(oldchunk, num_ways=2, word_size=1))
                chunks = new_chunks

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sf2_maincpu('ub68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sf2ub.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")


        # See if the J ROM is present
        if in_files['ja-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames_ja = [
                'sf2j_30a.11e',
                'sf2u.37b',
                'sf2_31a.bin',
                'sf2_38a.bin',
                'sf2_28a.bin',
                'sf2_35a.bin',
                'sf2_29a.bin',
                'sf2_36a.bin'
            ]
            func_map['maincpu'] = sf2_maincpu('ja-68k', maincpu_filenames_ja)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_ja = 'sf2ja.zip'
            logger.info(f"Building {mame_name_ja}...")
            out_files.append(
                {'filename': mame_name_ja, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_ja}.")

            logger.info("Skipping sf2jl.zip as it needs a key but isn't in an old keyless MAME.")
        else:
            logger.info("Japanese ROMs not found, skipping.")


        return out_files

    ################################################################################
    # Street Fighter Alpha                                                         #
    ################################################################################

    def _handle_sfa(self, mbundle_entries):
        out_files = []
        func_map = {}
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterAlpha.z80')
        in_files['qs'] = mbundle_entries.get('StreetFighterAlpha.qs')
        in_files['nv'] = mbundle_entries.get('StreetFighterAlpha.nv')
        in_files['u-68k'] = mbundle_entries.get('StreetFighterAlpha.u.68k')
        in_files['j-68k'] = mbundle_entries.get('StreetFighterAlpha.j.68k')
        in_files['jr2-68k'] = mbundle_entries.get('StreetFighterAlpha.jr2.68k')

        #vrom
        vrom_filenames = [
            "sfz.14m",
            "sfz.16m",
            "sfz.18m",
            "sfz.20m",
        ]
        func_map['vrom'] = self._deshuffle_gfx_common(vrom_filenames, 8)


        # z80
        z80_filenames = [
            'sfz.01',
            'sfz.02'
        ]
        def z80(in_files):
            chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
            return dict(zip(z80_filenames, chunks))
        func_map['z80'] = z80

        # qsound
        qsound_filenames = [
            'sfz.11m',
            'sfz.12m'
        ]
        def qsound(in_files):
            chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            return dict(zip(qsound_filenames, chunks))
        func_map['qsound'] = qsound

        logger.info("Processing SFA1 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)


        # maincpu
        maincpu_filenames = [
            'sfzu.03a',
            'sfz.04a',
            'sfz.05a',
            'sfz.06'
        ]
        def sfa_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                contents = transforms.swap_endian(contents)
                chunks = transforms.equal_split(contents, num_chunks = 4)

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sfa_maincpu('u-68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sfau.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # See if the J ROM is present
        if in_files['j-68k'] is not None and in_files['jr2-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames_j = [
                'sfzj.03c',
                'sfz.04b',
                'sfz.05a',
                'sfz.06'
            ]
            func_map['maincpu'] = sfa_maincpu('j-68k', maincpu_filenames_j)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_j = 'sfzj.zip'
            logger.info(f"Building {mame_name_j}...")
            out_files.append(
                {'filename': mame_name_j, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_j}.")

            func_map = {}
            maincpu_filenames_jr2 = [
                'sfzj.03b',
                'sfz.04a',
                'sfz.05a',
                'sfz.06'
            ]
            func_map['maincpu'] = sfa_maincpu('jr2-68k', maincpu_filenames_jr2)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_jr2 = 'sfzjr2.zip'
            logger.info(f"Building {mame_name_jr2}...")
            out_files.append(
                {'filename': mame_name_jr2, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_jr2}.")

        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files

    ################################################################################
    # Street Fighter Alpha 2                                                       #
    ################################################################################

    def _handle_sfa2(self, mbundle_entries):
        out_files = []
        func_map = {}
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha2.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterAlpha2.z80')
        in_files['qs'] = mbundle_entries.get('StreetFighterAlpha2.qs')
        in_files['u168k'] = mbundle_entries.get('StreetFighterAlpha2.u1.68k')
        in_files['j-68k'] = mbundle_entries.get('StreetFighterAlpha2.j.68k')
        in_files['jr1-68k'] = mbundle_entries.get('StreetFighterAlpha2.jr1.68k')

        vrom_filenames = [
            "sz2.13m",
            "sz2.14m",
            "sz2.15m",
            "sz2.16m",
            "sz2.17m",
            "sz2.18m",
            "sz2.19m",
            "sz2.20m"
        ]
        func_map['vrom'] = self._deshuffle_gfx_common(
            vrom_filenames,
            20,
            final_split = [0x400000, 0x100000]
        )

        # z80
        z80_filenames = [
            'sz2.01a',
            'sz2.02a'
        ]
        def z80(in_files):
            chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
            return dict(zip(z80_filenames, chunks))
        func_map['z80'] = z80

        # qsound
        qsound_filenames = [
            'sz2.11m',
            'sz2.12m'
        ]
        def qsound(in_files):
            chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            return dict(zip(qsound_filenames, chunks))
        func_map['qsound'] = qsound

        logger.info("Processing SFA2 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        maincpu_filenames = [
            "sz2u.03",
            "sz2u.04",
            "sz2u.05",
            "sz2u.06",
            "sz2u.07",
            "sz2u.08"
        ]
        def sfa2_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                contents = transforms.swap_endian(contents)
                chunks = transforms.equal_split(contents, num_chunks = 6)

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sfa2_maincpu('u168k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sfa2u.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # See if the J ROM is present
        if in_files['j-68k'] is not None and in_files['jr1-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames_j = [
                "sz2j.03a",
                "sz2j.04a",
                "sz2.05a",
                "sz2.06",
                "sz2j.07a",
                "sz2.08"
            ]
            func_map['maincpu'] = sfa2_maincpu('j-68k', maincpu_filenames_j)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_j = 'sfz2j.zip'
            logger.info(f"Building {mame_name_j}...")
            out_files.append(
                {'filename': mame_name_j, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_j}.")

            logger.info("Skipping sfz2jr1.zip as it needs a key but isn't in an old keyless MAME.")

        else:
            logger.info("Japanese ROMs not found, skipping.")


        return out_files

    ################################################################################
    # Street Fighter Alpha 3                                                       #
    ################################################################################

    def _handle_sfa3(self, mbundle_entries):
        out_files = []
        func_map = {}
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterAlpha3.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterAlpha3.z80')
        in_files['qs'] = mbundle_entries.get('StreetFighterAlpha3.qs')

        in_files['u68k'] = mbundle_entries.get('StreetFighterAlpha3.u.68k')

        in_files['j-68k'] = mbundle_entries.get('StreetFighterAlpha3.j.68k')
        in_files['jr2-68k'] = mbundle_entries.get('StreetFighterAlpha3.jr2.68k')

        vrom_filenames = [
            "sz3.13m",
            "sz3.14m",
            "sz3.15m",
            "sz3.16m",
            "sz3.17m",
            "sz3.18m",
            "sz3.19m",
            "sz3.20m"
        ]
        func_map['vrom'] = self._deshuffle_gfx_common(
            vrom_filenames,
            32,
            final_split = [0x400000, 0x400000]
        )

        # z80
        z80_filenames = [
            'sz3.01',
            'sz3.02'
        ]
        def z80(in_files):
            chunks = transforms.equal_split(in_files['z80'], num_chunks=2)
            return dict(zip(z80_filenames, chunks))
        func_map['z80'] = z80

        # qsound
        qsound_filenames = [
            'sz3.11m',
            'sz3.12m'
        ]
        def qsound(in_files):
            chunks = transforms.equal_split(in_files['qs'], num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            return dict(zip(qsound_filenames, chunks))
        func_map['qsound'] = qsound

        logger.info("Processing SFA3 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)


        func_map = {}
        maincpu_filenames = [
            "sz3u.03c",
            "sz3u.04c",
            "sz3.05c",
            "sz3.06c",
            "sz3.07c",
            "sz3.08c",
            "sz3.09c",
            "sz3.10b"
        ]
        def sfa3_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                contents = transforms.swap_endian(contents)
                chunks = transforms.equal_split(contents, num_chunks = 8)

                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sfa3_maincpu('u68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sfa3u.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        # See if the J ROM is present
        if in_files['j-68k'] is not None and in_files['jr2-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames_j = [
                "sz3j.03c",
                "sz3j.04c",
                "sz3.05c",
                "sz3.06c",
                "sz3.07c",
                "sz3.08c",
                "sz3.09c",
                "sz3.10b"
            ]
            func_map['maincpu'] = sfa3_maincpu('j-68k', maincpu_filenames_j)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_j = 'sfz3j.zip'
            logger.info(f"Building {mame_name_j}...")
            out_files.append(
                {'filename': mame_name_j, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_j}.")

            func_map = {}
            maincpu_filenames_jr2 = [
                "sz3j.03",
                "sz3j.04",
                "sz3.05",
                "sz3.06",
                "sz3.07",
                "sz3.08",
                "sz3.09",
                "sz3.10"
            ]
            func_map['maincpu'] = sfa3_maincpu('jr2-68k', maincpu_filenames_jr2)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_jr2 = 'sfz3jr2.zip'
            logger.info(f"Building {mame_name_jr2}...")
            out_files.append(
                {'filename': mame_name_jr2, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_jr2}.")

        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files

    ################################################################################
    # Street Fighter 3                                                             #
    ################################################################################

    def _sf3_common(self, mbundle_entries, in_bios_filename, in_simm_bank_files, simm_prefix, bios_filename, mame_name):
        out_files = []
        func_map = {}
        in_files = {}
        simm_size = 2*1024*1024
        for simm_bank_num, simm_filename in in_simm_bank_files.items():
            bank_name = f'simm{simm_bank_num}'
            in_files[bank_name] = mbundle_entries.get(simm_filename)
            func_map[bank_name] = self._process_simm_common(bank_name, simm_prefix, simm_size)

        in_files['bios'] = mbundle_entries.get(in_bios_filename)
        func_map['bios'] = helpers.name_file_helper("bios", bios_filename)

        out_files.append({'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)})

        return out_files

    def _handle_sf3(self, mbundle_entries):
        in_prefix = "StreetFighterIII"
        in_simm_bank_nums = [1, 3, 4, 5]
        in_simm_files = dict(zip(in_simm_bank_nums,
            list(map(lambda x:f'{in_prefix}.s{x}', in_simm_bank_nums))))
        in_bios_file = f'{in_prefix}.bios'
        return self._sf3_common(
            mbundle_entries,
            in_bios_file,
            in_simm_files,
            'sfiii',
            "sfiii_asia_nocd.29f400.u2",
            'sfiiina.zip'
        )

    ################################################################################
    # Street Fighter 3 2nd Impact                                                  #
    ################################################################################

    def _handle_sf3_2i(self, mbundle_entries):
        in_prefix = "StreetFighterIII_2ndImpact"
        in_simm_bank_nums = list(range(1,6))
        in_simm_files = dict(zip(in_simm_bank_nums,
            list(map(lambda x:f'{in_prefix}.s{x}', in_simm_bank_nums))))
        in_bios_file = f'{in_prefix}.bios'
        return self._sf3_common(
            mbundle_entries,
            in_bios_file,
            in_simm_files,
            'sfiii2',
            "sfiii2_asia_nocd.29f400.u2",
            'sfiii2n.zip'
        )

    ################################################################################
    # Street Fighter 3 3rd Strike                                                  #
    ################################################################################

    def _handle_sf3_3s(self, mbundle_entries):
        in_prefix = "StreetFighterIII_3rdStrike"
        in_simm_files = {
            1: f'{in_prefix}.r1.s1',
            2: f'{in_prefix}.r1.s2',
            3: f'{in_prefix}.s3',
            4: f'{in_prefix}.s4',
            5: f'{in_prefix}.s5',
            6: f'{in_prefix}.s6'
        }
        in_bios_file = f'{in_prefix}.bios'
        return self._sf3_common(
            mbundle_entries,
            in_bios_file,
            in_simm_files,
            'sfiii3',
            "sfiii3_japan_nocd.29f400.u2",
            'sfiii3nr1.zip'
        )

    ################################################################################
    # Street Fighter 2 Championship Edition                                        #
    ################################################################################

    def _handle_sf2ce(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterII_CE.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterII_CE.z80')
        in_files['oki'] = mbundle_entries.get('StreetFighterII_CE.oki')
        in_files['68k'] = mbundle_entries.get('StreetFighterII_CE.ua.68k')
        in_files['jb-68k'] = mbundle_entries.get('StreetFighterII_CE.jb.68k')

        # audiocpu
        audiocpu_filenames = [
            "s92_09.bin"
        ]
        def audiocpu(in_files):
            contents = in_files['z80']
            return dict(zip(audiocpu_filenames, [contents]))
        func_map['audiocpu'] = audiocpu

        # gfx
        gfx_filenames = [
            "s92_01.bin",
            "s92_02.bin",
            "s92_03.bin",
            "s92_04.bin",
            "s92_05.bin",
            "s92_06.bin",
            "s92_07.bin",
            "s92_08.bin",
            "s92_10.bin",
            "s92_11.bin",
            "s92_12.bin",
            "s92_13.bin"
        ]
        def gfx(in_files):
            contents = in_files['vrom']
            chunks = transforms.equal_split(contents, num_chunks=3)

            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(self._cps2_gfx_deinterleave(oldchunk, num_ways=4, word_size=2))
            chunks = new_chunks
            return dict(zip(gfx_filenames, chunks))
        func_map['gfx'] = gfx

        # oki
        oki_filenames = [
            's92_18.bin',
            's92_19.bin'
        ]
        def oki(in_files):
            chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
            return dict(zip(oki_filenames, chunks))
        func_map['oki'] = oki

        ph_files = {
            'bprg1.11d': 0x117,
            'buf1': 0x117,
            'c632.ic1': 0x117,
            'ioa1': 0x117,
            'iob1.12d': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'ioc1.ic7': 0x104
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        logger.info("Processing SF2CE common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)


        func_map = {}
        # maincpu
        maincpu_filenames = [
            "s92u-23a",
            "sf2ce.22",
            "s92_21a.bin"
        ]
        def sf2ce_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 3)
                chunks = transforms.swap_endian_all(chunks)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sf2ce_maincpu('68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sf2ceua.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        if in_files['jb-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames_jb = [
                "s92j_23b.bin",
                "s92j_22b.bin",
                "s92_21a.bin"
            ]
            func_map['maincpu'] = sf2ce_maincpu('jb-68k', maincpu_filenames_jb)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_jb = 'sf2cej.zip'
            logger.info(f"Building {mame_name_jb}...")
            out_files.append(
                {'filename': mame_name_jb, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_jb}.")

            logger.info("Skipping sf2ceja.zip as it needs a key but isn't in an old keyless MAME.")
        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files

    ################################################################################
    # Street Fighter 2 Hyper Fighting                                              #
    ################################################################################

    def _handle_sf2hf(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('StreetFighterII_HF.u.vrom')
        in_files['z80'] = mbundle_entries.get('StreetFighterII_HF.z80')
        in_files['oki'] = mbundle_entries.get('StreetFighterII_HF.oki')
        in_files['68k'] = mbundle_entries.get('StreetFighterII_HF.u.68k')
        in_files['j-vrom'] = mbundle_entries.get('StreetFighterII_HF.j.p16.p32.vrom')
        in_files['j-68k'] = mbundle_entries.get('StreetFighterII_HF.j.68k')

        # audiocpu
        audiocpu_filenames = [
            "s92_09.bin"
        ]
        def audiocpu(in_files):
            contents = in_files['z80']
            return dict(zip(audiocpu_filenames, [contents]))
        func_map['audiocpu'] = audiocpu

        # oki
        oki_filenames = [
            's92_18.bin',
            's92_19.bin'
        ]
        def oki(in_files):
            chunks = transforms.equal_split(in_files['oki'], num_chunks=2)
            return dict(zip(oki_filenames, chunks))
        func_map['oki'] = oki

        ph_files = {
            'bprg1.11d': 0x117,
            'buf1': 0x117,
            'c632.ic1': 0x117,
            'ioa1': 0x117,
            'iob1.12d': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'ioc1.ic7': 0x104
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        logger.info("Processing SF2HF common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        # maincpu
        maincpu_filenames = [
            "sf2_23a",
            "sf2_22.bin",
            "sf2_21.bin"
        ]
        def sf2hf_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 3)
                chunks = transforms.swap_endian_all(chunks)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = sf2hf_maincpu('68k', maincpu_filenames)

        # gfx
        gfx_filenames = [
            "s92_01.bin",
            "s92_02.bin",
            "s92_03.bin",
            "s92_04.bin",
            "s92_05.bin",
            "s92_06.bin",
            "s92_07.bin",
            "s92_08.bin",
            "s2t_10.bin",
            "s2t_11.bin",
            "s2t_12.bin",
            "s2t_13.bin"
        ]
        def sf2hf_gfx(in_file_name, filenames):
            def gfx(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks=3)

                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(
                        self._cps2_gfx_deinterleave(oldchunk, num_ways=4, word_size=2)
                    )
                chunks = new_chunks
                return dict(zip(filenames, chunks))
            return gfx
        func_map['gfx'] = sf2hf_gfx('vrom', gfx_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "sf2t.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")

        if in_files['j-68k'] is not None and in_files['j-vrom'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames = [
                "s2tj_23.bin",
                "sft_22.bin",
                "sft_21.bin"
            ]
            func_map['maincpu'] = sf2hf_maincpu('j-68k', maincpu_filenames)
            # gfx
            gfx_filenames = [
                "s92_01.bin",
                "s92_02.bin",
                "s92_03.bin",
                "s92_04.bin",
                "s92_05.bin",
                "s92_06.bin",
                "s92_07.bin",
                "s92_08.bin",
                "s2t_10.bin",
                "s2t_11.bin",
                "s2t_12.bin",
                "s2t_13.bin"
            ]
            func_map['gfx'] = sf2hf_gfx('j-vrom', gfx_filenames)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name_jb = 'sf2tj.zip'
            logger.info(f"Building {mame_name_jb}...")
            out_files.append(
                {'filename': mame_name_jb, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name_jb}.")
        else:
            logger.info("Japanese ROMs not found, skipping.")


        return out_files

    ################################################################################
    # Super Street Fighter 2                                                       #
    ################################################################################

    def _handle_ssf2(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('SuperStreetFighterII.vrom')
        in_files['z80'] = mbundle_entries.get('SuperStreetFighterII.z80')
        in_files['qsound'] = mbundle_entries.get('SuperStreetFighterII.qs')
        in_files['68k'] = mbundle_entries.get('SuperStreetFighterII.u.68k')
        in_files['j-68k'] = mbundle_entries.get('SuperStreetFighterII.j.68k')
        in_files['jr1-68k'] = mbundle_entries.get('SuperStreetFighterII.jr1.68k')

        # audiocpu
        audiocpu_filenames = [
            "ssf.01"
        ]
        def audiocpu(in_files):
            contents = in_files['z80']
            return dict(zip(audiocpu_filenames, [contents]))
        func_map['audiocpu'] = audiocpu


        vrom_filenames = [
            "ssf.13m",
            "ssf.14m",
            "ssf.15m",
            "ssf.16m",
            "ssf.17m",
            "ssf.18m",
            "ssf.19m",
            "ssf.20m"
        ]
        func_map['vrom'] = self._deshuffle_gfx_common(
            vrom_filenames,
            12,
            final_split = [0x200000, 0x100000]
        )

        # qsound
        qsound_filenames = [
            "ssf.q01",
            "ssf.q02",
            "ssf.q03",
            "ssf.q04",
            "ssf.q05",
            "ssf.q06",
            "ssf.q07",
            "ssf.q08"
        ]
        def qsound(in_files):
            chunks = transforms.equal_split(in_files['qsound'], num_chunks=8)
            return dict(zip(qsound_filenames, chunks))
        func_map['qsound'] = qsound

        logger.info("Processing SSF2 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        # maincpu
        maincpu_filenames = [
            "ssfu.03a",
            "ssfu.04a",
            "ssfu.05",
            "ssfu.06",
            "ssfu.07"
        ]
        def ssf2_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = 5)
                chunks = transforms.swap_endian_all(chunks)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = ssf2_maincpu('68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ssf2u.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")


        if in_files['j-68k'] is not None and in_files['jr1-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames = [
                "ssfj.03b",
                "ssfj.04a",
                "ssfj.05",
                "ssfj.06b",
                "ssfj.07"
            ]
            func_map['maincpu'] = ssf2_maincpu('j-68k', maincpu_filenames)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name = 'ssf2j.zip'
            logger.info(f"Building {mame_name}...")
            out_files.append(
                {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name}.")
            func_map = {}
            maincpu_filenames = [
                "ssfj.03a",
                "ssfj.04a",
                "ssfj.05",
                "ssfj.06",
                "ssfj.07"
            ]
            func_map['maincpu'] = ssf2_maincpu('jr1-68k', maincpu_filenames)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name = 'ssf2jr1.zip'
            logger.info(f"Building {mame_name}...")
            out_files.append(
                {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name}.")
        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files

    ################################################################################
    # Super Street Fighter 2 Turbo                                                 #
    ################################################################################

    def _handle_ssf2t(self, mbundle_entries):
        func_map = {}
        out_files = []
        in_files = {}
        in_files['vrom'] = mbundle_entries.get('SuperStreetFighterIITurbo.vrom')
        in_files['z80'] = mbundle_entries.get('SuperStreetFighterIITurbo.z80')
        in_files['qsound'] = mbundle_entries.get('SuperStreetFighterIITurbo.qs')
        in_files['68k'] = mbundle_entries.get('SuperStreetFighterIITurbo.u.68k')
        in_files['j-68k'] = mbundle_entries.get('SuperStreetFighterIITurbo.j.68k')
        in_files['jr1-68k'] = mbundle_entries.get('SuperStreetFighterIITurbo.jr1.68k')

        # audiocpu
        audiocpu_filenames = [
            "sfx.01",
            "sfx.02"
        ]
        def audiocpu(in_files):
            contents = in_files['z80']
            chunks = transforms.equal_split(contents, num_chunks = len(audiocpu_filenames))
            return dict(zip(audiocpu_filenames, chunks))
        func_map['audiocpu'] = audiocpu

        vrom_filenames = [
            "sfx.13m",
            "sfx.14m",
            "sfx.21m",
            "sfx.15m",
            "sfx.16m",
            "sfx.23m",
            "sfx.17m",
            "sfx.18m",
            "sfx.25m",
            "sfx.19m",
            "sfx.20m",
            "sfx.27m"
        ]
        func_map['vrom'] = self._deshuffle_gfx_common(
            vrom_filenames,
            16,
            final_split = [0x200000, 0x100000, 0x100000]
        )

        # qsound
        qsound_filenames = [
            "sfx.11m",
            "sfx.12m",
        ]
        def qsound(in_files):
            chunks = transforms.equal_split(in_files['qsound'], num_chunks=2)
            return dict(zip(qsound_filenames, chunks))
        func_map['qsound'] = qsound

        logger.info("Processing SSFT2 common files...")
        common_file_map = helpers.process_rom_files(in_files, func_map)

        func_map = {}
        # maincpu
        maincpu_filenames = [
            "sfxu.03e",
            "sfxu.04a",
            "sfxu.05",
            "sfxu.06b",
            "sfxu.07a",
            "sfxu.08",
            "sfx.09"
        ]
        def ssf2t_maincpu(in_file_name, filenames):
            def maincpu(in_files):
                contents = in_files[in_file_name]
                chunks = transforms.equal_split(contents, num_chunks = len(maincpu_filenames))
                chunks = transforms.swap_endian_all(chunks)
                return dict(zip(filenames, chunks))
            return maincpu
        func_map['maincpu'] = ssf2t_maincpu('68k', maincpu_filenames)
        func_map['common'] = helpers.existing_files_helper(common_file_map)
        mame_name = "ssf2tu.zip"
        logger.info(f"Building {mame_name}...")
        out_files.append(
            {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
        )
        logger.info(f"Extracted {mame_name}.")


        if in_files['j-68k'] is not None:
            logger.info("Japanese ROMs found, extracting...")
            func_map = {}
            maincpu_filenames = [
                "sfxj.03c",
                "sfxj.04a",
                "sfxj.05",
                "sfxj.06a",
                "sfxj.07",
                "sfxj.08",
                "sfx.09"
            ]
            func_map['maincpu'] = ssf2t_maincpu('j-68k', maincpu_filenames)
            func_map['common'] = helpers.existing_files_helper(common_file_map)
            mame_name = 'ssf2xj.zip'
            logger.info(f"Building {mame_name}...")
            out_files.append(
                {'filename': mame_name, 'contents': helpers.build_rom(in_files, func_map)}
            )
            logger.info(f"Extracted {mame_name}.")

            logger.info("Skipping ssf2xjr1.zip as it needs a key but isn't in an old keyless MAME.")
        else:
            logger.info("Japanese ROMs not found, skipping.")

        return out_files
