'''Implementation of neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
import logging
import os
import lzma
from gex.lib.tasks.basetask import BaseTask
from gex.lib.tasks import helpers
from gex.lib.utils.blob import transforms

logger = logging.getLogger('gextoolbox')

class NeoGeoClassicsHumbleTask(BaseTask):
    '''Implements neogeo_classics_humble: Neo Geo Classics by SNK Playmore on Humble'''
    _task_name = "neogeo_classics_humble"
    _title = "Neo Geo Classics by SNK Playmore on Humble Store"
    _details_markdown = '''
This task covers a variety of SNK Neo Geo releases Humble Store.
In some cases, these games simply have ZIP files for the ROM; in other cases, the files are in a subfolder.

This also covers most collections/bundles, but only if they install as separate titles. 
As of right now, the only exception known is Samurai Shodown Neogeo Collection.
    '''
    _default_input_folder = r"C:\Program Files (x86)\GOG Galaxy\Games"
    _input_folder_desc = "Game Library (Amazon, Steam, etc.) folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }

    def _check_dirs(self, in_dir, child_dirs):
        for child_dir in child_dirs:
            path = os.path.join(in_dir, child_dir)
            if os.path.exists(path):
                return path
        return None

    def _verify_input_zip(self, contents, entries):
        zip_metas = zip_lib.get_metadata(contents)
        # Ensure the file name lists are the same
        real_filenames = set(zip_metas.keys())
        expected_filenames = set(entries.keys())
        if real_filenames != expected_filenames:
            logger.info(f"Could NOT verify {file_name}: File lists don't match!")
            return False
        # Compare file size/CRC
        for inner_filename, zip_meta in zip_metas.items():
            verify_entry = entries[inner_filename]
            if zip_meta['crc'] != verify_entry['crc'] or zip_meta['size'] != verify_entry['size'] :
                logger.info(f"Could NOT verify {file_name}: {inner_filename} should be {verify_entry['crc']} at {verify_entry['size']} bytes, found {zip_meta['crc']} at {zip_meta['size']}")
                return False
        logger.info(f"Verified {file_name}.")
        return True

    def execute(self, in_dir, out_dir):
        in_files = self._metadata['in']['files']

        current_neogeo_bios_ver = None

        # Find folders
        folders = list(set(map(lambda x: x['rel_path'][0], in_files.values())))
        found_folders = []
        for folder in folders:
            path = os.path.join(in_dir, folder)
            if os.path.exists(path):
                logger.info(f"Found {folder}...")
                found_folders.append(folder)
            else:
                logger.info(f"No {folder} folder found...")

        # Process titles
        out_files = {}
        for folder in found_folders:
            title_in_files = [v for v in in_files.values() if v['rel_path'][0] == folder]

            title_neogeo = next(v for v in title_in_files if v['filename'] == "neogeo.zip")
            title_gameroms = [v for v in title_in_files if v['filename'] != "neogeo.zip"]

            for title_gamerom in title_gameroms:
                zip_path = os.path.join(in_dir, *title_gamerom['rel_path'], title_gamerom['filename'])
                if os.path.exists(zip_path):
                    logger.info(f"Found zip {zip_path}...")
                    read_file_entry = self.read_datafile(in_dir, title_gamerom)
                    out_files[title_gamerom['filename']] = read_file_entry['contents']

            if title_neogeo:
                title_bios_version = list(title_neogeo['versions'].keys())[0]
                if title_bios_version == 'enhanced' and current_neogeo_bios_ver != 'enhanced':
                    zip_path = os.path.join(in_dir, *title_neogeo['rel_path'], title_neogeo['filename'])
                    if os.path.exists(zip_path):
                        logger.info(f"Found enhanced NeoGeo BIOS zip {zip_path}...")
                        read_file_entry = self.read_datafile(in_dir, title_neogeo)
                        out_files[title_neogeo['filename']] = read_file_entry['contents']
                        current_neogeo_bios_ver = 'enhanced'
                elif title_bios_version == 'basic' and current_neogeo_bios_ver is None:
                    zip_path = os.path.join(in_dir, *title_neogeo['rel_path'], title_neogeo['filename'])
                    if os.path.exists(zip_path):
                        logger.info(f"Found basic NeoGeo BIOS zip {zip_path}...")
                        read_file_entry = self.read_datafile(in_dir, title_neogeo)
                        out_files[title_neogeo['filename']] = read_file_entry['contents']
                        current_neogeo_bios_ver = 'basic'


        # Write out the files
        for filename, contents in out_files.items():
            _ = self.verify_out_file(filename, contents)
            out_path = os.path.join(out_dir, filename)
            with open(out_path, "wb") as out_file:
                logger.info(f"Writing verified {filename}...")
                out_file.write(contents)


# BSTARS2
# Dotemu2mame.js has this title
# https://gist.github.com/cxx/81b9f45eb5b3cb87b4f3783ccdf8894f


# Looks like Humble release removes team locations

# ZOOM TABLE
# bstars2_zoom_table -> 000-lo.lo

# NEOGEO BIOS
# bstars2_bios_m68k -> neo-epo.bin

# NEOGEO SFIX
# bstars2_bios_sfix -> sfix.sfix
#     transform: NeoGeo.sfix_reorder


# function sfix_reorder(bin)
# {
#     const tmp = Buffer.allocUnsafe(32);
#     for (let i = 0; i < bin.length; i += 32) {
#         for (let j = 0; j < 8; j++) {
#             tmp[j+16] = bin[i+4*j+0];
#             tmp[j+24] = bin[i+4*j+1];
#             tmp[j+ 0] = bin[i+4*j+2];
#             tmp[j+ 8] = bin[i+4*j+3];
#         }
#         tmp.copy(bin, i);
#     }
#     return bin;
# }

# YAMAHA SOUND
# bstars2_adpcm

#     const ymsnd_files = [];
#     const ymsnd_size = fs.statSync(path.join(srcdir, `${name}_adpcm`)).size;
#     for (let i = 1; i <= Math.ceil(ymsnd_size/conf.rom_size[1]); i++)
#         ymsnd_files.push(`${id}-v${i}.v${i}`);

#         ymsnd: {
#             input: `${name}_adpcm`, output: ymsnd_files,
#             transform: bin => split(bin, conf.rom_size[1])
#         },

# SPRITES
# bstars2_tiles

#     const sprites_size = fs.statSync(path.join(srcdir, `${name}_tiles`)).size;
#     const sprites_files = [];
#     for (let i = 1; i <= Math.ceil(sprites_size/2/conf.rom_size[2])*2; i++)
#         sprites_files.push(`${id}-c${i}.c${i}`);


#         sprites: {
#             input: `${name}_tiles`, output: sprites_files,
#             transform: bin => {
#                 NeoGeo.deoptimize_sprites(bin);
#                 if ('cmc_encrypt_gfx' in conf)
#                     conf.cmc_encrypt_gfx(bin);
#                 const a = interleave(bin).map(b => split(b, conf.rom_size[2]));
#                 return a[0].flatMap((b, i) => [b, a[1][i]]);
#             }
#         }


# // from http://i486.mods.jp/ichild/?page_id=62
# // Original author: Imaha486
# function deoptimize_sprites(buf)
# {
#     const tmp = Buffer.allocUnsafe(0x80);
#     for (let i = 0; i < buf.length; i += 0x80) {
#         tmp.fill(0);
#         for (let y = 0; y < 0x10; y++) {
#             let dstData;
#             dstData = buf[i+(y*8)+0] <<  0 |
#                       buf[i+(y*8)+1] <<  8 |
#                       buf[i+(y*8)+2] << 16 |
#                       buf[i+(y*8)+3] << 24;
#             for (let x = 0; x < 8; x++) {
#                 tmp[0x43 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
#                 tmp[0x41 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
#                 tmp[0x42 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
#                 tmp[0x40 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
#             }

#             dstData = buf[i+(y*8)+4] <<  0 |
#                       buf[i+(y*8)+5] <<  8 |
#                       buf[i+(y*8)+6] << 16 |
#                       buf[i+(y*8)+7] << 24;
#             for (let x = 0; x < 8; x++) {
#                 tmp[0x03 | y << 2] |= (dstData >> x*4+3 & 1) << 7-x;
#                 tmp[0x01 | y << 2] |= (dstData >> x*4+2 & 1) << 7-x;
#                 tmp[0x02 | y << 2] |= (dstData >> x*4+1 & 1) << 7-x;
#                 tmp[0x00 | y << 2] |= (dstData >> x*4+0 & 1) << 7-x;
#             }
#         }
#         tmp.copy(buf, i);
#     }
#     return buf;
# }


# MAINCPU
# bstars2_game_m68k

#     rom_size: [ 0x080000, 0x100000, 0x100000 ]

#     const maincpu_files = [`${id}-p1.p1`];
#     if (maincpu.length > conf.rom_size[0]) {
#         if (maincpu.slice(conf.rom_size[0]).every(b => b == 0))
#             maincpu = maincpu.slice(0, conf.rom_size[0]);
#         else
#             maincpu_files.push(`${id}-p2.sp2`);
#     }
#         maincpu: {
#             input: maincpu, output: maincpu_files,
#             transform: bin => {
#                 if (conf.swap_68k) {
#                     const a = split_at(bin, bin.length/2);
#                     bin = Buffer.concat([a[1], a[0]]);
#                 }
#                 if ('sma_encrypt' in conf)
#                     conf.sma_encrypt(bin);

#                 const rom_size = conf.rom_size[0];
#                 if (bin.length == rom_size) return bin;

#                 const p1_size = bin.length >= 0x100000 + rom_size ?
#                       0x100000 : bin.length - rom_size;

#                 const a = split_at(bin, p1_size);
#                 if ('sma_encrypt' in conf)
#                     a[0] = a[0].slice(0x0c0000);
#                 return [a[0], ...split(a[1], rom_size)];
#             }
#         },

# GAME SFIX
# bstars2_game_sfix -> 041-s1.s1
#     transform: NeoGeo.sfix_reorder


# function sfix_reorder(bin)
# {
#     const tmp = Buffer.allocUnsafe(32);
#     for (let i = 0; i < bin.length; i += 32) {
#         for (let j = 0; j < 8; j++) {
#             tmp[j+16] = bin[i+4*j+0];
#             tmp[j+24] = bin[i+4*j+1];
#             tmp[j+ 0] = bin[i+4*j+2];
#             tmp[j+ 8] = bin[i+4*j+3];
#         }
#         tmp.copy(bin, i);
#     }
#     return bin;
# }

# AUDIOCPU
# bstars_game_m68k -> 041-m1.m1


        logger.info("Processing complete.")
