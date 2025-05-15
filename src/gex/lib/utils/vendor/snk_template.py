
def handle_MAMENAME(bundle_contents):
    func_map = {}
    def MAMENAME_maincpu(in_files):
        contents = in_files['MAMENAME_game_m68k']

        chunks = transforms.equal_split(contents, num_chunks=2)

        return {"NEOGEONUM-p1.p1": chunks[0]}
    func_map['maincpu'] = MAMENAME_maincpu
    adpcm_file_map = {
        'NEOGEONUM-v1.v1': 0x400000,
        'NEOGEONUM-v2.v2': 0x200000,
    }
    func_map['adpcm'] = helpers.custom_split_helper('MAMENAME_adpcm', adpcm_file_map)
    func_map['zoom'] = helpers.name_file_helper("MAMENAME_zoom_table", "000-lo.lo")
    func_map['audiocpu'] = helpers.name_file_helper("MAMENAME_game_z80", "NEOGEONUM-m1.m1")

    def MAMENAME_sprites(in_files):
        contents = in_files['MAMENAME_tiles']
        deoptimized = deoptimize_sprites(contents)
        filenames = [
            "NEOGEONUM-c1.c1",
            "NEOGEONUM-c2.c2",
            "NEOGEONUM-c3.c3",
            "NEOGEONUM-c4.c4",
        ]
        chunks = transforms.custom_split(deoptimized, [0x800000, 0x200000])
        chunks = transforms.deinterleave_all(chunks, 2, 1)
        return dict(zip(filenames, chunks))
    func_map['sprites'] = MAMENAME_sprites

    def MAMENAME_fixed(in_files):
        contents = in_files['MAMENAME_game_sfix']
        return {"NEOGEONUM-s1.s1": sfix_reorder(contents)}
    func_map['fixed'] = MAMENAME_fixed

    return helpers.build_rom(bundle_contents, func_map)
