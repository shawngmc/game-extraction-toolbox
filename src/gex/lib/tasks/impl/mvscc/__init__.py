'''Implementation of mvscc: MARVEL vs. CAPCOM Fighting Collection: Arcade Classics'''
import logging
import os

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MVSCCTask(BaseTask):
    '''Implements mvscc: MARVEL vs. CAPCOM Fighting Collection: Arcade Classics'''
    _task_name = "mvscc"
    _title = "MARVEL vs. CAPCOM Fighting Collection: Arcade Classics"
    _details_markdown = '''
This is reverse-engineered based on the CBEYB work from https://web.archive.org/web/20220213232104/http://blog.livedoor.jp/scrap_a/archives/23114141.html.
This was a Japanese set of shell scripts and odd generic operation executables. There is some weird encoding here too.

This script will extract and prep the ROMs. Some per-rom errata are in the notes below. All CRCs are currently mismatched.

TODO: Implement the rest of the games: The Punisher and MvC2.
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("MARVEL vs. CAPCOM Fighting Collection")
    _input_folder_desc = "MVSCC Steam folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def execute(self, in_dir, out_dir):
        # for each output file entry
        for out_file_entry in self._metadata['out']['files']:
            pkg_name = out_file_entry['in_file']
            # Check the status of it
            if out_file_entry['status'] == 'no-rom':
                logger.info(f"Skipping {pkg_name} - cannot extract...")
            else:
                logger.info(f"Extracting {pkg_name}...")

                # read the matching input file
                in_file_entry = self._metadata['in']['files'][pkg_name]
                loaded_file = self.read_datafile(in_dir, in_file_entry)

                # extract the input file
                arc_contents = arc.extract(loaded_file['contents'])

                # Get the bin entry
                merged_rom_contents = None
                for _, arc_content in arc_contents.items():
                    if arc_content['path'].startswith('bin'):
                        merged_rom_contents = arc_content['contents']

                # run the handler
                handler_func = self.find_handler_func(pkg_name)
                if merged_rom_contents is not None and handler_func is not None:
                    output_contents = handler_func(merged_rom_contents)

                    _ = self.verify_out_file(out_file_entry['filename'], output_contents)

                    with open(os.path.join(out_dir, out_file_entry['filename']), "wb") as out_file:
                        out_file.write(output_contents)
                elif merged_rom_contents is None:
                    logger.warning("Could not find merged rom data in arc.")
                elif handler_func is None:
                    logger.warning("Could not find matching handler function.")
        logger.info("Processing complete.")
        
    ################################################################################
    # X-Men: Children of the Atom                                                  #
    ################################################################################
    def _handle_xmcotau(self, merged_contents):
        _xmn_gfx_filenames = [f'xmn.{i}m' for i in range(13, 21)]
        _xmn_audiocpu_filenames = [
            'xmn.01a',
            'xmn.02a'
        ]
        _vam_qsound_filenames = [
            'xmn.11m',
            'xmn.12m'
        ]
        func_map = {}
        maincpu_filenames = ["xmnu.03e","xmnu.04e"] + [f"xmn.{i:02}a" for i in range(5, 11)]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(_xmn_gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, _xmn_audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, _vam_qsound_filenames)

        return helpers.build_rom(merged_contents, func_map)
    
    ################################################################################
    # Marvel Super Heroes                                                          #
    ################################################################################
    def _handle_mshh(self, merged_contents):
        gfx_filenames = [f'msh.{i}m' for i in range(13, 21)]
        audiocpu_filenames = [
            'msh.01',
            'msh.02'
        ]
        qsound_filenames = [
            'msh.11m',
            'msh.12m'
        ]
        func_map = {}
        maincpu_filenames = [
            "mshh.03c",
            "mshh.04c",
            "msh.05a",
            "msh.06b",
            "msh.07a",
            "msh.08a",
            "msh.09a",
            "msh.10b",
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, qsound_filenames)

        return helpers.build_rom(merged_contents, func_map)
    
    ################################################################################
    # X-Men Vs. Street Fighter                                                     #
    ################################################################################
    def _handle_xmvsfu(self, merged_contents):
        gfx_filenames = [f'xvs.{i}m' for i in range(13, 21)]
        audiocpu_filenames = [
            'xvs.01',
            'xvs.02'
        ]
        qsound_filenames = [
            'xvs.11m',
            'xvs.12m'
        ]
        func_map = {}
        maincpu_filenames = [
            "xvsu.03k",
            "xvsu.04k",
            "xvs.05a",
            "xvs.06a",
            "xvs.07",
            "xvs.08",
            "xvs.09",
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x400000, qsound_filenames)

        return helpers.build_rom(merged_contents, func_map)
    
    ################################################################################
    # Marvel Super Heroes vs. Street Fighter                                       #
    ################################################################################
    def _handle_mshvsfu(self, merged_contents):
        gfx_filenames = [f'mvs.{i}m' for i in range(13, 21)]
        audiocpu_filenames = [
            'mvs.01',
            'mvs.02'
        ]
        qsound_filenames = [
            'mvs.11m',
            'mvs.12m'
        ]
        func_map = {}
        maincpu_filenames = [
            "mvsu.03g",
            "mvsu.04g",
            "mvs.05d",
            "mvs.06a",
            "mvs.07b",
            "mvs.08a",
            "mvs.09b",
            "mvs.10b",
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, qsound_filenames)

        return helpers.build_rom(merged_contents, func_map)
    
    ################################################################################
    # Marvel vs. Capcom: Clash of Super Heroes                                     #
    ################################################################################
    def _handle_mvscu(self, merged_contents):
        gfx_filenames = [f'mvc.{i}m' for i in range(13, 21)]
        audiocpu_filenames = [
            'mvc.01',
            'mvc.02'
        ]
        qsound_filenames = [
            'mvc.11m',
            'mvc.12m'
        ]
        func_map = {}
        maincpu_filenames = [
            "mvcu.03d",
            "mvcu.04d",
            "mvc.05a",
            "mvc.06a",
            "mvc.07",
            "mvc.08",
            "mvc.09",
            "mvc.10",
        ]
        func_map['maincpu'] = capcom.maincpu_cps2(
            0x40, 0x400000, 8, maincpu_filenames)
        func_map['gfx'] = capcom.gfx_cps2(gfx_filenames, helpers.slice_helper(
            0x0800040, length=0x2000000), split=[0x400000, 0x400000])
        func_map['audiocpu'] = capcom.audiocpu_cps2(
            0x2800040, audiocpu_filenames)
        func_map['qsound'] = capcom.qsound_cps2(
            0x2850040, 0x800000, qsound_filenames)

        return helpers.build_rom(merged_contents, func_map)
