'''Implmentation of saga: Collection of SaGa Final Fantasy Legend'''
from collections import namedtuple
import logging
import os
import lz4
import UnityPy
import lz4.block
import lz4.frame
from gex.lib.tasks.basetask import BaseTask
from gex.lib.utils.blob import transforms
from gex.lib.tasks import helpers
from gex.lib.tasks.impl.saga.EndianBinaryReader import EndianBinaryReader

logger = logging.getLogger('gextoolbox')

class SagaTask(BaseTask):
    '''Implments saga: Collection of SaGa Final Fantasy Legend'''
    _task_name = "saga"
    _title = "Collection of SaGa Final Fantasy Legend"
    _details_markdown = '''
These are extracted from the Unity asset bundle files.
See https://github.com/farmerbb/RED-Project/issues/39 for more info.
'''
    _out_file_notes = {}
    _default_input_folder = helpers.gen_steam_app_default_folder("Sa・Ga COLLECTION")
    _input_folder_desc = "Collection of SaGa Steam folder"

    def get_out_file_info(self):
        '''Return a list of output files'''
        return {
            "files": self._metadata['out']['files'],
            "notes": self._metadata['out']['notes']
        }
    
    def unpackSagaUnityArchive(self, unityFileData):
        # Hackily based off of UnityPy, which is great but too many dependencies
        # We know:
        # - The files are UnityFS BundleFiles
        # - The compression is LZ4HC, and there are no alignment fixes to apply
        # - We know the entries are SerializedFile


        BlockInfo = namedtuple("BlockInfo", "uncompressedSize compressedSize flags")
        DirectoryInfoFS = namedtuple("DirectoryInfoFS", "offset size flags path")

        reader = EndianBinaryReader(unityFileData['contents'])

        # Read the UnityFileHeader
        signature = reader.read_string_to_null()
        version = reader.read_u_int()
        version_player = reader.read_string_to_null()
        version_engine = reader.read_string_to_null()

        # Read the UnityFSHeader
        size = reader.read_long()
        compressedSize = reader.read_u_int()
        uncompressedSize = reader.read_u_int()
        dataflags = reader.read_u_int()

        # Read Block Entries
        blocksInfoBytes = reader.read_bytes(compressedSize)
        blocksInfoBytes = lz4.block.decompress(blocksInfoBytes, uncompressedSize)
        blocksInfoReader = EndianBinaryReader(blocksInfoBytes, offset=reader.Position)
        uncompressedDataHash = blocksInfoReader.read_bytes(16)
        blocksInfoCount = blocksInfoReader.read_int()
        m_BlocksInfo = [
            BlockInfo(
                blocksInfoReader.read_u_int(),  # uncompressedSize
                blocksInfoReader.read_u_int(),  # compressedSize
                blocksInfoReader.read_u_short(),  # flags
            )
            for _ in range(blocksInfoCount)
        ]

        # Read Node Entries
        nodesCount = blocksInfoReader.read_int()
        m_DirectoryInfo = [
            DirectoryInfoFS(
                blocksInfoReader.read_long(),  # offset
                blocksInfoReader.read_long(),  # size
                blocksInfoReader.read_u_int(),  # flags
                blocksInfoReader.read_string_to_null(),  # path
            )
            for _ in range(nodesCount)
        ]

        # Create Block Reader
        blocksReader = EndianBinaryReader(
            b"".join(
                lz4.block.decompress(
                    reader.read_bytes(blockInfo.compressedSize),
                    blockInfo.uncompressedSize,
                )
                for i, blockInfo in enumerate(m_BlocksInfo)
            ),
            offset=(blocksInfoReader.real_offset()),
        )
        
        # Read the files
        for node in m_DirectoryInfo:
            reader.Position = node.offset
            name = node.path
            node_reader = EndianBinaryReader(
                reader.read(node.size), offset=(reader.BaseOffset + node.offset)
            )
            allbytes = node_reader.read_bytes(100)
            print(f" ${name}")
            # f = ImportHelper.parse_file(
            #     node_reader, self, name, is_dependency=self.is_dependency
            # )

            # if isinstance(f, (EndianBinaryReader, SerializedFile.SerializedFile)):
            #     if self.environment:
            #         self.environment.register_cab(name, f)

            # # required for BundleFiles
            # f.flags = getattr(node, "flags", 0)
            # self.files[name] = f


        return m_DirectoryInfo, blocksReader


        # https://vscode.dev/github/shawngmc/game-extraction-toolbox/blob/developon.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/UnityPy/environment.py#L138
        # Checks file type, decides FileType.BundleFile

        # https://vscode.dev/github/shawngmc/game-extraction-toolbox/blob/developon.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/UnityPy/helpers/ImportHelper.py#L143-L144
        # Make a BundleFile object

        # https://vscode.dev/github/shawngmc/game-extraction-toolbox/blob/developon.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/UnityPy/files/BundleFile.py#L32
        # Read Bundle File Header
        # - Read signature (string to null, 8 bytes w/null)
        # - Read version (uint, 4 bytes)
        # - Read player Ver (string to null, 6 bytes w/null) 
        # - Read engine Ver (string to null, 12 bytes w/null) 

        # https://vscode.dev/github/shawngmc/game-extraction-toolbox/blob/developon.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/UnityPy/files/BundleFile.py#L89
        # Read UnityFSHeader
        # Read size (long, 8 bytes)
        # Read compressedHeaderSize (uint, 4 bytes)
        # Read uncompressedHeaderSize (uint, 4 bytes)
        # Read dataflags (uint, 4 bytes)

        # https://vscode.dev/github/shawngmc/game-extraction-toolbox/blob/developon.Python.3.13_qbz5n2kfra8p0/LocalCache/local-packages/Python313/site-packages/UnityPy/files/BundleFile.py#L137-L138
        # Read Compressed data (compressedSize bytes)






        # UnityFS
        # Header 30-50
        # kArchiveBlocksAndDirectoryInfoCombined 50-126
        # Decompress LZ4HC
        # kArchiveBlocksAndDirectoryInfoCombined  76b -> 101b
        #     Read uncompressedhash (16)
        #     Read num info blocks (4)
        #     BlockInfo 1 
        #         Read uncompSize (4)   131072
        #         Read compSize (4)     105806
        #         Read Flags (2)        3
        #     BlockInfo 2
        #         Read uncompSize (4)   4308
        #         Read compSize (4)     3864
        #         Read Flags (2)        3
        #     Read num nodes (4)
        #     Node 1
        #     Read offset (8)						0					
        #     Read size (8)						135380
        #     Read flags (4)
        #     Read path (string to null, 8 bytes w/null)		CAB-2bc09eb64eebc83dfafe8f931a64b1cd
        # Read blocks
        #     Block 1 (105806 bytes)
        #     Decompress LZ4HC
        #     Block 2 (3864 bytes)
        #     Decompress LZ4HC



    def execute(self, in_dir, out_dir):
        logger.error("SaGa is currently awaiting reimplementation.")

        # for each output file entry
        # for out_file_entry in self._metadata['out']['files']:
        #     pkg_name = out_file_entry['extract']['in_file']
        #     logger.info(f"Extracting {pkg_name}...")

        #     # read the matching input file
        #     in_file_entry = self._metadata['in']['files'][pkg_name]
        #     loaded_file = self.read_datafile(in_dir, in_file_entry)

        #     if pkg_name == "saga1":
        #         # load the archive
        #         unity_bundle = UnityPy.load(loaded_file['contents'])

            # files = self.unpackSagaUnityArchive(loaded_file)


            # if pkg_name == "ffl1":
            #     # Manual hackiness!
            #     # block1_comp = transforms.cut(loaded_file['contents'], 0x7E, 105806)
            #     # block1_decomp = lz4.block.decompress(block1_comp, 131072)
            #     # block2_comp = transforms.cut(loaded_file['contents'], 0x19DCC, 3864)
            #     # block2_decomp = lz4.block.decompress(block2_comp, 4308)
            #     # full_node = transforms.merge([block1_decomp, block2_decomp])
            #     # rom_data = transforms.cut(full_node, 0x10D4, 0x20000)

                
            # else:
            #     # load the archive
            #     unity_bundle = UnityPy.load(loaded_file['contents'])



            #     # Get the rom asset entry
            #     entries = unity_bundle.container
            #     rom_asset = unity_bundle.container.get(out_file_entry['extract']['archive_path'])
            #     if rom_asset is None:
            #         logger.warning("Could not find rom asset in archive.")
            #     else:
            #         rom_data = rom_asset.read().m_Script.encode("utf-8", "surrogateescape")

            # _ = self.verify_out_file(out_file_entry['filename'], rom_data)

            # with open(os.path.join(out_dir, out_file_entry['filename']), "wb") as out_file:
            #     out_file.write(rom_data)
        logger.info("Processing complete.")

    # def execute(self, in_dir, out_dir):
    #     zamngp_file = self.read_all_datafiles(in_dir).get("zamngp")
    #     exe_data = zamngp_file['contents']
    #     file_ver = zamngp_file['version']
    #     if file_ver is not None:
    #         logger.info(f"Found {file_ver}...")

    #     for game in self._metadata['out']['files']:
    #         game_data = None
    #         game_header = bytes.fromhex(game['extract']['header_bytes'])
    #         target_size = game['extract']['length']

    #         if file_ver is not None:
    #             logger.info(f"Pulling {game['game']} from known offset...")
    #             version_info = game['extract']['versions'][file_ver]
    #             start = int(version_info['start'], 16)
    #             game_data = exe_data[start:start+target_size]
    #         else:
    #             logger.info(f"Finding {game['game']}...")

    #             # Try check_offsets
    #             logger.info(f"Finding {game['game']} via known offsets...")
    #             for version_info in game['extract']['versions'].values():
    #                 check_offset = int(version_info['start'], 16)
    #                 check_header = exe_data[check_offset:check_offset+10]
    #                 if check_header == game_header:
    #                     logger.info(f"Found header at {hex(check_offset)}!")
    #                     game_data = exe_data[check_offset:check_offset+target_size]
    #                     crc = hash_helper.get_crc(game_data)[2:].upper().rjust(8, "0")
    #                     if crc == game['verify']['crc']:
    #                         logger.info(f"Found crc match at {hex(check_offset)}!")
    #                         break
    #                     else:
    #                         logger.info(f"False header match at {hex(check_offset)}!")
    #                         game_data = None

    #             # Do the manual search
    #             if not game_data:
    #                 logger.info(f"Finding {game['game']} via full search - please wait...")
    #                 for offset in range(0, len(exe_data) - target_size):
    #                     check_header = exe_data[offset:offset+10]
    #                     if check_header == game_header:
    #                         logger.info(f"Found header at {hex(offset)}!")
    #                         game_data = exe_data[offset:offset+target_size]
    #                         crc = hash_helper.get_crc(game_data)[2:].upper().rjust(8, "0")
    #                         if crc == game['verify']['crc']:
    #                             logger.info(f"Found crc match at {hex(offset)}!")
    #                             break
    #                         else:
    #                             logger.info(f"False header match at {hex(offset)}!")
    #                             game_data = None

    #         if game_data:
    #             _ = self.verify_out_file(game['filename'], game_data)
    #             logger.info(f"Saving {game['filename']}...")
    #             with open(os.path.join(out_dir, game['filename']), "wb") as out_file:
    #                 out_file.write(game_data)
    #         else:
    #             logger.warning(f"Game {game['game']} not found!")

    #     logger.info("Processing complete.")

