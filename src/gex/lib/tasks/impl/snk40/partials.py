
out_file_info = [
    {
        "game": "ASO: ArmoredScrumObject",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Guerilla War",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Psycho Soldier",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "TNKIII",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Ikari I",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Ikari 2 Victory Road",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Bermuda Triangle / World Wars",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "MarvinsMaze",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    },
    {
        "game": "Athena",
        "system": "Arcade",
        "filename": "N/A",
        "notes": [1]
    }
]

def extract(bundle_contents):
    out_files = []
    out_files.extend(extract_tnk3(bundle_contents))
    return out_files


def extract_tnk3(bundle_contents):
    return []