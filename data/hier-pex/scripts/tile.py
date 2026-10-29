import sys, klayout.db as kdb
src, rows, cols, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ly = kdb.Layout(); ly.read(src)
cell = ly.cell("SRAMCIMsbc")
top = ly.create_cell(f"T{rows}x{cols}")
for r in range(rows):
    for c in range(cols):
        # odd rows mirrored about the shared rail, as an array would be
        t = kdb.DTrans(c * 0.54, r * 0.27) if r % 2 == 0 else kdb.DTrans(kdb.DTrans.M0, kdb.DVector(c * 0.54, (r + 1) * 0.27))
        top.insert(kdb.DCellInstArray(cell.cell_index(), t))
# a few top-level labels so extraction has pins
for li in ly.layer_indexes():
    info = ly.get_info(li)
    for s in cell.shapes(li).each():
        if s.is_text():
            top.shapes(li).insert(s.dtext)
opt = kdb.SaveLayoutOptions(); opt.select_cell(top.cell_index())
ly.write(out, opt)
print(top.name)
