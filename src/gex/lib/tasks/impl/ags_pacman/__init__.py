'''Implementation of ags_pacman: Namco Arcade Game Series: Pac-Man'''
import logging
from gex.lib.tasks.zipsplicetask import ZipSpliceTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSPacManTask(ZipSpliceTask):
    '''Implements ags_pacman: Namco Arcade Game Series: Pac-Man'''
    _task_name = "ags_pacman"
    _title = "Namco Arcade Game Series: Pac-Man"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("PAC-MAN")
    _input_folder_desc = "AGS Pac-Man install folder"
