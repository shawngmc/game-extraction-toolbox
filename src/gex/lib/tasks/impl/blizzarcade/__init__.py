'''Implementation of blizzarcade: Blizzard Arcade Collection'''
from gex.lib.tasks.copytask import CopyTask
from gex.lib.tasks import helpers

class BubsyTask(CopyTask):
    '''Implements blizzarcade: Blizzard Arcade Collection'''
    _task_name = "blizzarcade"
    _title = "Blizzard Arcade Collection"
    _details_markdown = '''
These are the ROMs just sitting in the install folder. 
    '''
    _default_input_folder = r"C:\Program Files (x86)\Blizzard Arcade Collection"
    _input_folder_desc = "Blizzard Arcade Collection install folder"
