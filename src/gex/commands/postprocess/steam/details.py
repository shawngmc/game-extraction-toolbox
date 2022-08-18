import os
import click
from rich.console import Console
from rich.markdown import Markdown

@click.command()
@click.option('--task', 'task', help = 'name of the transform set to run', required=True)
def details(task):
    """Get details about a specific Steam extraction task"""

    # logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    md_path = os.path.join(dir_path, "..", "..", "..", "lib", "transforms", f'{task}.md')
    if not os.path.exists(md_path):
        print(md_path)
        raise Exception("Task not found to describe.")
    else:
        with open(md_path, "r") as curr_file:
            file_content = curr_file.read()
            console = Console()
            md = Markdown(file_content)
            console.print(md)
