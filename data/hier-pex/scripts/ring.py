"""An N-stage ring oscillator of INVx1_ASAP7_75t_R (N odd), laid out as a snake in two rows sharing
the VDD rail: row 0 left to right, row 1 rotated 180 degrees right to left. Y of each stage goes to A
of the next by an M2 strap with V1 on both M1 pins; M2 / V2 / M3 turnarounds at both ends close the
ring. Labels: S<i> on the input of stage i (S0 = ring node 0), VDD, VSS_0 (row 0), VSS_1 (row 1).
  ring.py <stages> <out.gds>"""
import os
import sys

import klayout.db as kdb

N, out = int(sys.argv[1]), sys.argv[2]
assert N % 2 == 1
lib = kdb.Layout()
lib.read(os.environ["ASAP7_STDCELLS"] + "/GDS/asap7sc7p5t_28_R_220121a.gds")
ly = kdb.Layout()
ly.dbu = lib.dbu
inv = ly.create_cell("INVx1_ASAP7_75t_R")
src = lib.cell("INVx1_ASAP7_75t_R")
for li in lib.layer_indexes():
    info = lib.get_info(li)
    for s in src.shapes(li).each():
        if not s.is_text():                       # the cell's own labels would name the nets
            inv.shapes(ly.layer(info)).insert(s)
top = ly.create_cell(f"RO{N}")
M1, V1, M2, V2, M3 = (ly.layer(n, 0) for n in (19, 21, 20, 25, 30))
LBL = ly.layer(19, 251)
P, H = 0.162, 0.27
n0 = (N + 1) // 2                                 # row 0: stages 0 .. n0-1, row 1: n0 .. N-1
n1 = N - n0


def box(layer, x0, y0, x1, y1):
    top.shapes(layer).insert(kdb.DBox(x0, y0, x1, y1))


def via(layer, x, y):                             # an 18 nm via centred on (x, y)
    box(layer, x - 0.009, y - 0.009, x + 0.009, y + 0.009)


def label(name, x, y):
    top.shapes(LBL).insert(kdb.DText(name, x, y))


ya, yb = 0.135, 2 * H - 0.135                     # strap tracks of row 0 / row 1
for k in range(n0):                               # row 0
    top.insert(kdb.DCellInstArray(inv.cell_index(), kdb.DTrans(k * P, 0)))
for k in range(n1):                               # row 1: R180, x index k from the left
    top.insert(kdb.DCellInstArray(inv.cell_index(), kdb.DTrans(kdb.DTrans.R180, kdb.DVector(k * P + P, 2 * H))))
# row 0: Y of stage k (x k*P + 0.135) to A of stage k+1 (x (k+1)*P + 0.027)
for k in range(n0 - 1):
    xy, xa = k * P + 0.135, (k + 1) * P + 0.027
    via(V1, xy, ya); via(V1, xa, ya)
    box(M2, xy - 0.009, ya - 0.009, xa + 0.009, ya + 0.009)
# row 1: stage n0 + j sits at x index n1-1-j; Y at x idx*P + 0.027, A of the next at (idx-1)*P + 0.135
for j in range(n1 - 1):
    idx = n1 - 1 - j
    xy, xa = idx * P + 0.027, (idx - 1) * P + 0.135
    via(V1, xy, yb); via(V1, xa, yb)
    box(M2, xa - 0.009, yb - 0.009, xy + 0.009, yb + 0.009)
# right turnaround: Y of stage n0-1 (row 0, last) up to A of stage n0 (row 1, x index n1-1)
xy, xa, xt = (n0 - 1) * P + 0.135, (n1 - 1) * P + 0.135, n0 * P + 0.06
via(V1, xy, ya); box(M2, xy - 0.009, ya - 0.009, xt + 0.009, ya + 0.009); via(V2, xt, ya)
box(M3, xt - 0.009, ya - 0.009, xt + 0.009, yb + 0.009)
via(V2, xt, yb); box(M2, xa - 0.009, yb - 0.009, xt + 0.009, yb + 0.009); via(V1, xa, yb)
# left turnaround: Y of stage N-1 (row 1, x index 0) down to A of stage 0 (row 0, x index 0)
xy, xa, xt = 0.027, 0.027, -0.06
via(V1, xy, yb); box(M2, xt - 0.009, yb - 0.009, xy + 0.009, yb + 0.009); via(V2, xt, yb)
box(M3, xt - 0.009, ya - 0.009, xt + 0.009, yb + 0.009)
via(V2, xt, ya); box(M2, xt - 0.009, ya - 0.009, xa + 0.009, ya + 0.009); via(V1, xa, ya)
# labels: the input of every stage (on its A pin's M1), the rails
for i in range(N):
    if i < n0:
        label(f"S{i}", i * P + 0.027, 0.2)
    else:
        idx = n1 - 1 - (i - n0)
        label(f"S{i}", idx * P + P - 0.027, 2 * H - 0.2)
label("VSS_0", 0.03, 0.0)
label("VDD", 0.03, H)
label("VSS_1", 0.03, 2 * H)
opt = kdb.SaveLayoutOptions()
opt.select_cell(top.cell_index())
ly.write(out, opt)
print(top.name, n0, n1)
