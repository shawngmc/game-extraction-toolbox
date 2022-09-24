import click
from rich.console import Console
from rich.markdown import Markdown
from texttable import Texttable
from gex.lib.utils import helper

@click.command()
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
def details(task):
    """Get details about a specific extraction task"""

    task_class = helper.load_task(task)
    if task_class is None:
        raise Exception(f"Task {task} not found to describe.")

    markdown_text = get_header_display(task_class)
    markdown_text += "\n\n"
    markdown_text += task_class.get_details_markdown()
    markdown_text += "\n\n"
    console = Console()
    formatted_text = Markdown(markdown_text)
    console.print(formatted_text)
    print(get_output_display(task_class))
    prop_table = get_prop_display(task_class)
    if prop_table:
        print(prop_table)


def get_header_display(task_class):
    '''Get a markdown-formatted header for this task for help, etc.'''
    markdown_text = f'# {task_class.get_task_name()}: {task_class.get_title()}\n'
    markdown_text += f'  Expected input dir: {task_class.get_input_folder_description()}\n\n'
    markdown_text += f'  Default input dir: "{task_class.get_default_input_folder()}"\n'
    return markdown_text

def get_output_display(task_class):
    '''Get a display table for the output files for this task'''
    out_file_info = task_class.get_out_file_info()
    table = Texttable()
    table.add_row(["Game", "System", "Status", "Filename", "Notes"])
    for item in out_file_info['files']:
        notes = " ".join([str(note) for note in item['notes']])
        table.add_row([item['game'], item['system'], item['status'], item['filename'], notes])
    output = table.draw()

    if out_file_info['notes']:
        output += "\n\n"
        for key, value in out_file_info['notes'].items():
            output += f"{key}: {value}\n"

    return output

def get_prop_display(task_class):
    '''Get a display table for the props available for this task'''
    if not task_class.get_prop_info():
        return None

    table = Texttable()
    table.add_row(["Name", "Type", "Default", "Description"])
    for key, value in task_class.get_prop_info().items():
        table.add_row([key, value['type'], str(value['default']), value['description']])
    return table.draw()
