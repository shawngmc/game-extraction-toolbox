'''Containes the BaseTask class, the base class for tasks'''
class BaseTask:
    '''Base class for rom extraction tasks'''
    _task_name = None
    _title = None
    _details_markdown = None
    _default_input_folder = None
    _input_folder_desc = None
    _short_description = None

    def get_task_name(self):
        '''Get the task name, a short string for referring to the task'''
        return self._task_name

    def get_details_markdown(self):
        '''Get markdown for the details/help docs for this task'''
        return self._details_markdown

    def get_title(self):
        '''Get the nicely formatted name of this task'''
        return self._title

    def get_short_description(self):
        '''Get a short description/note for this task'''
        return self._short_description

    def get_default_input_folder(self):
        '''Get the default input folder for this task'''
        return self._default_input_folder

    def get_input_folder_description(self):
        '''Get a short description of what the input folder should refer to'''
        return self._input_folder_desc

    def get_header_markdown(self):
        '''Get a markdown-formatted header for this task for help, etc.'''
        markdown_text = f'# {self.get_task_name()}: {self.get_title()}\n'
        if len(self.get_short_description()) > 0:
            markdown_text += f'  {self.get_short_description()}\n\n'
        markdown_text += f'  Expected input dir: {self.get_input_folder_description()} '
        markdown_text += f' (ex. "{self.get_default_input_folder()}")\n'
        return markdown_text

    def find_handler_func(self, package_name):
        '''Utility function to look for a sub-package handler in a task'''
        if f'_handle_{package_name}' in dir(self):
            return getattr(self, f'_handle_{package_name}')
        return None

    def execute(self, in_dir, out_dir):
        '''Main implementation call for the extraction task'''
