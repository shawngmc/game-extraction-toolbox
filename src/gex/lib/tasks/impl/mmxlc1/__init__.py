'''Implementation of mmxlc1: Mega Man X Legacy Collection 1'''
from gex.lib.tasks.splicetask import SpliceTask
from gex.lib.tasks import helpers

class MegaManXLegacyCollection1Task(SpliceTask):
    '''Implements mmxlc1: Mega Man X Legacy Collection 1'''
    _task_name = "mmxlc1"
    _title = "Mega Man X Legacy Collection 1"
    _details_markdown = '''
Based on: https://github.com/s3phir0th115/MMXLC1-Rom-Extractor/blob/master/mmxlc_rom_extract.py

Mega Man X4 does not appear to be ROM based, but investigation is ongoing.
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("Mega Man X Legacy Collection")
    _input_folder_desc = "Steam MMxLC install folder"
