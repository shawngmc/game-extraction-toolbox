import logging

logger = logging.getLogger('gextoolbox')

out_file_info = [
    {
        "game": "Alpha Mission",
        "system": "NES",
        "filename": "ASO.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Alpha Mission",
        "system": "NES",
        "filename": "ASO_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Athena",
        "system": "NES",
        "filename": "Athena.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Athena",
        "system": "NES",
        "filename": "Athena_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Crystalis",
        "system": "NES",
        "filename": "Crystalis.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Crystalis",
        "system": "NES",
        "filename": "Crystalis_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Guerrilla War",
        "system": "NES",
        "filename": "GuerrillaWar.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Guerrilla War",
        "system": "NES",
        "filename": "GuerrillaWar_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari Warriors",
        "system": "NES",
        "filename": "Ikari.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari Warriors",
        "system": "NES",
        "filename": "Ikari_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari II: Victory Road",
        "system": "NES",
        "filename": "Ikari2.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari II: Victory Road",
        "system": "NES",
        "filename": "Ikari2_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "NES",
        "filename": "Ikari3.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Ikari III: The Rescue",
        "system": "NES",
        "filename": "Ikari3_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Iron Tank",
        "system": "NES",
        "filename": "IronTank.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "Iron Tank",
        "system": "NES",
        "filename": "IronTank_jp.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "NES",
        "filename": "POW.nes",
        "status": "good",
        "notes": []
    },
    {
        "game": "P.O.W",
        "system": "NES",
        "filename": "POW_jp.nes",
        "status": "good",
        "notes": []
    }
]

def extract(bundle_contents):
    out_files = []
    for key, value in bundle_contents['main'].items():
        if key.endswith(".nes"):
            logger.info(f"Extracting {key}...")
            out_files.append({'filename': key, 'contents': value})
    return out_files
