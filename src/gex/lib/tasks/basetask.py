'''Containes the BaseTask class, the base class for tasks'''

import copy

class BaseTask:
    '''Base class for rom extraction tasks'''
    _task_name = None
    _title = None
    _details_markdown = None
    _default_input_folder = None
    _input_folder_desc = None
    _out_file_list = []
    _out_file_notes = {}
    _prop_info = {}
    _props = {}

    def __init__(self):
        for prop_key, prop_value in self._prop_info.items():
            self._props[prop_key] = prop_value['default']

    def set_props(self, in_props):
        '''Set any additional props for this task'''
        for value in in_props:
            print(value)
            if '=' in value:
                key, value = value.split('=')
            else:
                key = value
            self._props[key] = value

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": copy.deepcopy(self._out_file_list),
            "notes": copy.deepcopy(self._out_file_notes)
        }

    def get_prop_info(self):
        '''Return a list of available props'''
        return copy.deepcopy(self._prop_info)

    def get_task_name(self):
        '''Get the task name, a short string for referring to the task'''
        return self._task_name

    def get_details_markdown(self):
        '''Get markdown for the details/help docs for this task'''
        return self._details_markdown

    def get_title(self):
        '''Get the nicely formatted name of this task'''
        return self._title

    def get_default_input_folder(self):
        '''Get the default input folder for this task'''
        return self._default_input_folder

    def get_input_folder_description(self):
        '''Get a short description of what the input folder should refer to'''
        return self._input_folder_desc

    def find_handler_func(self, package_name):
        '''Utility function to look for a sub-package handler in a task'''
        if f'_handle_{package_name}' in dir(self):
            return getattr(self, f'_handle_{package_name}')
        return None

    def execute(self, in_dir, out_dir):
        '''Main implementation call for the extraction task'''
