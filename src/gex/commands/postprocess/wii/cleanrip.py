import os
import re
import zlib
import click

def list_files(list_dir):
    files = []
    for (_, _, filenames) in os.walk(list_dir):
        for filename in filenames:
            files.append(os.path.join(dir, filename))
        break
    return files

@click.command()
@click.option('--srcdir', 'src_dir', 
    help='path to directory with cleanrip output files', required=True)
@click.option('--destdir', 'dest_dir', 
    help='path to send reassembled, verified ROMs to', required=True)
def cleanrip(src_dir, dest_dir):
    """Clean up Cleanrip dumps"""

    print("NYI")
    # List files in output dir
    src_files = list_files(src_dir)

    # Build output sets
    sets = dict()
    for src_file in src_files:
        print(f"Handling {src_file}...")
        filename = os.path.basename(src_file)

        # Get the disc ID and find/make the set object
        disc_id_match = re.match("([A-Z0-9]{6})", filename)
        if disc_id_match is not None:
            disc_id = disc_id_match.group(0)
            current_set = None
            if disc_id in sets:
                current_set = sets[disc_id]
            else:
                current_set = dict()
                sets[disc_id] = current_set

            if filename.endswith(".bca"):
                current_set["bca"] = filename
            elif filename.endswith("-dumpinfo.txt"):
                current_set["dumpinfo"] = filename
            else:
                part_match = re.search("(?<=part)(\d)(?=.iso\Z)", filename)
                if part_match is not None:
                    part_array = None
                    if "parts" in current_set:
                        part_array = current_set["parts"]
                    else:
                        part_array = []
                        current_set["parts"] = part_array
                    part_array.append(filename)
        else:
            print(
                f"Skipping {filename} since it doesn't match name pattern...")

    # Verify valid sets
    invalid_set_keys = []
    for set_id, current_set in sets.items():
        if not "dumpinfo" in current_set:
            # We need a dumpinfo to get data
            print(f"No dumpinfo for set {set_id} - skipping set!")
            invalid_set_keys.append(set_id)
        else:
            # Check the part array for continuity
            part_array = current_set["parts"]
            part_array.sort()
            for part_idx, part_filename in enumerate(part_array):
                if part_filename != f"{set_id}.part{part_idx}.iso":
                    print(
                        f"{set_id}: {part_idx} found {part_filename}, which is incorrct; skipping set!")
                    invalid_set_keys.append(set_id)
                    break

    for invalid_set_key in invalid_set_keys:
        del sets[invalid_set_key]

    # Get game name and hash from XXXXXX-dumpinfo.txt
    for set_id, current_set in sets.items():
        print(current_set)
        with open(os.path.join(src_dir, current_set["dumpinfo"])) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            print(lines)
            for line in lines:
                if line.startswith("Internal Name: "):
                    current_set["name"] = line[len("Internal Name: "):]
                    safename = current_set["name"]
                    safename = re.sub(r' +', '_', safename)
                    safename = re.sub(r'[\W]+', '', safename)
                    current_set["safename"] = safename
                elif line.startswith("CRC32: "):
                    current_set["crc"] = line[len("CRC32: "):]

    print("Found sets: ")
    for set_id, current_set in sets.items():
        print(f"  {set_id}")
        print(f"    {current_set['name']}")
        print(f"    {current_set['safename']}")
        print(f"    {current_set['parts']}")
        print(f"    {current_set['crc']}")

    for set_id, current_set in sets.items():
        print(f"Reading parts for {current_set['name']}...")
        content = bytes()
        for partname in current_set['parts']:
            with open(os.path.join(src_dir, partname), 'rb') as infile:
                content += infile.read()

        print(f"Checking checksum for {current_set['name']}...")
        crc_val = hex(zlib.crc32(content))
        if crc_val != hex(int(current_set['crc'], 16)):
            print(
                f"CRC does not match - found {crc_val}, expected {hex(int(current_set['crc'], 16))} - skipping set!")
        else:
            print(f"Creating file for {current_set['name']}...")
            with open(os.path.join(dest_dir, f"{current_set['safename']}.iso"), 'wb') as outfile:
                outfile.write(content)
