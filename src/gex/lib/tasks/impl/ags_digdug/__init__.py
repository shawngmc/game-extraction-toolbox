'''Implementation of ags_digdug: Namco Arcade Game Series: Dig Dug'''
import logging
from gex.lib.tasks.zipsplicetask import ZipSpliceTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class AGSDigDugTask(ZipSpliceTask):
    '''Implements ags_digdug: Namco Arcade Game Series: Dig Dug'''
    _task_name = "ags_digdug"
    _title = "Namco Arcade Game Series: Dig Dug"
    _details_markdown = '''
Based on: https://github.com/farmerbb/RED-Project/blob/master/ROM%20Extraction/namco-ags-extract.sh

These are pulled out of the plugin DLL.
    '''
    _default_input_folder = helpers.gen_steam_app_default_folder("DIG DUG")
    _input_folder_desc = "AGS Dig Dug install folder"
