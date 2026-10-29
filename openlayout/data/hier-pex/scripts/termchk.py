# terminal shapes: the cached-per-abstract path against shapes_of_terminal for every terminal
import sys, tempfile, klayout.db as kdb
from pathlib import Path
from openlayout import pex
w = Path(tempfile.mkdtemp())
lv = pex.extract_netlist(Path(sys.argv[1]).resolve(), sys.argv[2], w)
circ = lv.netlist().circuit_by_name(sys.argv[2])
to_um = kdb.CplxTrans(lv.internal_layout().dbu); cache = {}; bad = n = comb = 0
for net in circ.each_net():
    for tr in net.each_terminal():
        d = tr.device(); n += 1
        if any(True for _ in d.each_combined_abstract()): comb += 1; continue
        t = to_um.inverted() * d.trans * to_um
        k = (d.device_abstract.cell_index(), tr.terminal_id())
        if k not in cache: cache[k] = lv.shapes_of_terminal(tr, t.inverted())
        a = {li: r.transformed(t) for li, r in cache[k].items()}
        b = lv.shapes_of_terminal(tr, kdb.ICplxTrans())
        if set(a) != set(b) or any(not (a[li] ^ b[li]).is_empty() for li in a): bad += 1
print("terminals", n, "combined", comb, "mismatch", bad, "abstract keys", len(cache))
