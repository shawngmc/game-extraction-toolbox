import os
import click
import psutil

@click.command()
@click.option('--target', 'target_dir',
    help = 'path to directory of files to search for', required=True)
@click.option('--search', 'search_dir',
    help = 'path to directory of files to search within', required=True)
def bulk(target_dir, search_dir):
    """CLI tool to find target files w/offsets within the files of a search path"""

    file_cache = {}

    def precache_file(file_path):
        file_data = read_bin_file(file_path)
        file_cache[file_path] = file_data

    def read_bin_file(path):
        try:
            with open(path, "rb") as file:
                content = file.read()
                return content
        except IOError:
            print('Error While Opening the file!')

    def find_match(archive_content, sub_content):
        for i in range(0x0, len(archive_content) - len(sub_content)):
            if archive_content[i] == sub_content[0]:
                valid = True
                for j in range(0, len(sub_content)-1):
                    if archive_content[i+j] != sub_content[j]:
                        valid = False
                        break
                if valid:
                    return {'start': i, 'end': i+len(sub_content)}
        return None

    def list_child_files(child_path):
        child_files = []
        for (_, _, filenames) in os.walk(child_path):
            for filename in filenames:
                child_files.append(os.path.join(child_path, filename))
            break
        return child_files

    def memory_usage():
        process = psutil.Process(os.getpid())
        print(f"Using {process.memory_info().rss} bytes...")  # in bytes

    search_files = list_child_files(search_dir)
    target_files = list_child_files(target_dir)

    matches = []

    print("Precaching...")
    for target_file in target_files:
        print(f" Precaching {target_file}...")
        precache_file(target_file)

    print("After caching:")
    memory_usage()

    print("Searching...")
    for search_file in search_files:
        print(f" Searching {search_file}...")
        search_content = read_bin_file(search_file)

        for target_file in target_files:
            target_content = file_cache[target_file]
            match = find_match(search_content, target_content)
            if match is None:
                print(f"  No match found for {target_file}")
            else:
                print(f"  Match for {target_file} from {hex(match['start'])} to {hex(match['end'])}!")
                matches.append(match)
            memory_usage()
