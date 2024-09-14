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

    ################################################################################
    # Marvel Super Heroes                                                          #
    ################################################################################
    # CPS2 Game

    ################################################################################
    # X-Men vs. Street Fighter                                                     #
    ################################################################################
    # CPS2 Game

    ################################################################################
    # Marvel Super Heroes vs. Street Fighter                                       #
    ################################################################################
    # CPS2 Game

    ################################################################################
    # Marvel vs. Capcom                                                            #
    ################################################################################
    # CPS2 Game

    ################################################################################
    # The Punisher                                                                 #
    ################################################################################
    # CPS1 Game

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


