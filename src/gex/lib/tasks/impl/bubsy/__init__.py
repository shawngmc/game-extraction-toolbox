'''Implementation of bubsy: Bubsy Two-Fur'''
from gex.lib.tasks.copytask import CopyTask
from gex.lib.tasks import helpers

class BubsyTask(CopyTask):
    '''Implements bubsy: Bubsy Two-Fur'''
    _task_name = "bubsy"
    _title = "Bubsy Two-Fur"
    _details_markdown = '''
These are the ROMs just sitting in the install folder. 
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Bubsy Two-Fur")
    _input_folder_desc = "Bubsy Two-Fur Steam Folder"
