'''Implemntation of disneyac: Disney Afternoon Collection'''
from gex.lib.tasks.splicetask import SpliceTask
from gex.lib.tasks import helpers

class DisneyAfternoonCollectionTask(SpliceTask):
    '''Implemnts disneyac: Disney Afternoon Collection'''
    _task_name = "disneyac"
    _title = "Disney Afternoon Collection"
    _details_markdown = '''
Based on MMLC & DAC Extractor - https://github.com/HTV04/mmlc-dac-extractor
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("DisneyAfternoon")
    _input_folder_desc = "DisneyAfternoon Folder (Steam install folder)"
