"""The library's reference extraction (xAct3D) of a cell: its subcircuit and the PM_ subcircuits it
uses, out of $ASAP7_STDCELLS/CDL/xAct3D_extracted/asap7sc7p5t_28_R.sp.
  ref_inv.py <cell> <out.sp>"""
import os
import re
import sys

cell, out = sys.argv[1], sys.argv[2]
text = open(os.environ["ASAP7_STDCELLS"] + "/CDL/xAct3D_extracted/asap7sc7p5t_28_R.sp").read()
keep = []
for m in re.finditer(r"^\.subckt (\S+).*?^\.ends[^\n]*", text, re.M | re.S | re.I):
    name = m.group(1)
    if name == cell or name.startswith(f"PM_{cell}%"):
        keep.append(m.group(0))
open(out, "w").write(f"* {cell}: reference extraction (xAct3D), from the ASAP7 library\n" + "\n".join(keep) + "\n")
print(len(keep), "subcircuits")
