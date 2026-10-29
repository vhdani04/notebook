"""Testbench for a labelled SRAMCIMsbc tile netlist: write Q=1 into cell (r, c) (BL_c high, BLB_c
low, one WL_r pulse), then toggle that cell's XB twice; P = Q AND NOT XB rises and falls. The other
XBs stay high (their P low), the other bit lines are held high, all rails at 0.7 / 0 V.
  gen_tb.py <netlist> <r> <c> <out.sp> [wave file] [load fF on P]"""
import sys

net, r, c, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
wave = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
load = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
sub = next(l for l in open(net) if l.startswith(".subckt")).split()
name, pins = sub[1], sub[2:]
P, XB = f"P_{r}_{c}", f"XB_{r}_{c}"
src = []
for p in pins:
    if p.startswith("VDD"):
        v = "0.7"
    elif p.startswith("VSS"):
        v = "0"
    elif p == f"WL_{r}":
        v = "pwl(0 0 0.1n 0 0.12n 0.7 0.6n 0.7 0.62n 0)"
    elif p.startswith("WL_"):
        v = "0"
    elif p == f"BL_{c}":
        v = "0.7"
    elif p == f"BLB_{c}":
        v = "0"
    elif p.startswith(("BL_", "BLB_")):
        v = "0.7"
    elif p == XB:
        v = "pwl(0 0.7 1n 0.7 1.02n 0 2n 0 2.02n 0.7 3n 0.7 3.02n 0 4n 0 4.02n 0.7)"
    elif p.startswith("XB_"):
        v = "0.7"
    else:
        continue                                     # the P outputs stay open
    src.append(f"V{p} {p} 0 {v}")
lines = [f"* {name}: write 1 into cell ({r}, {c}), toggle its XB, P delays (load {load:g} fF)",
         ".include /home/vhdani/openlayout/models/asap7_ngspice/7nm_TT.pm", f".include {net}",
         *src, f"X1 {' '.join(pins)} {name}"]
if load > 0:
    lines.append(f"CL {P} 0 {load:g}f")
lines += [".tran 1p 4.6n", ".control", "set num_threads=1", "run",
          f"meas tran p_at_1p9 find v({P}) at=1.9n",
          f"meas tran p_at_2p9 find v({P}) at=2.9n",
          f"meas tran tpr1 trig v({XB}) val=0.35 fall=1 targ v({P}) val=0.35 rise=1",
          f"meas tran tpf1 trig v({XB}) val=0.35 rise=1 targ v({P}) val=0.35 fall=1",
          f"meas tran tpr2 trig v({XB}) val=0.35 fall=2 targ v({P}) val=0.35 rise=2",
          f"meas tran tpf2 trig v({XB}) val=0.35 rise=2 targ v({P}) val=0.35 fall=2",
          f"meas tran trise trig v({P}) val=0.14 rise=1 targ v({P}) val=0.56 rise=1",
          f"meas tran tfall trig v({P}) val=0.56 fall=1 targ v({P}) val=0.14 fall=1"]
if wave:
    lines.append(f"wrdata {wave} v({P}) v({XB})")
lines += [".endc", ".end", ""]
open(out, "w").write("\n".join(lines))
