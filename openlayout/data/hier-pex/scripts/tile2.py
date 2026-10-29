"""SRAMCIMsbc tiled rows x cols (odd rows mirrored about the shared rail), every cell labelled:
WL_<r> per row, BL_<c> / BLB_<c> per column, XB_<r>_<c> and P_<r>_<c> per cell, VDD_<k> / VSS_<k> on rail k (y = k x 0.27 um).
  tile2.py <cell.gds> <rows> <cols> <out.gds>"""
import sys, klayout.db as kdb
src, rows, cols, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ly = kdb.Layout(); ly.read(src)
cell = ly.cell("SRAMCIMsbc")
top = ly.create_cell(f"A{rows}x{cols}")
labels = [(ly.get_info(li), s.dtext) for li in ly.layer_indexes() for s in cell.shapes(li).each() if s.is_text()]
for r in range(rows):
    for c in range(cols):
        t = kdb.DTrans(c * 0.54, r * 0.27) if r % 2 == 0 else kdb.DTrans(kdb.DTrans.M0, kdb.DVector(c * 0.54, (r + 1) * 0.27))
        top.insert(kdb.DCellInstArray(cell.cell_index(), t))
        for info, tx in labels:
            n = tx.string
            name = {"WL": f"WL_{r}" if c == 0 else None, "BL": f"BL_{c}" if r == 0 else None,
                    "BL_Bar": f"BLB_{c}" if r == 0 else None, "XB": f"XB_{r}_{c}", "P": f"P_{r}_{c}",
                    "VDD": None, "VSS": None}.get(n)
            if n in ("VDD", "VSS") and c == 0:      # each rail its own name: VDD_<k> / VSS_<k>, k = rail index
                name = f"{n}_{round(tx.transformed(t).y / 0.27)}"
            if name:
                t2 = tx.transformed(t); t2.string = name
                top.shapes(ly.layer(info)).insert(t2)
opt = kdb.SaveLayoutOptions(); opt.select_cell(top.cell_index())
ly.write(out, opt); print(top.name)
