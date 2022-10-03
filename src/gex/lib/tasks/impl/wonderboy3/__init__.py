'''Implementation of wonderboy3: Wonder Boy The Dragon's Trap'''
from gex.lib.tasks.copytask import CopyTask
from gex.lib.tasks import helpers

class WonderBoyTask(CopyTask):
    '''Implements wonderboy3: Wonder Boy The Dragon's Trap'''
    _task_name = "wonderboy3"
    _title = "Wonder Boy The Dragon's Trap"
    _details_markdown = '''
This is just sitting in the install folder. 

Note that the white box instead of the Sega logo is an intentional change for this release.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Wonder Boy The Dragon's Trap")
    _input_folder_desc = "Wonder Boy The Dragon's Trap Steam Folder"
