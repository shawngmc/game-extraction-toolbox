'''Template task to implment tasks with'''
import logging

from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class MyTask(BaseTask):
    '''Implments xxxxxx: Xxxx Xxxx Xxxx'''
    _task_name = ""
    _title = ""
    _details_markdown = '''

    '''
    _default_input_folder = r""
    _input_folder_desc = ""


    def execute(self, in_dir, out_dir):
        '''Main implementation call for the extraction task'''
        logger.info("Processing complete.")
