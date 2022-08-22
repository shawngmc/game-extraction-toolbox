import click
from rich.console import Console
from rich.markdown import Markdown

from gex.lib.utils import helper

@click.command()
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
def details(task):
    """Get details about a specific extraction task"""

    task_class = helper.load_task(task)
    if task_class is None:
        raise Exception(f"Task {task} not found to describe.")

    markdown_text = task_class.get_header_markdown()
    markdown_text += "\n\n"
    markdown_text += task_class.get_details_markdown()
    console = Console()
    formatted_text = Markdown(markdown_text)
    console.print(formatted_text)
