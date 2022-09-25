'''Implementation of cbeub: Capcom Beat 'em Up Bundle'''
import re
import glob
import logging
import os

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.utils.blob import transforms
from gex.lib.tasks import helpers

from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class CBEUBTask(BaseTask):
    '''Implements cbeub: Capcom Beat 'em Up Bundle'''
    _task_name = "cbeub"
    _title = "Capcom Beat 'em Up Bundle"
    _details_markdown = '''
The notes I found were at https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.
This script will extract and prep the ROMs. Some per-rom errata are in the notes below.
'''
    _out_file_list = [
        {
            "game": "Final Fight (U)",
            "system": "Arcade",
            "filename": "ffight.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "Final Fight (J)",
            "system": "Arcade",
            "filename": "ffightj.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "King of Dragons (U)",
            "system": "Arcade",
            "filename": "kod.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "King of Dragons (J)",
            "system": "Arcade",
            "filename": "kodf.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "Captain Commando (U)",
            "system": "Arcade",
            "filename": "captcomm.zip",
            "status": "playable",
            "notes": [2, 3]
        },
        {
            "game": "Captain Commando (J)",
            "system": "Arcade",
            "filename": "captcommj.zip",
            "status": "playable",
            "notes": [2, 3]
        },
        {
            "game": "Knights of the Round (U)",
            "system": "Arcade",
            "filename": "knights.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "Knights of the Round (J)",
            "system": "Arcade",
            "filename": "knightsj.zip",
            "status": "playable",
            "notes": [2]
        },
        {
            "game": "Warriors of Fate (U)",
            "system": "Arcade",
            "filename": "wof.zip",
            "status": "playable",
            "notes": [2, 4]
        },
        {
            "game": "Warriors of Fate (J)",
            "system": "Arcade",
            "filename": "wofj.zip",
            "status": "playable",
            "notes": [2, 4]
        },
        {
            "game": "Powered Gear (U)",
            "system": "Arcade",
            "filename": "pgear.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Powered Gear (J)",
            "system": "Arcade",
            "filename": "armwar.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Battle Circuit (U)",
            "system": "Arcade",
            "filename": "batcir.zip",
            "status": "playable",
            "notes": [1]
        },
        {
            "game": "Battle Circuit (J)",
            "system": "Arcade",
            "filename": "batcirj.zip",
            "status": "playable",
            "notes": [1]
        }
    ]

    _out_file_notes = {
        "1": "These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require",
        "2": "These ROMs play fine, even in the current MAME, despite the bad CRCs. The bad CRCs are small ancillary files that aren't strictly required or included, but stubbed out to pass checks. ",
        "3": "The JP version of this ROM is fine in modern MAME 0.246; the English version needs 0.139",
        "4": "The Audio CPU ROM for this is not present in the expected format. Further investigation required."
    }
    _default_input_folder = helpers.gen_steam_app_default_folder("CBEUB")
    _input_folder_desc = "CBEUB Steam folder"

    def execute(self, in_dir, out_dir):
        pak_files = self._find_files(in_dir)
        for file_path in pak_files:
            file_name = os.path.basename(file_path)
            pkg_name = self._pkg_name_map[file_name]
            logger.info(f"Extracting {file_name}: {pkg_name}")
            try:
                with open(file_path, "rb") as curr_file:
                    file_content = bytearray(curr_file.read())
                    arc_contents = arc.extract(file_content)
                    output_files = []

                    # Get the bin entry
                    merged_rom_contents = None
                    for _, arc_content in arc_contents.items():
                        if arc_content['path'].startswith('bin'):
                            merged_rom_contents = arc_content['contents']

                    handler_func = self.find_handler_func(pkg_name)
                    if merged_rom_contents is not None and handler_func is not None:
                        output_files = handler_func(merged_rom_contents)
                        for output_file in output_files:
                            out_path = os.path.join(out_dir, output_file['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(output_file['contents'])
                    elif merged_rom_contents is None:
                        logger.warning(
                            "Could not find merged rom data in arc.")
                    elif handler_func is None:
                        logger.warning(
                            "Could not find matching handler function.")
            except Exception as _:
                logger.warning(f'Error while processing {file_path}!')

        logger.info("Processing complete.")

    _pkg_name_map = {
        "game_00.arc": "ffightj",
        "game_01.arc": "ffight",
        "game_10.arc": "kodj",
        "game_11.arc": "kod",
        "game_20.arc": "captcommj",
        "game_21.arc": "captcomm",
        "game_30.arc": "knightsj",
        "game_31.arc": "knights",
        "game_40.arc": "wofj",
        "game_41.arc": "wof",
        "game_50.arc": "pgear",
        "game_51.arc": "armwar",
        "game_60.arc": "batcirj",
        "game_61.arc": "batcir",
    }

    def _find_files(self, base_path):
        arc_path = os.path.join(base_path, "nativeDX11x64", "arc")
        candidate_files = glob.glob(arc_path + '/game_*.arc')
        archive_list = []
        for candidate in candidate_files:
            if re.search(r'game_\d\d.arc', candidate):
                archive_list.append(candidate)
        return archive_list

    def _deshuffle_gfx_common(self, start, length, filenames, num_deinterleave_split, do_split):
        def gfx(contents):
            # Cut out the section
            contents = contents[start:start + length]

            # This is weird... it's a bit shuffle, not byte-level and not a normal interleave
            bit_order = [
                7, 3, 15, 11, 23, 19, 31, 27,
                6, 2, 14, 10, 22, 18, 30, 26,
                5, 1, 13, 9, 21, 17, 29, 25,
                4, 0, 12, 8, 20, 16, 28, 24,
                39, 35, 47, 43, 55, 51, 63, 59,
                38, 34, 46, 42, 54, 50, 62, 58,
                37, 33, 45, 41, 53, 49, 61, 57,
                36, 32, 44, 40, 52, 48, 60, 56
            ]
            chunks = transforms.split_bit_shuffle(
                contents, word_size_bytes=8, bit_order=bit_order, num_ways=num_deinterleave_split)

            # Split it
            if do_split:
                new_chunks = []
                for oldchunk in chunks:
                    new_chunks.extend(
                        transforms.equal_split(oldchunk, num_chunks=2))
                chunks = new_chunks

            return dict(zip(filenames, chunks))
        return gfx

    def _audio_common(self, start, filenames):
        def audio(contents):
            chunks = []

            # Add the audio CPU
            chunks.append(contents[start:start + 0x8000] +
                          contents[start + 0x10000:start + 0x18000])

            # Add the qsound
            qsound_start = start + 0x18000
            qsound_contents = contents[qsound_start:qsound_start + 0x40000]
            chunks.extend(transforms.equal_split(
                qsound_contents, num_chunks=2))

            return dict(zip(filenames, chunks))
        return audio

    ################################################################################
    # Final Fight                                                                  #
    ################################################################################

    def _handle_ffight(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "ff_42.11h",
            "ffe_43.12h",
            "ff_36.11f",
            "ff_37.12f",
            "ff-32m.8h"
        ]

        def maincpu(contents):
            chunk_5 = contents[0x080040:0x100040]
            contents = contents[0x40:0x080040]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)

            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(
                    transforms.equal_split(oldchunk, num_chunks=2))
            chunks = new_chunks

            # Add 5th non-interleaved chunk
            chunks.append(chunk_5)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "ff-5m.7a",
            "ff-7m.9a",
            "ff-1m.3a",
            "ff-3m.5a"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x200000, gfx_filenames, 4, False)

        audio_filenames = [
            'ff_09.12b',
            'ff_18.11c',
            'ff_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x600040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            's224b.1a': 0x117,
            'iob1.11e': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'ffight.zip', 'contents': zip_contents})

        return out_files

    def _handle_ffightj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "ff42.bin",
            "ff43.bin",
            "ffj_40.10h",
            "ffj_41.11h",
            "ff36.bin",
            "ff37.bin",
            "ffj_34.10f",
            "ffj_35.11f"
        ]

        def maincpu(contents):
            contents = contents[0x40:0x100040]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(
                    transforms.equal_split(oldchunk, num_chunks=4))
            chunks = new_chunks
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "ffj_09.4b",
            "ffj_10.5b",
            "ffj_01.4a",
            "ffj_02.5a",
            "ffj_13.9b",
            "ffj_14.10b",
            "ffj_05.9a",
            "ffj_06.10a",
            "ffj_24.5e",
            "ffj_25.7e",
            "ffj_17.5c",
            "ffj_18.7c",
            "ffj_38.8h",
            "ffj_39.9h",
            "ffj_32.8f",
            "ffj_33.9f"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x200000, gfx_filenames, 8, True)

        audio_filenames = [
            'ff_23.bin',
            'ffj_30.bin',
            'ffj_31.bin'
        ]
        func_map['audio'] = self._audio_common(0x600040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            's222b.1a': 0x117,
            'lwio.12c': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'ffightj.zip', 'contents': zip_contents})
        return out_files

    ################################################################################
    # The King of Dragons                                                          #
    ################################################################################

    def _handle_kod(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "kde_37a.11f",
            "kde_38a.12f",
            "kd_35.9f",
            "kd_36a.10f",
            "kde_30a.11e",
            "kde_31a.12e",
            "kd_28.9e",
            "kd_29.10e"
        ]

        def maincpu(contents):
            contents = contents[0x40:0x100040]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)

            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(
                    transforms.equal_split(oldchunk, num_chunks=4))
            chunks = new_chunks

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "kd-5m.4a",
            "kd-6m.4c",
            "kd-7m.6a",
            "kd-8m.6c",
            "kd-1m.3a",
            "kd-2m.3c",
            "kd-3m.5a",
            "kd-4m.5c"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'kd_9.12a',
            'kd_18.11c',
            'kd_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'kd29b.1a': 0x117,
            'iob1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'kod.zip', 'contents': zip_contents})

        return out_files

    def _handle_kodj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "kdj_37a.11f",
            "kdj_38a.12f",
            "kdj_30a.11e",
            "kdj_31a.12e",
            "kd_33.6f"
        ]

        def maincpu(contents):
            chunk_5 = contents[0x080040:0x100040]
            contents = contents[0x40:0x080040]
            chunks = transforms.deinterleave(contents, num_ways=2, word_size=1)
            new_chunks = []
            for oldchunk in chunks:
                new_chunks.extend(
                    transforms.equal_split(oldchunk, num_chunks=2))
            chunks = new_chunks

            # Add 5th non-interleaved chunk
            chunks.append(chunk_5)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "kd_06.8a",
            "kd_15.8c",
            "kd_08.10a",
            "kd_17.10c",
            "kd_05.7a",
            "kd_14.7c",
            "kd_07.9a",
            "kd_16.9c"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'kd_09.12a',
            'kd_18.11c',
            'kd_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'kd29b.1a': 0x117,
            'iob1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'kodj.zip', 'contents': zip_contents})
        return out_files

    ################################################################################
    # Captain Commando                                                             #
    ################################################################################

    def _handle_captcomm(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "cce_23f.8f",
            "cc_28f.9f",
            "cc_22f.7f",
            "cc_24f.9e"
        ]

        def maincpu(contents):
            # Only the last 2 128k chunks actually need deinterleaved...
            maincpu_area = contents[0x40:0x140040]
            deint_chunks = transforms.deinterleave(
                maincpu_area[0x100000:0x140000], num_ways=2, word_size=1)
            chunks = []
            chunks.append(maincpu_area[0x0:0x80000])
            chunks.append(deint_chunks[0])
            chunks.append(maincpu_area[0x80000:0x100000])
            chunks.append(deint_chunks[1])
            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "cc-5m.3a",
            "cc-6m.7a",
            "cc-7m.5a",
            "cc-8m.9a",
            "cc-1m.4a",
            "cc-2m.8a",
            "cc-3m.6a",
            "cc-4m.10a"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'cc_09.11a',
            'cc_18.11c',
            'cc_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'cc63b.1a': 0x117,
            'iob1.12d': 0x117,
            'ccprg1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632b.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append(
            {'filename': 'captcomm.zip', 'contents': zip_contents}
        )
        return out_files

    def _handle_captcommj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "ccj_23f.8f",
            "ccj_28f.9f",
            "ccj_22f.7f",
            "ccj_24f.9e"
        ]

        def maincpu(contents):
            # Only the last 2 128k chunks actually need deinterleaved...
            maincpu_area = contents[0x40:0x140040]
            deint_chunks = transforms.deinterleave(
                maincpu_area[0x100000:0x140000], num_ways=2, word_size=1)

            chunks = []
            chunks.append(maincpu_area[0x0:0x80000])
            chunks.append(deint_chunks[0])
            chunks.append(maincpu_area[0x80000:0x100000])
            chunks.append(deint_chunks[1])

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "cc_01.3a",
            "cc_05.7a",
            "cc_02.4a",
            "cc_06.8a",
            "cc_03.5a",
            "cc_07.9a",
            "cc_04.6a",
            "cc_08.10a"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'ccj_09.12a',
            'ccj_18.11c',
            'ccj_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'cc63b.1a': 0x117,
            'iob1.12d': 0x117,
            'ccprg1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append(
            {'filename': 'captcommj.zip', 'contents': zip_contents})

        return out_files

    ################################################################################
    # Knights of the Round                                                         #
    ################################################################################

    def _handle_knights(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "kr_23e.8f",
            "kr_22.7f"
        ]

        def maincpu(contents):
            # Only the last 2 128k chunks actually need deinterleaved...
            maincpu_area = contents[0x40:0x100040]
            chunks = transforms.equal_split(maincpu_area, num_chunks=2)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "kr-5m.3a",
            "kr-6m.7a",
            "kr-7m.5a",
            "kr-8m.9a",
            "kr-1m.4a",
            "kr-2m.8a",
            "kr-3m.6a",
            "kr-4m.10a"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'kr_09.11a',
            'kr_18.11c',
            'kr_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'kr63b.1a': 0x117,
            'iob1.12d': 0x117,
            'bprg1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'knights.zip', 'contents': zip_contents})

        return out_files

    def _handle_knightsj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "kr_23j.8f",
            "kr_22.7f"
        ]

        def maincpu(contents):
            # Only the last 2 128k chunks actually need deinterleaved...
            maincpu_area = contents[0x40:0x100040]
            chunks = transforms.equal_split(maincpu_area, num_chunks=2)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "kr_01.3a",
            "kr_05.7a",
            "kr_02.4a",
            "kr_06.8a",
            "kr_03.5a",
            "kr_07.9a",
            "kr_04.6a",
            "kr_08.10a"
        ]
        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'kr_09.12a',
            'kr_18.11c',
            'kr_19.12c'
        ]
        func_map['audio'] = self._audio_common(0x800040, audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'rom1': 0x117,
            'sou1': 0x117,
            'kr63b.1a': 0x117,
            'iob1.12d': 0x117,
            'bprg1.11d': 0x117,
            'ioc1.ic7': 0x104,
            'c632.ic1': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append(
            {'filename': 'knightsj.zip', 'contents': zip_contents})

        return out_files

    ################################################################################
    # Warriors of Fate                                                             #
    ################################################################################

    def _wof_audio(self, filenames):
        def audio(contents):
            start = 0x800040
            chunks = []

            # Add the audio CPU
            audiocpu_content = contents[start:start + 0x8000] + \
                contents[start + 0x10000:start + 0x28000]
            chunks.append(audiocpu_content)

            # Add the qsound
            qsound_start = start + 0x50000
            qsound_contents = contents[qsound_start:qsound_start + 0x200000]
            chunks.extend(transforms.equal_split(
                qsound_contents, num_chunks=4))

            return dict(zip(filenames, chunks))
        return audio

    def _handle_wof(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "tk2e_23c.8f",
            "tk2e_22c.7f"
        ]

        def maincpu(contents):
            maincpu_area = contents[0x40:0x100040]
            chunks = transforms.equal_split(maincpu_area, num_chunks=2)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "tk2-1m.3a",
            "tk2-5m.7a",
            "tk2-3m.5a",
            "tk2-7m.9a",
            "tk2-2m.4a",
            "tk2-6m.8a",
            "tk2-4m.6a",
            "tk2-8m.10a"
        ]

        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'tk2_qa.5k',
            'tk2-q1.1k',
            'tk2-q2.2k',
            'tk2-q3.3k',
            'tk2-q4.4k'
        ]
        func_map['audio'] = self._wof_audio(audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg2': 0x117,
            'rom1': 0x117,
            'tk263b.1a': 0x117,
            'iob1.12d': 0x117,
            'bprg1.11d': 0x117,
            'ioc1.ic1': 0x104,
            'd7l1.7l': 0x117,
            'd8l1.8l': 0x117,
            'd9k1.9k': 0x117,
            'd10f1.10f': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'wof.zip', 'contents': zip_contents})

        return out_files

    def _handle_wofj(self, merged_contents):
        out_files = []
        func_map = {}

        maincpu_filenames = [
            "tk2j_23c.8f",
            "tk2j_22c.7f"
        ]

        def maincpu(contents):
            maincpu_area = contents[0x40:0x100040]
            chunks = transforms.equal_split(maincpu_area, num_chunks=2)

            return dict(zip(maincpu_filenames, chunks))
        func_map['maincpu'] = maincpu

        gfx_filenames = [
            "tk2_01.3a",
            "tk2_05.7a",
            "tk2_02.4a",
            "tk2_06.8a",
            "tk2_03.5a",
            "tk2_07.9a",
            "tk2_04.6a",
            "tk2_08.10a"
        ]

        func_map['gfx'] = self._deshuffle_gfx_common(
            0x400040, 0x400000, gfx_filenames, 4, True)

        audio_filenames = [
            'tk2_qa.5k',
            'tk2-q1.1k',
            'tk2-q2.2k',
            'tk2-q3.3k',
            'tk2-q4.4k'
        ]
        func_map['audio'] = self._wof_audio(audio_filenames)

        ph_files = {
            'buf1': 0x117,
            'ioa1': 0x117,
            'prg1': 0x117,
            'sou1': 0x117,
            'rom1': 0x117,
            'tk263b.1a': 0x117,
            'iob1.12d': 0x117,
            'bprg1.11d': 0x117,
            'ioc1.ic1': 0x104,
            'd7l1.7l': 0x117,
            'd8l1.8l': 0x117,
            'd9k1.9k': 0x117,
            'd10f1.10f': 0x117
        }
        func_map['placeholders'] = helpers.placeholder_helper(ph_files)

        zip_contents = helpers.build_rom(merged_contents, func_map)
        out_files.append({'filename': 'wofj.zip', 'contents': zip_contents})

        return out_files

    ################################################################################
    # Armored Warriors                                                             #
    ################################################################################

    def _armwar_gfx(self, contents):
        contents = contents[0x0800040:0x1C00040]

        contents = capcom.common_gfx_deshuffle(contents)

        chunks = transforms.equal_split(contents, num_chunks=20)

        # Interleave each pair of chunks
        new_chunks = []
        for oddchunk, evenchunk in zip(chunks[0::2], chunks[1::2]):
            new_chunks.append(transforms.interleave(
                [oddchunk, evenchunk], word_size=8))
        chunks = new_chunks

        contents = transforms.merge(chunks)

        # Deinterleave the chunks into our files
        new_chunks = []
        chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
        for chunk in chunks:
            new_chunks.extend(transforms.custom_split(
                chunk, [0x400000, 0x100000]))
        chunks = new_chunks
        filenames = [
            'pwg.13m',
            'pwg.14m',
            'pwg.15m',
            'pwg.16m',
            'pwg.17m',
            'pwg.18m',
            'pwg.19m',
            'pwg.20m'
        ]
        return dict(zip(filenames, chunks))

    def _armwar_audio(self, contents):
        chunks = []
        chunks.append(contents[0x1C00040:0x1C08040] +
                      contents[0x1C10040:0x1C28040])
        chunks.append(contents[0x1C28040:0x1C48040])
        filenames = [
            'pwg.01',
            'pwg.02'
        ]
        return dict(zip(filenames, chunks))

    def _armwar_qsound(self, contents):
        contents = contents[0x1C50040:0x2050040]
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'pwg.11m',
            'pwg.12m'
        ]
        return dict(zip(filenames, chunks))

    def _handle_armwar(self, merged_contents):
        out_files = []

        def maincpu(contents):
            contents = contents[0x40:0x400040]
            chunks = transforms.equal_split(contents, num_chunks=8)
            filenames = [
                "pwge.03c",
                "pwge.04c",
                "pwge.05b",
                "pwg.06",
                "pwg.07",
                "pwg.08",
                "pwg.09a",
                "pwg.10"
            ]
            return dict(zip(filenames, chunks))
        func_map = {}
        func_map['maincpu'] = maincpu
        func_map['gfx'] = self._armwar_gfx
        func_map['audiocpu'] = self._armwar_audio
        func_map['qsound'] = self._armwar_qsound
        out_files.append({'filename': 'armwar.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})
        return out_files

    def _handle_pgear(self, merged_contents):
        out_files = []

        def maincpu(contents):
            contents = contents[0x40:0x400040]
            chunks = transforms.equal_split(contents, num_chunks=8)
            filenames = [
                "pwgj.03a",
                "pwgj.04a",
                "pwgj.05a",
                "pwg.06",
                "pwg.07",
                "pwg.08",
                "pwg.09a",
                "pwg.10"
            ]
            return dict(zip(filenames, chunks))
        func_map = {}
        func_map['maincpu'] = maincpu
        func_map['gfx'] = self._armwar_gfx
        func_map['audiocpu'] = self._armwar_audio
        func_map['qsound'] = self._armwar_qsound
        out_files.append({'filename': 'pgear.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})
        return out_files

    ################################################################################
    # Battle Circuit                                                               #
    ################################################################################

    def _batcir_gfx(self, contents):
        contents = contents[0x0800040:0x1800040]

        contents = capcom.common_gfx_deshuffle(contents)

        chunks = transforms.equal_split(contents, num_chunks=16)

        # Interleave each pair of chunks
        new_chunks = []
        for oddchunk, evenchunk in zip(chunks[0::2], chunks[1::2]):
            new_chunks.append(transforms.interleave(
                [oddchunk, evenchunk], word_size=8))
        chunks = new_chunks

        contents = transforms.merge(chunks)

        # Deinterleave the chunks into our 4 files
        chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
        filenames = [
            'btc.13m',
            'btc.15m',
            'btc.17m',
            'btc.19m'
        ]
        return dict(zip(filenames, chunks))

    def _batcir_audio(self, contents):
        chunks = []
        chunks.append(contents[0x1800040:0x1808040] +
                      contents[0x1810040:0x1828040])
        chunks.append(contents[0x1828040:0x1848040])
        filenames = [
            'btc.01',
            'btc.02'
        ]
        return dict(zip(filenames, chunks))

    def _batcir_qsound(self, contents):
        contents = contents[0x1850040:0x1C50040]
        chunks = transforms.equal_split(contents, num_chunks=2)
        chunks = transforms.swap_endian_all(chunks)
        filenames = [
            'btc.11m',
            'btc.12m'
        ]
        return dict(zip(filenames, chunks))

    def _handle_batcir(self, merged_contents):
        out_files = []

        def maincpu(contents):
            contents = contents[0x40:0x380040]
            chunks = transforms.equal_split(contents, num_chunks=7)
            filenames = [
                "btce.03",
                "btce.04",
                "btce.05",
                "btce.06",
                "btc.07",
                "btc.08",
                "btc.09"
            ]
            return dict(zip(filenames, chunks))
        func_map = {}
        func_map['maincpu'] = maincpu
        func_map['gfx'] = self._batcir_gfx
        func_map['audiocpu'] = self._batcir_audio
        func_map['qsound'] = self._batcir_qsound
        out_files.append({'filename': 'batcir.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})
        return out_files

    def _handle_batcirj(self, merged_contents):
        out_files = []

        def maincpu(contents):
            contents = contents[0x40:0x380040]
            chunks = transforms.equal_split(contents, num_chunks=7)
            filenames = [
                "btcj.03",
                "btcj.04",
                "btcj.05",
                "btcj.06",
                "btc.07",
                "btc.08",
                "btc.09"
            ]
            return dict(zip(filenames, chunks))
        func_map = {}
        func_map['maincpu'] = maincpu
        func_map['gfx'] = self._batcir_gfx
        func_map['audiocpu'] = self._batcir_audio
        func_map['qsound'] = self._batcir_qsound
        out_files.append({'filename': 'batcirj.zip', 'contents': helpers.build_rom(
            merged_contents, func_map)})
        return out_files
