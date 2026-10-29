"""Ring-oscillator testbenches (TT, 0.7 V): the oscillation period at node s0 over 6 periods.
  ring_tb.py array <RO netlist> <out.sp>              the extracted ring (flat or windowed)
  ring_tb.py cells <INV netlist> <subckt> <N> <out.sp> N copies of one inverter subcircuit, ideal wires
  ring_tb.py schematic <N> <out.sp>                    N schematic inverters (no parasitics)
The reference INVx1 (xAct3D) has the pins VSS VDD A Y, OpenLayout's A VDD VSS Y: the order is read
from the subckt line."""
import re
import sys

MODELS = "/home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm"
mode = sys.argv[1]
body = []
if mode == "array":
    net, out = sys.argv[2], sys.argv[3]
    sub = next(l for l in open(net) if l.startswith(".subckt")).split()
    name, pins = sub[1], sub[2:]
    n = sum(1 for p in pins if re.fullmatch(r"S\d+", p))
    conn = [p.lower() if re.fullmatch(r"S\d+", p) else ("vdd" if p.startswith("VDD") else "0") for p in pins]
    body += [f".include {net}", f"X1 {' '.join(conn)} {name}"]
elif mode == "cells":
    net, cell, n, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
    text = open(net).read()
    pins = re.search(rf"^\.subckt {re.escape(cell)} (.*)$", text, re.M | re.I).group(1).split()
    body.append(f".include {net}")
    for i in range(n):
        m = {"A": f"s{i}", "Y": f"s{(i + 1) % n}", "VDD": "vdd", "VSS": "0"}
        body.append(f"X{i} {' '.join(m[p.upper()] for p in pins)} {cell}")
else:
    n, out = int(sys.argv[2]), sys.argv[3]
    body += [".subckt INVS A VDD VSS Y", "N1 Y A VSS VSS nmos_rvt l=20n nfin=3",
             "N2 Y A VDD VDD pmos_rvt l=20n nfin=3", ".ends"]
    body += [f"X{i} s{i} vdd 0 s{(i + 1) % n} INVS" for i in range(n)]
ic = " ".join(f"v(s{i})={0.7 if i % 2 else 0}" for i in range(n))
lines = [f"* ring oscillator, {n} stages ({mode})", f".include {MODELS}", "Vdd vdd 0 0.7", *body,
         f".ic {ic}", ".tran 1p 8n", ".control", "set num_threads=1", "run",
         "meas tran t4 when v(s0)=0.35 rise=4", "meas tran t10 when v(s0)=0.35 rise=10",
         "let period = (t10 - t4) / 6", f"let stage = period / {2 * n}",
         "print period stage", ".endc", ".end", ""]
open(out, "w").write("\n".join(lines))
