import logging

from gex.lib.tasks.basetask import BaseTask

logger = logging.getLogger('gextoolbox')

class MyTask(BaseTask):
    _task_name = ""
    _title = ""
    _details_markdown = '''

    '''
    _default_input_folder = r""
    _input_folder_desc = ""
    _short_description = ""


    def execute(self, in_dir, out_dir):
        logger.info("Processing complete.")
