'''Implementation of ags_mspacman: Namco Arcade Game Series: Ms. Pac-Man'''
import logging
from gex.lib.tasks.zipsplicetask import ZipSpliceTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSMsPacManTask(ZipSpliceTask):
    '''Implements ags_mspacman: Namco Arcade Game Series: Ms. Pac-Man'''
    _task_name = "ags_mspacman"
    _title = "Namco Arcade Game Series: Ms. Pac-Man"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL, and is not yet a playable ROM.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("Ms. PAC-MAN")
    _input_folder_desc = "AGS Ms. Pac-Man install folder"
