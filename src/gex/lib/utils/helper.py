'''Contains more generic utility functions'''

import importlib
import inspect
import os

from gex.lib.tasks.basetask import BaseTask

def cleanpath(path_str):
    '''Clean the double-quotes from a path'''
    if path_str.startswith("\""):
        path_str = path_str[1:]
    if path_str.endswith("\""):
        path_str = path_str[:-1]
    return path_str

def preparepath(out_path):
    '''Make sure the output folder exists and is writable or can be created'''
    if not os.path.exists(out_path):
        try:
            os.makedirs(out_path)
        except OSError as error:
            raise Exception("Cannot create output folder.") from error
    else:
        if not os.access(out_path, os.W_OK):
            raise Exception("Cannot write to output folder.")

def load_task(task):
    '''Load a task module's task class from the task name'''
    package = f'gex.lib.tasks.impl.{task}'
    transform_module = importlib.import_module(package)
    clsmembers = inspect.getmembers(transform_module, inspect.isclass)
    for name, typedef in clsmembers:
        if not name == 'BaseTask' and issubclass(typedef, BaseTask):
            return typedef()
    return None

def get_task_names():
    pass
