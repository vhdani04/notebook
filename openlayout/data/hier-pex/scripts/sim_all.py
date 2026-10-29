"""P delays (gen_tb.py) of a labelled tile: every available netlist (flat, windowed halos) at a few
probe cells - corner (0,0), bottom edge (0,C/2), interior (R/2,C/2), opposite corner (R-1,C-1).
Appends to sim/delays.csv.
  sim_all.py <tile, e.g. a4x8> [load fF]"""
import csv
import os
import re
import subprocess
import sys

D = os.path.expanduser("~/papers/notebook/data/hier-pex")
tile = sys.argv[1]
load = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
R, C = map(int, tile[1:].split("x"))
nets = {"flat": f"{D}/flat/{tile}.flat.pex.spice"}
for h in ("0.1", "0.15", "0.2"):
    nets[f"win{h}"] = f"{D}/win/{tile}.h{h}.pex.spice"
cells = sorted({(0, 0), (0, C // 2), (R // 2, C // 2), (R - 1, C - 1)})
keys = ["p_at_1p9", "p_at_2p9", "tpr1", "tpf1", "tpr2", "tpf2", "trise", "tfall"]
rows = []
for var, net in nets.items():
    if not os.path.isfile(net):
        print(f"{tile} {var}: no netlist")
        continue
    for r, c in cells:
        tb = f"{D}/sim/tb_{tile}_{var}_{r}_{c}_L{load:g}.sp"
        subprocess.run(["python3", f"{D}/scripts/gen_tb.py", net, str(r), str(c), tb, "-", str(load)], check=True)
        res = subprocess.run(["ngspice", "-b", tb], capture_output=True, text=True, timeout=3600)
        open(tb.replace(".sp", ".log"), "w").write(res.stdout + res.stderr)
        m = {k: float(v) for k, v in re.findall(r"^(\w+)\s*=\s*([-+0-9.eE]+)", res.stdout, re.M) if k in keys}
        row = {"tile": tile, "netlist": var, "r": r, "c": c, "load_fF": load, **{k: m.get(k) for k in keys}}
        rows.append(row)
        print(f"{tile} {var:8s} ({r},{c}) " + " ".join(f"{k}={m[k] * 1e12:.3f}ps" if k in m and k.startswith("t")
                                                       else f"{k}={m.get(k)}" for k in keys), flush=True)
path = f"{D}/sim/delays.csv"
new = not os.path.isfile(path)
with open(path, "a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    if new:
        w.writeheader()
    w.writerows(rows)
