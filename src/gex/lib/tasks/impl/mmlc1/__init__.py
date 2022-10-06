'''Implementation of mmlc1: Mega Man Legacy Collection 1'''
from gex.lib.tasks.splicetask import SpliceTask
from gex.lib.tasks import helpers

class MegaManLegacyCollection1Task(SpliceTask):
    '''Implements mmlc1: Mega Man Legacy Collection 1'''
    _task_name = "mmlc1"
    _title = "Mega Man Legacy Collection 1"
    _details_markdown = '''
Based on MMLC & DAC Extractor - https://github.com/HTV04/mmlc-dac-extractor
'''
    _default_input_folder = helpers.gen_steam_app_default_folder("Suzy")
    _input_folder_desc = "'Suzy' Folder (Steam MMLC install folder)"
