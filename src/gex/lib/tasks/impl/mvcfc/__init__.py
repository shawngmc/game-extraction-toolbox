'''Implementation of mvcfc: Marvel vs. Capcom Fighting Collection'''
import logging
import os

from gex.lib.archive import arc
from gex.lib.utils.vendor import capcom
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers

logger = logging.getLogger('gextoolbox')

class MVCFCTask(BaseTask):
    '''Implements mvcfc: Marvel vs. Capcom Fighting Collection'''
    _task_name = "mvcfc"
    _title = "Marvel vs. Capcom Fighting Collection"
    _details_markdown = '''
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("MARVEL vs. CAPCOM Fighting Collection")
    _input_folder_desc = "MVCFC Steam folder"

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
    # X-Men Children of the Atom                                                   #
    ################################################################################
    # CPS2 Game

# xmcotaj
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# xmcotaj.key          |        20 |                      | good    |                      | key               |          0 | no  | d278b4ac | 06d94e8a203172792f405c73f9cbb37f4738429f
# xmn.01a              |    131072 |                      | good    | xmn.01a              | audiocpu          |          0 | no  | 40f479ea | f29e15f537675305264ae2138a0a537fb9e2008b
# xmn.02a              |    131072 |                      | good    | xmn.02a              | audiocpu          |      28000 | no  | 39d9b5ad | af502debfd36100d4fc971ed25fdf9d7121d6f18
# xmn.05a              |    524288 |                      | good    |                      | maincpu           |     100000 | no  | ac0d7759 | 650d4474b13f16af7910a0f721fcda2ddb2414fd
# xmn.06a              |    524288 |                      | good    | xmn.06a              | maincpu           |     180000 | no  | 1b86a328 | 2469cd705139ee9f1142e6e379e68d0c9675b37e
# xmn.07a              |    524288 |                      | good    | xmn.07a              | maincpu           |     200000 | no  | 2c142a44 | 7624875f9c39b361fc83e52e87e0fd5e96279713
# xmn.08a              |    524288 |                      | good    | xmn.08a              | maincpu           |     280000 | no  | f712d44f | 0d18d4a4eacad94a66beca6ec509ac7f690c6882
# xmn.09a              |    524288 |                      | good    | xmn.09a              | maincpu           |     300000 | no  | 9241cae8 | bb6980abf25aaf3eb14e230ca6942f3e2ab2c660
# xmn.10a              |    524288 |                      | good    |                      | maincpu           |     380000 | no  | 53c0eab9 | e3b1ec1fd517735f7801cfebb257c43185c6d3fb
# xmn.11m              |   2097152 |                      | good    | xmn.11m              | qsound            |          0 | no  | c848a6bc | ac8ac564d3c43225822f8bc330eba9f35b24b0a4
# xmn.12m              |   2097152 |                      | good    | xmn.12m              | qsound            |     200000 | no  | 729c188f | 3279774ad8aebbcf0fc779cdfcbe21044dd192ad
# xmn.13m              |   4194304 |                      | good    | xmn.13m              | gfx               |          0 | no  | bf4df073 | 4d2740c3a827f0ec2cf75ad99c65e393c6a11c23
# xmn.14m              |   4194304 |                      | good    | xmn.14m              | gfx               |    1000000 | no  | 778237b7 | 89a759ec383518ec52f5059d10ec342f2247aa20
# xmn.15m              |   4194304 |                      | good    | xmn.15m              | gfx               |          2 | no  | 4d7e4cef | 50b8797b8099a8d76ad063ba1201a13dbb88ae3a
# xmn.16m              |   4194304 |                      | good    | xmn.16m              | gfx               |    1000002 | no  | 67b36948 | 692fb6e4096b880aa22996d554b160f664bbd907
# xmn.17m              |   4194304 |                      | good    | xmn.17m              | gfx               |          4 | no  | 513eea17 | a497477ad9ac13180911d8745ef6ee1955c0b877
# xmn.18m              |   4194304 |                      | good    | xmn.18m              | gfx               |    1000004 | no  | 015a7c4c | cccc95dafd076a1a9fa004710006149c42d058ba
# xmn.19m              |   4194304 |                      | good    | xmn.19m              | gfx               |          6 | no  | d23897fc | 1e31627999736652252164d32662779a1ac6ca29
# xmn.20m              |   4194304 |                      | good    | xmn.20m              | gfx               |    1000006 | no  | 9dde2758 | 17ba259cad03c7b5d56c0a5eda9ab53521665729
# xmnj.03e             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 0df29f5f | 83993ea90e7a602c3db137d08c008dcd9bee3055
# xmnj.04e             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 4a65833b | cd899674ba6448fb3841247d3f434e82b19c5399


# xmcotau
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# xmcotau.key          |        20 |                      | good    |                      | key               |          0 | no  | 623d3357 | 27e8209e5a0917b127f0e65c53e95c28d78e7a0e
# xmn.01a              |    131072 |                      | good    | xmn.01a              | audiocpu          |          0 | no  | 40f479ea | f29e15f537675305264ae2138a0a537fb9e2008b
# xmn.02a              |    131072 |                      | good    | xmn.02a              | audiocpu          |      28000 | no  | 39d9b5ad | af502debfd36100d4fc971ed25fdf9d7121d6f18
# xmn.05a              |    524288 |                      | good    |                      | maincpu           |     100000 | no  | ac0d7759 | 650d4474b13f16af7910a0f721fcda2ddb2414fd
# xmn.06a              |    524288 |                      | good    | xmn.06a              | maincpu           |     180000 | no  | 1b86a328 | 2469cd705139ee9f1142e6e379e68d0c9675b37e
# xmn.07a              |    524288 |                      | good    | xmn.07a              | maincpu           |     200000 | no  | 2c142a44 | 7624875f9c39b361fc83e52e87e0fd5e96279713
# xmn.08a              |    524288 |                      | good    | xmn.08a              | maincpu           |     280000 | no  | f712d44f | 0d18d4a4eacad94a66beca6ec509ac7f690c6882
# xmn.09a              |    524288 |                      | good    | xmn.09a              | maincpu           |     300000 | no  | 9241cae8 | bb6980abf25aaf3eb14e230ca6942f3e2ab2c660
# xmn.10a              |    524288 |                      | good    |                      | maincpu           |     380000 | no  | 53c0eab9 | e3b1ec1fd517735f7801cfebb257c43185c6d3fb
# xmn.11m              |   2097152 |                      | good    | xmn.11m              | qsound            |          0 | no  | c848a6bc | ac8ac564d3c43225822f8bc330eba9f35b24b0a4
# xmn.12m              |   2097152 |                      | good    | xmn.12m              | qsound            |     200000 | no  | 729c188f | 3279774ad8aebbcf0fc779cdfcbe21044dd192ad
# xmn.13m              |   4194304 |                      | good    | xmn.13m              | gfx               |          0 | no  | bf4df073 | 4d2740c3a827f0ec2cf75ad99c65e393c6a11c23
# xmn.14m              |   4194304 |                      | good    | xmn.14m              | gfx               |    1000000 | no  | 778237b7 | 89a759ec383518ec52f5059d10ec342f2247aa20
# xmn.15m              |   4194304 |                      | good    | xmn.15m              | gfx               |          2 | no  | 4d7e4cef | 50b8797b8099a8d76ad063ba1201a13dbb88ae3a
# xmn.16m              |   4194304 |                      | good    | xmn.16m              | gfx               |    1000002 | no  | 67b36948 | 692fb6e4096b880aa22996d554b160f664bbd907
# xmn.17m              |   4194304 |                      | good    | xmn.17m              | gfx               |          4 | no  | 513eea17 | a497477ad9ac13180911d8745ef6ee1955c0b877
# xmn.18m              |   4194304 |                      | good    | xmn.18m              | gfx               |    1000004 | no  | 015a7c4c | cccc95dafd076a1a9fa004710006149c42d058ba
# xmn.19m              |   4194304 |                      | good    | xmn.19m              | gfx               |          6 | no  | d23897fc | 1e31627999736652252164d32662779a1ac6ca29
# xmn.20m              |   4194304 |                      | good    | xmn.20m              | gfx               |    1000006 | no  | 9dde2758 | 17ba259cad03c7b5d56c0a5eda9ab53521665729
# xmnu.03e             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 0bafeb0e | 170c819bd7ffafefb9b2a587509bdf2c0415474b
# xmnu.04e             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | c29bdae3 | c605a4fd90336459c7b24cd7b2b243eef10f6407



    ################################################################################
    # Marvel Super Heroes                                                          #
    ################################################################################
    # CPS2 Game

# mshj
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# msh.01               |    131072 |                      | good    | msh.01               | audiocpu          |          0 | no  | c976e6f9 | 281025e5aaf97c0aeddc8bd0f737d092daadad9e
# msh.02               |    131072 |                      | good    | msh.02               | audiocpu          |      28000 | no  | ce67d0d9 | 324226597cc5a11603f04085fef7715a314ecc05
# msh.05a              |    524288 |                      | good    |                      | maincpu           |     100000 | no  | f37539e6 | 770febc25ca5615b6c2023727edab3c68b15b2c4
# msh.06b              |    524288 |                      | good    | msh.06b              | maincpu           |     180000 | no  | 803e3fa4 | 0acdeda65002521bf24130cbf06f9faa1dcef9e5
# msh.07a              |    524288 |                      | good    | msh.07a              | maincpu           |     200000 | no  | c45f8e27 | 4d28e0782c31ce56e728ac6ef5edd10437f00637
# msh.08a              |    524288 |                      | good    | msh.08a              | maincpu           |     280000 | no  | 9ca6f12c | 26ad682667b983b805e1f577426e5fca8ee3c82b
# msh.09a              |    524288 |                      | good    | msh.09a              | maincpu           |     300000 | no  | 82ec27af | caf76268063ba91d28e8af684d60c2d71f29b9b9
# msh.10b              |    524288 |                      | good    | msh.10b              | maincpu           |     380000 | no  | 8d931196 | 983e62efcdb4c8db6bce6acf4f86acb9447b565d
# msh.11m              |   2097152 |                      | good    | msh.11m              | qsound            |          0 | no  | 37ac6d30 | ec67421fbf4a08a686e76792cb35e9cbf04d022d
# msh.12m              |   2097152 |                      | good    | msh.12m              | qsound            |     200000 | no  | de092570 | a03d0df901f6ea79685eaed67db65bee14ec29c6
# msh.13m              |   4194304 |                      | good    | msh.13m              | gfx               |          0 | no  | 09d14566 | c96463654043f22da5e844c6da17aa9273dc3439
# msh.14m              |   4194304 |                      | good    | msh.14m              | gfx               |    1000000 | no  | 4197973e | 93aeea1a480b5f452c8a40ae3fff956796b859fa
# msh.15m              |   4194304 |                      | good    | msh.15m              | gfx               |          2 | no  | ee962057 | 24e359accb5f71a5863d7bad4088719fa547f88c
# msh.16m              |   4194304 |                      | good    | msh.16m              | gfx               |    1000002 | no  | 438da4a0 | ca93b14c3a570f9dd582efbb3f0536a92e535042
# msh.17m              |   4194304 |                      | good    | msh.17m              | gfx               |          4 | no  | 604ece14 | 880fb62b33ba4cceb38635e4ec056fac11a3c70f
# msh.18m              |   4194304 |                      | good    | msh.18m              | gfx               |    1000004 | no  | 4db92d94 | f1b25ccc0627139ad5b287a8f2ab3b4a2fb8b8e4
# msh.19m              |   4194304 |                      | good    | msh.19m              | gfx               |          6 | no  | 94a731e8 | 1e784a3412e7361e3001494e1daf840ef8c20449
# msh.20m              |   4194304 |                      | good    | msh.20m              | gfx               |    1000006 | no  | a2b0c6c0 | 71016c01c1a706b73cf5b9ac7e384a030c6cf08d
# mshj.03g             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 261f4091 | f4509780768e3601720d0d78c8a9824d410d59da
# mshj.04g             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 61d791c6 | 9f883bcc48058a99c4ba653d0855c58c5d081243
# mshj.key             |        20 |                      | good    |                      | key               |          0 | no  | 888761ac | a1c72deedab2bafe5d594bba905a6274575b6e56


# mshh
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# msh.01               |    131072 |                      | good    | msh.01               | audiocpu          |          0 | no  | c976e6f9 | 281025e5aaf97c0aeddc8bd0f737d092daadad9e
# msh.02               |    131072 |                      | good    | msh.02               | audiocpu          |      28000 | no  | ce67d0d9 | 324226597cc5a11603f04085fef7715a314ecc05
# msh.05               |    524288 |                      | good    | msh.05               | maincpu           |     100000 | no  | 6a091b9e | 7fa54e69e1a1ca348cb08d892d55023e9a3ff4cb
# msh.06b              |    524288 |                      | good    | msh.06b              | maincpu           |     180000 | no  | 803e3fa4 | 0acdeda65002521bf24130cbf06f9faa1dcef9e5
# msh.07a              |    524288 |                      | good    | msh.07a              | maincpu           |     200000 | no  | c45f8e27 | 4d28e0782c31ce56e728ac6ef5edd10437f00637
# msh.08a              |    524288 |                      | good    | msh.08a              | maincpu           |     280000 | no  | 9ca6f12c | 26ad682667b983b805e1f577426e5fca8ee3c82b
# msh.09a              |    524288 |                      | good    | msh.09a              | maincpu           |     300000 | no  | 82ec27af | caf76268063ba91d28e8af684d60c2d71f29b9b9
# msh.10b              |    524288 |                      | good    | msh.10b              | maincpu           |     380000 | no  | 8d931196 | 983e62efcdb4c8db6bce6acf4f86acb9447b565d
# msh.11m              |   2097152 |                      | good    | msh.11m              | qsound            |          0 | no  | 37ac6d30 | ec67421fbf4a08a686e76792cb35e9cbf04d022d
# msh.12m              |   2097152 |                      | good    | msh.12m              | qsound            |     200000 | no  | de092570 | a03d0df901f6ea79685eaed67db65bee14ec29c6
# msh.13m              |   4194304 |                      | good    | msh.13m              | gfx               |          0 | no  | 09d14566 | c96463654043f22da5e844c6da17aa9273dc3439
# msh.14m              |   4194304 |                      | good    | msh.14m              | gfx               |    1000000 | no  | 4197973e | 93aeea1a480b5f452c8a40ae3fff956796b859fa
# msh.15m              |   4194304 |                      | good    | msh.15m              | gfx               |          2 | no  | ee962057 | 24e359accb5f71a5863d7bad4088719fa547f88c
# msh.16m              |   4194304 |                      | good    | msh.16m              | gfx               |    1000002 | no  | 438da4a0 | ca93b14c3a570f9dd582efbb3f0536a92e535042
# msh.17m              |   4194304 |                      | good    | msh.17m              | gfx               |          4 | no  | 604ece14 | 880fb62b33ba4cceb38635e4ec056fac11a3c70f
# msh.18m              |   4194304 |                      | good    | msh.18m              | gfx               |    1000004 | no  | 4db92d94 | f1b25ccc0627139ad5b287a8f2ab3b4a2fb8b8e4
# msh.19m              |   4194304 |                      | good    | msh.19m              | gfx               |          6 | no  | 94a731e8 | 1e784a3412e7361e3001494e1daf840ef8c20449
# msh.20m              |   4194304 |                      | good    | msh.20m              | gfx               |    1000006 | no  | a2b0c6c0 | 71016c01c1a706b73cf5b9ac7e384a030c6cf08d
# mshu.03              |    524288 |                      | good    |                      | maincpu           |          0 | no  | d2805bdd | a6f78c31a82168bb5f7d614dcebbeab8231e2d75
# mshu.04              |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 743f96ff | abb82359bb68966028ea33e94996803599f3e273
# mshu.key             |        20 |                      | good    |                      | key               |          0 | no  | 745c1bee | 86d31f266f0fc20ca5f1607eebf4db688323147f





    ################################################################################
    # X-Men vs. Street Fighter                                                     #
    ################################################################################
    # CPS2 Game

# xmvsfj
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# xmvsfj.key           |        20 |                      | good    |                      | key               |          0 | no  | 87576cda | 65905400f4462c175baa93b43e015e8596def31b
# xvs.01               |    131072 |                      | good    | xvs.01               | audiocpu          |          0 | no  | 3999e93a | fefcff8a9a5c83df7655a16187cf9ba3e7efbb25
# xvs.02               |    131072 |                      | good    | xvs.02               | audiocpu          |      28000 | no  | 101bdee9 | 75920e88bf46fcd33a7957777a1d799818ffb0d6
# xvs.05a              |    524288 |                      | good    | xvs.05a              | maincpu           |     100000 | no  | 7db6025d | 2d74f48f83f45359bfaca28ab686625766af12ee
# xvs.06a              |    524288 |                      | good    | xvs.06a              | maincpu           |     180000 | no  | e8e2c75c | 929408cb5d98e95cec75ea58e4701b0cbdbcd016
# xvs.07               |    524288 |                      | good    | xvs.07               | maincpu           |     200000 | no  | 08f0abed | ef16c376232dba63b0b9bc3aa0640f9001ccb68a
# xvs.08               |    524288 |                      | good    | xvs.08               | maincpu           |     280000 | no  | 81929675 | 19cf7afbc1daaefec40195e40ba74970f3906a1c
# xvs.09               |    524288 |                      | good    | xvs.09               | maincpu           |     300000 | no  | 9641f36b | dcba3482d1ba37ccfb30d402793ee063c6621aed
# xvs.11m              |   2097152 |                      | good    | xvs.11m              | qsound            |          0 | no  | 9cadcdbc | 64d3bd53b04daec84c9af4aa3ff010867b3d306d
# xvs.12m              |   2097152 |                      | good    | xvs.12m              | qsound            |     200000 | no  | 7b11e460 | a581c84acaaf0ce056841c15a6f36889e88be68d
# xvs.13m              |   4194304 |                      | good    | xvs.13m              | gfx               |          0 | no  | f6684efd | c0a2f3a9e82ab8b084a500aec71ac633e947328c
# xvs.14m              |   4194304 |                      | good    | xvs.14m              | gfx               |    1000000 | no  | bcac2e41 | 838ff24f7e8543a787a55a5d592c9517ce3b8b93
# xvs.15m              |   4194304 |                      | good    | xvs.15m              | gfx               |          2 | no  | 29109221 | 898b8f678fd03c462ce0d8eb7fb3441ef601085b
# xvs.16m              |   4194304 |                      | good    | xvs.16m              | gfx               |    1000002 | no  | ea04a272 | cd7c79037b5b4a39bef5156433e984dc4dc2c081
# xvs.17m              |   4194304 |                      | good    | xvs.17m              | gfx               |          4 | no  | 92db3474 | 7b6f4c8ebfdac167b25f35029068b6253c141fe6
# xvs.18m              |   4194304 |                      | good    | xvs.18m              | gfx               |    1000004 | no  | b0def86a | da3a6705ea7050fc5c2c10d33400ed67be9f455d
# xvs.19m              |   4194304 |                      | good    | xvs.19m              | gfx               |          6 | no  | 3733473c | 6579da7145c95b3ad00844a5fc8c2e22c23365e2
# xvs.20m              |   4194304 |                      | good    | xvs.20m              | gfx               |    1000006 | no  | 4b40ff9f | 9a981d442132efff09a27408d74646ba357c7357
# xvsj.03m             |    524288 |                      | good    |                      | maincpu           |          0 | no  | e2944372 | 5ad99eb3f1fa1266a7310e8a39f4cb86105e8d5e
# xvsj.04m             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | c20b8524 | 1297332c94f4cad725c83a453baa63c1fa25d854


# xmvsfu
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# xmvsfu.key           |        20 |                      | good    |                      | key               |          0 | no  | eca13458 | 4de2691de7de104dbba1f10b3f738e6f2b708a15
# xvs.01               |    131072 |                      | good    | xvs.01               | audiocpu          |          0 | no  | 3999e93a | fefcff8a9a5c83df7655a16187cf9ba3e7efbb25
# xvs.02               |    131072 |                      | good    | xvs.02               | audiocpu          |      28000 | no  | 101bdee9 | 75920e88bf46fcd33a7957777a1d799818ffb0d6
# xvs.05a              |    524288 |                      | good    | xvs.05a              | maincpu           |     100000 | no  | 7db6025d | 2d74f48f83f45359bfaca28ab686625766af12ee
# xvs.06a              |    524288 |                      | good    | xvs.06a              | maincpu           |     180000 | no  | e8e2c75c | 929408cb5d98e95cec75ea58e4701b0cbdbcd016
# xvs.07               |    524288 |                      | good    | xvs.07               | maincpu           |     200000 | no  | 08f0abed | ef16c376232dba63b0b9bc3aa0640f9001ccb68a
# xvs.08               |    524288 |                      | good    | xvs.08               | maincpu           |     280000 | no  | 81929675 | 19cf7afbc1daaefec40195e40ba74970f3906a1c
# xvs.09               |    524288 |                      | good    | xvs.09               | maincpu           |     300000 | no  | 9641f36b | dcba3482d1ba37ccfb30d402793ee063c6621aed
# xvs.11m              |   2097152 |                      | good    | xvs.11m              | qsound            |          0 | no  | 9cadcdbc | 64d3bd53b04daec84c9af4aa3ff010867b3d306d
# xvs.12m              |   2097152 |                      | good    | xvs.12m              | qsound            |     200000 | no  | 7b11e460 | a581c84acaaf0ce056841c15a6f36889e88be68d
# xvs.13m              |   4194304 |                      | good    | xvs.13m              | gfx               |          0 | no  | f6684efd | c0a2f3a9e82ab8b084a500aec71ac633e947328c
# xvs.14m              |   4194304 |                      | good    | xvs.14m              | gfx               |    1000000 | no  | bcac2e41 | 838ff24f7e8543a787a55a5d592c9517ce3b8b93
# xvs.15m              |   4194304 |                      | good    | xvs.15m              | gfx               |          2 | no  | 29109221 | 898b8f678fd03c462ce0d8eb7fb3441ef601085b
# xvs.16m              |   4194304 |                      | good    | xvs.16m              | gfx               |    1000002 | no  | ea04a272 | cd7c79037b5b4a39bef5156433e984dc4dc2c081
# xvs.17m              |   4194304 |                      | good    | xvs.17m              | gfx               |          4 | no  | 92db3474 | 7b6f4c8ebfdac167b25f35029068b6253c141fe6
# xvs.18m              |   4194304 |                      | good    | xvs.18m              | gfx               |    1000004 | no  | b0def86a | da3a6705ea7050fc5c2c10d33400ed67be9f455d
# xvs.19m              |   4194304 |                      | good    | xvs.19m              | gfx               |          6 | no  | 3733473c | 6579da7145c95b3ad00844a5fc8c2e22c23365e2
# xvs.20m              |   4194304 |                      | good    | xvs.20m              | gfx               |    1000006 | no  | 4b40ff9f | 9a981d442132efff09a27408d74646ba357c7357
# xvsu.03k             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 8739ef61 | 2eb5912d3026bed0f720d28e1bf3a7ceb5b80803
# xvsu.04k             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | e11d35c1 | d838199b2767d9f02fa0f103c5d587a4c78c0d21

    ################################################################################
    # Marvel Super Heroes vs. Street Fighter                                       #
    ################################################################################
    # CPS2 Game

# mshvsfj
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# mshvsfj.key          |        20 |                      | good    |                      | key               |          0 | no  | 565eeebb | 762844b59b2fcf529a26ad3dde8282415db926b3
# mvs.01               |    131072 |                      | good    | mvs.01               | audiocpu          |          0 | no  | 68252324 | 138ef320ef27956b2ab5591d49a1315b7b0a194c
# mvs.02               |    131072 |                      | good    | mvs.02               | audiocpu          |      28000 | no  | b34e773d | 3bcf44bf06c35814cff29d244142db7abe05bd39
# mvs.05h              |    524288 |                      | good    |                      | maincpu           |     100000 | no  | 77870dc3 | 924a7c82456bb44d7b0be65af11dbe1a2420a3f0
# mvs.06a              |    524288 |                      | good    | mvs.06a              | maincpu           |     180000 | no  | 959f3030 | fbbaa915324815246738f3426232e623f039ce26
# mvs.07b              |    524288 |                      | good    | mvs.07b              | maincpu           |     200000 | no  | 7f915bdb | 683da09c5ba55e31b59aa95a8e13c45dc574ab3c
# mvs.08a              |    524288 |                      | good    | mvs.08a              | maincpu           |     280000 | no  | c2813884 | 49e5d4bc48f90c8146cb6aafb9240aff0119f1a7
# mvs.09b              |    524288 |                      | good    | mvs.09b              | maincpu           |     300000 | no  | 3ba08818 | 9ab132a3cac55fcccebe6c99b6fb0ba1305f8f6e
# mvs.10b              |    524288 |                      | good    | mvs.10b              | maincpu           |     380000 | no  | cf0dba98 | f4c1f8a6e7a79ecc6241d5268b3039f8a09ea516
# mvs.11m              |   4194304 |                      | good    | mvs.11m              | qsound            |          0 | no  | 86219770 | 4e5b68d382a5aa37f8b0b6434c53a2b95f5f9a4d
# mvs.12m              |   4194304 |                      | good    | mvs.12m              | qsound            |     400000 | no  | f2fd7f68 | 28a30d55d3eaf963006c7cbe7c288099cd3ba536
# mvs.13m              |   4194304 |                      | good    | mvs.13m              | gfx               |          0 | no  | 29b05fd9 | e8fdb1ee5515a560eb4256ae4fd99bb1192e1a87
# mvs.14m              |   4194304 |                      | good    | mvs.14m              | gfx               |    1000000 | no  | b3b1972d | 0f2c3fb7de014181ee481ec35d0578b2c116c2dc
# mvs.15m              |   4194304 |                      | good    | mvs.15m              | gfx               |          2 | no  | faddccf1 | 4ed03ea91883a0413325f57edcc1614120b5922c
# mvs.16m              |   4194304 |                      | good    | mvs.16m              | gfx               |    1000002 | no  | 08aadb5d | 3a2c222eca3e7df80ce69951b3db6442312751a4
# mvs.17m              |   4194304 |                      | good    | mvs.17m              | gfx               |          4 | no  | 97aaf4c7 | 6a054921cc14fe080cb3f62c391f8ae3cc7e8ba9
# mvs.18m              |   4194304 |                      | good    | mvs.18m              | gfx               |    1000004 | no  | c1228b35 | 7afdfb552888c79d0fbb30242b3d917b87fad57a
# mvs.19m              |   4194304 |                      | good    | mvs.19m              | gfx               |          6 | no  | cb70e915 | da4d2480d348ac6dfd01256a88f4f3db8357ae46
# mvs.20m              |   4194304 |                      | good    | mvs.20m              | gfx               |    1000006 | no  | 366cc6c2 | 6f2a789087c8e404c5227b927fa8328c03593243
# mvsj.03i             |    524288 |                      | good    |                      | maincpu           |          0 | no  | d8cbb691 | 16820cf3bc7285477e61bd598a3ed4ea5e0e770d
# mvsj.04i             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 32741ace | 36db3a3aeaf29369977593c051bf5665cffefb2d

# mshvsfu
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# mshvsfu.key          |        20 |                      | good    |                      | key               |          0 | no  | 4c04797b | dc1d59862d07112b75348ae5ad925d3716099e82
# mvs.01               |    131072 |                      | good    | mvs.01               | audiocpu          |          0 | no  | 68252324 | 138ef320ef27956b2ab5591d49a1315b7b0a194c
# mvs.02               |    131072 |                      | good    | mvs.02               | audiocpu          |      28000 | no  | b34e773d | 3bcf44bf06c35814cff29d244142db7abe05bd39
# mvs.05d              |    524288 |                      | good    |                      | maincpu           |     100000 | no  | 921fc542 | b813082a480d42d663c713062892245faabe9101
# mvs.06a              |    524288 |                      | good    | mvs.06a              | maincpu           |     180000 | no  | 959f3030 | fbbaa915324815246738f3426232e623f039ce26
# mvs.07b              |    524288 |                      | good    | mvs.07b              | maincpu           |     200000 | no  | 7f915bdb | 683da09c5ba55e31b59aa95a8e13c45dc574ab3c
# mvs.08a              |    524288 |                      | good    | mvs.08a              | maincpu           |     280000 | no  | c2813884 | 49e5d4bc48f90c8146cb6aafb9240aff0119f1a7
# mvs.09b              |    524288 |                      | good    | mvs.09b              | maincpu           |     300000 | no  | 3ba08818 | 9ab132a3cac55fcccebe6c99b6fb0ba1305f8f6e
# mvs.10b              |    524288 |                      | good    | mvs.10b              | maincpu           |     380000 | no  | cf0dba98 | f4c1f8a6e7a79ecc6241d5268b3039f8a09ea516
# mvs.11m              |   4194304 |                      | good    | mvs.11m              | qsound            |          0 | no  | 86219770 | 4e5b68d382a5aa37f8b0b6434c53a2b95f5f9a4d
# mvs.12m              |   4194304 |                      | good    | mvs.12m              | qsound            |     400000 | no  | f2fd7f68 | 28a30d55d3eaf963006c7cbe7c288099cd3ba536
# mvs.13m              |   4194304 |                      | good    | mvs.13m              | gfx               |          0 | no  | 29b05fd9 | e8fdb1ee5515a560eb4256ae4fd99bb1192e1a87
# mvs.14m              |   4194304 |                      | good    | mvs.14m              | gfx               |    1000000 | no  | b3b1972d | 0f2c3fb7de014181ee481ec35d0578b2c116c2dc
# mvs.15m              |   4194304 |                      | good    | mvs.15m              | gfx               |          2 | no  | faddccf1 | 4ed03ea91883a0413325f57edcc1614120b5922c
# mvs.16m              |   4194304 |                      | good    | mvs.16m              | gfx               |    1000002 | no  | 08aadb5d | 3a2c222eca3e7df80ce69951b3db6442312751a4
# mvs.17m              |   4194304 |                      | good    | mvs.17m              | gfx               |          4 | no  | 97aaf4c7 | 6a054921cc14fe080cb3f62c391f8ae3cc7e8ba9
# mvs.18m              |   4194304 |                      | good    | mvs.18m              | gfx               |    1000004 | no  | c1228b35 | 7afdfb552888c79d0fbb30242b3d917b87fad57a
# mvs.19m              |   4194304 |                      | good    | mvs.19m              | gfx               |          6 | no  | cb70e915 | da4d2480d348ac6dfd01256a88f4f3db8357ae46
# mvs.20m              |   4194304 |                      | good    | mvs.20m              | gfx               |    1000006 | no  | 366cc6c2 | 6f2a789087c8e404c5227b927fa8328c03593243
# mvsu.03g             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 0664ab15 | 939fb1e3c06c33fc212b26ecfceac3180e108e9d
# mvsu.04g             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 97e060ee | 787924e04508c83ecd4c3a872882d2be9e57eb50

    ################################################################################
    # Marvel vs. Capcom                                                            #
    ################################################################################
    # CPS2 Game

# mvscj

# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# mvc.01               |    131072 |                      | good    | mvc.01               | audiocpu          |          0 | no  | 41629e95 | 36925c05b5fdcbe43283a882d021e5360c947061
# mvc.02               |    131072 |                      | good    | mvc.02               | audiocpu          |      28000 | no  | 963abf6b | 6b784870e338701cefabbbe4669984b5c4e8a9a5
# mvc.05a              |    524288 |                      | good    | mvc.05a              | maincpu           |     100000 | no  | 2d8c8e86 | b07d640a734c5d336054ed05195786224c9a6cd4
# mvc.06a              |    524288 |                      | good    | mvc.06a              | maincpu           |     180000 | no  | 8528e1f5 | cd065c05268ab581b05676da544baf6af642acac
# mvc.07               |    524288 |                      | good    | mvc.07               | maincpu           |     200000 | no  | c3baa32b | d35589847e0753e869ffcd7c3abed925bfdb0fa2
# mvc.08               |    524288 |                      | good    | mvc.08               | maincpu           |     280000 | no  | bc002fcd | 0b6735a071a9274f7ab25c743271fc30411fe819
# mvc.09               |    524288 |                      | good    | mvc.09               | maincpu           |     300000 | no  | c67b26df | 6e9969246c57269d7ba0992a5cc319c8910bf8a9
# mvc.10               |    524288 |                      | good    | mvc.10               | maincpu           |     380000 | no  | 0fdd1e26 | 5fa684d823b4f4eec61ed9e9b8938af5272ae1ed
# mvc.11m              |   4194304 |                      | good    | mvc.11m              | qsound            |          0 | no  | 850fe663 | 81e519d05a08855f242ea2e17ee0859b449db895
# mvc.12m              |   4194304 |                      | good    | mvc.12m              | qsound            |     400000 | no  | 7ccb1896 | 74caadf3282fcc6acffb1bbe3734106f81124121
# mvc.13m              |   4194304 |                      | good    | mvc.13m              | gfx               |          0 | no  | fa5f74bc | 79a619248938a85ce4f7794a704647b9cf564fbc
# mvc.14m              |   4194304 |                      | good    | mvc.14m              | gfx               |    1000000 | no  | 7f1df4e4 | ede92b31c1fe87f91b4fe74ac211f2fb5f863bc2
# mvc.15m              |   4194304 |                      | good    | mvc.15m              | gfx               |          2 | no  | 71938a8f | 6982f7203458c1c46a1c1c13c0d0f2a5e109d271
# mvc.16m              |   4194304 |                      | good    | mvc.16m              | gfx               |    1000002 | no  | 90bd3203 | ed83208c486ea0f407b7e5d16a8cf242a6f73774
# mvc.17m              |   4194304 |                      | good    | mvc.17m              | gfx               |          4 | no  | 92741d07 | ddfd70eab7c983ab452194b1860059f8ad694459
# mvc.18m              |   4194304 |                      | good    | mvc.18m              | gfx               |    1000004 | no  | 67aaf727 | e0e69104e31d2c41e18c0d24e9ab962406a7ca9a
# mvc.19m              |   4194304 |                      | good    | mvc.19m              | gfx               |          6 | no  | bcb72fc6 | 46ab98dcdf6f5d611646a22a7355939ef5b2bbe5
# mvc.20m              |   4194304 |                      | good    | mvc.20m              | gfx               |    1000006 | no  | 8b0bade8 | c5732361bb4bf284c4d12a82ac2c5750b1f9d441
# mvcj.03a             |    524288 |                      | good    |                      | maincpu           |          0 | no  | 3df18879 | 2b91da6e5dd792967337e873ebb08ecf5194a97b
# mvcj.04a             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 07d212e8 | c5420e9bd580910c1f1d0264240aeef20aac30a7
# mvscj.key            |        20 |                      | good    |                      | key               |          0 | no  | 9dedbcaf | 6468dd20ba89e4f6dc03340d218694690151ebe0

# mvscu
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# mvc.01               |    131072 |                      | good    | mvc.01               | audiocpu          |          0 | no  | 41629e95 | 36925c05b5fdcbe43283a882d021e5360c947061
# mvc.02               |    131072 |                      | good    | mvc.02               | audiocpu          |      28000 | no  | 963abf6b | 6b784870e338701cefabbbe4669984b5c4e8a9a5
# mvc.05a              |    524288 |                      | good    | mvc.05a              | maincpu           |     100000 | no  | 2d8c8e86 | b07d640a734c5d336054ed05195786224c9a6cd4
# mvc.06a              |    524288 |                      | good    | mvc.06a              | maincpu           |     180000 | no  | 8528e1f5 | cd065c05268ab581b05676da544baf6af642acac
# mvc.07               |    524288 |                      | good    | mvc.07               | maincpu           |     200000 | no  | c3baa32b | d35589847e0753e869ffcd7c3abed925bfdb0fa2
# mvc.08               |    524288 |                      | good    | mvc.08               | maincpu           |     280000 | no  | bc002fcd | 0b6735a071a9274f7ab25c743271fc30411fe819
# mvc.09               |    524288 |                      | good    | mvc.09               | maincpu           |     300000 | no  | c67b26df | 6e9969246c57269d7ba0992a5cc319c8910bf8a9
# mvc.10               |    524288 |                      | good    | mvc.10               | maincpu           |     380000 | no  | 0fdd1e26 | 5fa684d823b4f4eec61ed9e9b8938af5272ae1ed
# mvc.11m              |   4194304 |                      | good    | mvc.11m              | qsound            |          0 | no  | 850fe663 | 81e519d05a08855f242ea2e17ee0859b449db895
# mvc.12m              |   4194304 |                      | good    | mvc.12m              | qsound            |     400000 | no  | 7ccb1896 | 74caadf3282fcc6acffb1bbe3734106f81124121
# mvc.13m              |   4194304 |                      | good    | mvc.13m              | gfx               |          0 | no  | fa5f74bc | 79a619248938a85ce4f7794a704647b9cf564fbc
# mvc.14m              |   4194304 |                      | good    | mvc.14m              | gfx               |    1000000 | no  | 7f1df4e4 | ede92b31c1fe87f91b4fe74ac211f2fb5f863bc2
# mvc.15m              |   4194304 |                      | good    | mvc.15m              | gfx               |          2 | no  | 71938a8f | 6982f7203458c1c46a1c1c13c0d0f2a5e109d271
# mvc.16m              |   4194304 |                      | good    | mvc.16m              | gfx               |    1000002 | no  | 90bd3203 | ed83208c486ea0f407b7e5d16a8cf242a6f73774
# mvc.17m              |   4194304 |                      | good    | mvc.17m              | gfx               |          4 | no  | 92741d07 | ddfd70eab7c983ab452194b1860059f8ad694459
# mvc.18m              |   4194304 |                      | good    | mvc.18m              | gfx               |    1000004 | no  | 67aaf727 | e0e69104e31d2c41e18c0d24e9ab962406a7ca9a
# mvc.19m              |   4194304 |                      | good    | mvc.19m              | gfx               |          6 | no  | bcb72fc6 | 46ab98dcdf6f5d611646a22a7355939ef5b2bbe5
# mvc.20m              |   4194304 |                      | good    | mvc.20m              | gfx               |    1000006 | no  | 8b0bade8 | c5732361bb4bf284c4d12a82ac2c5750b1f9d441
# mvcu.03d             |    524288 |                      | good    |                      | maincpu           |          0 | no  | c6007557 | c027c1a204345ce611cb042d60939e4de156763f
# mvcu.04d             |    524288 |                      | good    |                      | maincpu           |      80000 | no  | 724b2b20 | 872bbcf5d344d634f3523318fa4763e6d6302bb5
# mvscu.key            |        20 |                      | good    |                      | key               |          0 | no  | a83db333 | 7f7288ceadf233d913728f7c4a8841adcb5994e8



    ################################################################################
    # The Punisher                                                                 #
    ################################################################################
    # CPS1 Game

# punisherj
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# bprg1.11d            |       279 |                      | good    | bprg1.11d            | bboardplds        |          0 | no  | 31793da7 | 400fa7ac517421c978c1ee7773c30b9ed0c5d3f3
# buf1                 |       279 |                      | good    | buf1                 | aboardplds        |          0 | no  | eb122de7 | b26b5bfe258e3e184f069719f9fd008d6b8f6b9b
# d7l1.7l              |       279 |                      | good    | d7l1.7l              | dboardplds        |          0 | no  | 27b7410d | 06d0cba0226850f100ff1f539bd7d5db0f90c730
# d8l1.8l              |       279 |                      | good    | d8l1.8l              | dboardplds        |          0 | no  | 539fc7da | cad5c91629c6247e49ccbbcbfe6b08229eafae07
# d9k2.9k              |       279 |                      | good    | d9k2.9k              | dboardplds        |          0 | no  | cd85a156 | a88f8939c5d93e65d7bcc0eb3ee5b6f4f1114e3a
# d10f1.10f            |       279 |                      | good    | d10f1.10f            | dboardplds        |          0 | no  | 6619c494 | 3aef656c07182a2186f810f30e0d854dd5bd8d18
# ioa1                 |       279 |                      | good    | ioa1                 | aboardplds        |          0 | no  | 59c7ee3b | fbb887c5b4f5cb8df77cec710eaac2985bc482a6
# iob1.12d             |       279 |                      | good    | iob1.12d             | bboardplds        |          0 | no  | 3abc0700 | 973043aa46ec6d5d1db20dc9d5937005a0f9f6ae
# ioc1.ic1             |       260 |                      | good    | ioc1.ic1             | cboardplds        |          0 | no  | a399772d | 55471189db573dd61e3087d12c55564291672c77
# prg2                 |       279 |                      | good    | prg2                 | aboardplds        |          0 | no  | 4386879a | c36896d169d8c78393609acbbe4397931292a033
# ps-1m.3a             |    524288 |                      | good    | ps-1m.3a             | gfx               |          0 | no  | 77b7ccab | e08e5d55a79e4c0c8ca819d6d7d2a14f753c6ec3
# ps-2m.4a             |    524288 |                      | good    | ps-2m.4a             | gfx               |          4 | no  | 64fa58d4 | d4a774285ed15273195b6b26d2965ce370e54e73
# ps-3m.5a             |    524288 |                      | good    | ps-3m.5a             | gfx               |          2 | no  | 0122720b | 5f0d3097e097f64106048156fbb0d343fe78fffa
# ps-4m.6a             |    524288 |                      | good    | ps-4m.6a             | gfx               |          6 | no  | 60da42c8 | 95eec4a58d9628a2d9764951dd8dc11e4860a899
# ps-5m.7a             |    524288 |                      | good    | ps-5m.7a             | gfx               |     200000 | no  | c54ea839 | 0733f37329edd9d0cace1319a7544b40aa7ecb0b
# ps-6m.8a             |    524288 |                      | good    | ps-6m.8a             | gfx               |     200004 | no  | a544f4cc | 9552df8934ba25f19a22f2e07783712d8c8ef03c
# ps-7m.9a             |    524288 |                      | good    | ps-7m.9a             | gfx               |     200002 | no  | 04c5acbd | fddc94b0f36d4d22d7c357856ae15b7514c342d3
# ps-8m.10a            |    524288 |                      | good    | ps-8m.10a            | gfx               |     200006 | no  | 8f02f436 | a2f0ebb7e9593469c7b843f8962a66f3d77f79e5
# ps-q1.1k             |    524288 |                      | good    | ps-q1.1k             | qsound            |          0 | no  | 31fd8726 | 1d73a76682e9fb908db0c55b9a18163f7539fea1
# ps-q2.2k             |    524288 |                      | good    | ps-q2.2k             | qsound            |      80000 | no  | 980a9eef | 36571381f349bc726508a7e618ba1c635ec9d271
# ps-q3.3k             |    524288 |                      | good    | ps-q3.3k             | qsound            |     100000 | no  | 0dd44491 | 903cea1d7f3120545ea3229d30fbd687d11ad68f
# ps-q4.4k             |    524288 |                      | good    | ps-q4.4k             | qsound            |     180000 | no  | bed42f03 | 21302f7e75f9c795392a3b34e16a959fc5f6e4e9
# ps63b.1a             |       279 |                      | good    | ps63b.1a             | bboardplds        |          0 | no  | 03a758b0 | f0035f0dac927af50e21f5c57b7b4462856aa50c
# ps_21.6f             |    524288 |                      | good    | ps_21.6f             | maincpu           |     100000 | no  | 8affa5a9 | 268760b83b1723ff50a019ec51ef7af2e49935bf
# ps_q.5k              |    131072 |                      | good    | ps_q.5k              | audiocpu          |          0 | no  | 49ff4446 | 87af12f87a940a6c5428b4574ad44a4b54867bc3
# psu_24.9e            |    131072 |                      | good    |                      | maincpu           |      80000 | no  | 1cfecad7 | f4dcf5066dc59507cece0c53ccc208e4323ae26f
# psu_25.10e           |    131072 |                      | good    |                      | maincpu           |      c0000 | no  | c51acc94 | 34ffd6392914e3e67d7d0804215bd1193846b554
# psu_26.11e           |    131072 |                      | good    |                      | maincpu           |          0 | no  | 9236d121 | 52d5d00009f61089157319943cde8f1a1ed48ad4
# psu_27.12e           |    131072 |                      | good    |                      | maincpu           |      40000 | no  | 61c960a1 | f8fe651283cc1f138d013cab65b833505de6df9f
# psu_28.9f            |    131072 |                      | good    |                      | maincpu           |      80001 | no  | bdf921c1 | 89a6709756c7c32e7c888806f983ce5af61cfcef
# psu_29.10f           |    131072 |                      | good    |                      | maincpu           |      c0001 | no  | 52dce1ca | 45277abe34feacdcaedaec56f513b7437d4260e9
# psu_30.11f           |    131072 |                      | good    |                      | maincpu           |          1 | no  | 8320e501 | bb3b74135df9dd494a277a1bc3bef2917351203f
# psu_31.12f           |    131072 |                      | good    |                      | maincpu           |      40001 | no  | 78d4c298 | 6e7fbaed9ad9230a6e5035c6eda64b2f1f83048c
# rom1                 |       279 |                      | good    | rom1                 | aboardplds        |          0 | no  | 41dc73b9 | 7d4c9f1693c821fbf84e32dd6ef62ddf14967845


# punisheru
# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# bprg1.11d            |       279 |                      | good    | bprg1.11d            | bboardplds        |          0 | no  | 31793da7 | 400fa7ac517421c978c1ee7773c30b9ed0c5d3f3
# buf1                 |       279 |                      | good    | buf1                 | aboardplds        |          0 | no  | eb122de7 | b26b5bfe258e3e184f069719f9fd008d6b8f6b9b
# d7l1.7l              |       279 |                      | good    | d7l1.7l              | dboardplds        |          0 | no  | 27b7410d | 06d0cba0226850f100ff1f539bd7d5db0f90c730
# d8l1.8l              |       279 |                      | good    | d8l1.8l              | dboardplds        |          0 | no  | 539fc7da | cad5c91629c6247e49ccbbcbfe6b08229eafae07
# d9k2.9k              |       279 |                      | good    | d9k2.9k              | dboardplds        |          0 | no  | cd85a156 | a88f8939c5d93e65d7bcc0eb3ee5b6f4f1114e3a
# d10f1.10f            |       279 |                      | good    | d10f1.10f            | dboardplds        |          0 | no  | 6619c494 | 3aef656c07182a2186f810f30e0d854dd5bd8d18
# ioa1                 |       279 |                      | good    | ioa1                 | aboardplds        |          0 | no  | 59c7ee3b | fbb887c5b4f5cb8df77cec710eaac2985bc482a6
# iob1.12d             |       279 |                      | good    | iob1.12d             | bboardplds        |          0 | no  | 3abc0700 | 973043aa46ec6d5d1db20dc9d5937005a0f9f6ae
# ioc1.ic1             |       260 |                      | good    | ioc1.ic1             | cboardplds        |          0 | no  | a399772d | 55471189db573dd61e3087d12c55564291672c77
# prg2                 |       279 |                      | good    | prg2                 | aboardplds        |          0 | no  | 4386879a | c36896d169d8c78393609acbbe4397931292a033
# ps-q1.1k             |    524288 |                      | good    | ps-q1.1k             | qsound            |          0 | no  | 31fd8726 | 1d73a76682e9fb908db0c55b9a18163f7539fea1
# ps-q2.2k             |    524288 |                      | good    | ps-q2.2k             | qsound            |      80000 | no  | 980a9eef | 36571381f349bc726508a7e618ba1c635ec9d271
# ps-q3.3k             |    524288 |                      | good    | ps-q3.3k             | qsound            |     100000 | no  | 0dd44491 | 903cea1d7f3120545ea3229d30fbd687d11ad68f
# ps-q4.4k             |    524288 |                      | good    | ps-q4.4k             | qsound            |     180000 | no  | bed42f03 | 21302f7e75f9c795392a3b34e16a959fc5f6e4e9
# ps63b.1a             |       279 |                      | good    | ps63b.1a             | bboardplds        |          0 | no  | 03a758b0 | f0035f0dac927af50e21f5c57b7b4462856aa50c
# ps_01.3a             |    524288 |                      | good    | ps-1m.3a             | gfx               |          0 | no  | 77b7ccab | e08e5d55a79e4c0c8ca819d6d7d2a14f753c6ec3
# ps_02.4a             |    524288 |                      | good    | ps-3m.5a             | gfx               |          2 | no  | 0122720b | 5f0d3097e097f64106048156fbb0d343fe78fffa
# ps_03.5a             |    524288 |                      | good    | ps-2m.4a             | gfx               |          4 | no  | 64fa58d4 | d4a774285ed15273195b6b26d2965ce370e54e73
# ps_04.6a             |    524288 |                      | good    | ps-4m.6a             | gfx               |          6 | no  | 60da42c8 | 95eec4a58d9628a2d9764951dd8dc11e4860a899
# ps_05.7a             |    524288 |                      | good    | ps-5m.7a             | gfx               |     200000 | no  | c54ea839 | 0733f37329edd9d0cace1319a7544b40aa7ecb0b
# ps_06.8a             |    524288 |                      | good    | ps-7m.9a             | gfx               |     200002 | no  | 04c5acbd | fddc94b0f36d4d22d7c357856ae15b7514c342d3
# ps_07.9a             |    524288 |                      | good    | ps-6m.8a             | gfx               |     200004 | no  | a544f4cc | 9552df8934ba25f19a22f2e07783712d8c8ef03c
# ps_08.10a            |    524288 |                      | good    | ps-8m.10a            | gfx               |     200006 | no  | 8f02f436 | a2f0ebb7e9593469c7b843f8962a66f3d77f79e5
# ps_q.5k              |    131072 |                      | good    | ps_q.5k              | audiocpu          |          0 | no  | 49ff4446 | 87af12f87a940a6c5428b4574ad44a4b54867bc3
# psj_21.6f            |    524288 |                      | good    | ps_21.6f             | maincpu           |     100000 | no  | 8affa5a9 | 268760b83b1723ff50a019ec51ef7af2e49935bf
# psj_22.7f            |    524288 |                      | good    |                      | maincpu           |      80000 | no  | e01036bc | a01886014dabe8f9ab45619865c6bd9f27472eae
# psj_23.8f            |    524288 |                      | good    |                      | maincpu           |          0 | no  | 6b2fda52 | 5f95a79b7b802609ae9ddd6641cc52610d428bf4
# rom1                 |       279 |                      | good    | rom1                 | aboardplds        |          0 | no  | 41dc73b9 | 7d4c9f1693c821fbf84e32dd6ef62ddf14967845


    ################################################################################
    # Marvel vs Capcom 2                                                           #
    ################################################################################
    # NAOMI Game
    # - Audio has been heavily reworked
    #   - Sound effects are in the g050 in PCM WAV files
    #   - BGM is in nativeDX11x64/sound/bgm/mvc2 in Voribis Ogg files
    # - At least SOME ROM data appears to be missing - likely the audio data


# NAME                 |      SIZE | BIOS                 | STATUS  | MERGE                | REGION            |     OFFSET | OPT | CRC      | SHA1                                    
# ---------------------+-----------+----------------------+---------+----------------------+-------------------+------------+-----+----------+-----------------------------------------
# 315-6188.ic31        |      8244 |                      | good    | 315-6188.ic31        | altera_pof        |          0 | no  | 7c9fea46 | f77c07ae65dfed18c1c4c632c8945be21d02ddaf    Missing
# boot_rom_64b8.ic606  |    524288 | bios21               | good    | boot_rom_64b8.ic606  | maincpu           |          0 | no  | 7a50fab9 | ef79f448e0bf735d1264ad4f051d24178822110f
# develop.ic27         |   2097152 | bios23               | good    | develop.ic27         | maincpu           |          0 | no  | 309a196a | 409b50371feb648f10efd6b7ac420bf08d9a3b5a
# develop110.ic27      |   2097152 | bios22               | good    | develop110.ic27      | maincpu           |          0 | no  | de7cfdb0 | da16800edc4d49f70481c124d487f544c2fa8ce7
# epr-21336a.ic27      |   2097152 | bios26               | baddump | epr-21336a.ic27      | maincpu           |          0 | no  | d3d57af8 | 0eb72c2a20ad8b86d442b77760eab5e89521d469
# epr-21576.ic27       |   2097152 | bios7                | good    | epr-21576.ic27       | maincpu           |          0 | no  | 9dad3495 | 5fb66f9a2b68d120f059c72758e65d34f461044a
# epr-21576a.ic27      |   2097152 | bios6                | good    | epr-21576a.ic27      | maincpu           |          0 | no  | cedfe439 | f27798bf3d890863ef0c1d9dcb4e7782249dca27
# epr-21576b.ic27      |   2097152 | bios5                | good    | epr-21576b.ic27      | maincpu           |          0 | no  | 755a6e07 | 7e8b8ccfc063144d89668e7224dcd8a36c54f3b3
# epr-21576c.ic27      |   2097152 | bios4                | baddump | epr-21576c.ic27      | maincpu           |          0 | no  | 4599ad13 | 7e730e9452a792d76f210c33a955d385538682c7
# epr-21576d.ic27      |   2097152 | bios3                | good    | epr-21576d.ic27      | maincpu           |          0 | no  | 3b2afa7b | d007e1d321c198a38c5baff86eb2ab84385d150a
# epr-21576e.ic27      |   2097152 | bios2                | good    | epr-21576e.ic27      | maincpu           |          0 | no  | 08c0add7 | e7c1a7673cb2ccb21748ef44105e46d1bad7266d
# epr-21576g.ic27      |   2097152 | bios1                | good    | epr-21576g.ic27      | maincpu           |          0 | no  | d2a1c6bf | 6d27d71aec4dfba98f66316ae74a1426d567698a
# epr-21576h.ic27      |   2097152 | bios0                | good    | epr-21576h.ic27      | maincpu           |          0 | no  | d4895685 | 91424d481ff99a8d3f4c45cea6d3f0eada049a6d
# epr-21576h_multi.ic27 |   2097152 | bios25               | good    | epr-21576h_multi.ic27 | maincpu           |          0 | no  | cce01f1f | cca17119ad13e3a4ef7cb6902a37b65d6a844aee
# epr-21577a.ic27      |   2097152 | bios18               | good    | epr-21577a.ic27      | maincpu           |          0 | no  | 969dc491 | 581d1eae328b87b67508a7586ffc60cee256f70f
# epr-21577d.ic27      |   2097152 | bios17               | good    | epr-21577d.ic27      | maincpu           |          0 | no  | 60ddcbbe | 58b15096d269d6df617ca1810b66b47deb184958
# epr-21577e.ic27      |   2097152 | bios16               | good    | epr-21577e.ic27      | maincpu           |          0 | no  | cf36e97b | b085305982e7572e58b03a9d35f17ae319c3bbc6
# epr-21577g.ic27      |   2097152 | bios15               | good    | epr-21577g.ic27      | maincpu           |          0 | no  | 25f64af7 | 99f9e6cc0642319bd2da492611220540add573e8
# epr-21577h.ic27      |   2097152 | bios14               | good    | epr-21577h.ic27      | maincpu           |          0 | no  | fdf17452 | 5f3e4b677f0046ce690a4f096b0481e5dd8bb6e6
# epr-21578a.ic27      |   2097152 | bios13               | good    | epr-21578a.ic27      | maincpu           |          0 | no  | 6c9aad83 | 555918de76d8dbee2a97d8a95297ef694b3e803f
# epr-21578d.ic27      |   2097152 | bios12               | good    | epr-21578d.ic27      | maincpu           |          0 | no  | dfd5f42a | 614a0db4743a5e5a206190d6786ade24325afbfd
# epr-21578e.ic27      |   2097152 | bios11               | good    | epr-21578e.ic27      | maincpu           |          0 | no  | 087f09a3 | 0418eb2cf9766f0b1b874a4e92528779e22c0a4a
# epr-21578f.ic27      |   2097152 | bios10               | good    | epr-21578f.ic27      | maincpu           |          0 | no  | 628a27fd | dae7add616b1a2478f00608823e88c3b82a0e78f
# epr-21578g.ic27      |   2097152 | bios9                | good    | epr-21578g.ic27      | maincpu           |          0 | no  | 55413214 | bd2748365a9fc1821c9369aa7155d7c41c4df43e
# epr-21578h.ic27      |   2097152 | bios8                | good    | epr-21578h.ic27      | maincpu           |          0 | no  | 7b452946 | 8e9f153bbada24b37066dc45b64a7bf0d4f26a9b
# epr-21579.ic27       |   2097152 | bios20               | good    | epr-21579.ic27       | maincpu           |          0 | no  | 71f9c918 | d15af8b947f41eea7c203b565cd403e3f37a2017
# epr-21579d.ic27      |   2097152 | bios19               | good    | epr-21579d.ic27      | maincpu           |          0 | no  | 33513691 | b1d8c7c516e1471a788fcf7a02a794ad2f05aeeb
# epr-23062a.ic22      |   4194304 |                      | good    |                      | rom_board         |          0 | no  | 96038276 | 877ba02c92082567280afcb1ae40b3bbfc8a63e8
# main_eeprom.bin      |       128 |                      | good    | main_eeprom.bin      | main_eeprom       |          0 | no  | fea29cbb | 4099f1747aafa07db34f6e072cd9bfaa83bae10e
# mpr-23048.ic1        |   8388608 |                      | good    | mpr-23048.ic17s      | rom_board         |     800000 | no  | 93d7a63a | c50d10b4a3f9db51eae5749f5b665d7c8ab6c898     Missing
# mpr-23049.ic2        |   8388608 |                      | good    | mpr-23049.ic18       | rom_board         |    1000000 | no  | 003dcce0 | fb71c8ca9271d2155878c72d8fe2df3031e6c014     Missing
# mpr-23050.ic3        |   8388608 |                      | good    | mpr-23050.ic19s      | rom_board         |    1800000 | no  | 1d6b88a7 | ba42e9d1d912d88a7ad839b878975ba590634320     Missing
# mpr-23051.ic4        |   8388608 |                      | good    | mpr-23051.ic20       | rom_board         |    2000000 | no  | 01226aaa | a4c6a0eda05e53d0e51b92a4317a86a708a7efdb     Incomplete: 0x001E7C60 in known good is at 0x00392840 is this dump, but prior is missing
# mpr-23052.ic5        |   8388608 |                      | good    | mpr-23052.ic21s      | rom_board         |    2800000 | no  | 74bee120 | 5a0fb48fa758a2be2e08e3b1298103c5aa748835     0x00A22FC0  ???
# mpr-23053.ic6        |   8388608 |                      | good    | mpr-23053.ic22       | rom_board         |    3000000 | no  | d92d4401 | a868780f8d2e176ff10781e1c08bf932f34ac504     0x01225B00  ???
# mpr-23054.ic7        |   8388608 |                      | good    | mpr-23054.ic23s      | rom_board         |    3800000 | no  | 78ba02e8 | 0f696a33e1e6671001efc309ed62f084a246ad24     0x01A27060  ???
# mpr-23055.ic8        |   8388608 |                      | good    | mpr-23055.ic24       | rom_board         |    4000000 | no  | 84319604 | c3dde162e043a54e1325202b46191b32e8784a1c     0x022296A0  ???
# mpr-23056.ic9        |   8388608 |                      | good    | mpr-23056.ic25s      | rom_board         |    4800000 | no  | d7386034 | be1f3ca5f283e428dc59dc072de3e7d36e122d53     0x02A2D100  Has cut-out blanks
# mpr-23057.ic10       |   8388608 |                      | good    | mpr-23057.ic26       | rom_board         |    5000000 | no  | a3f087db | b52d7c072cb5c2fdd10d0ac0b62cebe48b229ae3     0x0322F220
# mpr-23058.ic11       |   8388608 |                      | good    | mpr-23058.ic27s      | rom_board         |    5800000 | no  | 61a6cc5d | 34e52cb076888313a80f2b87876b8d37b91d85a0     0x03A314E0
# mpr-23059.ic12s      |   8388608 |                      | good    | mpr-23059.ic28       | rom_board         |    6000000 | no  | 64808024 | 1a6c60c330642b273978d3dd02d95d17d36ee3f2     0x04292A60
# mpr-23060.ic13s      |   8388608 |                      | good    | mpr-23060.ic29       | rom_board         |    6800000 | no  | 67519942 | fc758d9075625f8140d5d828c8f6b7a91bcc9119     0x04A679C0
# mpr-23061.ic14s      |   8388608 |                      | good    | mpr-23061.ic30s      | rom_board         |    7000000 | no  | fb1844c4 | 1d1571516a6dbed0c4ded3b80efde9cc9281f66f     0x05F1A2A0
# sflash.ic37          |       132 |                      | good    |                      | some_eeprom       |          0 | no  | 37a66f3c | df6cd2cdc2813caa5da4dc9f171998485bcbdc44     Missing
# x76f100_eeprom.bin   |       132 |                      | good    | x76f100_eeprom.bin   | naomibd_eeprom    |          0 | no  | 3ea24b6a | 3a730ebcf56e0060fef6b1b02eb2eb7cfb7e61dc
# zukinver0930.ic25    |   2097152 | bios24               | good    | zukinver0930.ic25    | maincpu           |          0 | no  | 58e17c23 | 19330f906accf1b859f56bbcedc2edff73747599


