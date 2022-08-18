
class BaseTask:
    _task_name = None
    _title = None
    _details_markdown = None
    _default_input_folder = None
    _input_folder_desc = None
    _short_description = None

    def get_task_name(self):
        return self._task_name

    def get_details_markdown(self):
        return self._details_markdown

    def get_title(self):
        return self._title

    def get_short_description(self):
        return self._short_description

    def get_default_input_folder(self):
        return self._default_input_folder

    def get_input_folder_description(self):
        return self._input_folder_desc

    def get_header_markdown(self):
        markdown_text = f'# {self.get_task_name()}: {self.get_title()}\n'
        if len(self.get_short_description()) > 0:
            markdown_text += f'  {self.get_short_description()}\n\n'
        markdown_text += f'  Expected input dir: {self.get_input_folder_description()} (ex. "{self.get_default_input_folder()}")\n'
        return markdown_text

    def find_handler_func(self, package_name):
        if f'_handle_{package_name}' in dir(self):
            return getattr(self, f'_handle_{package_name}')
        return None

    def execute(self, in_dir, out_dir):
        pass
