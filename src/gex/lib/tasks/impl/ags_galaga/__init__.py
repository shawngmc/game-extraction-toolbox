'''Implementation of ags_galaga: Namco Arcade Game Series: Galaga'''
import logging
from gex.lib.tasks.zipsplicetask import ZipSpliceTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSGalagaTask(ZipSpliceTask):
    '''Implements ags_galaga: Namco Arcade Game Series: Galaga'''
    _task_name = "ags_galaga"
    _title = "Namco Arcade Game Series: Galaga"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("GALAGA")
    _input_folder_desc = "AGS Galaga install folder"
