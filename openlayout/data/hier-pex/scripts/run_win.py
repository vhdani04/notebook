"""Windowed PEX of a labelled tile, its summary (window kinds, halo, times) as JSON beside the netlist.
  run_win.py <tile.gds> <cell> <halo> <out.pex.spice> [jobs]"""
import json, sys, time
from openlayout import pex
gds, cell, halo, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 1
t = time.time()
s = pex.extract(gds, cell, out, cap="window", halo=halo, jobs=jobs)
s["wall_s"] = time.time() - t
json.dump(s, open(out.replace(".pex.spice", ".json"), "w"), indent=1)
w = s["windows"]
print(f"{cell} halo {halo}: {w['windows']} windows, {w['solved']} solved, {w['cached']} cached, "
      f"halo used {w['halo']}, {s['capacitors']} C, {s['wall_s']:.0f} s")
