'''Implementation of cas1_old: Capcom Arcade Stadium 1 (OLD)'''
import glob
import zipfile
import logging
import os
import io

from gex.lib.archive import kpka
from gex.lib.file import identify
from gex.lib.tasks.basetask import BaseTask
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')
# TODO: Cleanup the details report - file map is much more complex with depotID and manifestID

class CAS1OldTask(BaseTask):
    '''Implements cas1_old: Capcom Arcade Stadium 1 (OLD)'''
    _task_name = 'cas1_old'
    _title = "Capcom Arcade Stadium 1 (OLD)"
    _details_markdown = '''
Capcom Arcade Stadium 1, ~30 arcade games, as downloaded from depot using old manifests

Pulling CAS1 via old Steam Depots:

The notes I found were at https://retropie.org.uk/forum/topic/10918/where-to-legally-acquire-content-to-play-on-retropie/606?lang=en-US. 
Essentially, while a new version was added to steam, the old version can be specifically downloaded.
You can pull these by visiting steam://nav/console (this opens a hidden CLI within Steam), then using the command 'download_depot <GameID> <DepotID> <ManifestID>'
This will download them into your Steam folder, under steamapps\content\app_<GameID>\depot_<DepotID>
An easier tool to pull the old versions can be found here: https://github.com/SteamRE/DepotDownloader

After that, this script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                             | **DepotID**     | **ManifestID**          | **MAME Ver.**     | **FB Neo**     | **ENG Filename**     | **ENG CRC**     | **JP Filename**     | **JP CRC**     | **Notes**  
---------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------------|------------|-----------  
 **Powered Gear**                     | 1556723     | 305464856399220085  | MAME 0.139    | Y          | pgear.zip        | OK          | N/A             | N/A        | (1)       
 **Warriors of Fate**                 | 1556720     | 4950348891858375781 | MAME 0.139    | Y          | wofu.zip         | Bad         | wofj.zip        | Bad        | (1)       
 **Senjo no Okamill**                 | 1556714     | 4064909307706647901 | MAME 0.139    | N          | N/A              | N/A         | mercsj.zip      | Bad        | (1)       
 **Captain Commando**                 | 1556718     | 2975445377289899248 | MAME 0.246    | Y          | captcomm.zip     | OK          | captcommj.zip   | OK         |           
 **Street Fighter II**                | 1556717     | 7823458246757484640 | MAME 0.246    | Y          | sf2um.zip        | OK          | sf2jl.zip       | OK         |           
 **Varth Operation Thunderstorm**     | 1556719     | 2957041054036881699 | MAME 0.246    | Y          | varth.zip        | OK          | varthj.zip      | OK         |           
 **1942**                             | 1556702     | 7110820738848130277 | MAME 0.246    | Y          | 1942.zip         | OK          | N/A             | OK         |           
 **Bionic Commando**                  | 1556707     | 3238877912290772385 | MAME 0.246    | Y          | bionicc2.zip     | OK          | N/A             | OK         |           
 **Commando**                         | 1556703     | 5154503909431550517 | MAME 0.246    | EN         | commandou.zip    | OK          | commandoj.zip   | Bad        | (2)       
 **Dynasty Wars**                     | 1556711     | 5906401061810674850 | MAME 0.246    | Y          | dynwar.zip       | OK          | dynwarj.zip     | OK         |           
 **Final Fight**                      | 1556712     | 1427558570204465271 | MAME 0.246    | N          | ffightu.zip      | Bad         | ffightj.zip     | Bad        | (2)       
 **Forgotton Worlds**                 | 1556708     | 2495421590891474725 | MAME 0.246    | EN         | forgottnuaa.zip  | OK          | lostwrld.zip    | Bad        | (2)       
 **Ghouls 'n Ghosts**                 | 1556709     | 7553746399143380961 | MAME 0.246    | Y          | ghoulsu.zip      | OK          | daimakai.zip    | OK         |           
 **Ghosts 'n Goblins**                | 1556690     | 5034024650887104340 | MAME 0.246    | Y          | gng.zip          | OK          | makaimurg.zip   | OK         |           
 **Pirate Ship Higemaru**             | 1556701     | 3568513687229079528 | MAME 0.246    | Y          | higemaru.zip     | OK          | N/A             | N/A        |           
 **Legendary Wings**                  | 1556706     | 8788446018740704096 | MAME 0.246    | Y          | lwings.zip       | OK          | lwingsja.zip    | OK         |           
 **Mega Twins**                       | 1556715     | 7832027131156162352 | MAME 0.246    | JP         | mtwins.zip       | Bad         | chikij.zip      | OK         | (2)       
 **Section Z**                        | 1556704     | 7517264779277019420 | MAME 0.246    | Y          | sectionza.zip    | OK          | N/A             | N/A        |           
 **Strider**                          | 1556710     | 8512960795726908906 | MAME 0.246    | EN         | striderua.zip    | OK          | striderjr.zip   | Bad        | (2) (3)   
 **Street Fighter II Hyper Fighting** | 1556721     | 317521835646003561  | MAME 0.246    | Y          | sf2hfu.zip       | OK          | sf2hfj.zip      | OK         |           
 **Tatakai no Banka**                 | 1556705     | 7200344018849026230 | MAME 0.246    | N          | N/A              | N/A         | trojanj.zip     | Bad        | (2)       
 **Vulgus**                           | 1556700     | 9143855046040096923 | MAME 0.246    | N          | vulgus.zip       | Bad         | vulgusj.zip     | Bad        | (2)       
 **US Navy: Carrier Air Wing**        | 1556716     | 187920547906050452  | MAME 0.246    | N          | cawingu.zip      | Bad         | cawingj.zip     | Bad        | (2)       
 **Cyberbots: Fullmetal Madness**     | 1556724     | 4293976514552436962 | MAME 0.139    | N          | cybotsu.zip      | OK          | cybotsj.zip     | OK         | (1)       
 **19XX: The War Against Destiny**    | 1556725     | 4171961223274458606 | MAME 0.139    | N          | 19xx.zip         | Bad?        | 19xxj.zip       | Bad?       | (1) (4)   
 **Battle Circuit**                   | 1556726     | 5500917457208551111 | MAME 0.139    | N          | batcir.zip       | OK          | batcirj.zip     | OK         | (1)       
 **Giga Wing**                        | 1556727     | 1585945610334979859 | MAME 0.139    | N          | gigawing.zip     | OK          | gigawingj.zip   | OK         | (1)       
 **1944: The Loop Master**            | 1556728     | 3525105251099559918 | MAME 0.139    | N          | 1944.zip         | OK          | 1944j.zip       | OK         | (1) (4)   
 **Progear**                          | 1556729     | 6184184127241976915 | MAME 0.139    | N          | progear.zip      | OK          | progearj.zip    | OK         | (1)       
 **1941: Counter Attack**             | 1556713     | 2745567461535328718 | MAME 0.246    | Y          | 1941u.zip        | OK          | 1941j.zip       | OK         | (7)       
 **Super Street Fighter II Turbo**    | 1556722     | 2744654918197522324 | MAME 0.139    | N          | ssf2tu.zip       | OK          | ssf2xj.zip      | Bad        | (1)       
 **1943: The Battle of Midway**       | 1515951     | 1597238681896386079 | N/A           | EN         | 1943u.zip        | OK          | 1943j.zip       | BAD        | (5)       
 **3 Wonders**                        | 1556709     | 7553746399143380961 | MAME 0.246    | Y          | 3wondersu.zip    | OK          | N/A             | N/A        | (6)       

    '''
    _out_file_list = [
    ]

    _out_file_notes = {
        "1": "These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require",
        "2": "These ROMs play fine, even in the current MAME, despite the bad CRCs. This is likely due to Capcom redumping or making a minor modification to omit copyright/trademark material.",
        "3": "This ROM specifically complains about a bad dump on a specific file; it still plays OK.",
        "4": "This ROM is using an older naming convention to help allow emulation in the older MAME it requires.",
        "5": "Embedded in main package; JP version is missing too much, but US version can run in FB Neo",
        "6": "Embedded in a specific depot of Ghouls n Ghosts",
        "7": "Includes extra ROM 1941.zip; same solid compatibility",
    }
    _default_input_folder = r"C:\Program Files (x86)\Steam\steamapps\content"
    _input_folder_desc = "SteamApps Content Folder"

    _pkg_name_map = {
        "1515951": "1943",
        "1556690": "Ghosts 'n Goblins",
        "1556700": "Vulgus",
        "1556701": "Pirate Ship Higemaru",
        "1556702": "1942",
        "1556703": "Commando",
        "1556704": "Section Z",
        "1556705": "Tatakai no Banka",
        "1556706": "Legendary Wings",
        "1556707": "Bionic Commando",
        "1556708": "Forgotton Worlds / Lost World",
        "1556709": "Ghouls 'n Ghosts (and 3 Wonders)",
        "1556710": "Strider",
        "1556711": "Dynasty Wars",
        "1556712": "Final Fight",
        "1556713": "1941 Counter Attack",
        "1556714": "Senjou no Ookami II",
        "1556715": "Mega Twins",
        "1556716": "Carrier Air Wing",
        "1556717": "Street Fighter II",
        "1556718": "Captain Commando",
        "1556719": "Varth Operation Thunderstorm",
        "1556720": "Warriors of Fate",
        "1556721": "Street Fighter II Hyper Fighting",
        "1556722": "Super Street Fighter II Turbo",
        "1556723": "Powered Gear: Strategic Variant Armor Equipment",
        "1556724": "Cyberbots: Fullmetal Madness",
        "1556725": "19XX: The War Against Destiny",
        "1556726": "Battle Circuit",
        "1556727": "Giga Wing",
        "1556728": "1944: The Loop Master",
        "1556729": "Progear"
    }

    def _twiddle_zip(self, zip_bytes, remove_list=None, rename_dict=None, lowercase_all=False):
        remove_list = remove_list if remove_list else []
        rename_dict = rename_dict if rename_dict else {}
        new_contents = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as old_archive:
            zip_entries = list(old_archive.infolist())
            with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
                for file_entry in zip_entries:
                    # Skip files to remove
                    if not file_entry.filename in remove_list:
                        with old_archive.open(file_entry) as file_read_obj:
                            file_data = file_read_obj.read()
                            filename = file_entry.filename
                            # If a file needs renamed, do so
                            if filename in rename_dict:
                                filename = rename_dict.get(filename)
                            # If filenames should be made lowercase, do so
                            if lowercase_all:
                                filename = filename.lower()
                            # add to new archive
                            new_archive.writestr(filename, file_data)
        return new_contents.getvalue()

    def _merged_rom_handler(self, zip_contents, func_map):
        new_data = dict()
        with zipfile.ZipFile(io.BytesIO(zip_contents), "r") as old_archive:
            zip_entries = list(old_archive.infolist())

            def get_type(zip_entry):
                return zip_entry.filename.split('.')[1]
            for file_entry in zip_entries:
                # read in the entry - we need the body either way
                with old_archive.open(file_entry) as file_read_obj:
                    file_data = file_read_obj.read()
                    type_name = get_type(file_entry)
                    type_func = func_map.get(type_name)
                    if type_func is not None:
                        new_data.update(type_func(file_data))
        # Build the new zip file
        new_contents = io.BytesIO()
        with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
            for name, data in new_data.items():
                new_archive.writestr(name, data)
        return new_contents.getvalue()

    def _weird_subzip_handler(self, kpka_contents, target_offset, subzip_filename):
        # Used for 3wonders in ghouls jp and 1941 in 1941j
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == target_offset:
                    contents = file_entry['contents']
                    subzip_contents = None
                    with zipfile.ZipFile(io.BytesIO(contents), "r") as old_archive:
                        zip_entries = list(old_archive.infolist())
                        for file_entry in zip_entries:
                            if file_entry.filename == subzip_filename:
                                with old_archive.open(file_entry) as file_read_obj:
                                    subzip_contents = file_read_obj.read()
                    # If extra rom was found, pull it out to allow normal processing and save it
                    if subzip_contents is not None:
                        subzip_fixed = self._standard_kpka_contents_processing(
                            {'0': {'contents': subzip_contents}})[0]
                        out_files.append(subzip_fixed)
                        contents = self._twiddle_zip(
                            contents, remove_list=[subzip_filename])
                    other_zip = self._standard_kpka_contents_processing(
                        {'0': {'contents': contents}})[0]
                    out_files.append(other_zip)
                else:
                    other_zip = self._standard_kpka_contents_processing({'0': file_entry})[
                        0]
                    out_files.append(other_zip)
        return out_files

    def _handle_1515951(self, kpka_contents):
        out_files = []
        # Start with standard processing
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        # Remove 1943j as it's just too broken
        out_files = list(
            filter(lambda i: i['filename'] != "1943j.zip", out_files))
        return out_files

    def _handle_1556690(self, kpka_contents):
        out_files = []
        # Start with standard processing
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        for out_file in out_files:
            if out_file['filename'] == 'makaimurg.zip':
                out_file['contents'] = self._twiddle_zip(
                    out_file['contents'], remove_list=['gg1.bin'])
        return out_files

    def _handle_1556708(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:
                    contents = self._twiddle_zip(
                        file_entry['contents'], lowercase_all=True)
                    out_files.append(
                        {'filename': 'lostwrld.zip', 'contents': contents})
                else:
                    # This is ok for standard processing
                    ffightj_zip = self._standard_kpka_contents_processing({'0': file_entry})[
                        0]
                    out_files.append(ffightj_zip)
        return out_files

    def _handle_1556709(self, kpka_contents):
        return self._weird_subzip_handler(kpka_contents, 352, "3wondersu.zip")

    def _handle_1556710(self, kpka_contents):
        out_files = []
        # Start with standard processing
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        for out_file in out_files:
            if out_file['filename'] == 'striderjr2.zip':
                out_file['filename'] = 'striderjr.zip'
            elif out_file['filename'] == 'striderua.zip':
                out_file['contents'] = self._twiddle_zip(
                    out_file['contents'], remove_list=['st24b2.1a'])
        return out_files

    def _handle_1556711(self, kpka_contents):
        out_files = []
        # Start with standard processing
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        for out_file in out_files:
            if out_file['filename'] == 'dynwarj.zip':
                out_file['contents'] = self._twiddle_zip(
                    out_file['contents'], remove_list=['TK_14.BIN'])
        return out_files

    def _handle_1556712(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 1497211:
                    contents = self._twiddle_zip(
                        file_entry['contents'], lowercase_all=True)
                    out_files.append(
                        {'filename': 'ffightu.zip', 'contents': contents})
                else:
                    # This is ok for standard processing
                    ffightj_zip = self._standard_kpka_contents_processing({'0': file_entry})[
                        0]
                    out_files.append(ffightj_zip)
        return out_files

    def _handle_1556713(self, kpka_contents):
        return self._weird_subzip_handler(kpka_contents, 352, "1941.zip")

    def _handle_1556714(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                # This is merjs; rename it
                out_files.append(
                    {'filename': 'mercsj.zip', 'contents': file_entry['contents']})
        return out_files

    def _handle_1556715(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 1511592:
                    out_files.append(
                        {'filename': 'mtwins.zip', 'contents': file_entry['contents']})
                else:
                    other_zip = self._standard_kpka_contents_processing({'0': file_entry})[
                        0]
                    out_files.append(other_zip)
        return out_files

    def _handle_1556716(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 1538278:
                    out_files.append(
                        {'filename': 'cawingu.zip', 'contents': file_entry['contents']})
                else:
                    other_zip = self._standard_kpka_contents_processing({'0': file_entry})[
                        0]
                    out_files.append(other_zip)
        return out_files

    def _handle_1556717(self, kpka_contents):
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        for out_file in out_files:
            if out_file['filename'] == 'sf2ul.zip':
                out_file['filename'] = 'sf2um.zip'
                rename_dict = {
                    "sf2_05(m1).bin": "sf2-1m.3a",
                    "sf2_06(m5).bin": "sf2-5m.4a",
                    "sf2_07(m3).bin": "sf2-3m.5a",
                    "sf2_08(m7).bin": "sf2-7m.6a",
                    "sf2_14(m2).bin": "sf2-2m.3c",
                    "sf2_15(m6).bin": "sf2-6m.4c",
                    "sf2_16(m4).bin": "sf2-4m.5c",
                    "sf2_17(m8).bin": "sf2-8m.6c",
                    "sf2_24(m9).bin": "sf2-9m.3d",
                    "sf2_25(m13).bin": "sf2-13m.4d",
                    "sf2_26(m11).bin": "sf2-11m.5d",
                    "sf2_27(m15).bin": "sf2-15m.6d",
                    "sf2_28m.bin": "sf-2u_28m.9e",
                    "sf2_30m.bin": "sf-2u_30m.11e",
                    "sf2_31m.bin": "sf-2u_31m.12e",
                    "sf2_35m.bin": "sf-2u_35m.9f",
                    "sf2_38m.bin": "sf-2u_38m.12f",
                    "sf2j_29b.bin": "sf-2u_29m.10e",
                    "sf2j_36b.bin": "sf-2u_36m.10f",
                    "sf2u_09.bin": "sf2_09.12a",
                    "sf2u_18.bin": "sf2_18.11c",
                    "sf2u_19.bin": "sf2_19.12c",
                    "sf2u_37m.bin": "sf-2u_37m.11f",
                }
                out_file['contents'] = self._twiddle_zip(
                    out_file['contents'], rename_dict=rename_dict, lowercase_all=True)
        return out_files

    def _handle_1556718(self, kpka_contents):
        out_files = []
        # Start with standard processing
        out_files = self._standard_kpka_contents_processing(kpka_contents)
        # For each resulting zip, remove the optional and bad CRC files
        for out_file in out_files:
            out_file['contents'] = self._twiddle_zip(
                out_file['contents'], rename_dict={'c632b.ic1': 'c632.ic1'})
        return out_files

    def _handle_1556722(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.custom_split(
                contents, [8388608, 4194304, 4194304])
            chunks = transforms.deinterleave_all(
                chunks, num_ways=4, word_size=2)
            filenames = [
                'sfx.13m',
                'sfx.15m',
                'sfx.17m',
                'sfx.19m',
                'sfx.14m',
                'sfx.16m',
                'sfx.18m',
                'sfx.20m',
                'sfx.21m',
                'sfx.23m',
                'sfx.25m',
                'sfx.27m'
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x48000, length=0x8000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            chunks = transforms.equal_split(contents, num_chunks=2)
            filenames = [
                'sfx.01',
                'sfx.02'
            ]
            return dict(zip(filenames, chunks))

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            filenames = [
                'sfx.11m',
                'sfx.12m'
            ]
            return dict(zip(filenames, chunks))

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # ssf2xj
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x380000, length=0x3FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=7)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "sfxj.03d",
                            "sfxj.04a",
                            "sfxj.05",
                            "sfxj.06b",
                            "sfxj.07a",
                            "sfxj.08",
                            "sfx.09"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'ssf2xj.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
                else:  # ssf2tu
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x380000, length=0x3FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=7)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "sfxu.03e",
                            "sfxu.04a",
                            "sfxu.05",
                            "sfxu.06b",
                            "sfxu.07a",
                            "sfxu.08",
                            "sfxu.09"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                            'filename': 'ssf2tu.zip',
                            'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                        })
        return out_files

    def _handle_1556724(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.deinterleave_all(
                chunks, num_ways=4, word_size=2)
            filenames = [
                "cyb.13m",
                "cyb.15m",
                "cyb.17m",
                "cyb.19m",
                "cyb.14m",
                "cyb.16m",
                "cyb.18m",
                "cyb.20m"
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x48000, length=0x8000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            chunks = transforms.equal_split(contents, num_chunks=2)

            return {
                'cyb.01': chunks[0],
                'cyb.02': chunks[1]
            }

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)

            return {
                'cyb.11m': chunks[0],
                'cyb.12m': chunks[1]
            }

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # cybotsj
                    func_map = {}

                    def maincpu(contents):
                        chunks = transforms.equal_split(contents, num_chunks=8)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "cybj.03",
                            "cybj.04",
                            "cyb.05",
                            "cyb.06",
                            "cyb.07",
                            "cyb.08",
                            "cyb.09",
                            "cyb.10"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'cybotsj.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
                else:  # cybotsu
                    func_map = {}

                    def maincpu(contents):
                        chunks = transforms.equal_split(contents, num_chunks=8)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "cybu.03",
                            "cybu.04",
                            "cyb.05",
                            "cyb.06",
                            "cyb.07",
                            "cyb.08",
                            "cyb.09",
                            "cyb.10"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'cybotsu.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
        return out_files

    def _handle_1556725(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # 19xxj
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x280000, length=0x180000)
                        chunks = transforms.equal_split(contents, num_chunks=5)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            '19xj.03a',
                            '19xj.04a',
                            '19xj.05a',
                            '19xj.06a',
                            '19xj.07a'
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu

                    def gfx(contents):
                        contents = transforms.splice_out(
                            contents, 0x200000, length=0x600000)
                        chunks = transforms.equal_split(contents, num_chunks=5)
                        chunks = transforms.deinterleave_all(
                            chunks, num_ways=4, word_size=2)
                        filenames = [
                            '19x-69.4j',
                            '19x-59.4d',
                            '19x-79.4m',
                            '19x-89.4p',
                            '19x-73.8j',
                            '19x-63.8d',
                            '19x-83.8m',
                            '19x-93.8p',
                            '19x-74.9j',
                            '19x-64.9d',
                            '19x-84.9m',
                            '19x-94.9p',
                            '19x-75.10j',
                            '19x-65.10d',
                            '19x-85.10m',
                            '19x-95.10p',
                            '19x-76.11j',
                            '19x-66.11d',
                            '19x-86.11m',
                            '19x-96.11p'
                        ]

                        return dict(zip(filenames, chunks))
                    func_map['gfx'] = gfx

                    def audiocpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x28000, length=0x28000)
                        contents = transforms.splice_out(
                            contents, 0x8000, length=0x8000)
                        return {
                            '19x-01.1a': contents
                        }
                    func_map['audiocpu'] = audiocpu

                    def qsound(contents):
                        chunks = transforms.equal_split(contents, num_chunks=8)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "19x-51.6a",
                            "19x-52.7a",
                            "19x-53.8a",
                            "19x-54.9a",
                            "19x-55.10a",
                            "19x-56.11a",
                            "19x-57.12a",
                            "19x-58.13a"
                        ]

                        return dict(zip(filenames, chunks))
                    func_map['qsound'] = qsound

                    out_files.append({'filename': '19xxj.zip', 'contents': self._merged_rom_handler(
                        file_entry['contents'], func_map)})
                else:  # 19xx
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x280000, length=0x180000)
                        chunks = transforms.equal_split(contents, num_chunks=5)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            '19xu.03',
                            '19xu.04',
                            '19xu.05',
                            '19xu.06',
                            '19x.07',
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu

                    def gfx(contents):
                        contents = transforms.splice_out(
                            contents, 0x200000, length=0x600000)
                        chunks = transforms.custom_split(
                            contents, [2097152, 8388608])
                        chunks = transforms.deinterleave_all(
                            chunks, num_ways=4, word_size=2)
                        filenames = [
                            "19x.13m",
                            "19x.15m",
                            "19x.17m",
                            "19x.19m",
                            "19x.14m",
                            "19x.16m",
                            "19x.18m",
                            "19x.20m",
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['gfx'] = gfx

                    def audiocpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x28000, length=0x28000)
                        contents = transforms.splice_out(
                            contents, 0x8000, length=0x8000)
                        return {
                            '19x.01': contents
                        }
                    func_map['audiocpu'] = audiocpu

                    def qsound(contents):
                        chunks = transforms.equal_split(contents, num_chunks=2)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "19x.11m",
                            "19x.12m"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': '19xx.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
        return out_files

    def _handle_1556726(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
            filenames = [
                'btc.13m',
                'btc.15m',
                'btc.17m',
                'btc.19m'
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x48000, length=0x8000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            chunks = transforms.equal_split(contents, num_chunks=2)
            filenames = [
                'btc.01',
                'btc.02'
            ]
            return dict(zip(filenames, chunks))

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            filenames = [
                'btc.11m',
                'btc.12m'
            ]
            return dict(zip(filenames, chunks))

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # batcirj
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x380000, length=0x3FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=7)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "btcj.03",
                            "btcj.04",
                            "btcj.05",
                            "btcj.06",
                            "btc.07",
                            "btc.08",
                            "btc.09"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'batcirj.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
                else:  # batcir
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x380000, length=0x3FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=7)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "btce.03",
                            "btce.04",
                            "btce.05",
                            "btce.06",
                            "btc.07",
                            "btc.08",
                            "btc.09"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'batcir.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
        return out_files

    def _handle_1556727(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.deinterleave(contents, num_ways=4, word_size=2)
            filenames = [
                'ggw.13m',
                'ggw.15m',
                'ggw.17m',
                'ggw.19m'
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x28000, length=0x28000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            return {'ggw.01': contents}

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            filenames = [
                'ggw.11m',
                'ggw.12m'
            ]
            return dict(zip(filenames, chunks))

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # gigawingj
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x180000, length=0x27FFFF)
                        chunks = transforms.equal_split(contents, num_chunks=3)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "ggwj.03a",
                            "ggwj.04a",
                            "ggwj.05a",
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'gigawingj.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
                else:  # gigawing
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x180000, length=0x27FFFF)
                        chunks = transforms.equal_split(contents, num_chunks=3)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "ggwu.03",
                            "ggwu.04",
                            "ggw.05",
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'gigawing.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
        return out_files

    def _handle_1556728(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.custom_split(contents, [16777216, 4194304])
            chunks = transforms.deinterleave_all(
                chunks, num_ways=4, word_size=2)
            filenames = [
                "nff.13m",
                "nff.15m",
                "nff.17m",
                "nff.19m",
                "nff.14m",
                "nff.16m",
                "nff.18m",
                "nff.20m",
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x28000, length=0x28000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            return {'nff.01': contents}

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=2)
            chunks = transforms.swap_endian_all(chunks)
            filenames = [
                'nff.11m',
                'nff.12m'
            ]
            return dict(zip(filenames, chunks))

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # 1944j
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x180000, length=0x27FFFF)
                        chunks = transforms.equal_split(contents, num_chunks=3)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "nffj.03",
                            "nffj.04",
                            "nffj.05",
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({'filename': '1944j.zip', 'contents': self._merged_rom_handler(
                        file_entry['contents'], func_map)})
                else:  # 1944
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x180000, length=0x27FFFF)
                        chunks = transforms.equal_split(contents, num_chunks=3)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "nffu.03",
                            "nff.04",
                            "nffu.05",
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({'filename': '1944.zip', 'contents': self._merged_rom_handler(
                        file_entry['contents'], func_map)})
        return out_files

    def _handle_1556729(self, kpka_contents):
        out_files = []

        def gfx(contents):
            chunks = transforms.deinterleave(contents, num_ways=8, word_size=1)
            filenames = [
                "pga-simm.01c",
                "pga-simm.01d",
                "pga-simm.01a",
                "pga-simm.01b",
                "pga-simm.03c",
                "pga-simm.03d",
                "pga-simm.03a",
                "pga-simm.03b"
            ]
            return dict(zip(filenames, chunks))

        def audiocpu(contents):
            contents = transforms.splice_out(contents, 0x28000, length=0x28000)
            contents = transforms.splice_out(contents, 0x8000, length=0x8000)
            return {'pga.01': contents}

        def qsound(contents):
            chunks = transforms.equal_split(contents, num_chunks=4)
            chunks = transforms.swap_endian_all(chunks)
            filenames = [
                "pga-simm.05a",
                "pga-simm.05b",
                "pga-simm.06a",
                "pga-simm.06b"
            ]
            return dict(zip(filenames, chunks))

        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                if file_entry['offset'] == 352:  # progearj
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x100000, length=0x2FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=2)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "pgaj.03",
                            "pgaj.04"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'progearj.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
                else:  # progear
                    func_map = {}

                    def maincpu(contents):
                        contents = transforms.splice_out(
                            contents, 0x100000, length=0x2FFFFF)
                        chunks = transforms.equal_split(contents, num_chunks=2)
                        chunks = transforms.swap_endian_all(chunks)
                        filenames = [
                            "pgau.03",
                            "pgau.04"
                        ]
                        return dict(zip(filenames, chunks))
                    func_map['maincpu'] = maincpu
                    func_map['gfx'] = gfx
                    func_map['audiocpu'] = audiocpu
                    func_map['qsound'] = qsound
                    out_files.append({
                        'filename': 'progear.zip',
                        'contents': self._merged_rom_handler(file_entry['contents'], func_map)
                    })
        return out_files

    def _find_files(self, in_path):
        return glob.glob(os.path.join(in_path, "**", "*.pak"), recursive=True)

    def _rebuild_mame_subfolder_zip(self, contents):
        # open old zipfile
        with zipfile.ZipFile(io.BytesIO(contents), "r") as old_archive:
            zip_entries = list(old_archive.infolist())

            first_entry = zip_entries[0].filename
            first_entry_parts = first_entry.split('/')
            if len(first_entry_parts) == 1:
                raise Exception(
                    f'not a mame subfolder zip - no slash in first zip entry {first_entry}')
            if len(first_entry_parts) > 2:
                raise Exception(
                    f'not a mame subfolder zip - too many slashes in first zip entry {first_entry}')
            prefix = first_entry_parts[0]

            for file_entry in zip_entries:
                curr_prefix = file_entry.filename.split('/')[0]
                if curr_prefix != prefix:
                    raise Exception(
                        f'not a mame subfolder zip - {curr_prefix} != {prefix}')

            new_contents = io.BytesIO()
            with zipfile.ZipFile(new_contents, "w", compression=zipfile.ZIP_DEFLATED) as new_archive:
                for file_entry in zip_entries:
                    curr_entry_name = file_entry.filename.split('/')[1]
                    with old_archive.open(file_entry) as file_read_obj:
                        file_data = file_read_obj.read()

                        # add to new archive
                        new_archive.writestr(curr_entry_name, file_data)

            ret_obj = {
                'filename': f'{prefix}.zip',
                'contents': new_contents.getvalue()
            }
            return ret_obj

    def _standard_kpka_contents_processing(self, kpka_contents):
        out_files = []
        for file_entry in kpka_contents.values():
            if identify.check_if_zip(file_entry['contents']):
                rebuilt = self._rebuild_mame_subfolder_zip(
                    file_entry['contents'])
                out_files.append(rebuilt)
        return out_files

    def execute(self, in_dir, out_dir):
        pak_files = self._find_files(in_dir)
        for file in pak_files:
            file_id = None
            if os.path.basename(file) == "re_chunk_000.pak":
                file_id = "1515951"
            else:
                file_id = file[-11:-4]

            if file_id in self._pkg_name_map:
                logger.info(f"Extracting {file}: {self._pkg_name_map[file_id]}")
                try:
                    with open(file, "rb") as curr_file:
                        file_content = bytearray(curr_file.read())
                        kpka_contents = kpka.extract(file_content)
                        output_files = []

                        handler_func = self.find_handler_func(file_id)
                        if handler_func:
                            # Reflectively call the appropriate function to process the file
                            output_files = handler_func(kpka_contents)
                        else:
                            output_files = self._standard_kpka_contents_processing(
                                kpka_contents)

                        for output_file in output_files:
                            out_path = os.path.join(out_dir, output_file['filename'])
                            with open(out_path, "wb") as out_file:
                                out_file.write(output_file['contents'])
                except OSError as error:
                    logger.warning(f'Error while processing {file}!')
                    logger.warning(error)
            else:
                logger.info(f'Skipping {file} as it contains no known ROMS!')

        logger.info("Processing complete.")
